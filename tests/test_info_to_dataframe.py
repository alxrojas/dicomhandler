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

patient_0_p = pydicom.dataset.Dataset()
patient_0_p.PatientName = "Mike Wazowski"
patient_0_p.PatientID = "0"
patient_0_p.PatientBirthDate = "20000101"
patient_0_p.OperatorsName = "Mike Wazowski"
patient_0_p.InstanceCreationDate = "20200101"
patient_0_p.Modality = "RTPLAN"

patient_0_s = pydicom.dataset.Dataset()
patient_0_s.PatientName = "Mike Wazowski"
patient_0_s.PatientID = "0"
patient_0_s.PatientBirthDate = "20000101"
patient_0_s.OperatorsName = "Mike Wazowski"
patient_0_s.InstanceCreationDate = "20200101"
patient_0_s.Modality = "RTSTRUCT"

ip = pydicom.dataset.Dataset()
ip.IsocenterPosition = MultiValue(float,[0, 0, 0])

cps = pydicom.dataset.Dataset()
cps.ControlPointSequence = [ip]

patient_0_p.BeamSequence = [cps]

drs_0 = pydicom.dataset.Dataset()
drs_1 = pydicom.dataset.Dataset()
drs_2 = pydicom.dataset.Dataset()
drs_3 = pydicom.dataset.Dataset()
drs_4 = pydicom.dataset.Dataset()
drs_5 = pydicom.dataset.Dataset()
drs_6 = pydicom.dataset.Dataset()
drs_7 = pydicom.dataset.Dataset()
drs_8 = pydicom.dataset.Dataset()
drs_9 = pydicom.dataset.Dataset()

drs_0.DoseReferenceDescription = 'Met1'
drs_0.TargetPrescriptionDose = 21.0
drs_2.DoseReferenceDescription = 'Met2'
drs_2.TargetPrescriptionDose = 21.0
drs_4.DoseReferenceDescription = 'Met3'
drs_4.TargetPrescriptionDose = 21.0
drs_6.DoseReferenceDescription = 'Met4'
drs_6.TargetPrescriptionDose = 21.0
drs_8.DoseReferenceDescription = 'Met5'
drs_8.TargetPrescriptionDose = 21.0

drs_1.DoseReferencePointCoordinates = MultiValue(float, [0,0,0])
drs_1.TargetPrescriptionDose = 21.8111
drs_3.DoseReferencePointCoordinates = MultiValue(float, [1,0,0])
drs_3.TargetPrescriptionDose = 22.2111
drs_5.DoseReferencePointCoordinates = MultiValue(float, [0,1,0])
drs_5.TargetPrescriptionDose = 23.2111
drs_7.DoseReferencePointCoordinates = MultiValue(float, [0,0,1])
drs_7.TargetPrescriptionDose = 24.1111
drs_9.DoseReferencePointCoordinates = MultiValue(float, [1,1,1])
drs_9.TargetPrescriptionDose = 22.2111

patient_0_p.DoseReferenceSequence = [drs_0, drs_1, drs_2, drs_3, drs_4, drs_5, drs_6, drs_7, drs_8, drs_9] 

ds_seq_struct_1 = pydicom.dataset.Dataset()
ds_seq_struct_2 = pydicom.dataset.Dataset()
ds_seq_struct_3 = pydicom.dataset.Dataset()
ds_seq_struct_4 = pydicom.dataset.Dataset()
ds_seq_struct_5 = pydicom.dataset.Dataset()
ds_seq_struct_6 = pydicom.dataset.Dataset()
ds_seq_struct_1.ROIName = 'Met1'
ds_seq_struct_2.ROIName = 'Met2'
ds_seq_struct_3.ROIName = 'Met3'
ds_seq_struct_4.ROIName = 'Met4'
ds_seq_struct_5.ROIName = 'Met5'
ds_seq_struct_6.ROIName = "Coord 1"
patient_0_s.StructureSetROISequence = [
    ds_seq_struct_1,
    ds_seq_struct_2,
    ds_seq_struct_3,
    ds_seq_struct_4,
    ds_seq_struct_5,
    ds_seq_struct_6
]

ds_seq_cont_1 = pydicom.dataset.Dataset()


pyd_corte_1_met1 = pydicom.dataset.Dataset()
pyd_corte_1_met2 = pydicom.dataset.Dataset()
pyd_corte_1_met3 = pydicom.dataset.Dataset()
pyd_corte_1_met4 = pydicom.dataset.Dataset()
pyd_corte_1_met5 = pydicom.dataset.Dataset()
ds_vect_iso = pydicom.dataset.Dataset()

