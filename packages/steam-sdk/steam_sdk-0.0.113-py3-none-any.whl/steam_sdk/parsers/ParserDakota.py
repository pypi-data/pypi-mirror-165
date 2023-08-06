import os
from pathlib import Path

from steam_sdk.data.DataDakota import DataDakota
from steam_sdk.parsers.dict_to_in import dict_to_in
from steam_sdk.parsers.ParserYAML import yaml_to_data_class


class ParserDakota:
    """
        Class with methods to read/write FiQuS information from/to other programs
    """

    def __init__(self, input_DAKOTA_data_yaml, verbose: bool = True):
        """
            Initialization using a BuilderDAKOTA object containing DAKOTA parameter structure
            Read the DAKOTA input variables from a input_DAKOTA_data_yaml file and parse into the object

        """
        self.dakota_data = yaml_to_data_class(full_file_path=input_DAKOTA_data_yaml, data_class=DataDakota)

        if verbose:
            print('File {} was loaded.'.format(input_DAKOTA_data_yaml))

    def writeDAKOTA2in(self, output_file_full_path: str, verbose: bool = False):
        """
        Writes the DAKOTA object into a respective .in file according to the format
        """

        # If the output folder is not an empty string, and it does not exist, make it
        output_path = os.path.dirname(output_file_full_path)
        if verbose:
            print('output_path: {}'.format(output_path))
        if output_path != '' and not os.path.isdir(output_path):
            print("Output folder {} does not exist. Making it now".format(output_path))
            Path(output_path).mkdir(parents=True)

        dict_to_in(self.dakota_data.DAKOTA_analysis.dict(), output_file_full_path)
