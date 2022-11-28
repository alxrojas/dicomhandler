import pydicom
from pydicom.multival import MultiValue
import pytest


@pytest.fixture()
def patient_1():
    patient = pydicom.dataset.Dataset()
    patient.PatientName = "mario rossi"
    patient.PatientID = "3"
    patient.PatientBirthDate = "20000101"
    patient.OperatorsName = "guido rossi"
    patient.InstanceCreationDate = "20200101"
    patient.Modality = "RTSTRUCT"


    # pydicom.StructureROISequence[0].ROIName
    ds_seq_struct_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2 = pydicom.dataset.Dataset()
    ds_seq_struct_3 = pydicom.dataset.Dataset()
    ds_seq_struct_4 = pydicom.dataset.Dataset()
    ds_seq_struct_5 = pydicom.dataset.Dataset()
    ds_seq_struct_1.ROIName = "cubo"
    ds_seq_struct_2.ROIName = "space"
    ds_seq_struct_3.ROIName = "punto"
    ds_seq_struct_4.ROIName = "error"
    ds_seq_struct_5.ROIName = "Coord 1"
    patient.StructureSetROISequence = [
        ds_seq_struct_1,
        ds_seq_struct_2,
        ds_seq_struct_3,
        ds_seq_struct_4,
        ds_seq_struct_5,
    ]


    # patient.ROIContourSequence[0].ContourSequence[0].ContourData
    ds_seq_cont_1 = pydicom.dataset.Dataset()

    origin = pydicom.dataset.Dataset()
    pyd_corte_1_cubo = pydicom.dataset.Dataset()
    pyd_corte_2_cubo = pydicom.dataset.Dataset()
    pyd_corte_3_cubo = pydicom.dataset.Dataset()
    pyd_corte_4_cubo = pydicom.dataset.Dataset()
    pyd_corte_1_space = pydicom.dataset.Dataset()
    pyd_corte_2_space = pydicom.dataset.Dataset()
    pyd_corte_3_space = pydicom.dataset.Dataset()
    pyd_corte_1_punto = pydicom.dataset.Dataset()
    pyd_corte_1_error = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()

    corte_1_cubo = [0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 2.0, 0.0]
    corte_2_cubo = [0.0, 0.0, 0.3, 2.0, 0.0, 0.3, 2.0, 2.0, 0.3, 0.0, 2.0, 0.3]
    corte_3_cubo = [0.0, 0.0, 0.6, 2.0, 0.0, 0.6, 2.0, 2.0, 0.6, 0.0, 2.0, 0.6]
    corte_4_cubo = [0.0, 0.0, 1.2, 2.0, 0.0, 1.2, 2.0, 2.0, 1.2, 0.0, 2.0, 1.2]
    corte_1_space = [1.2, 1.3, 1.5, 1.2, 7, 1.5, 1.2, 10, 1.5]
    corte_2_space = [1.2, 1.3, 1.5, 1.2, 7, 1.5, 1.2, 10, 1.5]
    corte_3_space = [1.2, 2.0, 3, 1.2, 3.0, 3, 1.2, 4.5, 3]
    corte_1_punto = [1.0, 1.0, 1.0]
    corte_1_error = [1, 1, 1, 2, 2, 3, 4.0]
    iso = [0.0, 0.0, 0.0]
    pyd_corte_1_cubo.ContourData = MultiValue(float, corte_1_cubo)
    pyd_corte_2_cubo.ContourData = MultiValue(float, corte_2_cubo)
    pyd_corte_3_cubo.ContourData = MultiValue(float, corte_3_cubo)
    pyd_corte_4_cubo.ContourData = MultiValue(float, corte_4_cubo)
    pyd_corte_1_space.ContourData = MultiValue(float, corte_1_space)
    pyd_corte_2_space.ContourData = MultiValue(float, corte_2_space)
    pyd_corte_3_space.ContourData = MultiValue(float, corte_3_space)
    pyd_corte_1_punto.ContourData = MultiValue(float, corte_1_punto)
    pyd_corte_1_error.ContourData = MultiValue(float, corte_1_error)
    ds_vect_iso.ContourData = MultiValue(float, iso)

    ds_cont_struct_1 = pydicom.dataset.Dataset()
    ds_cont_struct_2 = pydicom.dataset.Dataset()
    ds_cont_struct_3 = pydicom.dataset.Dataset()
    ds_cont_struct_4 = pydicom.dataset.Dataset()
    ds_cont_struct_orig = pydicom.dataset.Dataset()
    ds_cont_struct_1.ContourSequence = [
        pyd_corte_1_cubo,
        pyd_corte_2_cubo,
        pyd_corte_3_cubo,
        pyd_corte_4_cubo,
    ]
    ds_cont_struct_2.ContourSequence = [
        pyd_corte_1_space,
        pyd_corte_2_space,
        pyd_corte_3_space,
    ]
    ds_cont_struct_3.ContourSequence = [pyd_corte_1_punto]
    ds_cont_struct_4.ContourSequence = [pyd_corte_1_error]
    ds_cont_struct_orig.ContourSequence = [ds_vect_iso]
    patient.ROIContourSequence = [
        ds_cont_struct_1,
        ds_cont_struct_2,
        ds_cont_struct_3,
        ds_cont_struct_4,
        ds_cont_struct_orig,
    ]
    return patient
    
