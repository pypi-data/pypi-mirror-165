import os
import sys
import subprocess
from steam_sdk.parsers.ParserYAML import yaml_to_data_class
from steam_sdk.data.DataFiQuS import DataFiQuS
import pip
import subprocess
import sys


class DriverFiQuS:
    """
        Class to drive FiQuS models
    """

    def __init__(self, FiQuS_path='', FiQuS_GetDP_path=''):
        pass
        # try:
        #     from fiqus.MainFiQuS import MainFiQuS
        #     print('FiQuS is already installed!')
        # except Exception as err:
        #     print(err)
        #     print('FiQuS is not installed. Installing it now!')
        #     #subprocess.check_call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'])
        #     current_path = os.getcwd()
        #     os.chdir(FiQuS_path)
        #     subprocess.check_call([sys.executable, "-m", "pip", "install", 'fiqus'])
        #     os.chdir(current_path)
        #     from fiqus.MainFiQuS import MainFiQuS

        sys.path.insert(0, FiQuS_path)
        from fiqus.MainFiQuS import MainFiQuS as MF
        self.MainFiQuS = MF
        # try:
        #     import fiqus
        #     print('Imported okay')
        # except ImportError:
        #     current_path = os.getcwd()
        #     os.chdir(FiQuS_path)
        #     #subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'upgrade', 'pip'])
        #     #subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', '-y', 'fiqus'])
        #     #subprocess.check_call([sys.executable, 'setup.py', 'bdist_wheel', 'sdist'])
        #     subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'fiqus'])
        #     os.chdir(current_path)
        #     #subprocess.check_call([sys.executable, "fiqus", "--no-index", "--find-links", "E://Python//steam-fiqus-dev"])
        #     #subprocess.check_call([sys.executable, "-m" 'fiqus', '--no-index', '--find-links', r'E:///Python//steam-fiqus-dev'])
        # finally:
        #     pass
        #     #import fiqus



    def run_FiQuS(self, input_file_path: str, outputDirectory: str = 'output', verbose=True):


        #
        # # act
        pass
        #self.MainFiQuS(input_file_path=input_file_path, model_folder=outputDirectory)
        # print(fdm)
        # # Unpack arguments
        # path_exe = self.path_exe
        # path_folder_FiQuS = self.path_folder_FiQuS
        # path_folder_FiQuS_input = self.path_folder_FiQuS_input
        # verbose = self.verbose
        #
        # full_path_input = os.path.join(path_folder_FiQuS_input, simFileName)
        # full_path_output = os.path.join(path_folder_FiQuS, outputDirectory)
        #
        # model_data_path = os.path.join(full_path_input + '.yaml')
        #
        # if not os.path.isdir(full_path_output):
        #     print("Output folder {} does not exist. Making it now".format(full_path_output))
        #     Path(full_path_output).mkdir(parents=True)
        #
        # if verbose:
        #     print('path_exe =             {}'.format(path_exe))
        #     print('path_folder_FiQuS =    {}'.format(path_folder_FiQuS))
        #     print('simFileName =          {}'.format(simFileName))
        #     print('outputDirectory =      {}'.format(outputDirectory))
        #     print('full_path_input =      {}'.format(full_path_input))
        #     print('full_path_output =     {}'.format(full_path_output))

        # Run model
        #return subprocess.call(['py', self.path_exe, model_data_path, outputDirectory])

