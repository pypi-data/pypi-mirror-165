from pydantic import BaseModel
from typing import (List, Union, Literal, Dict)
from steam_sdk.data.DataSettings import DataSettings


############################
# General parameters
class Model(BaseModel):
    """
        Level 2: Class for information on the model
    """
    name: str = None
    version: str = None
    case: str = None
    state: str = None


class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    analysis_name: str = None
    flag_permanent_settings: bool = None
    model: Model = Model()


############################
# Working folders
class WorkingFolders(BaseModel):
    """
        Level 1: Class for information on the working folders
    """
    library_path: str = None  #
    output_path: str = None  # it would be nice if model_name and software could be read as parameters from other keys (anchors)
    temp_path: str = None


############################
# Analysis step definition
class MakeModel(BaseModel):
    """
        Level 2: Analysis step to generate a model using BuilderModel
    """
    type: Literal['MakeModel']
    model_name: str = None
    file_model_data: str = None  # it would be nice if it could be read as parameters from other keys (anchors)
    case_model: str = None
    software: List[str] = []
    simulation_name: str = None
    simulation_number: int = None
    flag_build: bool = None
    flag_dump_all: bool = None
    verbose: bool = None
    flag_plot_all: bool = None
    flag_json: bool = None


class ModifyModel(BaseModel):
    """
        Level 2: Analysis step to modify an existing BuilderModel object by changing one variable
    """
    type: Literal['ModifyModel']
    model_name: str = None
    variable_to_change: str = None
    variable_value: list = []
    new_model_name: List[str] = []  # if not empty, new copies of the model object will be built
    simulation_numbers: List[int] = []  # if not empty, simulation files will be built
    simulation_name: str = None
    software: List[str] = []


class ModifyModelMultipleVariables(BaseModel):
    """
        Level 2: Analysis step to modify an existing BuilderModel object by changing a list of variables
    """
    type: Literal['ModifyModelMultipleVariables']
    model_name: str = None
    variables_to_change: List[str] = []
    variables_value: List[list] = [[]]
    new_model_name: List[str] = []  # if not empty, new copies of the model object will be built
    simulation_numbers: List[int] = []  # if not empty, simulation files will be built
    simulation_name: str = None
    software: List[str] = []


class SetUpFolder(BaseModel):
    """
        Level 2: Analysis step to set up the folder structure for the required simulation software
    """
    type: Literal['SetUpFolder']
    simulation_name: str = None
    software: List[str] = []


class AddAuxiliaryFile(BaseModel):
    """
        Level 2: Analysis step to add/change an auxiliary file
    """
    type: Literal['AddAuxiliaryFile']
    software: str = None
    simulation_name: str = None
    simulation_numbers: List[int] = []  # if not empty, simulation files will be built
    full_path_aux_file: str = None
    new_file_name: str = None  # if empty, file is not renamed


class RunSimulation(BaseModel):
    """
        Level 2: Analysis step to run a simulation file
    """
    type: Literal['RunSimulation']
    software: str = None
    simulation_name: str = None
    simulation_numbers: List[int] = []
    simFileType: str = None


class PostProcess(BaseModel):
    """
        Level 2: Analysis step to run a simulation file
    """
    type: Literal['PostProcess']


# class AnalysisStep(BaseModel):
#     """
#         Level 1: Class for information on the analysis step
#         Objects of this class will be defined in AnalysisStepDefinition
#     """
#     step: Union[MakeModel, ModifyModel, ModifyModelMultipleVariables, SetUpFolder, ChangeAuxiliaryFile, RunSimulation, PostProcess] = {}

############################
# Highest level
class DataAnalysis(BaseModel):
    '''
        **Class for the circuit netlist inputs**

        This class contains the data structure of an analysis performed with STEAM_SDK.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModelCircuit object
    '''

    GeneralParameters: General = General()
    PermanentSettings: DataSettings = DataSettings()
    WorkingFolders: WorkingFolders = WorkingFolders()
    AnalysisStepDefinition: Dict[str, Union[MakeModel, ModifyModel, ModifyModelMultipleVariables, SetUpFolder, AddAuxiliaryFile, RunSimulation, PostProcess]] = {}
    AnalysisStepSequence: List[str] = []  # Here the analysis steps are defined, in execution order. Names must be defined in AnalysisStepDefinition. Repetitions ARE allowed.