@pytest.fixture()
def patient_2():
    patient = pydicom.dataset.Dataset()
    patient.PatientName = "mario rossi"
    patient.PatientID = "3"
    patient.PatientBirthDate = "20000101"
    patient.OperatorsName = "guido rossi"
    patient.InstanceCreationDate = "20200101"
    patient.Modality = "RTSTRUCT"

    ds_seq_struct_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2 = pydicom.dataset.Dataset()
    ds_seq_struct_3 = pydicom.dataset.Dataset()
    ds_seq_struct_4 = pydicom.dataset.Dataset()
    ds_seq_struct_5 = pydicom.dataset.Dataset()
    ds_seq_struct_6 = pydicom.dataset.Dataset()
    ds_seq_struct_1.ROIName = "space1"
    ds_seq_struct_2.ROIName = "space2"
    ds_seq_struct_3.ROIName = "space3"
    ds_seq_struct_4.ROIName = "space4"
    ds_seq_struct_5.ROIName = "space5"
    ds_seq_struct_6.ROIName = "space6"
    patient.StructureSetROISequence = [
        ds_seq_struct_1,
        ds_seq_struct_2,
        ds_seq_struct_3,
        ds_seq_struct_4,
        ds_seq_struct_5,
        ds_seq_struct_6,
    ]

    pyd_corte_1_space1 = pydicom.dataset.Dataset()
    pyd_corte_1_space2 = pydicom.dataset.Dataset()
    pyd_corte_1_space3 = pydicom.dataset.Dataset()
    pyd_corte_1_space4 = pydicom.dataset.Dataset()
    pyd_corte_1_space5 = pydicom.dataset.Dataset()
    pyd_corte_1_space6 = pydicom.dataset.Dataset()
    corte_1_space1 = [0.0, 1.0, 0.0, 1.0, 0.0, 0.0]
    corte_1_space2 = [1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 3.0, 0.0, 0.0]
    corte_1_space3 = [1.0, 1.0, 0.0, 2.0, -1.0, 0.0, 3.0, 0.0, 0.0]
    corte_1_space4 = [1.0, 0.0, 0.0]
    corte_1_space5 = []
    corte_1_space6 = [1.0, 0.0, 0.0, 1.0, 2.0, 0.0]
    pyd_corte_1_space1.ContourData = MultiValue(float, corte_1_space1)
    pyd_corte_1_space2.ContourData = MultiValue(float, corte_1_space2)
    pyd_corte_1_space3.ContourData = MultiValue(float, corte_1_space3)
    pyd_corte_1_space4.ContourData = MultiValue(float, corte_1_space4)
    pyd_corte_1_space5.ContourData = MultiValue(float, corte_1_space5)
    pyd_corte_1_space6.ContourData = MultiValue(float, corte_1_space6)
    ds_cont_struct_1 = pydicom.dataset.Dataset()
    ds_cont_struct_2 = pydicom.dataset.Dataset()
    ds_cont_struct_3 = pydicom.dataset.Dataset()
    ds_cont_struct_4 = pydicom.dataset.Dataset()
    ds_cont_struct_5 = pydicom.dataset.Dataset()
    ds_cont_struct_6 = pydicom.dataset.Dataset()
    ds_cont_struct_1.ContourSequence = [pyd_corte_1_space1]
    ds_cont_struct_2.ContourSequence = [pyd_corte_1_space2]
    ds_cont_struct_3.ContourSequence = [pyd_corte_1_space3]
    ds_cont_struct_4.ContourSequence = [pyd_corte_1_space4]
    ds_cont_struct_5.ContourSequence = [pyd_corte_1_space5]
    ds_cont_struct_6.ContourSequence = [pyd_corte_1_space6]
    patient.ROIContourSequence = [
        ds_cont_struct_1,
        ds_cont_struct_2,
        ds_cont_struct_3,
        ds_cont_struct_4,
        ds_cont_struct_5,
        ds_cont_struct_6,
    ]
    return patient
