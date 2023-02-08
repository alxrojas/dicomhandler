import json
import os
from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import DicomInfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


@pytest.mark.parametrize(
    "patient, expected",
    [
        ("patient_17_p.gz", does_not_raise()),
        ("patient_18_p.gz", pytest.raises(ValueError)),
        ("patient_19_p.gz", pytest.raises(TypeError)),
    ],
)
# These tests verify if the method raises/doesn't raise errors
# in the correct way.
def test_raises_df_areas(patient, expected, di_1p_fixt):
    with expected:
        dicom_info = di_1p_fixt(patient, "test_summarize_to_dataframe")
        dicom_info.summarize_to_dataframe(area=True)


@pytest.mark.parametrize(
    "patient",
    [
        ("patient_17_p.gz"),
    ],
)
# This test verifies if the method generates in the correct way
# the areas dataframe.
def test_equality_df_areas(patient, di_1p_fixt):
    dicom_info1 = di_1p_fixt(patient, "test_summarize_to_dataframe")
    df_exp = pd.read_csv(
        os.getcwd() + "/tests/data/test_summarize_to_dataframe/exp_df_area.csv"
    )
    df_res = dicom_info1.summarize_to_dataframe(area=True)
    assert_frame_equal(df_res, df_exp)


@pytest.mark.parametrize(
    "patient",
    [("patient_17_p.gz")],
)
# This test verifies if the method generates in the correct way
# the plan dataframe.
def test_equality_df_plan(patient, di_1p_fixt):
    dicom_info = di_1p_fixt(patient, "test_summarize_to_dataframe")
    df_exp = pd.read_csv(
        os.getcwd() + "/tests/data/test_summarize_to_dataframe/exp_df_plan.csv"
    )
    df_res = dicom_info.summarize_to_dataframe(area=False)
    df_exp["Reference coordinates [mm]"] = df_exp[
        "Reference coordinates [mm]"
    ].apply(lambda x: json.loads(x))
    assert_frame_equal(df_res, df_exp)


@pytest.mark.parametrize(
    "patient_mock, expected",
    [("patient_mock_4", pytest.raises(ValueError))],
)
# This test verifies if the method generates in the correct way
# a value error if the DICOM Plan is not present.
def test_plan_present(patient_mock, request, expected):
    with expected:
        DicomInfo(
            request.getfixturevalue(patient_mock)
        ).summarize_to_dataframe(area=True)
