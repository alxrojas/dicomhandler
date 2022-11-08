import pydicom
import pytest
from pydicom.multival import MultiValue

from dicomhandler.dicom_info import Dicominfo

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


@pytest.mark.parametrize(
    "struct, margin, patient, expected",
    [
        ("space1", "1.0", patient, pytest.raises(TypeError)),
        ("space5", 1.0, patient, pytest.raises(ValueError)),
        ("space", 1.0, patient, pytest.raises(ValueError)),
        ("space1", 1, patient, pytest.raises(TypeError)),
    ],
)
def test_add_margin_cont(struct, margin, patient, expected):
    with expected:
        dicom_info1 = Dicominfo(patient)
        dicom_info1.add_margin(struct, margin)


@pytest.mark.parametrize(
    "struct, margin, patient, index, expected",
    [
        (
            "space1",
            1.0,
            patient,
            0,
            MultiValue(
                float, [-0.707107, 1.707107, 0.0, 1.707107, -0.707107, 0.0]
            ),
        ),
        (
            "space1",
            -1.0,
            patient,
            0,
            MultiValue(
                float, [0.707107, 0.292893, 0.0, 0.292893, 0.707107, 0.0]
            ),
        ),
        (
            "space2",
            1.0,
            patient,
            1,
            MultiValue(float, [0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 4.0, 0.0, 0.0]),
        ),
        (
            "space2",
            0.0,
            patient,
            1,
            patient.ROIContourSequence[1].ContourSequence[0].ContourData,
        ),
        (
            "space3",
            1.0,
            patient,
            2,
            MultiValue(
                float, [0.292893, 1.707107, 0.0, 2.0, -2.0, 0.0, 4.0, 0.0, 0.0]
            ),
        ),
        (
            "space3",
            -1.0,
            patient,
            2,
            MultiValue(
                float, [1.707107, 0.292893, 0.0, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0]
            ),
        ),
        (
            "space4",
            1.0,
            patient,
            3,
            MultiValue(
                float,
                [1.0, 1.0, 0.0, 2.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
            ),
        ),
        (
            "space4",
            -1.0,
            patient,
            3,
            MultiValue(float, [1.0, 0.0, 0.0]),
        ),
        (
            "space6",
            -1.0,
            patient,
            5,
            MultiValue(float, [1.0, 1.0, 0.0, 1.0, 1.0, 0.0]),
        ),
    ],
)
def test_add_margin(struct, margin, patient, index, expected):
    dicom_info1 = Dicominfo(patient)
    x = (
        dicom_info1.add_margin(struct, margin)
        .dicom_struct.ROIContourSequence[index]
        .ContourSequence[0]
        .ContourData
    )
    y = expected
    assert len(x) == len(y)
    print(x)
    print(y)
    assert all([abs(xi - yi) <= 0.00001 for xi, yi in zip(x, y)])
