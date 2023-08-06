from typing import Optional, Union, Dict, List, Tuple
import os

from quickstats import PathManager

class AnalysisPathManager(PathManager):
    
    DEFAULT_DIRECTORIES = {}
    DEFAULT_FILES       = {}
    
    def __init__(self, study_name:str="", base_path:Optional[str]=None,
                 directories:Optional[Dict[str, str]]=None,
                 files:Optional[Dict[str, Union[str, Tuple[Optional[str], str]]]]=None):
        
        if directories is None:
            directories = self.DEFAULT_DIRECTORIES
            
        if files is None:
            files = self.DEFAULT_FILES
            
        super().__init__(base_path=base_path, directories=directories, files=files)
        
        self.study_name    = study_name
        self.raw_base_path = base_path
        self.update()
        
    def update(self):
        if self.raw_base_path is None:
            base_path = self.study_name
        else:
            base_path = os.path.join(self.raw_base_path, self.study_name)
        self.base_path = base_path
        
    def set_study_name(self, study_name:str):
        self.study_name = study_name
        self.update()
        
    def set_base_path(self, base_path:str):
        self.raw_base_path = base_path
        self.update()