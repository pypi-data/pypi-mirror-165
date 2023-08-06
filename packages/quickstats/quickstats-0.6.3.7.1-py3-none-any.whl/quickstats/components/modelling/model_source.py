from typing import Optional, Union, List, Dict, Callable

import ROOT

from quickstats import AbstractObject
from .component_source import ComponentSource

class XMLModelSource(ComponentSource):
    
    def __init__(self, input_paths:Optional[Union[PathManager, str, List[str]]],
                 observable:Optional[RooRealVar]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(input_paths=input_paths,
                         observable=observable,
                         verbosity=verbosity)
        
    def construct_model(self, workspace:ROOT.RooWorkspace):
        pass