import os
from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import Dicominfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


data1 = {
    "x0 [mm]": [1.0],
    "y0 [mm]": [1.0],
    "z0 [mm]": [1.0],
}

data2 = {
    "x0 [mm]": [0.0, 1.0, 1.0, 0.0],
    "y0 [mm]": [0.0, 0.0, 1.0, 1.0],
    "z0 [mm]": [0.0, 0.0, 0.0, 0.0],
    "x1 [mm]": [0.0, 1.0, 1.0, 0.0],
    "y1 [mm]": [0.0, 0.0, 1.0, 1.0],
    "z1 [mm]": [1.0, 1.0, 1.0, 1.0],
}

data3 = {
    "x0 [mm]": [2.0],
    "y0 [mm]": [2.0],
    "z0 [mm]": [2.0],
}


@pytest.mark.parametrize(
    "dicom1, name, expected",
    [
        ("patient_15", "point", does_not_raise()),
        ("patient_14", "cube", does_not_raise()),
        ("patient_15", "POINT", pytest.raises(ValueError)),
        ("patient_14", "CU", pytest.raises(ValueError)),
    ],
)
def test_correct_name_structure(dicom1, name, expected, request):
    with expected:
        di = Dicominfo(request.getfixturevalue(dicom1))
        di.structure_to_excel("out_test", [name])
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, name",
    [
        ("patient_15", data1, "point"),
        ("patient_14", data2, "cube"),
    ],
)
def test_dataframe(dicom1, dataframe, name, request):
    di = Dicominfo(request.getfixturevalue(dicom1))
    di.structure_to_excel("out_test", [name])
    df1 = pd.read_excel("out_test.xlsx", sheet_name=name)
    df2 = pd.DataFrame(dataframe, dtype="int64")
    assert_frame_equal(df1, df2)
    os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, name",
    [
        ("patient_15", data1, "point"),
        ("patient_15", data3, "point2"),
    ],
)
def test_all_structures(dicom1, dataframe, name, request):
    di = Dicominfo(request.getfixturevalue(dicom1))
    di.structure_to_excel("out_test")
    df1 = pd.read_excel("out_test.xlsx", sheet_name=name)
    df2 = pd.DataFrame(dataframe, dtype="int64")
    assert_frame_equal(df1, df2)
    os.remove("out_test.xlsx")
