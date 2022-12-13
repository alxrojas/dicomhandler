import os
from contextlib import nullcontext as does_not_raise

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest

data1 = {
    "Unnamed: 0": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "ControlPoint0": [
        "GantryAngle",
        0.0,
        "GantryDirection",
        "CW",
        "TableDirection",
        0.0,
        "MLC",
        0.0,
        0.0,
        0.0,
    ],
}

data2 = {
    "Unnamed: 0": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    "ControlPoint0": [
        "GantryAngle",
        0.0,
        "GantryDirection",
        "CW",
        "TableDirection",
        0.0,
        "MLC",
        0.0,
        0.0,
        0.0,
    ],
    "ControlPoint1": [
        "GantryAngle",
        10.0,
        "GantryDirection",
        "CW",
        "TableDirection",
        0.0,
        "MLC",
        1.0,
        1.0,
        1.0,
    ],
}


@pytest.mark.parametrize(
    "patient, expected",
    [
        ("patient_3.gz", does_not_raise()),
        ("patient_4.gz", pytest.raises(ValueError)),
        ("patient_5.gz", pytest.raises(ValueError)),
    ],
)
def test_correct_modality(dicom_infos, patient, expected, request):
    with expected:

        di = dicom_infos(patient)
        di.mlc_to_excel("out_test")
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "patient, dataframe",
    [
        ("patient_3.gz", data1),
        ("patient_6.gz", data2),
    ],
)
def test_dataframe(dicom_infos, patient, dataframe, request):
    di = dicom_infos(patient)
    di.mlc_to_excel("out_test")
    df1 = pd.read_excel("out_test.xlsx")
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)
    os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "patient, dataframe, name",
    [
        ("patient_7.gz", data2, "Beam 0"),
        ("patient_7.gz", data2, "Beam 1"),
    ],
)
def test_datasheets(dicom_infos, patient, dataframe, name, request):
    di = dicom_infos(patient)
    di.mlc_to_excel("out_test")
    df1 = pd.read_excel("out_test.xlsx", sheet_name=name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)
    os.remove("out_test.xlsx")
