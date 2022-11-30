import os
from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import Dicominfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


data1 = {
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
    ]
}

data2 = {
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

index1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.mark.parametrize(
    "dicom1, expected",
    [
        ("patient_3", does_not_raise()),
        ("patient_4", pytest.raises(ValueError)),
        ("patient_5", pytest.raises(ValueError)),
    ],
)
def test_correct_modality(dicom1, expected, request):
    with expected:

        di = Dicominfo(request.getfixturevalue(dicom1))
        di.mlc_to_excel("out_test")
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, index",
    [
        ("patient_3", data1, index1),
        ("patient_6", data2, index1),
    ],
)
def test_dataframe(dicom1, dataframe, index, request):
    di = Dicominfo(request.getfixturevalue(dicom1))
    di.mlc_to_excel("out_test")
    df1 = pd.read_excel("out_test.xlsx", index_col=0, header=None).T
    df2 = pd.DataFrame(dataframe, index=index)
    assert_frame_equal(df1, df2, check_names=False)
    os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, name, index",
    [
        ("patient_7", data2, "Beam 0", index1),
        ("patient_7", data2, "Beam 1", index1),
    ],
)
def test_datasheets(dicom1, dataframe, name, index, request):
    di = Dicominfo(request.getfixturevalue(dicom1))
    di.mlc_to_excel("out_test")
    df1 = pd.read_excel(
        "out_test.xlsx", sheet_name=name, index_col=0, header=None
    ).T
    df2 = pd.DataFrame(dataframe, index=index)
    assert_frame_equal(df1, df2, check_names=False)
    os.remove("out_test.xlsx")
