#
# This fiel contains command line cryoloBM_tools for box management
#
import sys
import argparse
from typing import List
from cryoloBM.bmtool import BMTool


TYPE_CBOX=0
TYPE_COORDS=1
TYPE_EMAN_BOX=2
TYPE_EMAN_BOX_3D=3
TYPE_EMAN_HELICON=4
TYPE_EMAN_START_END=5
TYPE_RELION_STAR=6

def get_file_type(path):
    from cryolo import CoordsIO
    if CoordsIO.is_eman1_filament_start_end(path):
        return TYPE_EMAN_START_END
    if CoordsIO.is_eman1_helicon(path):
        return TYPE_EMAN_HELICON
    if CoordsIO.is_star_filament_file(path):
        return TYPE_RELION_STAR
    if path.endswith(".coords"):
        return TYPE_COORDS
    if path.endswith(".cbox"):
        return TYPE_CBOX
    return -1


def get_tool_list() -> List[BMTool]:
    tools = []

    from cryoloBM_tools.filamentresampling import FilamentResampleTool
    fil_resample_tool = FilamentResampleTool()
    tools.append(fil_resample_tool)

    from cryoloBM_tools.coords2warp import Coords2WarpTool
    c2w_tool = Coords2WarpTool()
    tools.append(c2w_tool)

    from cryoloBM_tools.priors2star import Priors2StarTool
    p2s_tool = Priors2StarTool()
    tools.append(p2s_tool)

    from cryoloBM_tools.scale import ScaleTool
    scale_tool = ScaleTool()
    tools.append(scale_tool)

    from cryoloBM_tools.rotatecboxcoords import RotateCBOXCoords
    rotate_tool = RotateCBOXCoords()
    tools.append(rotate_tool)

    from cryoloBM_tools.cbox2coords import CBOX2Coords
    cbox2coords_tool = CBOX2Coords()
    tools.append(cbox2coords_tool)

    from cryoloBM_tools.spherical_prior import SphericalPrior
    spherical_prior_tool = SphericalPrior()
    tools.append(spherical_prior_tool)

    from cryoloBM_tools.coords2cbox import Coords2CBOX
    coords2cbox_tool = Coords2CBOX()
    tools.append(coords2cbox_tool)

    from cryoloBM_tools.cbox_compare import CoordsCompare
    coordscompare_tool = CoordsCompare()
    tools.append(coordscompare_tool)

    from cryoloBM_tools.cbox2json import cbox2json
    cbox2json_tool = cbox2json()
    tools.append(cbox2json_tool)

    return tools

def _main_():

    parser = argparse.ArgumentParser(
        description="Boxmanager Tools",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(help="sub-command help")


    tools = get_tool_list()

    tools = sorted(tools, key=lambda x: x.get_command_name())

    for tool in tools:
        tool.create_parser(subparsers)

    args = parser.parse_args()

    for tool in tools:
        if tool.get_command_name() in sys.argv[1]:
            tool.run(args)

if __name__ == "__main__":
    _main_()