corte_1_met1 = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
corte_1_met2 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0,0.0,2.0,0.0]
corte_1_met3 = [0.0, 0.0, 1.0, 0.0, 0.0, 1.0]
corte_1_met4 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
corte_1_met5 = [0.0, 1.0, 0.0, 0.0, 10.0, 0.0]
iso = [0.0, 0.0, 0.0]
pyd_corte_1_met1.ContourData = MultiValue(float, corte_1_met1)
pyd_corte_1_met2.ContourData = MultiValue(float, corte_1_met2)
pyd_corte_1_met3.ContourData = MultiValue(float, corte_1_met3)
pyd_corte_1_met4.ContourData = MultiValue(float, corte_1_met4)
pyd_corte_1_met5.ContourData = MultiValue(float, corte_1_met5)
ds_vect_iso.ContourData = MultiValue(float, iso)

ds_cont_struct_1 = pydicom.dataset.Dataset()
ds_cont_struct_2 = pydicom.dataset.Dataset()
ds_cont_struct_3 = pydicom.dataset.Dataset()
ds_cont_struct_4 = pydicom.dataset.Dataset()
ds_cont_struct_5 = pydicom.dataset.Dataset()
ds_cont_struct_orig = pydicom.dataset.Dataset()
ds_cont_struct_1.ContourSequence = [
    pyd_corte_1_met1
]
ds_cont_struct_2.ContourSequence = [
    pyd_corte_1_met2
]
ds_cont_struct_3.ContourSequence = [pyd_corte_1_met3]
ds_cont_struct_4.ContourSequence = [pyd_corte_1_met4]
ds_cont_struct_5.ContourSequence = [pyd_corte_1_met5]
ds_cont_struct_orig.ContourSequence = [ds_vect_iso]
patient_0_s.ROIContourSequence = [
    ds_cont_struct_1,
    ds_cont_struct_2,
    ds_cont_struct_3,
    ds_cont_struct_4,
    ds_cont_struct_5,
    ds_cont_struct_orig,
]

patient_1_p = pydicom.dataset.Dataset()        # This patient has 5 metastasis en el plan, 4 metastasis en el struct
patient_1_p.PatientName = "Mike Wazowski"      
patient_1_p.PatientID = "0"
patient_1_p.PatientBirthDate = "20000101"
patient_1_p.OperatorsName = "Mike Wazowski"
patient_1_p.InstanceCreationDate = "20200101"
patient_1_p.Modality = "RTPLAN"

patient_1_s = pydicom.dataset.Dataset()
patient_1_s.PatientName = "Mike Wazowski"
patient_1_s.PatientID = "0"
patient_1_s.PatientBirthDate = "20000101"
patient_1_s.OperatorsName = "Mike Wazowski"
patient_1_s.InstanceCreationDate = "20200101"
patient_1_s.Modality = "RTSTRUCT"

ip = pydicom.dataset.Dataset()
ip.IsocenterPosition = MultiValue(float,[0, 0, 0])

cps = pydicom.dataset.Dataset()
cps.ControlPointSequence = [ip]

patient_1_p.BeamSequence = [cps]

drs_0 = pydicom.dataset.Dataset()
drs_1 = pydicom.dataset.Dataset()
drs_2 = pydicom.dataset.Dataset()
drs_3 = pydicom.dataset.Dataset()
drs_4 = pydicom.dataset.Dataset()
drs_5 = pydicom.dataset.Dataset()
drs_6 = pydicom.dataset.Dataset()
drs_7 = pydicom.dataset.Dataset()
drs_8 = pydicom.dataset.Dataset()
drs_9 = pydicom.dataset.Dataset()

drs_0.DoseReferenceDescription = 'Met1'
drs_0.TargetPrescriptionDose = 21.0
drs_2.DoseReferenceDescription = 'Met2'
drs_2.TargetPrescriptionDose = 21.0
drs_4.DoseReferenceDescription = 'Met3'
drs_4.TargetPrescriptionDose = 21.0
drs_6.DoseReferenceDescription = 'Met4'
drs_6.TargetPrescriptionDose = 21.0
drs_8.DoseReferenceDescription = 'Met5'
drs_8.TargetPrescriptionDose = 21.0

drs_1.DoseReferencePointCoordinates = MultiValue(float, [0,0,0])
drs_1.TargetPrescriptionDose = 21.8111
drs_3.DoseReferencePointCoordinates = MultiValue(float, [1,0,0])
drs_3.TargetPrescriptionDose = 22.2111
drs_5.DoseReferencePointCoordinates = MultiValue(float, [0,1,0])
drs_5.TargetPrescriptionDose = 23.2111
drs_7.DoseReferencePointCoordinates = MultiValue(float, [0,0,1])
drs_7.TargetPrescriptionDose = 24.1111
drs_9.DoseReferencePointCoordinates = MultiValue(float, [1,1,1])
drs_9.TargetPrescriptionDose = 22.2111

