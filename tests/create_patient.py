import os
import pathlib

import joblib

import pydicom
from pydicom.multival import MultiValue

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DATA_PATH = PATH / "data"

filename = os.path.join(DATA_PATH, "patient_22_s.gz")


def create_patient_pydicom():
    patient_2_s = pydicom.dataset.Dataset()
    patient_2_s.PatientName = "Mike Wazowski"
    patient_2_s.PatientID = "0"
    patient_2_s.PatientBirthDate = "20000101"
    patient_2_s.OperatorsName = "Mike Wazowski"
    patient_2_s.InstanceCreationDate = "20200101"
    patient_2_s.Modality = "RTSTRUCT"
    ds_seq_struct_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2 = pydicom.dataset.Dataset()
    ds_seq_struct_3 = pydicom.dataset.Dataset()
    ds_seq_struct_4 = pydicom.dataset.Dataset()
    ds_seq_struct_5 = pydicom.dataset.Dataset()
    ds_seq_struct_6 = pydicom.dataset.Dataset()
    ds_seq_struct_1.ROIName = "Met1+1"
    ds_seq_struct_2.ROIName = "Met2+1"
    ds_seq_struct_3.ROIName = "Met3+1"
    ds_seq_struct_4.ROIName = "Met4+1"
    ds_seq_struct_5.ROIName = "Met5+1"
    ds_seq_struct_6.ROIName = "Coord 1"
    patient_2_s.StructureSetROISequence = [
        ds_seq_struct_1,
        ds_seq_struct_2,
        ds_seq_struct_3,
        ds_seq_struct_4,
        ds_seq_struct_5,
        ds_seq_struct_6,
    ]

    pyd_corte_1_met1 = pydicom.dataset.Dataset()
    pyd_corte_1_met2 = pydicom.dataset.Dataset()
    pyd_corte_1_met3 = pydicom.dataset.Dataset()
    pyd_corte_1_met4 = pydicom.dataset.Dataset()
    pyd_corte_1_met5 = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()

    corte_1_met1 = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
    corte_1_met2 = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 2.0, 0.0]
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
    ds_cont_struct_1.ContourSequence = [pyd_corte_1_met1]
    ds_cont_struct_2.ContourSequence = [pyd_corte_1_met2]
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

    joblib.dump(patient_2_s, filename)


create_patient_pydicom()
