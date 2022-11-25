import os
from contextlib import nullcontext as does_not_raise

import numpy as np
import pandas as pd
import pydicom
import pytest
from pandas.testing import assert_frame_equal
from pydicom.multival import MultiValue

from dicomhandler.dicom_info import Dicominfo

patient1 = pydicom.dataset.Dataset()
patient1.PatientName = "Mike Wazowski"
patient1.PatientID = "0"
patient1.PatientBirthDate = "20000101"
patient1.OperatorsName = "Mike Wazowski"
patient1.InstanceCreationDate = "20200101"
patient1.Modality = "RTPLAN"
leaf_positions_1 = np.zeros(3)
mlc_1 = pydicom.dataset.Dataset()
mlc_1.LeafJawPositions = MultiValue(float, leaf_positions_1)
control_point_1 = pydicom.dataset.Dataset()
control_point_1.GantryAngle = ["0.0"]
control_point_1.GantryRotationDirection = ["CW"]
control_point_1.PatientSupportAngle = ["0.0"]
control_point_1.BeamLimitingDevicePositionSequence = [mlc_1, mlc_1, mlc_1]
control_point_seq = pydicom.dataset.Dataset()
control_point_seq.ControlPointSequence = [control_point_1]
patient1.BeamSequence = [control_point_seq]

patient2 = pydicom.dataset.Dataset()
patient2.PatientName = "Mike Wazowski"
patient2.PatientID = "0"
patient2.PatientBirthDate = "20000101"
patient2.OperatorsName = "Mike Wazowski"
patient2.InstanceCreationDate = "20200101"
patient2.Modality = "RTSTRUCT"

patient3 = pydicom.dataset.Dataset()
patient3.PatientName = "Mike Wazowski"
patient3.PatientID = "0"
patient3.PatientBirthDate = "20000101"
patient3.OperatorsName = "Mike Wazowski"
patient3.InstanceCreationDate = "20200101"
patient3.Modality = "RTDOSE"

patient4 = pydicom.dataset.Dataset()
patient4.PatientName = "Mike Wazowski"
patient4.PatientID = "0"
patient4.PatientBirthDate = "20000101"
patient4.OperatorsName = "Mike Wazowski"
patient4.InstanceCreationDate = "20200101"
patient4.Modality = "RTPLAN"
leaf_positions_1_4 = np.zeros(3)
mlc_1_4 = pydicom.dataset.Dataset()
mlc_1_4.LeafJawPositions = MultiValue(float, leaf_positions_1_4)
control_point_1_4 = pydicom.dataset.Dataset()
control_point_1_4.GantryAngle = ["0.0"]
control_point_1_4.GantryRotationDirection = ["CW"]
control_point_1_4.PatientSupportAngle = ["0.0"]
control_point_1_4.BeamLimitingDevicePositionSequence = [
    mlc_1_4,
    mlc_1_4,
    mlc_1_4,
]
leaf_positions_2_4 = np.ones(3)
mlc_2_4 = pydicom.dataset.Dataset()
mlc_2_4.LeafJawPositions = MultiValue(float, leaf_positions_2_4)
control_point_2_4 = pydicom.dataset.Dataset()
control_point_2_4.GantryAngle = ["10.0"]
control_point_2_4.GantryRotationDirection = ["CW"]
control_point_2_4.PatientSupportAngle = ["0.0"]
control_point_2_4.BeamLimitingDevicePositionSequence = [mlc_2_4]
control_point_seq_4 = pydicom.dataset.Dataset()
control_point_seq_4.ControlPointSequence = [
    control_point_1_4,
    control_point_2_4,
]
patient4.BeamSequence = [control_point_seq_4]

patient5 = pydicom.dataset.Dataset()
patient5.PatientName = "Mike Wazowski"
patient5.PatientID = "0"
patient5.PatientBirthDate = "20000101"
patient5.OperatorsName = "Mike Wazowski"
patient5.InstanceCreationDate = "20200101"
patient5.Modality = "RTPLAN"
leaf_positions_1_5 = np.zeros(3)
mlc_1_5 = pydicom.dataset.Dataset()
mlc_1_5.LeafJawPositions = MultiValue(float, leaf_positions_1_5)
control_point_1_5 = pydicom.dataset.Dataset()
control_point_1_5.GantryAngle = ["0.0"]
control_point_1_5.GantryRotationDirection = ["CW"]
control_point_1_5.PatientSupportAngle = ["0.0"]
control_point_1_5.BeamLimitingDevicePositionSequence = [
    mlc_1_5,
    mlc_1_5,
    mlc_1_5,
]
leaf_positions_2_5 = np.ones(3)
mlc_2_5 = pydicom.dataset.Dataset()
mlc_2_5.LeafJawPositions = MultiValue(float, leaf_positions_2_5)
control_point_2_5 = pydicom.dataset.Dataset()
control_point_2_5.GantryAngle = ["10.0"]
control_point_2_5.GantryRotationDirection = ["CW"]
control_point_2_5.PatientSupportAngle = ["0.0"]
control_point_2_5.BeamLimitingDevicePositionSequence = [mlc_2_5]
control_point_seq_5 = pydicom.dataset.Dataset()
control_point_seq_5.ControlPointSequence = [
    control_point_1_5,
    control_point_2_5,
]
patient5.BeamSequence = [control_point_seq_5, control_point_seq_5]

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
        (patient1, does_not_raise()),
        (patient2, pytest.raises(ValueError)),
        (patient3, pytest.raises(ValueError)),
    ],
)
def test_correct_modality(dicom1, expected):
    with expected:
        di = Dicominfo(dicom1)
        di.mlc_to_excel("out_test")
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, file, expected",
    [
        (patient1, "out_test", does_not_raise()),
        (patient1, "out_test.xlsx", does_not_raise()),
    ],
)
def test_filename(dicom1, file, expected):
    with expected:
        di = Dicominfo(dicom1)
        di.mlc_to_excel(file)
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, index",
    [
        (patient1, data1, index1),
        (patient4, data2, index1),
    ],
)
def test_dataframe(dicom1, dataframe, index):
    di = Dicominfo(dicom1)
    di.mlc_to_excel("out_test")
    df1 = pd.read_excel("out_test.xlsx", index_col=0, header=None).T
    df2 = pd.DataFrame(dataframe, index=index)
    assert_frame_equal(df1, df2, check_names=False)
    os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, name, index",
    [
        (patient5, data2, "Beam 0", index1),
        (patient5, data2, "Beam 1", index1),
    ],
)
def test_datasheets(dicom1, dataframe, name, index):
    di = Dicominfo(dicom1)
    di.mlc_to_excel("out_test")
    df1 = pd.read_excel(
        "out_test.xlsx", sheet_name=name, index_col=0, header=None
    ).T
    df2 = pd.DataFrame(dataframe, index=index)
    assert_frame_equal(df1, df2, check_names=False)
    os.remove("out_test.xlsx")