patient_1_p.DoseReferenceSequence = [drs_0, drs_1, drs_2, drs_3, drs_4, drs_5, drs_6, drs_7, drs_8, drs_9] 

ds_seq_struct_1 = pydicom.dataset.Dataset() 
ds_seq_struct_2 = pydicom.dataset.Dataset()
ds_seq_struct_3 = pydicom.dataset.Dataset()
ds_seq_struct_4 = pydicom.dataset.Dataset()
ds_seq_struct_5 = pydicom.dataset.Dataset()
ds_seq_struct_6 = pydicom.dataset.Dataset()
ds_seq_struct_1.ROIName = 'Met1'
ds_seq_struct_2.ROIName = 'Met2'

ds_seq_struct_4.ROIName = 'Met4'
ds_seq_struct_5.ROIName = 'Met5'
ds_seq_struct_6.ROIName = "Coord 1"
patient_1_s.StructureSetROISequence = [
    ds_seq_struct_1,
    ds_seq_struct_2,
   
    ds_seq_struct_4,
    ds_seq_struct_5,
    ds_seq_struct_6
]

ds_seq_cont_1 = pydicom.dataset.Dataset()


pyd_corte_1_met1 = pydicom.dataset.Dataset()
pyd_corte_1_met2 = pydicom.dataset.Dataset()

pyd_corte_1_met4 = pydicom.dataset.Dataset()
pyd_corte_1_met5 = pydicom.dataset.Dataset()
ds_vect_iso = pydicom.dataset.Dataset()

corte_1_met1 = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
corte_1_met2 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0,0.0,2.0,0.0]

corte_1_met4 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
corte_1_met5 = [0.0, 1.0, 0.0, 0.0, 10.0, 0.0]
iso = [0.0, 0.0, 0.0]
pyd_corte_1_met1.ContourData = MultiValue(float, corte_1_met1)
pyd_corte_1_met2.ContourData = MultiValue(float, corte_1_met2)

pyd_corte_1_met4.ContourData = MultiValue(float, corte_1_met4)
pyd_corte_1_met5.ContourData = MultiValue(float, corte_1_met5)
ds_vect_iso.ContourData = MultiValue(float, iso)

ds_cont_struct_1 = pydicom.dataset.Dataset()
ds_cont_struct_2 = pydicom.dataset.Dataset()

ds_cont_struct_4 = pydicom.dataset.Dataset()
ds_cont_struct_5 = pydicom.dataset.Dataset()
ds_cont_struct_orig = pydicom.dataset.Dataset()
ds_cont_struct_1.ContourSequence = [
    pyd_corte_1_met1
]
ds_cont_struct_2.ContourSequence = [
    pyd_corte_1_met2
]

ds_cont_struct_4.ContourSequence = [pyd_corte_1_met4]
ds_cont_struct_5.ContourSequence = [pyd_corte_1_met5]
ds_cont_struct_orig.ContourSequence = [ds_vect_iso]
patient_1_s.ROIContourSequence = [
    ds_cont_struct_1,
    ds_cont_struct_2,
 
    ds_cont_struct_4,
    ds_cont_struct_5,
    ds_cont_struct_orig,
]

patient_2_p = pydicom.dataset.Dataset()
patient_2_p.PatientName = "Mike Wazowski"
patient_2_p.PatientID = "0"
patient_2_p.PatientBirthDate = "20000101"
patient_2_p.OperatorsName = "Mike Wazowski"
patient_2_p.InstanceCreationDate = "20200101"
patient_2_p.Modality = "RTPLAN"

patient_2_s = pydicom.dataset.Dataset()
patient_2_s.PatientName = "Mike Wazowski"
patient_2_s.PatientID = "0"
patient_2_s.PatientBirthDate = "20000101"
patient_2_s.OperatorsName = "Mike Wazowski"
patient_2_s.InstanceCreationDate = "20200101"
patient_2_s.Modality = "RTSTRUCT"

ip = pydicom.dataset.Dataset()
ip.IsocenterPosition = MultiValue(float,[0, 0, 0])

cps = pydicom.dataset.Dataset()
cps.ControlPointSequence = [ip]

patient_2_p.BeamSequence = [cps]

