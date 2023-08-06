import re
from typing import List, Tuple, Dict, Union
from io import StringIO

import pandas as pd
from pymbse.commons import text_file


def extract_objective_table(
    output_lines: List[str],
    index_start_objective_table: int,
    n_objectives: int,
) -> pd.DataFrame:
    """Function extracting an objective table from ROXIE output file and converting it into a dataframe.

    :param output_lines: a list of lines from the output text file
    :param index_start_objective_table: a start index of the objective table
    :param n_objectives: the length of the objective table
    :return: dataframe with objective table
    """
    objectives_table = output_lines[
        index_start_objective_table : index_start_objective_table + n_objectives + 1
    ]
    objectives_table_lines = [
        "\t".join(objective_table.split()) for objective_table in objectives_table
    ]

    TESTDATA = StringIO("\n".join(objectives_table_lines))
    objective_table_df = pd.read_csv(TESTDATA, sep="\t", index_col=0)
    objective_table_df.rename(columns={"WEIGHTED": "WEIGHTED OBJ"}, inplace=True)
    objective_table_df.drop(columns="OBJ", inplace=True)
    return objective_table_df


def find_index_start_and_length_objective_table(
    output_lines: List[str], table_keyword: str
) -> Tuple[int, int]:
    """Function finding a start index and length of an objective table in output lines from a .output ROXIE file

    :param output_lines: list of output lines
    :param table_keyword: a keyword of the objective table
    :return: a tuple with objective table start index and its length
    """
    index_objective_table = None
    n_objectives = None
    for index_line, output_line in enumerate(output_lines):
        if "OBJECTIVE" in output_line and "S1" in output_line:
            index_objective_table = index_line

        if table_keyword in output_line:
            matches = re.findall(r"\d+", output_line)
            if matches:
                n_objectives = int(matches[0])

    if index_objective_table is None or n_objectives is None:
        raise IndexError("Objective table not found in the output")

    return index_objective_table, n_objectives


def convert_bottom_header_table_to_str(
    block_df: pd.DataFrame, keyword: str, line_suffix="", header_suffix=""
) -> str:
    """Function converting a dataframe with a keyword and suffix to string. The string is used to create a ROXIE .data
    input file.

    :param block_df: a dataframe with content to be converted into a bottom header table string
    :param keyword: a keyword for the table
    :param line_suffix: a string added at the end of each of line to match the ROXIE formatting
    :return: a string representation of a bottom header table
    """
    if header_suffix:
        keyword_and_length_str = "%s %s" % (keyword, header_suffix)
    else:
        keyword_and_length_str = "%s %d" % (keyword, len(block_df))
    if block_df.empty:
        return keyword_and_length_str
    else:
        block_str = block_df.to_string(index=False)
        block_str_lines = block_str.split("\n")
        block_str_lines = block_str_lines[1:] + [block_str_lines[0]]
        block_str = (line_suffix + "\n").join(block_str_lines)
        return "%s\n%s" % (keyword_and_length_str, block_str)


def convert_table_to_str(block_df: pd.DataFrame, keyword: str, header_suffix="") -> str:
    """Function converting a dataframe with a keyword and suffix to string without bottom header columns.
    The string is used to create a ROXIE .datainput file.

    :param block_df: a dataframe with content to be converted into a bottom header table string
    :param keyword: a keyword for the table
    :param line_suffix: a string added at the end of each of line to match the ROXIE formatting
    :return: a string representation of a bottom header table
    """
    if header_suffix:
        keyword_and_length_str = "%s %s" % (keyword, header_suffix)
    else:
        keyword_and_length_str = "%s %d" % (keyword, len(block_df))

    block_str = block_df.to_string(index=False)
    block_str_lines = block_str.split("\n")
    # header at the first index is skipped
    block_str = "\n".join(block_str_lines[1:])
    return "%s\n%s" % (keyword_and_length_str, block_str)


def read_bottom_header_table(roxie_file_path: str, keyword="CABLE") -> pd.DataFrame:
    """Function reading a bottom header table from ROXIE .data, .cadata, .output files

    :param roxie_file_path: a path to a roxie file
    :param keyword: a table keyword
    :return: a dataframe with content of a table given by a keyword
    """
    with open(roxie_file_path, "r") as text_file:
        text_file_lines = text_file.read().split("\n")

    index_start, n_lines = find_index_start_and_length_bottom_header_table(
        text_file_lines, keyword
    )
    return extract_bottom_header_table(text_file_lines, index_start, n_lines)


