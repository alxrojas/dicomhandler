import os
from contextlib import nullcontext as does_not_raise
from io import StringIO
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


@pytest.mark.parametrize(
    "patient_p, name_buff",
    [
        ("patient_0_p.gz", "mlc_buff_1.gz"),
    ],
)
# This test verifies if the method writes in the correct way
# the buffer. In order to do it, two dataframes from a
# expected buffer and output buffer are compared.
def test_equality_buffers(di_1p_fixt, patient_p, name_buff, load_buff):
    di = di_1p_fixt(patient_p, "test_mlc_to_csv")
    buff_out = StringIO()
    di.mlc_to_csv(path_or_buff=buff_out)
    buff_out.seek(0)
    result = pd.read_csv(buff_out)
    path = Path(os.getcwd() + "/tests/data/test_mlc_to_csv/" + name_buff)
    buff_exp = load_buff(path)
    buff_exp.seek(0)
    expected = pd.read_csv(buff_exp)
    assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "patient_p, name_csv, exp_csv",
    [
        ("patient_0_p.gz", "res_csv_mlc_1.csv", "exp_csv_mlc_1.csv"),
        ("patient_0_p.gz", "res_txt_mlc_1.txt", "exp_txt_mlc_1.txt"),
    ],
)
# These tests verify if the method writes in the correct way
# the csv file, when in input there is a path. In order to do it,
# two dataframes from a expected csv and output csv are compared.
def test_equality_csv_files(di_1p_fixt, patient_p, name_csv, exp_csv):
    di = di_1p_fixt(patient_p, "test_mlc_to_csv")
    path_file_out = Path(
        os.getcwd() + "/tests/data/test_mlc_to_csv/" + name_csv
    )
    di.mlc_to_csv(path_or_buff=path_file_out)
    result = pd.read_csv(path_file_out)
    path_exp_csv = Path(os.getcwd() + "/tests/data/test_mlc_to_csv/" + exp_csv)
    expected = pd.read_csv(path_exp_csv)
    assert_frame_equal(result, expected)
    os.remove(path_file_out)


@pytest.mark.parametrize(
    "patient_p, path_file_out, expected",
    [
        (
            "patient_0_p.gz",
            Path(os.getcwd() + "/tests/data/test_mlc_to_csv/res.cSv"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            os.getcwd() + "/tests/data/test_mlc_to_csv/res.csV",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            Path(os.getcwd() + "/tests/data/test_mlc_to_csv/res."),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            os.getcwd() + "/tests/data/test_mlc_to_csv/res.",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            Path(os.getcwd() + "/tests/data/test_mlc_to_csv/res.pdf"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            os.getcwd() + "/tests/data/test_mlc_to_csv/res.pdf",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            Path(os.getcwd() + "/tests/data/test_mlc_to_csv/.txt"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            os.getcwd() + "/tests/data/test_mlc_to_csv/.txt",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            Path(os.getcwd() + "/tests/data/test_mlc_to_csv/res.tXt"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_p.gz",
            os.getcwd() + "/tests/data/test_mlc_to_csv/res.txT",
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            Path(os.getcwd() + "/tests/data/test_mlc_to_csv/res"),
            pytest.raises(ValueError),
        ),
        (
            "patient_0_s.gz",
            os.getcwd() + "/tests/data/test_mlc_to_csv/res",
            pytest.raises(ValueError),
        ),
        ("patient_0_p.gz", None, does_not_raise()),
    ],
)
# These tests verify if the method raises/doesn't raise errors
# in the correct way.
def test_raises(
    di_1p_fixt,
    patient_p,
    path_file_out,
    expected,
):
    with expected:
        di = di_1p_fixt(patient_p, "test_mlc_to_csv")
        di.mlc_to_csv(path_or_buff=path_file_out)
