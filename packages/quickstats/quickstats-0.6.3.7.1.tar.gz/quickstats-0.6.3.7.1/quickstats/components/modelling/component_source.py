from typing import Optional, Union, List, Dict, Callable

import ROOT

from quickstats import AbstractObject
from quickstats.interface.root import RooRealVar

class ComponentSource(AbstractObject):
    
    """

    class ModelType(DescriptiveEnum):
        SIGNAL     = (0, "Signal Model")
        BACKGROUND = (1, "Background Model")
        AUXILIARY  = (2, "Auxiliary Model")
    
                
    @property
    def model_type(self) -> ModelType:
        return self._model_type
    
    @model_type.setter
    def model_type(self, value:Union[str, ModelType]):
        if isinstance(value, ModelType):
            self._model_type = value
        else:
            self._model_type = ModelType.parse(value)
    """
    
    @property
    def observable(self) -> RooRealVar:
        return self._observable
    
    @observable.setter
    def observable(self, value:Union[RooRealVar, ROOT.RooRealVar]):
        if value is None:
            self._observable = None
        elif isinstance(value, ROOT.RooRealVar):
            self._observable = RooRealVar(value)
        elif isinstance(value, RooRealVar):
            self._observable = value
        else:
            raise ValueError("observable must be an instance of ROOT.RooRealVar or"
                             "quickstats.interface.root.RooRealVar")
            
    @property
    def input_paths(self) -> PathManager:
        return self._input_paths
    
    @input_paths.setter
    def input_paths(self, value:Optional[Union[PathManager, str, List[str]]]=None):
        if value is None:
            self._input_paths = None
        if isinstance(value, PathManager):
            self._input_paths = value
        else:
            self._input_paths = PathManager(files=value)            
    
    def __init__(self, input_paths:Optional[Union[PathManager, str, List[str]]]=None,
                 observable:Optional[RooRealVar]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        
        self.input_paths  = input_paths
        self.observable   = observable
        
    def set_observable(self, observable:Union[RooRealVar, ROOT.RooRealVar]):
        self.observable = observable