def find_index_start_and_length_bottom_header_table(
    output_lines: List[str], table_keyword: str
) -> Tuple[int, int]:
    """Function finding the start and length of a table in ROXIE .output or .cadata or .data file.
    If a table keyword can't be found, the an IndexError is thrown.

    :param output_lines: a list of lines read from a ROXIE file
    :param table_keyword: a keyword for the objective table
    :return: a tuple with an index of the start of bottom header table and its length
    """
    len_keyword = len(table_keyword)
    for index_line, output_line in enumerate(output_lines):

        if (len(output_line) >= len_keyword) and (
            output_line[0:len_keyword] == table_keyword
        ):
            index_table_start = index_line
            matches = re.findall(r"\d+", output_line)
            if matches:
                n_lines_table = int(matches[0])
                return index_table_start, n_lines_table

    raise IndexError("Not found start index and length for keyword %s" % table_keyword)


def extract_bottom_header_table(
    text_file_lines: List[str], index_start: int, n_lines: int
) -> pd.DataFrame:
    """Function extracting a bottom header template from ROXIE .data and .cadata files. The method requires a start index
    in the table as well as the number of lines the table occupies.

    :param text_file_lines: an input list of lines from a ROXIE .data or .cadata file
    :param index_start: an index where the table starts
    :param n_lines: the number of lines occupied by the table
    :return: a dataframe with the table
    """
    value_rows = text_file_lines[index_start + 1 : index_start + n_lines + 1]
    header = text_file_lines[index_start + n_lines + 1]
    if "Comment" in header:
        columns = ",".join(header.split()[:-1])
    else:
        columns = ",".join(header.split())

    # Replace comment
    values_comma_separated = []
    comments = []
    for value_row in value_rows:
        if "'" in value_row:
            quotation_split = value_row.split("'")
            values_without_comment = ",".join(quotation_split[0].split())
            values_comma_separated.append(values_without_comment)
            comments.append(quotation_split[1])
        else:
            values_comma_separated.append(",".join(value_row.split()))

    TESTDATA = StringIO("\n".join([columns] + values_comma_separated))
    objective_table_df = pd.read_csv(TESTDATA, sep=",")
    if comments:
        objective_table_df["Comment"] = comments
    return objective_table_df


def read_nested_bottom_header_table(
    roxie_file_path: str, keyword="LAYER"
) -> pd.DataFrame:
    """Function reading a bottom header table from ROXIE .data, .cadata, .output files

    :param roxie_file_path: a path to a roxie file
    :param keyword: a table keyword
    :return: a nested dataframe with content of a table given by a keyword
    """
    with open(roxie_file_path, "r") as text_file:
        text_file_lines = text_file.read().split("\n")

    index_start, n_lines = find_index_start_and_length_bottom_header_table(
        text_file_lines, keyword
    )

    return extract_nested_bottom_header_table(text_file_lines, index_start, n_lines)


def extract_nested_bottom_header_table(
    text_file_lines: List[str], index_start: int, n_lines: int
):
    """Function extracting a bottom header template from ROXIE .data and .cadata files. The method requires a start index
    in the table as well as the number of lines the table occupies.

    :param text_file_lines: an input list of lines from a ROXIE .data or .cadata file
    :param index_start: an index where the table starts
    :param n_lines: the number of lines occupied by the table
    :return: a dataframe with the table
    """
    value_rows = text_file_lines[index_start + 1 : index_start + n_lines + 1]
    headers = text_file_lines[index_start + n_lines + 1].split()

    header_values = []
    for value_row in value_rows:
        header_value: Dict[str, Union[int, List[int]]] = {}
        values = value_row.split()
        for index, header in enumerate(headers[:-1]):
            header_value[header] = int(values[index])

        # It is assumed that the remaining values for a list assigned to the last column
        # Thus it starts from len(headers) - 1 until the last but one element (the last one is \ character)
        remaining_values = values[len(headers) - 1 : -1]
        header_value[headers[-1]] = [int(value) for value in remaining_values]
        header_values.append(header_value)

    return pd.DataFrame(header_values)


