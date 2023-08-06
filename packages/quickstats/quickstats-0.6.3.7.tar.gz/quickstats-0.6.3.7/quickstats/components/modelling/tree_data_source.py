from typing import Optional, Union, List, Dict, Callable

import ROOT

from quickstats import AbstractObject, DescriptiveEnum, PathManager
from quickstats.interface.root import RooRealVar

from .component_source import ComponentSource

class TreeDataSource(ComponentSource):

    def __init__(self, tree_name:str,
                 input_paths:Optional[Union[PathManager, str, List[str]]],
                 weight_name:Optional[str]=None,
                 observable:Optional[RooRealVar]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(input_paths=input_paths,
                         observable=observable,
                         verbosity=verbosity)
        self.weight_name  = weight_name
        self.tree_name    = tree_name
        
    def construct_dataset_from_tree(self, name:str, tree:Union[ROOT.TTree, ROOT.TChain]):
        variables = ROOT.RooArgSet()
        if self.observable is None:
            raise RuntimeError("observable not set")
        observable_var = self.observable.new()
        variables.add(observable_var)
        if self.weight_name is not None:
            weight_var = ROOT.RooRealVar(self.weight_name, self.weight_name, 1)
            variables.add(weight_var)
            dataset = ROOT.RooDataSet(name, name, variables,
                                      ROOT.RooFit.Import(tree),
                                      ROOT.RooFit.WeightVar(weight_var))
        else:
            dataset = ROOT.RooDataSet(name, name, variables,
                                      ROOT.RooFit.Import(tree))
        return dataset
    
    def construct_dataset(self, name:str, **file_kwargs):
        if self.input_paths is None:
            raise RuntimeError("input path(s) not set")
        if self.tree_name is None:
            raise RuntimeError("tree name not set")
        chain = ROOT.TChain(self.tree_name)
        for name in self.input_paths.files:
            path = self.input_paths.get_resolved_file(name, check_exist=True, **file_kwargs)
            chain.Add(path)
        dataset = self.construct_dataset_from_tree(name, chain)
        return dataset