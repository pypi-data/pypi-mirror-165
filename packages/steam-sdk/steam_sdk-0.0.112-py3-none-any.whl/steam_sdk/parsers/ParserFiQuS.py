import os
from pathlib import Path
import ruamel.yaml

from steam_sdk.builders.BuilderFiQuS import BuilderFiQuS
from steam_sdk.data import DataFiQuS as dF
from steam_sdk.parsers.ParserYAML import dict_to_yaml

class ParserFiQuS:
    """
        Class with methods to read/write FiQuS information from/to other programs
    """

    def __init__(self, builder_FiQuS: BuilderFiQuS = None):
        """
            Initialization using a BuilderFiQuS object containing FiQuS parameter structure
        """

        self.builder_FiQuS: BuilderFiQuS = builder_FiQuS

    def readFromYaml(self, file_name: str, verbose: bool = True):
        """
        """

        # Load yaml keys into DataModelMagnet dataclass
        with open(file_name + '.yaml', "r") as stream:
            dictionary_yaml = ruamel.yaml.safe_load(stream)
            self.builder_FiQuS.data_FiQuS = dF.DataFiQuS(**dictionary_yaml)

        with open(file_name + '.geom', "r") as stream:
            dictionary_yaml = ruamel.yaml.safe_load(stream)
            self.builder_FiQuS.data_FiQuS = dF.MultipoleGeometry(**dictionary_yaml)

        with open(file_name + '.set', "r") as stream:
            dictionary_yaml = ruamel.yaml.safe_load(stream)
            self.builder_FiQuS.data_FiQuS = dF.MultipoleSettings(**dictionary_yaml)

        if verbose:
            print('File {} was loaded.'.format(file_name))

    def writeFiQuS2yaml(self, full_path_file_name: str, verbose: bool = False):
        """
        ** Writes FiQuS input files **

        :param full_path_file_name:
        :param verbose:
        :return:
        """

        # If the output folder is not an empty string, and it does not exist, make it
        output_path = os.path.dirname(full_path_file_name)
        if verbose:
            print('output_path: {}'.format(output_path))
        if output_path != '' and not os.path.isdir(output_path):
            print("Output folder {} does not exist. Making it now".format(output_path))
            Path(output_path).mkdir(parents=True)

        if self.builder_FiQuS.data_FiQuS.magnet.type == 'multipole':
            dict_to_yaml(self.builder_FiQuS.data_FiQuS.dict(), full_path_file_name + '.yaml', list_exceptions=[])
            dict_to_yaml(self.builder_FiQuS.data_FiQuS_geo.dict(), full_path_file_name + '.geom', list_exceptions=[])
            dict_to_yaml(self.builder_FiQuS.data_FiQuS_set.dict(), full_path_file_name + '.set', list_exceptions=[])
        elif self.builder_FiQuS.data_FiQuS.magnet.type == 'CCT':
            dict_to_yaml(self.builder_FiQuS.data_FiQuS.dict(), full_path_file_name + '.yaml', list_exceptions=[])
        else:
            raise Exception('Incompatible magnet type.')
