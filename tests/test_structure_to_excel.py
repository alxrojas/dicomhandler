import os
from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import Dicominfo

import pandas as pd
from pandas.testing import assert_frame_equal

import pydicom
from pydicom.multival import MultiValue

import pytest

patient1 = pydicom.dataset.Dataset()
patient1.PatientName = "Mike Wazowski"
patient1.PatientID = "0"
patient1.PatientBirthDate = "20000101"
patient1.OperatorsName = "Mike Wazowski"
patient1.InstanceCreationDate = "20200101"
patient1.Modality = "RTSTRUCT"
ds_seq_struct_1_1 = pydicom.dataset.Dataset()
ds_seq_struct_1_1.ROIName = "cube"
patient1.StructureSetROISequence = [ds_seq_struct_1_1]
pyd_corte_1_punto = pydicom.dataset.Dataset()
pyd_corte_2_punto = pydicom.dataset.Dataset()
corte_1_1_point = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0]
corte_1_2_point = [0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0]
pyd_corte_1_punto.ContourData = MultiValue(float, corte_1_1_point)
pyd_corte_2_punto.ContourData = MultiValue(float, corte_1_2_point)
ds_cont_struct_1_1 = pydicom.dataset.Dataset()
ds_cont_struct_1_1.ContourSequence = [pyd_corte_1_punto, pyd_corte_2_punto]
patient1.ROIContourSequence = [
    ds_cont_struct_1_1,
]

patient2 = pydicom.dataset.Dataset()
patient2.PatientName = "Mike Wazowski"
patient2.PatientID = "0"
patient2.PatientBirthDate = "20000101"
patient2.OperatorsName = "Mike Wazowski"
patient2.InstanceCreationDate = "20200101"
patient2.Modality = "RTSTRUCT"
ds_seq_struct_2_1 = pydicom.dataset.Dataset()
ds_seq_struct_2_1.ROIName = "point"
ds_seq_struct_2_2 = pydicom.dataset.Dataset()
ds_seq_struct_2_2.ROIName = "point2"
patient2.StructureSetROISequence = [ds_seq_struct_2_1, ds_seq_struct_2_2]
pyd_corte_2_punto = pydicom.dataset.Dataset()
corte_2_1_point = [1.0, 1.0, 1.0]
pyd_corte_22_punto = pydicom.dataset.Dataset()
corte_2_2_point = [2.0, 2.0, 2.0]
pyd_corte_2_punto.ContourData = MultiValue(float, corte_2_1_point)
pyd_corte_22_punto.ContourData = MultiValue(float, corte_2_2_point)
ds_cont_struct_2_1 = pydicom.dataset.Dataset()
ds_cont_struct_2_1.ContourSequence = [pyd_corte_2_punto]
ds_cont_struct_2_2 = pydicom.dataset.Dataset()
ds_cont_struct_2_2.ContourSequence = [pyd_corte_22_punto]
patient2.ROIContourSequence = [ds_cont_struct_2_1, ds_cont_struct_2_2]

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
patient4.Modality = "RTSTRUCT"
ds_seq_struct_4_1 = pydicom.dataset.Dataset()
ds_seq_struct_4_1.ROIName = "point"
patient4.StructureSetROISequence = [ds_seq_struct_2_1]
pyd_corte_4_punto = pydicom.dataset.Dataset()
corte_4_1_point = [1.0, 1.0, 1.0]
pyd_corte_4_punto.ContourData = MultiValue(float, corte_4_1_point)
ds_cont_struct_4_1 = pydicom.dataset.Dataset()
ds_cont_struct_4_1.ContourSequence = [pyd_corte_4_punto]
patient4.ROIContourSequence = [ds_cont_struct_4_1]

data1 = {
    "x0 [mm]": [1.0],
    "y0 [mm]": [1.0],
    "z0 [mm]": [1.0],
}

data2 = {
    "x0 [mm]": [0.0, 1.0, 1.0, 0.0],
    "y0 [mm]": [0.0, 0.0, 1.0, 1.0],
    "z0 [mm]": [0.0, 0.0, 0.0, 0.0],
    "x1 [mm]": [0.0, 1.0, 1.0, 0.0],
    "y1 [mm]": [0.0, 0.0, 1.0, 1.0],
    "z1 [mm]": [1.0, 1.0, 1.0, 1.0],
}

data3 = {
    "x0 [mm]": [2.0],
    "y0 [mm]": [2.0],
    "z0 [mm]": [2.0],
}


@pytest.mark.parametrize(
    "dicom1, name, expected",
    [
        (patient2, "point", does_not_raise()),
        (patient1, "cube", does_not_raise()),
        (patient2, "POINT", pytest.raises(ValueError)),
        (patient1, "CU", pytest.raises(ValueError)),
    ],
)
def test_correct_name_structure(dicom1, name, expected):
    with expected:
        di = Dicominfo(dicom1)
        di.structure_to_excel("out_test", [name])
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, file, name, expected",
    [
        (patient2, "out_test", "point", does_not_raise()),
        (patient1, "out_test.xlsx", "cube", does_not_raise()),
    ],
)
def test_filename(dicom1, file, name, expected):
    with expected:
        di = Dicominfo(dicom1)
        di.structure_to_excel(file, [name])
        os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, name",
    [
        (patient2, data1, "point"),
        (patient1, data2, "cube"),
    ],
)
def test_dataframe(dicom1, dataframe, name):
    di = Dicominfo(dicom1)
    di.structure_to_excel("out_test", [name])
    df1 = pd.read_excel("out_test.xlsx", sheet_name=name)
    df2 = pd.DataFrame(dataframe, dtype="int64")
    assert_frame_equal(df1, df2)
    os.remove("out_test.xlsx")


@pytest.mark.parametrize(
    "dicom1, dataframe, name",
    [
        (patient2, data1, "point"),
        (patient2, data3, "point2"),
    ],
)
def test_all_structures(dicom1, dataframe, name):
    di = Dicominfo(dicom1)
    di.structure_to_excel("out_test")
    df1 = pd.read_excel("out_test.xlsx", sheet_name=name)
    df2 = pd.DataFrame(dataframe, dtype="int64")
    assert_frame_equal(df1, df2)
    os.remove("out_test.xlsx")
