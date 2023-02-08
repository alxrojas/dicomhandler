import os
from contextlib import nullcontext as does_not_raise
from io import StringIO
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


@pytest.mark.parametrize(
    "patient_s, list_struct, name_buff",
    [
        ("patient_0_s.gz", [], "struct_buff_1.gz"),
        ("patient_0_s.gz", ["space2", "space4"], "struct_buff_2.gz"),
        ("patient_0_s.gz", ["space6"], "struct_buff_3.gz"),
    ],
)
# These tests verify if the method writes in the correct way
# the buffer. In order to do it, two dataframes from a
# expected buffer and output buffer are compared.
def test_equality_buffers(
    di_1p_fixt, patient_s, list_struct, name_buff, load_buff
):
    di = di_1p_fixt(patient_s, "test_struct_to_csv")
    buff_res = StringIO()
    di.struct_to_csv(path_or_buff=buff_res, names=list_struct)
    buff_res.seek(0)
    result = pd.read_csv(buff_res)
    path = Path(os.getcwd() + "/tests/data/test_struct_to_csv/" + name_buff)
    buff_exp = load_buff(path)
    buff_exp.seek(0)
    expected = pd.read_csv(buff_exp)
    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "patient_s, list_struct, name_csv, exp_csv",
    [
        ("patient_0_s.gz", [], "res_csv_struct_1.csv", "exp_csv_struct_1.csv"),
        (
            "patient_0_s.gz",
            ["space2", "space4"],
            "res_csv_struct_2.csv",
            "exp_csv_struct_2.csv",
        ),
        (
            "patient_0_s.gz",
            ["space6"],
            "res_csv_struct_3.csv",
            "exp_csv_struct_3.csv",
        ),
        ("patient_0_s.gz", [], "res_txt_struct_1.txt", "exp_txt_struct_1.txt"),
        (
            "patient_0_s.gz",
            ["space2", "space4"],
            "res_txt_struct_2.txt",
            "exp_txt_struct_2.txt",
        ),
        (
            "patient_0_s.gz",
            ["space6"],
            "res_txt_struct_3.txt",
            "exp_txt_struct_3.txt",
        ),
    ],
)
# These tests verify if the method writes in the correct way
# the csv file, when in input there is a path. In order to do it,
# two dataframes from a expected csv and output csv are compared.
def test_equality_csv_files(
    di_1p_fixt, patient_s, list_struct, name_csv, exp_csv
):
    di = di_1p_fixt(patient_s, "test_struct_to_csv")
    path_file_res = Path(
        os.getcwd() + "/tests/data/test_struct_to_csv/" + name_csv
    )
    di.struct_to_csv(path_or_buff=path_file_res, names=list_struct)
    result = pd.read_csv(path_file_res)
    path_exp_csv = Path(
        os.getcwd() + "/tests/data/test_struct_to_csv/" + exp_csv
    )
    expected = pd.read_csv(path_exp_csv)
    assert_frame_equal(result, expected)
    os.remove(path_file_res)


@pytest.mark.parametrize(
    "patient_s, list_struct, path_file_res, expected",
    [
        (
            "patient_0_s.gz",
            [],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/res.cSv"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            [],
            os.getcwd() + "/tests/data/test_struct_to_csv/res.csV",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["space6"],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/res."),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["space6"],
            os.getcwd() + "/tests/data/test_struct_to_csv/res.",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["space6"],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/res.pdf"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["space6"],
            os.getcwd() + "/tests/data/test_struct_to_csv/res.pdf",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            [],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/.txt"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            [],
            os.getcwd() + "/tests/data/test_struct_to_csv/.txt",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["space2", "space4"],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/res.tXt"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["space2", "space4"],
            os.getcwd() + "/tests/data/test_struct_to_csv/res.tXt",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            ["name_struct_not_exist"],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/res.txt"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            ["name_struct_not_exist"],
            os.getcwd() + "/tests/data/test_struct_to_csv/res.txt",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            ["name_struct_not_exist"],
            Path(os.getcwd() + "/tests/data/test_struct_to_csv/res"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            ["name_struct_not_exist"],
            os.getcwd() + "/tests/data/test_struct_to_csv/res",
            pytest.raises(ValueError),
        ),
        ("patient_0_s.gz", [], None, does_not_raise()),
    ],
)
# These tests verify if the method raises/doesn't raise errors
# in the correct way.
def test_raises(
    di_1p_fixt,
    patient_s,
    list_struct,
    path_file_res,
    expected,
):
    with expected:
        di = di_1p_fixt(patient_s, "test_struct_to_csv")
        di.struct_to_csv(path_or_buff=path_file_res, names=list_struct)
