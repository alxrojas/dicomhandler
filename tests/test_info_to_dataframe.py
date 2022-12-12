from dicomhandler.dicom_info import Dicominfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest

df_cols = [
    "Target",
    "Prescribed dose [Gy]",
    "Reference point dose [Gy]",
    "Reference coordinates [mm]",
    "Distance to iso [mm]",
    "Structure coordinates [mm]",
    "Max radius [mm]",
    "Min radius [mm]",
    "Mean radius [mm]",
    "Distance to iso (from structure) [mm]",
]
rows_0 = [
    [
        "Met1",
        21.0,
        21.81,
        [0.0, 0.0, 0.0],
        0.0,
        [0.5, 0.0, 0.0],
        0.5,
        0.5,
        0.50,
        0.5,
    ],
    [
        "Met2",
        21.0,
        22.21,
        [1.0, 0.0, 0.0],
        1.0,
        [0.0, 1.0, 0.0],
        1.0,
        0.0,
        0.67,
        1.0,
    ],
    [
        "Met3",
        21.0,
        23.21,
        [0.0, 1.0, 0.0],
        1.0,
        [0.0, 0.0, 1.0],
        0.0,
        0.0,
        0.00,
        1.0,
    ],
    [
        "Met4",
        21.0,
        24.11,
        [0.0, 0.0, 1.0],
        1.0,
        [0.5, 0.0, 0.0],
        0.5,
        0.5,
        0.50,
        0.5,
    ],
    [
        "Met5",
        21.0,
        22.21,
        [1.0, 1.0, 1.0],
        1.7,
        [0.0, 5.5, 0.0],
        4.5,
        4.5,
        4.50,
        5.5,
    ],
]
df_exp_0 = pd.DataFrame(rows_0, columns=df_cols)

rows_1 = [
    [
        "Met1",
        21.0,
        21.81,
        [0.0, 0.0, 0.0],
        0.0,
        [0.5, 0.0, 0.0],
        0.5,
        0.5,
        0.50,
        0.5,
    ],
    [
        "Met2",
        21.0,
        22.21,
        [1.0, 0.0, 0.0],
        1.0,
        [0.0, 1.0, 0.0],
        1.0,
        0.0,
        0.67,
        1.0,
    ],
    ["Met3", 21.0, 23.21, [0.0, 1.0, 0.0], 1.0, None, None, None, None, None],
    [
        "Met4",
        21.0,
        24.11,
        [0.0, 0.0, 1.0],
        1.0,
        [0.5, 0.0, 0.0],
        0.5,
        0.5,
        0.50,
        0.5,
    ],
    [
        "Met5",
        21.0,
        22.21,
        [1.0, 1.0, 1.0],
        1.7,
        [0.0, 5.5, 0.0],
        4.5,
        4.5,
        4.50,
        5.5,
    ],
]
df_exp_1 = pd.DataFrame(rows_1, columns=df_cols)


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    "patient_struct, patient_plan, targets, expected",
    [
        ("patient_20_s.gz", "patient_20_p.gz", [], df_exp_0),
        (
            "patient_22_s.gz",
            "patient_22_p.gz",
            ["Met1+1", "Met2+1", "Met3+1", "Met4+1", "Met5+1"],
            df_exp_0,
        ),
        ("patient_21_s.gz", "patient_21_p.gz", [], df_exp_1),
    ],
)
def test_areas_dataframes(
    dicom_infos_2, patient_struct, patient_plan, targets, expected
):
    dicom_info1 = dicom_infos_2(patient_struct, patient_plan)
    df1 = dicom_info1.info_to_dataframe(targets=targets)
    assert_frame_equal(df1, expected)


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    "patient_struct, patient_plan, targets, expected",
    [
        (
            "patient_20_s.gz",
            "patient_20_p.gz",
            ["a", "b", "c"],
            pytest.raises(ValueError),
        ),
        (
            "patient_20_s.gz",
            "patient_20_p.gz",
            ["Met1", "Met2", "Met3", "Mettt", "Met5"],
            pytest.raises(ValueError),
        ),
    ],
)
def test_value_errors_info_to_dataframe(
    dicom_infos_2, patient_struct, patient_plan, targets, expected
):
    with expected:
        dicom_infos_2(patient_struct, patient_plan).info_to_dataframe(
            targets=targets
        )


@pytest.mark.filterwarnings("ignore")
@pytest.mark.parametrize(
    "patient_mock, expected",
    [
        ("patient_mock_2", pytest.raises(ValueError)),
        ("patient_mock_4", pytest.raises(ValueError)),
    ],
)
def test_plan_and_struct_present(patient_mock, request, expected):
    with expected:
        Dicominfo(request.getfixturevalue(patient_mock)).info_to_dataframe()


@pytest.mark.parametrize(
    "patient_struct, patient_plan, targets",
    [
        ("patient_20_s.gz", "patient_20_p.gz", []),
    ],
)
def test_warnings(dicom_infos_2, patient_struct, patient_plan, targets):
    with pytest.warns(UserWarning):
        dicom_infos_2(patient_struct, patient_plan).info_to_dataframe()
