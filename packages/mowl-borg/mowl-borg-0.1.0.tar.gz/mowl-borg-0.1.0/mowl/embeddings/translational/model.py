

from mowl.projection.factory import projector_factory
from mowl.projection.edge import Edge

#PyKEEN imports
from pykeen.triples import CoreTriplesFactory, TriplesFactory
from pykeen.models import TransE, TransH, TransR, TransD
from pykeen.training import SLCWATrainingLoop
from pykeen.evaluation import RankBasedEvaluator
import tempfile
import torch as th
from torch.optim import Adam
from deprecated.sphinx import deprecated
import logging
logging.basicConfig(level=logging.INFO)

@deprecated(version = "0.1.0", reason = "This class will no longer be available in future versions. ``Use mowl.kge.model.KGEModel`` instead.")
class TranslationalOnt():

    '''
    :param edges: List of edges
    :type edges: mowl.projection.edge.Edge
    :param trans_method: Translational model. Choices are: "transE", "transH", "transR", "transD".
    :type trans_method: str
    :param embedding_dim: Dimension of embedding for each node
    :type embedding_dim: int
    :param epochs: Number of epochs
    :type epochs: int
    :param device: Device to run the model. Default is `cpu`
    :type device: str
    '''
    
    def __init__(self,
                 edges,
                 trans_method="transE",
                 embedding_dim = 50,
                 epochs = 5,
                 batch_size = 32,
                 device = "cpu",
                 model_filepath = None,
    ):
        
        self.edges = edges
        self.trans_method = trans_method
        self.embedding_dim = embedding_dim
        self.epochs = epochs
        self.batch_size = batch_size
        self.device = device
        self.model = None
        self._trained = False
        self._data_loaded = False

        self.model_filepath = model_filepath
        
    def load_data(self):
        if self._data_loaded:
            return

        entities, relations = Edge.getEntitiesAndRelations(self.edges)

        logging.debug("Number of ontology classes: %d, relations %d.", len(entities), len(relations))

        self.entities_idx = {ent: idx for idx, ent in enumerate(entities)}
        self.relations_idx = {rel: idx for idx, rel in enumerate(relations)}

        mapped_triples = [(self.entities_idx[e.src()], self.relations_idx[e.rel()], self.entities_idx[e.dst()]) for e in self.edges]

        mapped_triples = th.tensor(mapped_triples).long()

        self.triples_factory = CoreTriplesFactory(mapped_triples, len(entities), len(relations), self.entities_idx, self.relations_idx)

        self._data_loaded = True

    def load_best_model(self):
        self.load_data()
        self.init_model()
        self.model.load_state_dict(th.load(self.model_filepath))
        self.model.eval()

    def init_model(self):
        self.load_data()
        
        self.model = self.trans_factory(self.trans_method, self.triples_factory, self.embedding_dim).to(self.device)
        
    def train(self): 
        self.load_data()
        
        self.init_model()

        optimizer = Adam(params=self.model.get_grad_params())

        training_loop = SLCWATrainingLoop(model=self.model, triples_factory=self.triples_factory, optimizer=optimizer)

        _ = training_loop.train(triples_factory=self.triples_factory, num_epochs=self.epochs, batch_size=self.batch_size)

        if self.model_filepath:
            th.save(self.model.state_dict(), self.model_filepath)
        self._trained = True

    def get_embeddings(self, load_best_model = True):

        self.load_data()
        self.init_model()
        if load_best_model:
            self.load_best_model()
                     
        embeddings = self.model.entity_representations[0](indices = None).cpu().detach().numpy()
        embeddings = {item[0]: embeddings[item[1]] for item in self.entities_idx.items()}

        rel_embeddings = self.model.relation_representations[0](indices = None).cpu().detach().numpy()
        rel_embeddings = {item[0]: rel_embeddings[item[1]] for item in self.relations_idx.items()}

        
        return embeddings, rel_embeddings

    def score_method_point(self, point):
        x, y, z = point
        x, y, z = self.entities_idx[x], self.relations_idx[y], self.entities_idx[z]
        ###implement code that checks dimensionality
        point = self.point_to_tensor([x,y,z])

        return - self.model.score_hrt(point)

    def score_method_tensor(self, data):
        return -self.model.score_hrt(data)
    
    def point_to_tensor(self, point):
        point = [list(point)]
        point = th.tensor(point).to(self.device)
        return point

    
    def trans_factory(self, method_name, triples_factory, embedding_dim):
        methods = {
            "transE": TransE,
            "transH": TransH,
            "transR": TransR,
            "transD": TransD
        }

        if method_name in methods:
            return methods[method_name](triples_factory=triples_factory, embedding_dim=embedding_dim)
        else:
            raise Exception(f"Method name unrecognized. Recognized methods are: {methods}")



