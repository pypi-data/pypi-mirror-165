import os
import sys
from pathlib import Path
from ruamel import yaml
from steam_sdk.builders.BuilderDakota import BuilderDakota
from steam_sdk.analyses.AnalysisSTEAM import AnalysisSTEAM
from steam_sdk.data.DataAnalysis import ModifyModel, AddAuxiliaryFile
from steam_sdk.data.DataAnalysis import DataAnalysis
from steam_sdk.parsers.ParserYAML import yaml_to_data_class

class ParsimDakota:

    def __init__(self, analysis_yaml_path: DataAnalysis = None):
        #self.Builder = BuilderDAKOTA(input_DAKOTA_yaml)
        # self.STEAM_Analysis = AnalysisSTEAM(relative_path_settings='..', input_dictionary=self.Builder.DAKOTA_data.dict(), verbose=True)
        #self.input_variables = self.Builder.DAKOTA_data.DAKOTA_analysis.variables
        #self.global_run_counter = 0

        self.analysis_data = yaml_to_data_class(analysis_yaml_path, DataAnalysis)

        path_dakota_python = os.path.join(self.analysis_data.PermanentSettings.Dakota_path, 'share\dakota\Python')
        print('path_dakota_python:        {}'.format(path_dakota_python))
        sys.path.insert(0, path_dakota_python)
        from dakota.interfacing import read_parameters_file
        self.read_parameters_file = read_parameters_file
        self.post_processed_results = {}
        self.file_to_post_process = ''

    def prepare_analysis(self, params):
        counter = 0
        additional_step_names = []

        step_modify_magnets = 'makeModel_Ref'
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets] = ModifyModel(type='MakeModel')
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].model_name = 'BM'
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].file_model_data = self.Builder.DAKOTA_data.STEAMmodel.file_model_data
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].case_model = self.Builder.DAKOTA_data.STEAMmodel.case_model
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].flag_build = True
        additional_step_names.append(step_modify_magnets)

        for variable in self.input_variables.variable_arguments['descriptors']:
            step_modify_magnets = 'modifyModel_magnets'
            self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets] = ModifyModel(
                type='ModifyModel')
            self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].model_name = 'BM'
            self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[
                step_modify_magnets].variable_to_change = variable
            self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].variable_value = params[counter]
            additional_step_names.append(step_modify_magnets)
            counter = counter + 1

        # Include last steps
        step_modify_magnets = 'modifyModel_last'
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets] = ModifyModel(type='ModifyModel')
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets].model_name = 'BM'
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[
            step_modify_magnets].simulation_name = self.Builder.DAKOTA_data.STEAMmodel.name
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[
            step_modify_magnets].software = self.Builder.DAKOTA_data.STEAMmodel.software
        additional_step_names.append(step_modify_magnets)
        ##
        step_modify_magnets = 'RunSimulation'
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[step_modify_magnets] = ModifyModel(
            type='RunSimulation')
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[
            step_modify_magnets].software = self.Builder.DAKOTA_data.STEAMmodel.software
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[
            step_modify_magnets].simulation_name = self.Builder.DAKOTA_data.STEAMmodel.name
        self.STEAM_Analysis.data_analysis.AnalysisStepDefinition[
            step_modify_magnets].simulation_numbers = self.global_run_counter
        additional_step_names.append(step_modify_magnets)
        self.global_run_counter = self.global_run_counter + 1
        return additional_step_names

    def post_process(self):
        # if self.Builder.DAKOTA_data.STEAMmodel.software == 'PSPICE':
        self._post_process_PSPICE()
        # elif self.Builder.DAKOTA_data.STEAMmodel.software == 'LEDET':
        #     self._post_process_LEDET()
        # elif self.Builder.DAKOTA_data.STEAMmodel.software == 'FiQuS':
        #     self._post_process_FiQuS()
        # elif self.Builder.DAKOTA_data.STEAMmodel.software == 'PyBBQ':
        #     self._post_process_PyBBQ()
        # else:
        #     raise Exception('Software not understood.')

    def _post_process_PSPICE(self):  # this should belong to the tool driver to know how to post process
        # use self.file_to_post_process to read the file
        # use file_to_post_process = os.path.join(self.STEAM_Analysis.output_path, f'{self.Builder.DAKOTA_data.STEAMmodel.name}.csd')
        self.post_processed_results = {'max_V': 12312}
        # return 1

    def _post_process_LEDET(self, outputfile: str):  # this should belong to the tool driver to know how to post process
        raise Exception('Not implemented yet.')

    def _post_process_FiQuS(self, outputfile: str):  # this should belong to the tool driver to know how to post process
        raise Exception('Not implemented yet.')

    def _post_process_PyBBQ(self, outputfile: str):  # this should belong to the tool driver to know how to post process
        raise Exception('Not implemented yet.')

    def drive(self):
        params, result_for_dakota = self.read_parameters_file()

        ## Run steps and change the model
        #self.prepare_analysis(params)

        ## Run the model
        #self.STEAM_Analysis.run_analysis()

        # Post process results to load post processing results to a dictionary of self.post_processed_results
        self.post_process()

        # Write back to DAKOTA
        for i, label in enumerate(result_for_dakota):
            if result_for_dakota[label].asv.function:
                result_for_dakota[label].function = self.post_processed_results[label]

        result_for_dakota.write()
        return 1
