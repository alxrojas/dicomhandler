from contextlib import nullcontext as does_not_raise

from pydicom.multival import MultiValue

import pytest

import os
import pathlib
from unittest.mock import Mock

from dicomhandler.dicom_info import Dicominfo
import pandas as pd
from pandas.testing import assert_frame_equal
import joblib

import pytest

import pydicom

patient_1 = pydicom.dataset.Dataset()
patient_1.PatientName = "Mike Wazowski"
patient_1.PatientID = "0"
patient_1.PatientBirthDate = "20000101"
patient_1.OperatorsName = "Mike Wazowski"
patient_1.InstanceCreationDate = "20200101"
patient_1.Modality = "RTPLAN"

mlc0_0_0 = pydicom.dataset.Dataset()
mlc0_0_1 = pydicom.dataset.Dataset()
mlc0_0_2 = pydicom.dataset.Dataset()
lpb0 = pydicom.dataset.Dataset()
lpb1 = pydicom.dataset.Dataset()
lpb2 = pydicom.dataset.Dataset()
mlc0_0_2.LeafJawPositions = MultiValue(float, [-9,-8,-7,0,0,0])
lpb2.LeafPositionBoundaries = MultiValue(float, [-100,-95,-90,-85])
control_point0_0 = pydicom.dataset.Dataset()
position_laminas_length = pydicom.dataset.Dataset()
control_point0_0.GantryAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_0.PatientSupportAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_0.GantryRotationDirection = "CW"
control_point0_0.BeamLimitingDevicePositionSequence = [
    mlc0_0_0,
    mlc0_0_1,
    mlc0_0_2,
]
mlc1_0_0 = pydicom.dataset.Dataset()
mlc1_0_1 = pydicom.dataset.Dataset()
mlc1_0_2 = pydicom.dataset.Dataset()
lpb0 = pydicom.dataset.Dataset()
lpb1 = pydicom.dataset.Dataset()
lpb2 = pydicom.dataset.Dataset()
mlc1_0_2.LeafJawPositions = MultiValue(float, [-3,-2,-1,1,2,3])
lpb2.LeafPositionBoundaries = MultiValue(float, [-100,-97.5,-95,-92.5])
control_point1_0 = pydicom.dataset.Dataset()
position_laminas_length = pydicom.dataset.Dataset()
control_point1_0.GantryAngle = pydicom.valuerep.DSfloat(0.0)
control_point1_0.PatientSupportAngle = pydicom.valuerep.DSfloat(5.0)
control_point1_0.GantryRotationDirection = "CC"
control_point1_0.BeamLimitingDevicePositionSequence = [
    mlc1_0_0,
    mlc1_0_1,
    mlc1_0_2,
]

mlc0_1_0 = pydicom.dataset.Dataset()
mlc0_1_0.LeafJawPositions = MultiValue(float, [-3,-2,-1,-3,-2,-1])
control_point0_1 = pydicom.dataset.Dataset()
control_point0_1.GantryAngle = pydicom.valuerep.DSfloat(10.0)
control_point0_1.GantryRotationDirection = "CW"
control_point0_1.PatientSupportAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_1.BeamLimitingDevicePositionSequence = [mlc0_1_0]
control_point0_seq_4 = pydicom.dataset.Dataset()
control_point0_seq_4.ControlPointSequence = [
    control_point0_0,
    control_point0_1,
]
control_point0_seq_4.BeamLimitingDeviceSequence = [
    lpb0,
    lpb1,
    lpb2
]
mlc1_1_0 = pydicom.dataset.Dataset()
mlc1_1_0.LeafJawPositions = MultiValue(float, [-3,-2,-1,3,2,1])
control_point1_1 = pydicom.dataset.Dataset()
control_point1_1.GantryAngle = pydicom.valuerep.DSfloat(10.0)
control_point1_1.GantryRotationDirection = "CC"
control_point1_1.PatientSupportAngle = pydicom.valuerep.DSfloat(5.0)
control_point1_1.BeamLimitingDevicePositionSequence = [mlc1_1_0]
control_point1_seq_4 = pydicom.dataset.Dataset()
control_point1_seq_4.ControlPointSequence = [
    control_point1_0,
    control_point1_1,
]
control_point1_seq_4.BeamLimitingDeviceSequence = [
    lpb0,
    lpb1,
    lpb2
]
patient_1.BeamSequence = [control_point0_seq_4, control_point1_seq_4]

patient_2 = pydicom.dataset.Dataset()
patient_2.PatientName = "Mike Wazowski"
patient_2.PatientID = "0"
patient_2.PatientBirthDate = "20000101"
patient_2.OperatorsName = "Mike Wazowski"
patient_2.InstanceCreationDate = "20200101"
patient_2.Modality = "RTPLAN"

