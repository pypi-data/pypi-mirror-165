from typing import Dict, Union, List, Optional

from quickstats.maths.numerics import get_proper_ranges

class RooRealVar:
    
    @property
    def value_range(self):
        return self._value_range
    
    @value_range.setter
    def value_range(self, value:Optional[List[float]]=None):
        self._value_range = self._parse_value_range(value, self.value)
   
    @property
    def named_ranges(self):
        return self._named_ranges
    
    @named_ranges.setter
    def named_ranges(self, value:Optional[Dict[str, List[float]]]=None):
        self._named_ranges = self._parse_named_ranges(value)
        
    def __init__(self, obj:Optional["ROOT.RooRealVar"]=None):
        if obj is not None:
            self.parse(obj)
        else:
            self.name   = None
            self.title  = None
            self.value  = None
            self.n_bins = None
            self.unit   = None
            self.value_range  = None
            self.named_ranges = None
        
    def parse(self, obj:"ROOT.RooRealVar"):
        import ROOT
        if not isinstance(obj, ROOT.RooRealVar):
            raise ValueError("object must be an instance of ROOT.RooRealVar")
        self.name   = obj.GetName()
        self.title  = obj.getTitle()
        self.value  = obj.getVal()
        self.n_bins = obj.getBins()
        self.unit   = obj.getUnit()
        _range = obj.getRange()
        self.value_range = [_range[0], _range[1]]
        named_ranges = {}
        for name in obj.getBinningNames():
            _range = obj.getRange(name)
            named_ranges[name] = [_range[0], _range[1]]
        self.named_ranges = _named_ranges
        
    @staticmethod
    def _parse_named_ranges(named_ranges:Optional[Dict[str, List[float]]]=None):
        if named_ranges is not None:
            ranges = get_proper_ranges(list(named_ranges.values()), no_overlap=False)
            result = {k:v for k, v in zip(named_ranges.keys(), ranges)}
            return result
        return None
    
    @staticmethod
    def _parse_value_range(value_range:Optional[List[float]]=None,
                           nominal_value:Optional[float]=None):
        if value_range is not None:
            result = get_proper_ranges(value_range, nominal_value)
            if result.shape != (1, 2):
                raise ValueError("value range must be list of size 2")
            return result[0]
        return None
                                
    @classmethod
    def create(cls, name:str, title:Optional[str]=None, value:float=0,
               value_range:Optional[List[float]]=None,
               named_ranges:Optional[Dict[str, List[float]]]=None,
               n_bins:Optional[int]=None, unit:Optional[str]=None):
        instance = cls()
        instance.name = name
        instance.title = title
        instance.value = value
        instance.value_range = value_range
        instance.named_ranges = named_ranges
        instance.n_bins = n_bins
        instance.unit = unit
        return instance
        
    def new(self):
            
        if self.name is None:
            raise RuntimeError("object not initialized")
            
        import ROOT
        
        if self.title is not None:
            title = self.title
        else:
            title = self.name
            
        variable = ROOT.RooRealVar(self.name, title, self.value)
 
        if self.value_range is not None:
            variable.setRange(self.value_range[0], self.value_range[1])
            
        if self.named_ranges is not None:
            for name, _range in self.named_ranges.items():
                variable.setRange(name, _range[0], _range[1])            
        
        if self.n_bins is not None:
            variable.setBins(self.n_bins)
            
        if self.unit is not None:
            variable.setUnit(self.unit)
            
        return variable