drs_0 = pydicom.dataset.Dataset()
drs_1 = pydicom.dataset.Dataset()
drs_2 = pydicom.dataset.Dataset()
drs_3 = pydicom.dataset.Dataset()
drs_4 = pydicom.dataset.Dataset()
drs_5 = pydicom.dataset.Dataset()
drs_6 = pydicom.dataset.Dataset()
drs_7 = pydicom.dataset.Dataset()
drs_8 = pydicom.dataset.Dataset()
drs_9 = pydicom.dataset.Dataset()

drs_0.DoseReferenceDescription = 'Met1'
drs_0.TargetPrescriptionDose = 21.0
drs_2.DoseReferenceDescription = 'Met2'
drs_2.TargetPrescriptionDose = 21.0
drs_4.DoseReferenceDescription = 'Met3'
drs_4.TargetPrescriptionDose = 21.0
drs_6.DoseReferenceDescription = 'Met4'
drs_6.TargetPrescriptionDose = 21.0
drs_8.DoseReferenceDescription = 'Met5'
drs_8.TargetPrescriptionDose = 21.0

drs_1.DoseReferencePointCoordinates = MultiValue(float, [0,0,0])
drs_1.TargetPrescriptionDose = 21.8111
drs_3.DoseReferencePointCoordinates = MultiValue(float, [1,0,0])
drs_3.TargetPrescriptionDose = 22.2111
drs_5.DoseReferencePointCoordinates = MultiValue(float, [0,1,0])
drs_5.TargetPrescriptionDose = 23.2111
drs_7.DoseReferencePointCoordinates = MultiValue(float, [0,0,1])
drs_7.TargetPrescriptionDose = 24.1111
drs_9.DoseReferencePointCoordinates = MultiValue(float, [1,1,1])
drs_9.TargetPrescriptionDose = 22.2111

patient_2_p.DoseReferenceSequence = [drs_0, drs_1, drs_2, drs_3, drs_4, drs_5, drs_6, drs_7, drs_8, drs_9] 

ds_seq_struct_1 = pydicom.dataset.Dataset()
ds_seq_struct_2 = pydicom.dataset.Dataset()
ds_seq_struct_3 = pydicom.dataset.Dataset()
ds_seq_struct_4 = pydicom.dataset.Dataset()
ds_seq_struct_5 = pydicom.dataset.Dataset()
ds_seq_struct_6 = pydicom.dataset.Dataset()
ds_seq_struct_1.ROIName = 'Met1+1'
ds_seq_struct_2.ROIName = 'Met2+1'
ds_seq_struct_3.ROIName = 'Met3+1'
ds_seq_struct_4.ROIName = 'Met4+1'
ds_seq_struct_5.ROIName = 'Met5+1'
ds_seq_struct_6.ROIName = "Coord 1"
patient_2_s.StructureSetROISequence = [
    ds_seq_struct_1,
    ds_seq_struct_2,
    ds_seq_struct_3,
    ds_seq_struct_4,
    ds_seq_struct_5,
    ds_seq_struct_6
]

ds_seq_cont_1 = pydicom.dataset.Dataset()


pyd_corte_1_met1 = pydicom.dataset.Dataset()
pyd_corte_1_met2 = pydicom.dataset.Dataset()
pyd_corte_1_met3 = pydicom.dataset.Dataset()
pyd_corte_1_met4 = pydicom.dataset.Dataset()
pyd_corte_1_met5 = pydicom.dataset.Dataset()
ds_vect_iso = pydicom.dataset.Dataset()

corte_1_met1 = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
corte_1_met2 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0,0.0,2.0,0.0]
corte_1_met3 = [0.0, 0.0, 1.0, 0.0, 0.0, 1.0]
corte_1_met4 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
corte_1_met5 = [0.0, 1.0, 0.0, 0.0, 10.0, 0.0]
iso = [0.0, 0.0, 0.0]
pyd_corte_1_met1.ContourData = MultiValue(float, corte_1_met1)
pyd_corte_1_met2.ContourData = MultiValue(float, corte_1_met2)
pyd_corte_1_met3.ContourData = MultiValue(float, corte_1_met3)
pyd_corte_1_met4.ContourData = MultiValue(float, corte_1_met4)
pyd_corte_1_met5.ContourData = MultiValue(float, corte_1_met5)
ds_vect_iso.ContourData = MultiValue(float, iso)