mlc0_0_0 = pydicom.dataset.Dataset()
mlc0_0_1 = pydicom.dataset.Dataset()
mlc0_0_2 = pydicom.dataset.Dataset()
lpb0_0 = pydicom.dataset.Dataset()
lpb1_0 = pydicom.dataset.Dataset()
lpb2_0 = pydicom.dataset.Dataset()
mlc0_0_2.LeafJawPositions = MultiValue(float, [-9,-8,-7,0,0,0])
lpb2_0.LeafPositionBoundaries = MultiValue(float, [-100,-95,-90]) #Here, there 2 leaves. The other beam has 3 leaves
control_point0_0 = pydicom.dataset.Dataset()
position_laminas_length = pydicom.dataset.Dataset()
control_point0_0.GantryAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_0.PatientSupportAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_0.GantryRotationDirection = "CW"
control_point0_0.BeamLimitingDevicePositionSequence = [
    mlc0_0_0,
    mlc0_0_1,
    mlc0_0_2,
]
mlc1_0_0 = pydicom.dataset.Dataset()
mlc1_0_1 = pydicom.dataset.Dataset()
mlc1_0_2 = pydicom.dataset.Dataset()
lpb0_1 = pydicom.dataset.Dataset()
lpb1_1 = pydicom.dataset.Dataset()
lpb2_1 = pydicom.dataset.Dataset()
mlc1_0_2.LeafJawPositions = MultiValue(float, [-3,-2,-1,1,2,3])
lpb2_1.LeafPositionBoundaries = MultiValue(float, [-100,-97.5,-95,-92.5])
control_point1_0 = pydicom.dataset.Dataset()
position_laminas_length = pydicom.dataset.Dataset()
control_point1_0.GantryAngle = pydicom.valuerep.DSfloat(0.0)
control_point1_0.PatientSupportAngle = pydicom.valuerep.DSfloat(5.0)
control_point1_0.GantryRotationDirection = "CC"
control_point1_0.BeamLimitingDevicePositionSequence = [
    mlc1_0_0,
    mlc1_0_1,
    mlc1_0_2,
]

mlc0_1_0 = pydicom.dataset.Dataset()
mlc0_1_0.LeafJawPositions = MultiValue(float, [-3,-2,-1,-3,-2,-1])
control_point0_1 = pydicom.dataset.Dataset()
control_point0_1.GantryAngle = pydicom.valuerep.DSfloat(10.0)
control_point0_1.GantryRotationDirection = "CW"
control_point0_1.PatientSupportAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_1.BeamLimitingDevicePositionSequence = [mlc0_1_0]
control_point0_seq_4 = pydicom.dataset.Dataset()
control_point0_seq_4.ControlPointSequence = [
    control_point0_0,
    control_point0_1,
]
control_point0_seq_4.BeamLimitingDeviceSequence = [
    lpb0_0,
    lpb1_0,
    lpb2_0
]
mlc1_1_0 = pydicom.dataset.Dataset()
mlc1_1_0.LeafJawPositions = MultiValue(float, [-3,-2,-1,3,2,1])
control_point1_1 = pydicom.dataset.Dataset()
control_point1_1.GantryAngle = pydicom.valuerep.DSfloat(10.0)
control_point1_1.GantryRotationDirection = "CC"
control_point1_1.PatientSupportAngle = pydicom.valuerep.DSfloat(5.0)
control_point1_1.BeamLimitingDevicePositionSequence = [mlc1_1_0]
control_point1_seq_4 = pydicom.dataset.Dataset()
control_point1_seq_4.ControlPointSequence = [
    control_point1_0,
    control_point1_1,
]
control_point1_seq_4.BeamLimitingDeviceSequence = [
    lpb0_1,
    lpb1_1,
    lpb2_1
]
patient_2.BeamSequence = [control_point0_seq_4, control_point1_seq_4]




patient_3 = pydicom.dataset.Dataset()
patient_3.PatientName = "Mike Wazowski"
patient_3.PatientID = "0"
patient_3.PatientBirthDate = "20000101"
patient_3.OperatorsName = "Mike Wazowski"
patient_3.InstanceCreationDate = "20200101"
patient_3.Modality = "RTPLAN"
mlc0_0_0 = pydicom.dataset.Dataset()
mlc0_0_1 = pydicom.dataset.Dataset()
mlc0_0_2 = pydicom.dataset.Dataset()
lpb0 = pydicom.dataset.Dataset()
lpb1 = pydicom.dataset.Dataset()
lpb2 = pydicom.dataset.Dataset()
mlc0_0_2.LeafJawPositions = MultiValue(float, [-9,-8,-7,0,0,0])
lpb2.LeafPositionBoundaries = MultiValue(float, [-100,-95,-90,-85])
control_point0_0 = pydicom.dataset.Dataset()
position_laminas_length = pydicom.dataset.Dataset()
control_point0_0.GantryAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_0.PatientSupportAngle = pydicom.valuerep.DSfloat(0.0)
control_point0_0.GantryRotationDirection = 1 # Gantry Rotation Direction is not a integer! Must be a str
control_point0_0.BeamLimitingDevicePositionSequence = [
    mlc0_0_0,
    mlc0_0_1,
    mlc0_0_2,
]
control_point0_seq_4 = pydicom.dataset.Dataset()
control_point0_seq_4.ControlPointSequence = [
    control_point0_0,

]
control_point0_seq_4.BeamLimitingDeviceSequence = [
    lpb0,
    lpb1,
    lpb2
]
patient_3.BeamSequence = [control_point0_seq_4]



df_cols = ['beam', 'checkpoint', 'area', 'gantry_angle','gantry_direction', 'table']

@pytest.mark.parametrize(
    "patient, expected",
    [
        (patient_1, does_not_raise()),
        (patient_2, pytest.raises(ValueError)),
        (patient_3, pytest.raises(TypeError)),
        
        #(, pytest.raises(ValueError)),
    ],
)
def test_rotate_input_struct(patient, expected):
    with expected:
        dicom_info1 = Dicominfo(patient)
        dicom_info1.areas_to_df()

@pytest.mark.parametrize(
    "patient, expected",
    [
        (patient_1, pd.DataFrame([[1, 1, 60.0, 0.0, 'CW', 0.0], [1, 2, 0.0, 10.0, 'CW', 0.0], [2, 1, 30.0, 0.0, 'CC', 5.0], [2, 2, 30.0, 10.0, 'CC', 5.0]], columns=df_cols))
    ],
)
def test_areas_dataframes(patient, expected):
        dicom_info1 = Dicominfo(patient)
        df1 = dicom_info1.areas_to_df()
        assert_frame_equal(df1, expected)
        
      
