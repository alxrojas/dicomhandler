from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import DicomInfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


df_cols_area = [
    "beam",
    "checkpoint",
    "area",
    "gantry_angle",
    "gantry_direction",
    "table",
]
df_area = pd.DataFrame(
    [
        [1, 1, 60.0, 0.0, "CW", 0.0],
        [1, 2, 0.0, 10.0, "CW", 0.0],
        [2, 1, 30.0, 0.0, "CC", 5.0],
        [2, 2, 30.0, 10.0, "CC", 5.0],
    ],
    columns=df_cols_area,
)
df_cols = [
    "Target",
    "Prescribed dose [Gy]",
    "Reference point dose [Gy]",
    "Reference coordinates [mm]",
    "Distance to iso [mm]",
]

df = [
    ["Met1", 21.0, 21.81, [0.0, 0.0, 0.0], 0.0],
    ["Met2", 21.0, 22.21, [1.0, 0.0, 0.0], 1.0],
    ["Met3", 21.0, 23.21, [0.0, 1.0, 0.0], 1.0],
    ["Met4", 21.0, 24.11, [0.0, 0.0, 1.0], 1.0],
    ["Met5", 21.0, 22.21, [1.0, 1.0, 1.0], 1.7],
]
df_p = pd.DataFrame(df, columns=df_cols)


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
        dicom_info1.summarize_to_dataframe(area=True)


@pytest.mark.parametrize(
    "patient, expected",
    [
        ("patient_17_p.gz", df_area),
    ],
)
def test_with_areas_dataframes(patient, expected, dicom_infos):
    dicom_info1 = dicom_infos(patient)
    df1 = dicom_info1.summarize_to_dataframe(area=True)
    assert_frame_equal(df1, expected)


@pytest.mark.parametrize(
    "patient, expected",
    [("patient_17_p.gz", df_p)],
)
def test_without_areas_dataframes(patient, expected, dicom_infos):
    dicom_info1 = dicom_infos(patient)
    df1 = dicom_info1.summarize_to_dataframe(area=False)
    assert_frame_equal(df1, expected)


@pytest.mark.parametrize(
    "patient_mock, expected",
    [("patient_mock_4", pytest.raises(ValueError))],
)
def test_plan_present(patient_mock, request, expected):
    with expected:
        DicomInfo(
            request.getfixturevalue(patient_mock)
        ).summarize_to_dataframe(area=True)