def read_block_coordinates_from_cnc_file(cnc_file_path: str) -> List[pd.DataFrame]:
    with open(cnc_file_path, "r") as file:
        cnc_lines = file.readlines()

    wedge_indices = [index for index, line in enumerate(cnc_lines) if "WEDGE" in line]
    wedge_indices += [len(cnc_lines) + 1]
    position_header_indices = [
        index for index, line in enumerate(cnc_lines) if "X(mm)" in line
    ]

    pattern = r"([+-]?\d+(?:\.\d+)?)"
    prog = re.compile(pattern)

    block_coordinates = []

    for index in range(len(position_header_indices)):
        index_start = position_header_indices[index] + 1
        index_stop = wedge_indices[index + 1] - 1
        coordinates = cnc_lines[index_start:index_stop]
        coordinates_df = pd.DataFrame(
            [prog.findall(coordinate) for coordinate in coordinates],
            columns=["X(mm)", "Y(mm)", "Z(mm)"],
        )
        coordinates_df[coordinates_df.columns] = coordinates_df[
            coordinates_df.columns
        ].apply(pd.to_numeric, errors="coerce")

        block_coordinates.append(coordinates_df)

    return block_coordinates


def convert_figures_of_merit_to_dict(fom_df: pd.DataFrame) -> dict:
    fom_dct = {}
    for index, row in fom_df.iterrows():
        key = "%s_%d_%d" % (index, row["S1"], row["S2"])
        fom_dct[key] = row["OBJECTIVE.1"]

    return fom_dct


def read_figures_of_merit_table_from_output(output_file_path: str) -> pd.DataFrame:
    """

    Returns:
        object:
    """
    N_OBJECTIVES_KEYWORD = "NUMBER OF OBJECTIVES AND CONSTRAINTS"
    output_file = open(output_file_path, "r")
    output_lines = output_file.read().split("\n")
    output_file.close()
    (
        idx_start_obj_table,
        n_objectives,
    ) = find_index_start_and_length_objective_table(output_lines, N_OBJECTIVES_KEYWORD)
    objective_table_df = extract_objective_table(
        output_lines, idx_start_obj_table, n_objectives
    )
    return objective_table_df


def update_force2d_with_field_scaling(
    roxie_force_input_path: str,
    roxie_force_output_path: str,
    field: float,
    target_field: float,
) -> None:
    """Static method scaling ROXIE force with actual and target field

    :param roxie_force_input_path: input path with ROXIE Lorentz force
    :param roxie_force_output_path: output path with ROXIE Lorentz force
    :param field: actual field in tesla
    :param target_field: target field in tesla
    """
    roxie_force_txt = text_file.readlines(roxie_force_input_path)

    # # convert text input to a list of floats
    scaling = (target_field / field) ** 2
    roxie_force = []
    for roxie_force_txt_el in roxie_force_txt:
        row_float = [
            float(el)
            for el in roxie_force_txt_el.replace("\n", "").split(" ")
            if el != ""
        ]
        row_float[2] *= scaling
        row_float[3] *= scaling
        roxie_force.append(row_float)

    with open(roxie_force_output_path, "w") as file_write:
        for roxie_force_el in roxie_force:
            row_str = [str(roxie_force_el_el) for roxie_force_el_el in roxie_force_el]
            file_write.write(" ".join(row_str) + "\n")


def convert_roxie_force_file_to_ansys(
    input_force_file_path: str, output_force_file_path: str
) -> None:
    """Function preparing a force file for ANSYS from a ROXIE Lorentz force file, .force2d

    :param input_force_file_path: a name of a ROXIE Lorentz force file
    :param output_force_file_path: a name of an output file for ANSYS
    """
    force_txt = text_file.readlines(input_force_file_path)

    ansys_force = []
    for force_txt_el in force_txt:
        row_float = [
            float(el) for el in force_txt_el.replace("\n", "").split(" ") if el != ""
        ]
        ansys_force.append("nodeNum = NODE(%f, %f, 0.0)" % tuple(row_float[:2]))
        ansys_force.append("F,nodeNum,FX, %f" % row_float[2])
        ansys_force.append("F,nodeNum,FY, %f" % row_float[3])

    text_file.writelines(output_force_file_path, ansys_force)
