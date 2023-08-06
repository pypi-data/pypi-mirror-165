from pydantic import BaseModel
from typing import (Dict, List, Union, Literal)
from steam_sdk.data.DataRoxieParser import RoxieData
from steam_sdk.data.DataModelMagnet import RunFiQuS
from steam_sdk.data.DataModelMagnet import MeshCCT
from steam_sdk.data.DataModelMagnet import SolveCCT
from steam_sdk.data.DataModelMagnet import FQPL_g
from steam_sdk.data.DataModelMagnet import Air_g
from steam_sdk.data.DataModelMagnet import OptionMultipole
from steam_sdk.data.DataModelMagnet import MeshMultipole
from steam_sdk.data.DataModelMagnet import PostProcMultipole


class MultipoleRibbon(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Ribbon']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class MultipoleRutherford(BaseModel):
    """
        Rutherford cable type
    """
    type: Literal['Rutherford']
    bare_cable_width: float = None
    bare_cable_height_mean: float = None


class MultipoleConductor(BaseModel):
    """
        Class for conductor type
    """
    cable: Union[MultipoleRutherford, MultipoleRibbon] = {'type': 'Rutherford'}


class MultipoleGeneralSetting(BaseModel):
    """
        Class for general information on the case study
    """
    I_ref: List[float] = None


class MultipoleModelDataSetting(BaseModel):
    """
        Class for model data
    """
    general_parameters: MultipoleGeneralSetting = MultipoleGeneralSetting()
    conductors: Dict[str, MultipoleConductor] = {}


class MultipoleSettings(BaseModel):
    """
        Class for FiQuS multipole settings (.set)
    """
    Model_Data_GS: MultipoleModelDataSetting = MultipoleModelDataSetting()


class MultipoleGeometry(BaseModel):
    """
        Class for FiQuS multipole Roxie data (.geom)
    """
    Roxie_Data: RoxieData = RoxieData()


# Modified classes with respect to Options_FiQuS.multipole
class MultipoleSolve(BaseModel):
    I_initial: List[float] = None
    pro_template: str = None  # file name of .pro template file
    getdp_exe_path: str = None  # absolute path to GetDP executable
    BH_curves_path: str = None  # absolute path to iron BH curves pro file
############################


# Modified classes with respect to Options_FiQuS.cct
class CCTWinding_G(BaseModel):  # Geometry related windings _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_wms: List[float] = None  # radius of the middle of the winding
    n_turnss: List[float] = None  # number of turns
    ndpts: List[int] = None  # number of divisions of turn, i.e. number of hexagonal elements for each turn
    ndpt_ins: List[int] = None  # number of divisions of terminals ins
    ndpt_outs: List[int] = None  # number of divisions of terminals outs
    lps: List[float] = None  # layer pitch
    alphas: List[float] = None  # tilt angle
    wwws: List[float] = None  # winding wire widths (assuming rectangular)
    wwhs: List[float] = None  # winding wire heights (assuming rectangular)


class CCTFormerG(BaseModel):  # Geometry related formers _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_ins: List[float] = None  # inner radius
    r_outs: List[float] = None  # outer radius
    z_mins: List[float] = None  # extend of former  in negative z direction
    z_maxs: List[float] = None  # extend of former in positive z direction


class CCTGeometry(BaseModel):
    """
        Level 2: Class for FiQuS CCT for FiQuS input
    """
    windings: CCTWinding_G = CCTWinding_G()
    fqpls: FQPL_g = FQPL_g()
    formers: CCTFormerG = CCTFormerG()
    air: Air_g = Air_g()


class CCTPostproc(BaseModel):
    """
        Class for FiQuS CCT input file
    """
    windings_wwns: List[int] = None  # wires in width direction numbers
    windings_whns: List[int] = None  # wires in height direction numbers
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like :LEDET3D
    winding_order: List[int] = None
    fqpl_export_trim_tol: List[float] = None  # this multiplier times winding extend gives 'z' coordinate above(below) which hexes are exported for LEDET, length of this list must match number of fqpls
    variables: List[str] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: List[str] = None  # Name of file extensions o post-process by python Gmsh API, like .pos
############################


class CCTDM(BaseModel):
    """
        Class for FiQuS CCT
    """
    type: Literal['CCT']
    geometry: CCTGeometry = CCTGeometry()
    mesh: MeshCCT = MeshCCT()
    solve: SolveCCT = SolveCCT()
    postproc: CCTPostproc = CCTPostproc()


class MPDM(BaseModel):
    """
        Class for FiQuS multipole
    """
    type: Literal['multipole']
    options: OptionMultipole = OptionMultipole()
    mesh: MeshMultipole = MeshMultipole()
    solve: MultipoleSolve = MultipoleSolve()
    post_proc: PostProcMultipole = PostProcMultipole()


class General(BaseModel):
    """
        Class for FiQuS general
    """
    magnet_name: str = None


class DataFiQuS(BaseModel):
    """
        Class for FiQuS
    """
    general: General = General()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[MPDM, CCTDM] = {'type': 'multipole'}


