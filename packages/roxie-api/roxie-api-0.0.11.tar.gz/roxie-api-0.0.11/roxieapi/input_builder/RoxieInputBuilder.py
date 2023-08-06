import os
from pathlib import Path

import jinja2
import pandas as pd

from roxieapi.api import convert_bottom_header_table_to_str, convert_table_to_str


class RoxieInputBuilder:
    """Class RoxieInputBuilder builds a ROXIE input"""

    comment = ""
    bhdata_path = ""
    cadata_path = ""
    iron_path = ""
    flags = {
        "LEND": False,
        "LWEDG": False,
        "LPERS": False,
        "LQUENCH": False,
        "LALGO": False,
        "LMIRIRON": False,
        "LBEMFEM": False,
        "LPSI": False,
        "LSOLV": False,
        "LIRON": False,
        "LMORPH": False,
        "LHARD": False,
        "LPOSTP": False,
        "LPEAK": False,
        "LINMARG": False,
        "LMARG": False,
        "LSELF": False,
        "LMQE": False,
        "LINDU": False,
        "LEDDY": False,
        "LSOLE": False,
        "LFIELD3": False,
        "LFISTR": False,
        "LSELF3": False,
        "LBRICK": False,
        "LLEAD": False,
        "LVRML": False,
        "LOPERA": False,
        "LOPER20": False,
        "LANSYS": False,
        "LRX2ANS": False,
        "LANS2RX": False,
        "LDXF": False,
        "LMAP2D": False,
        "LMAP3D": False,
        "LEXPR": False,
        "LFIL3D": False,
        "LFIL2D": False,
        "LCNC": False,
        "LANSYSCN": False,
        "LWEIRON": False,
        "LCATIA": False,
        "LEXEL": False,
        "LFORCE2D": False,
        "LAXIS": False,
        "LIMAGX": False,
        "LIMAGY": False,
        "LRAEND": False,
        "LMARKER": False,
        "LROLER2": False,
        "LROLERP": False,
        "LIMAGZZ": False,
        "LSTEP": False,
        "LIFF": False,
        "LICCA": False,
        "LICC": False,
        "LICCIND": False,
        "LITERNL": False,
        "LTOPO": False,
        "LQUEN3": False,
        "LAYER": False,
        "LEULER": False,
        "LHEAD": False,
        "LPLOT": False,
        "LVERS52": False,
        "LHARM": False,
        "LMATRF": False,
        "LF3LIN": False,
    }
    global2doption = pd.DataFrame()
    global3d = pd.DataFrame()
    block = pd.DataFrame()
    blockoption = pd.DataFrame()
    block3d = pd.DataFrame()
    lead = pd.DataFrame()
    brick = pd.DataFrame()
    iron_yoke = pd.DataFrame()
    extrusion = pd.DataFrame()
    permanentmag2 = pd.DataFrame()
    permanentmag1 = pd.DataFrame()
    layer = pd.DataFrame()
    algo = pd.DataFrame()
    design = pd.DataFrame()
    euler = pd.DataFrame()
    peak = pd.DataFrame()
    timetable2 = pd.DataFrame()
    timetable1 = pd.DataFrame()
    eddy = pd.DataFrame()
    eddyoptions = pd.DataFrame()
    quenchg = pd.DataFrame()
    quenchen = pd.DataFrame()
    quenchtm = pd.DataFrame()
    quenchp = pd.DataFrame()
    quenchs = pd.DataFrame()
    quench0d = pd.DataFrame()
    harmonictable = pd.DataFrame()
    matrf = pd.DataFrame()
    linefield = pd.DataFrame()
    harmonicoption = pd.DataFrame()
    graph = pd.DataFrame()
    graphoption = pd.DataFrame()
    plot2d = pd.DataFrame()
    plot2doption = pd.DataFrame()
    plot3d = pd.DataFrame()
    plot3doption = pd.DataFrame()
    ansysoptions = pd.DataFrame()
    objective = pd.DataFrame()

    def set_flag(self, flag_name: str, flag_value: bool) -> "RoxieInputBuilder":
        """Method setting a flag in a ROXIE input file. An error is thrown if a flag does not exist

        :param flag_name: name of a flag
        :param flag_value: value of a flag
        :return: an updated RoxieInputBuilder instance
        """
        if flag_name in self.flags.keys():
            self.flags[flag_name] = flag_value
        else:
            raise KeyError("Key")
        return self

    def build(self, output_path: str) -> None:
        """Method building a ROXIE input based on a template file

        :param output_path: an output path for the input .data file
        """
        output_str = self.prepare_data_file_str_from_template()

        with open(output_path, "wb") as input_file:
            input_file.write(bytes(output_str, "utf-8").replace(b"\r\n", b"\n"))

    def prepare_data_file_str_from_template(self) -> str:
        path = Path(os.path.dirname(__file__))
        template_loader = jinja2.FileSystemLoader(searchpath=path)
        template_env = jinja2.Environment(loader=template_loader)
        template_env.globals[
            "convert_bottom_header_table_to_str"
        ] = convert_bottom_header_table_to_str
        template_env.globals["convert_table_to_str"] = convert_table_to_str
        template_env.globals[
            "convert_flag_dct_to_str"
        ] = RoxieInputBuilder.convert_flag_dct_to_str
        template_env.globals["str"] = str

        TEMPLATE_FILE = "roxie_template.data"
        template = template_env.get_template(TEMPLATE_FILE)
        return template.render(input=self)

    @staticmethod
    def convert_flag_dct_to_str(flags: dict) -> str:
        """Static method converting a dictionary with flags into a formatted string

        :param flags: a dictionary with flags
        :return: a formatted string representation of the dictionary with flags
        """
        COLUMN_WIDTH = 11
        flag_per_line_count = 1
        flag_str = "  "
        for key, value in flags.items():
            temp = "%s=%s" % (key, "T" if value else "F")
            temp += (COLUMN_WIDTH - len(temp)) * " "
            if flag_per_line_count < 6:
                flag_str += temp
                flag_per_line_count += 1
            else:
                flag_str += temp + "\n  "
                flag_per_line_count = 1

        flag_str += "\n  /"
        return flag_str

    @staticmethod
    def append_to_outputs(
        outputs, keyword, df, line_suffix="", header_suffix=""
    ) -> None:
        """Static method appending to the output list (in place) a dataframe with a keyword

        :param outputs: a list of outputs for an input file
        :param keyword: a table keyword
        :param df: a dataframe
        """
        outputs.append("")
        outputs.append(
            convert_bottom_header_table_to_str(df, keyword, line_suffix, header_suffix)
        )
