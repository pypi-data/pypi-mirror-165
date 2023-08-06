from steam_sdk.data import DataModelMagnet as dM
from steam_sdk.data import DataRoxieParser as dR
from steam_sdk.data import DataFiQuS as dF


class BuilderFiQuS:
    """
        Class to generate FiQuS models
    """

    def __init__(self,
                 input_model_data: dM.DataModelMagnet = None,
                 input_roxie_data: dR.RoxieData = None,
                 flag_build: bool = True,
                 flag_plot_all: bool = False,
                 verbose: bool = True):
        """
            Object is initialized by defining FiQuS variable structure and file template.
            If verbose is set to True, additional information will be displayed
        """
        # Unpack arguments
        self.verbose: bool = verbose
        self.flag_plot_all: bool = flag_plot_all
        self.model_data: dM.DataModelMagnet = input_model_data
        self.roxie_data: dR.RoxieData = input_roxie_data

        if not self.model_data and flag_build:
            raise Exception('Cannot build model instantly without providing DataModelMagnet')

        # Data structure
        self.data_FiQuS = dF.DataFiQuS(magnet={'type': self.model_data.GeneralParameters.magnet_type})
        self.data_FiQuS.general.magnet_name = self.model_data.GeneralParameters.magnet_name
        self.data_FiQuS.magnet.type = self.model_data.GeneralParameters.magnet_type
        self.data_FiQuS.run = self.model_data.Options_FiQuS.run

        if self.data_FiQuS.magnet.type == 'multipole':
            self.data_FiQuS_geo = dF.MultipoleGeometry()
            self.data_FiQuS_set = dF.MultipoleSettings()
            if flag_build:
                self.buildDataMultipole()

        elif self.data_FiQuS.magnet.type == 'CCT':
            if flag_build:
                self.buildDataCCT()

        else:
            raise Exception('Incompatible magnet type.')

    def buildDataCCT(self):
        """
            Load selected conductor data from DataModelMagnet keys, check inputs, calculate and set missing variables
        """
        # --------- geometry ----------
        # windings
        for key, value in self.model_data.Options_FiQuS.cct.geometry.windings.dict().items():       # for keys that are present in the FiQUS Options model data (but not all keys in data FiQuS)
            self.data_FiQuS.magnet.geometry.windings.__setattr__(key, value)
        self.data_FiQuS.magnet.geometry.windings.n_turnss = self.model_data.CoilWindings.CCT_straight.winding_numberTurnsFormers  # additional, picked form other places in model data

        self.data_FiQuS.magnet.postproc.windings_wwns = self.model_data.CoilWindings.CCT_straight.winding_numRowStrands
        self.data_FiQuS.magnet.postproc.windings_whns = self.model_data.CoilWindings.CCT_straight.winding_numColumnStrands
        self.data_FiQuS.magnet.postproc.winding_order = self.model_data.CoilWindings.CCT_straight.winding_order

        # fqpls
        self.data_FiQuS.magnet.geometry.fqpls = self.model_data.Options_FiQuS.cct.geometry.fqpls

        # formers
        for key, value in self.model_data.Options_FiQuS.cct.geometry.formers.dict().items():       # for keys that are present in the model data (but not all keys in data FiQuS)
            self.data_FiQuS.magnet.geometry.formers.__setattr__(key, value)
        self.data_FiQuS.magnet.geometry.formers.r_ins = self.model_data.CoilWindings.CCT_straight.former_inner_radiuses  # additional, picked form other places in model data

        # air
        self.data_FiQuS.magnet.geometry.air = self.model_data.Options_FiQuS.cct.geometry.air   # for keys that are present in the model data and in data FiQuS - they are the same

        # ------------- mesh --------------
        self.data_FiQuS.magnet.mesh = self.model_data.Options_FiQuS.cct.mesh                # for keys that are present in the model data and in data FiQuS - they are the same

        # ------------- solve -------------
        self.data_FiQuS.magnet.solve = self.model_data.Options_FiQuS.cct.solve              # for keys that are present in the model data and in data FiQuS - they are the same

        # ------------- postproc ---------
        for key, value in self.model_data.Options_FiQuS.cct.postproc.dict().items():       # for keys that are present in the model data and in data FiQuS - they are the same
            self.data_FiQuS.magnet.postproc.__setattr__(key, value)

    def buildDataMultipole(self):
        """
            Load selected conductor data from DataModelMagnet keys, check inputs, calculate and set missing variables
        """
        # geom file
        self.data_FiQuS_geo.Roxie_Data = dR.RoxieData(**self.roxie_data.dict())

        # set file
        self.data_FiQuS_set.Model_Data_GS.general_parameters.I_ref = \
            [self.model_data.Options_LEDET.field_map_files.Iref] * len(self.data_FiQuS_geo.Roxie_Data.coil.coils)
        for cond in self.model_data.Conductors:
            self.data_FiQuS_set.Model_Data_GS.conductors[cond.name] = dF.MultipoleConductor(cable={'type': cond.cable.type})
            conductor = self.data_FiQuS_set.Model_Data_GS.conductors[cond.name]
            conductor.cable.bare_cable_width = cond.cable.bare_cable_width
            conductor.cable.bare_cable_height_mean = cond.cable.bare_cable_height_mean

        # yaml file
        self.data_FiQuS.magnet.options = self.model_data.Options_FiQuS.multipole.options
        self.data_FiQuS.magnet.options.plot_all = self.flag_plot_all

        self.data_FiQuS.magnet.mesh = self.model_data.Options_FiQuS.multipole.mesh

        self.data_FiQuS.magnet.solve.I_initial = \
            [self.model_data.Power_Supply.I_initial] * len(self.data_FiQuS_geo.Roxie_Data.coil.coils)
        self.data_FiQuS.magnet.solve.pro_template = self.model_data.Options_FiQuS.multipole.solve.pro_template
        self.data_FiQuS.magnet.solve.getdp_exe_path = self.model_data.Options_FiQuS.multipole.solve.getdp_exe_path
        self.data_FiQuS.magnet.solve.BH_curves_path = self.model_data.Options_FiQuS.multipole.solve.BH_curves_path

        self.data_FiQuS.magnet.post_proc = self.model_data.Options_FiQuS.multipole.post_proc
