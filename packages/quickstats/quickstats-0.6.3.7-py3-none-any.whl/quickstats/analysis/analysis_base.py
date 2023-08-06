from typing import Dict, List, Optional, Union, Tuple
import os
import json

from quickstats import AbstractObject

from .analysis_path_manager import AnalysisPathManager

class AnalysisBase(AbstractObject):
    
    def __init__(self, analysis_config_path:str,
                 plot_config_path:Optional[str]=None,
                 outdir:Optional[str]=None,
                 ntuple_dir:Optional[str]=None,
                 array_dir:Optional[str]=None,
                 model_dir:Optional[str]=None,
                 path_manager:Optional[AnalysisPathManager]=None,
                 verbosity:Optional[Union[int, str]]="INFO"):
        
        super().__init__(verbosity=verbosity)
        
        if path_manager is None:
            self.path_manager = AnalysisPathManager()
        else:
            self.path_manager = path_manager
        
        self.load_analysis_config(analysis_config_path)
        self.load_plot_config(plot_config_path)
        
        if outdir is None:
            outdir = self.config["paths"]["outputs"] 
        if ntuple_dir is None:
            ntuple_dir = self.config["paths"]["ntuples"]        
        if array_dir is None:
            array_dir = self.config["paths"]["arrays"]
        if model_dir is None:
            model_dir = self.config["paths"]["models"]
            
        # setup file paths used in the analysis pipeline
        self.update_paths(output_path=outdir,
                          ntuple_dir=ntuple_dir,
                          array_dir=array_dir,
                          model_dir=model_dir)
                                        
    def update_paths(self, output_path:Optional[str]=None,
                     directories:Optional[Dict[str, str]]=None,
                     files:Optional[Dict[str, Union[str, Tuple[Optional[str], str]]]]=None,
                     ntuple_dir:Optional[str]=None,
                     array_dir:Optional[str]=None,
                     model_dir:Optional[str]=None):
        
        if output_path is not None:
            self.path_manager.set_base_path(output_path)
        if directories is not None:
            self.path_manager.update_directories(directories)
        if files is not None:
            self.path_manager.update_files(files)
        if ntuple_dir is not None:
            self.path_manager.set_directory("ntuple", ntuple_dir, absolute=True)
        if array_dir is not None:
            self.path_manager.set_directory("array", array_dir, absolute=True)
        if model_dir is not None:
            self.path_manager.set_directory("model", model_dir, absolute=True)
            
    def set_study_name(self, study_name:str):
        self.path_manager.set_study_name(study_name)
        if "model" in self.path_manager.directories:
            model_dir = self.path_manager.directories["model"]
            basename = os.path.basename(os.path.dirname(model_dir))
            if basename != study_name:
                model_dir = os.path.join(model_dir, study_name)
                self.path_manager.set_directory("model", model_dir)
        
    def get_study_name(self):
        return self.path_manager.study_name
    
    def get_directory(self, directory_name:str):
        return self.path_manager.get_directory(directory_name)
    
    def get_file(self, file_name:str, validate:bool=False, **parameters):
        if validate:
            self._check_file(file_name, **parameters)
        return self.path_manager.get_resolved_file(file_name, **parameters)
    
    def _has_directory(self, directory_name:str):
        return self.path_manager.directory_exists(directory_name)
    
    def _has_file(self, file_name:str, **parameters):
        return self.path_manager.file_exists(file_name, **parameters)
    
    def _check_directory(self, directory_name:str):
        self.path_manager.check_directory(directory_name)
    
    def _check_file(self, file_name:str, **parameters):
        self.path_manager.check_file(file_name, **parameters)
        
    def load_analysis_config(self, config_path:str):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'file "{config_path}" does not exist')
        config_path = os.path.abspath(config_path)
        with open(config_path, "r") as file:
            self.config = json.load(file)
        self.path_manager.set_file("analysis_config", config_path)
        
    def load_plot_config(self, config_path:Optional[str]=None):
        # use the default plot config from the framework
        if config_path is None:
            self.plot_config = {}
            return None
        if not os.path.exists(config_path):
            raise FileNotFoundError(f'file "{config_path}" does not exist')
        config_path = os.path.abspath(config_path)
        with open(config_path, "r") as file:
            self.plot_config = json.load(file)
        self.path_manager.set_file("plot_config", config_path)
        
    def get_validated_samples(self, samples:Optional[List[str]]=None):
        if samples is not None:
            for sample in samples:
                if sample not in self.all_samples:
                    raise RuntimeError(f"unknown sample \"{sample}\"")
        else:
            samples = self.all_samples
        return samples        
        
    def resolve_channels(self, channels:List[str]):
        for channel in channels:
            if channel not in self.all_channels:
                raise ValueError(f"unknown channel: {channel}")
        return channels
    
    def resolve_samples(self, samples:Optional[List[str]]=None):
        if samples is None:
            return self.all_samples
        resolved_samples = []
        for sample_key in samples:
            if sample_key in self.config['samples']:
                for sample in self.config['samples'][sample_key]:
                    if sample not in resolved_samples:
                        resolved_samples.append(sample)
            elif (sample_key in self.all_samples) or (sample_key in self.extra_samples):
                resolved_samples.append(sample_key)
            else:
                raise RuntimeError(f"unknown sample \"{sample_key}\"")
        return resolved_samples

    def resolve_variables(self, variables:Optional[List[str]]=None):
        if variables is None:
            return self.all_variables
        resolved_variables = []
        for variable_key in variables:
            if variable_key in self.config['variables']:
                for variable in self.config['variables'][variable_key]:
                    if variable not in resolved_variables:
                        resolved_variables.append(variable)
            elif variable_key in self.all_variables:
                resolved_variables.append(variable_key)
            else:
                raise RuntimeError(f"unknown variable \"{variable_key}\"")
        return resolved_variables
    
    def resolve_class_labels(self, class_labels:Dict):
        resolved_class_labels = {}
        for label in class_labels:
            resolved_samples = self.resolve_samples(class_labels[label])
            for sample in resolved_samples:
                if sample not in resolved_class_labels:
                    resolved_class_labels[sample] = label
                else:
                    raise RuntimeError(f"multiple class labels found for the sample \"{sample}\"")
        return resolved_class_labels