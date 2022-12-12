from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import Dicominfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


df_cols = [
    "beam",
    "checkpoint",
    "area",
    "gantry_angle",
    "gantry_direction",
    "table",
]
df_exp0 = pd.DataFrame(
    [
        [1, 1, 60.0, 0.0, "CW", 0.0],
        [1, 2, 0.0, 10.0, "CW", 0.0],
        [2, 1, 30.0, 0.0, "CC", 5.0],
        [2, 2, 30.0, 10.0, "CC", 5.0],
    ],
    columns=df_cols,
)


@pytest.mark.parametrize(
    "patient, expected",
    [
        ("patient_17_p.gz", does_not_raise()),
        ("patient_18_p.gz", pytest.raises(ValueError)),
        ("patient_19_p.gz", pytest.raises(TypeError)),
    ],
)
def test_error_areas(patient, expected, dicom_infos):
    with expected:
        dicom_info1 = dicom_infos(patient)
        dicom_info1.areas_to_dataframe()


@pytest.mark.parametrize(
    "patient, expected",
    [("patient_17_p.gz", df_exp0)],
)
def test_areas_dataframes(patient, expected, dicom_infos):
    dicom_info1 = dicom_infos(patient)
    df1 = dicom_info1.areas_to_dataframe()
    assert_frame_equal(df1, expected)


@pytest.mark.parametrize(
    "patient_mock, expected",
    [("patient_mock_4", pytest.raises(ValueError))],
)
def test_plan_present(patient_mock, request, expected):
    with expected:
        Dicominfo(request.getfixturevalue(patient_mock)).areas_to_dataframe()