class TranslationalOntNew():

    '''
    :param triples_factory: PyKEEN triples factory.
    :type triples_factory: :class:`pykeen.triples.triples_factory.CoreTriplesFactory`
    :param model: Initialized PyKEEN model
    :type model: Initialized model of the type :class:`EntityRelationEmbeddingModel <pykeen.models.base.EntityRelationEmbeddingModel>` or :class:`ERModel <pykeen.models.nbase.ERModel>`.
    :param epochs: Number of epochs.
    :type epochs: int
    :param batch_size: Number of each data samples in each batch. Defaults to 32.
    :type batch_size: int, optional
    :param optimizer: Optimizer to be used while training the model. Defaults to :class:`torch.optim.Adam`.
    :type optimizer: subclass of :class:`torch.optim.Optimizer`, optional
    :param lr: Learning rate. Defaults to 1e-3.
    :type lr: float, optional
    :param device: Device to run the model. Defaults to `cpu`.
    :type device: str
    :param model_filepath: Path for saving the model. Defaults to :class:`tempfile.NamedTemporaryFile`
    :type model_filepath: str, optional
    '''
    
    def __init__(self,
                 triples_factory,
                 pykeen_model,
                 epochs,
                 batch_size = 32,
                 optimizer = Adam,
                 lr = 1e-3,
                 device = "cpu",
                 model_filepath = None,
    ):
        self.triples_factory = triples_factory
        self.device = device
        self.model = pykeen_model.to(self.device)
        self.epochs = epochs
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.lr = lr
        
        if model_filepath is None:
            model_filepath = tempfile.NamedTemporaryFile()
            model_filepath = model_filepath.name
        self.model_filepath = model_filepath
        
        self._trained = False
        self._data_loaded = False

    def load_best_model(self):
        self.model.load_state_dict(th.load(self.model_filepath))
        self.model.eval()

    def train(self): 
        optimizer = self.optimizer(params=self.model.get_grad_params(), lr = self.lr)

        training_loop = SLCWATrainingLoop(model=self.model, triples_factory=self.triples_factory, optimizer=optimizer)

        _ = training_loop.train(triples_factory=self.triples_factory, num_epochs=self.epochs, batch_size=self.batch_size)

        th.save(self.model.state_dict(), self.model_filepath)
        self._trained = True

    def get_embeddings(self, load_best_model = True):
        if load_best_model:
            self.load_best_model()
                     
        embeddings = self.model.entity_representations[0](indices = None).cpu().detach().numpy()
        embeddings = {item[0]: embeddings[item[1]] for item in self.triples_factory.entity_to_id.items()}

        rel_embeddings = self.model.relation_representations[0](indices = None).cpu().detach().numpy()
        rel_embeddings = {item[0]: rel_embeddings[item[1]] for item in self.triples_factory.relation_to_id.items()}

        
        return embeddings, rel_embeddings

    def score_method_point(self, point):
        x, y, z = point
        x, y, z = self.entities_idx[x], self.relations_idx[y], self.entities_idx[z]
        ###implement code that checks dimensionality
        point = self.point_to_tensor([x,y,z])

        return - self.model.predict_hrt(point)

    def score_method_tensor(self, data):
        return -self.model.predict_hrt(data)
    
    def point_to_tensor(self, point):
        point = [list(point)]
        point = th.tensor(point).to(self.device)
        return point