ds_cont_struct_1 = pydicom.dataset.Dataset()
ds_cont_struct_2 = pydicom.dataset.Dataset()
ds_cont_struct_3 = pydicom.dataset.Dataset()
ds_cont_struct_4 = pydicom.dataset.Dataset()
ds_cont_struct_5 = pydicom.dataset.Dataset()
ds_cont_struct_orig = pydicom.dataset.Dataset()
ds_cont_struct_1.ContourSequence = [
    pyd_corte_1_met1
]
ds_cont_struct_2.ContourSequence = [
    pyd_corte_1_met2
]
ds_cont_struct_3.ContourSequence = [pyd_corte_1_met3]
ds_cont_struct_4.ContourSequence = [pyd_corte_1_met4]
ds_cont_struct_5.ContourSequence = [pyd_corte_1_met5]
ds_cont_struct_orig.ContourSequence = [ds_vect_iso]
patient_2_s.ROIContourSequence = [
    ds_cont_struct_1,
    ds_cont_struct_2,
    ds_cont_struct_3,
    ds_cont_struct_4,
    ds_cont_struct_5,
    ds_cont_struct_orig,
]







df_cols = ['Target', 'Prescribed dose [Gy]', 'Reference point dose [Gy]', 'Reference coordinates [mm]',
           'Distance to iso [mm]', 'Structure coordinates [mm]', 'Max radius [mm]', 'Min radius [mm]',
           'Mean radius [mm]', 'Distance to iso (from structure) [mm]']
rows_0 = [['Met1', 21.0, 21.81, [0.0, 0.0, 0.0], 0.0, [0.5, 0.0, 0.0], 0.5, 0.5, 0.50, 0.5],
 	['Met2', 21.0, 22.21, [1.0, 0.0, 0.0], 1.0, [0.0, 1.0, 0.0], 1.0, 0.0, 0.67, 1.0],
 	['Met3', 21.0, 23.21, [0.0, 1.0, 0.0], 1.0, [0.0, 0.0, 1.0], 0.0, 0.0, 0.00, 1.0],
 	['Met4', 21.0, 24.11, [0.0, 0.0, 1.0], 1.0, [0.5, 0.0, 0.0], 0.5, 0.5, 0.50, 0.5],
 	['Met5', 21.0, 22.21, [1.0, 1.0, 1.0], 1.7, [0.0, 5.5, 0.0], 4.5, 4.5, 4.50, 5.5] ]
df_exp_0 = pd.DataFrame(rows_0, columns=df_cols)

rows_1 = [['Met1', 21.0, 21.81, [0.0, 0.0, 0.0], 0.0, [0.5, 0.0, 0.0], 0.5, 0.5, 0.50, 0.5],
 	['Met2', 21.0, 22.21, [1.0, 0.0, 0.0], 1.0, [0.0, 1.0, 0.0], 1.0, 0.0, 0.67, 1.0],
 	['Met3', 21.0, 23.21, [0.0, 1.0, 0.0], 1.0, None, None, None, None, None],
 	['Met4', 21.0, 24.11, [0.0, 0.0, 1.0], 1.0, [0.5, 0.0, 0.0], 0.5, 0.5, 0.50, 0.5],
 	['Met5', 21.0, 22.21, [1.0, 1.0, 1.0], 1.7, [0.0, 5.5, 0.0], 4.5, 4.5, 4.50, 5.5] ]
df_exp_1 = pd.DataFrame(rows_1, columns=df_cols)




@pytest.mark.filterwarnings("ignore:info_to_dataframe")
@pytest.mark.parametrize(
    "patient_struct, patient_plan, targets, expected",
    [
        (patient_0_s, patient_0_p, [], df_exp_0),
        (patient_2_s, patient_2_p, ['Met1+1','Met2+1','Met3+1','Met4+1','Met5+1'], df_exp_0),
        (patient_1_s, patient_1_p, [], df_exp_1),
        
    ],
)
def test_areas_dataframes(patient_struct, patient_plan, targets, expected):
        dicom_info1 = Dicominfo(patient_struct, patient_plan)
        df1 = dicom_info1.info_to_dataframe(targets=targets)
        assert_frame_equal(df1, expected)

@pytest.mark.parametrize(
    "patient_struct, patient_plan, targets, expected",
    [
        (patient_0_s, patient_0_p, ["a","b","c"], pytest.raises(ValueError)),
        (patient_0_s, patient_0_p, ["Met1", "Met2", "Met3", "Mettt", "Met5"], pytest.raises(ValueError))
    ],
)
def test_value_errors_info_to_dataframe(patient_struct, patient_plan, targets, expected):
    with expected:
        Dicominfo(patient_struct, patient_plan).info_to_dataframe(targets=targets)
        
@pytest.mark.parametrize(
    "patient_mock, expected",
    [
        ("patient_mock_2", pytest.raises(ValueError)),  
        ("patient_mock_4", pytest.raises(ValueError))
    ],
)
def test_plan_and_struct_present(patient_mock, request, expected):
    with expected:
        Dicominfo(request.getfixturevalue(patient_mock)).info_to_dataframe()


