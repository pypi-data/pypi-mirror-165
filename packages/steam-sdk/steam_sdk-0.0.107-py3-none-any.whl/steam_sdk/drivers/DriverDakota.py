import subprocess
import os


class DriverDakota:

    def __init__(self, Dakota_path, analysis_yaml_path=None, dakota_input_folder=None, dakota_output_folder=None):

        # Define settings file
        self.Dakota_path = Dakota_path
        self.analysis_yaml_path = analysis_yaml_path
        self.dakota_output_folder = dakota_output_folder

    def run(self, input_file_path):
        """
        Runs dakota.exe with the input file specified
        :param input_file_path: full path to the input file, with its name and .in
        :return: None, runs dakota
        """
        os.chdir(self.dakota_output_folder)
        with open('driver_link.py', 'w') as f:
            f.write('from steam_sdk.drivers.DriverAnalysis import DriverAnalysis')
            f.write(f'\nda = DriverAnalysis(r"{self.analysis_yaml_path}")')
            f.write('\nda.drive()')

        subprocess.call([self.Dakota_path, '-i', input_file_path])

