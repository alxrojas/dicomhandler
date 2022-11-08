from contextlib import nullcontext as does_not_raise

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


@pytest.mark.parametrize(
    "struct, angle, key, expected",
    [
        ("cuadrad", 359.999, "yaw", pytest.raises(ValueError)),
        (2, 200.0, "yaw", pytest.raises(ValueError)),
        ("punto", 200.0, "yaw", does_not_raise()),
        ("punto", 361.1, "yaw", pytest.raises(ValueError)),
        ("cubo", "1", "yaw", pytest.raises(TypeError)),
        ("cubo", 200.1, "yy", pytest.raises(ValueError)),
        ("error", 200, "yaw", pytest.raises(ValueError)),
        ("cubo", 200.1, "yaw", does_not_raise()),
    ],
)
def test_rotate_input_struct(struct, angle, key, expected):
    with expected:
        dicom_info1 = Dicominfo(patient)
        dicom_info1.rotate(struct, angle, key)


@pytest.mark.parametrize(
    "struct, angle, key, args, expected",
    [
        ("cubo", 200.0, "yaw", [0.0, 0.0], pytest.raises(ValueError)),
        ("cubo", 200.0, "yaw", [1, 1, 1], pytest.raises(ValueError)),
        ("cubo", 200.0, "yaw", [0.0, 1.0, 0.0], does_not_raise()),
        ("cubo", 200.0, "yaw", [0.0, 1.0, 0.0, 2], pytest.raises(ValueError)),
    ],
)
def test_rotate_input_par_args(struct, angle, key, args, expected):
    with expected:
        dicom_info1 = Dicominfo(patient)
        dicom_info1.rotate(struct, angle, key, args)


@pytest.mark.parametrize(
    "struct, angle, key, patient",
    [
        ("punto", 359.999, "yaw", patient),
        ("punto", 359.999, "pitch", patient),
        ("punto", 359.999, "roll", patient),
        ("punto", 0.0, "yaw", patient),
        ("punto", 0.0, "pitch", patient),
        ("punto", 0.0, "roll", patient),
    ],
)
def test_rotate_punto_0_360(struct, angle, key, patient, *args):
    dicom_info1 = Dicominfo(patient)
    x = (
        dicom_info1.rotate(struct, angle, key)
        .dicom_struct.ROIContourSequence[1]
        .ContourSequence[0]
        .ContourData
    )
    y = patient.ROIContourSequence[1].ContourSequence[0].ContourData
    print(x)
    print(y)
    assert len(x) == len(y)
    assert all([abs(xi - yi) <= 0.00000001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, angle, key, patient",
    [
        ("cubo", 359.999, "yaw", patient),
        ("cubo", 359.999, "pitch", patient),
        ("cubo", 359.999, "roll", patient),
        ("cubo", 0.0, "yaw", patient),
        ("cubo", 0.0, "pitch", patient),
        ("cubo", 0.0, "roll", patient),
    ],
)
def test_rotate_cubo_0_360(struct, angle, key, patient, *args):
    dicom_info = Dicominfo(patient)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[0])):
        x = (
            dicom_info.rotate(struct, angle, key)
            .dicom_struct.ROIContourSequence[0]
            .ContourSequence[i]
            .ContourData
        )
        y = patient.ROIContourSequence[0].ContourSequence[i].ContourData
        print(x)
        print(y)
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.0001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, angle1, angle2, angle3, key, patient",
    [
        ("space", 100, 20, -120, "yaw", patient),
        ("space", 1, 5, -6, "pitch", patient),
        ("space", 19, 21, -40, "roll", patient),
        ("space", 100, -50, -50, "yaw", patient),
        ("space", 300, -200, -100, "pitch", patient),
        ("space", 200, 0, -200, "roll", patient),
    ],
)
def test_rotate_space(struct, angle1, angle2, angle3, key, patient, *args):
    dicom_info = Dicominfo(patient)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[1])):
        x = (
            dicom_info.rotate(struct, angle1, key)
            .rotate(struct, angle2, key)
            .rotate(struct, angle3, key)
            .dicom_struct.ROIContourSequence[1]
            .ContourSequence[i]
            .ContourData
        )
        y = patient.ROIContourSequence[1].ContourSequence[i].ContourData
        print(x)
        print(y)
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00000001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, angle, key, patient, expected",
    [
        (
            "punto",
            90,
            "roll",
            patient,
            MultiValue(float, [1.0, -1.00000267, 0.99999533]),
        ),
        (
            "punto",
            90,
            "yaw",
            patient,  # fmt: skip
            MultiValue(float, [-1.00000267, 0.99999533, 1]),
        ),
        (
            "punto",
            90,
            "pitch",
            patient,
            MultiValue(float, [0.99999533, 1.0, -1.00000267]),
        ),
    ],
)
def test_rotate_punto(struct, angle, key, patient, expected):
    dicom_info = Dicominfo(patient)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[2])):
        x = (
            dicom_info.rotate(struct, angle, key)
            .dicom_struct.ROIContourSequence[2]
            .ContourSequence[i]
            .ContourData
        )
        y = expected
        print(x)
        print(y)
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, angle, key, origin, expected",
    [
        (
            "cubo",
            200.0,
            "yaw",
            MultiValue(float, [0.0, 0.0, 0.0]),
            does_not_raise(),
        ),
        (
            "cubo",
            200.0,
            "yaw",
            MultiValue(float, [0.0, 0.0, 0.0, 1]),
            pytest.raises(ValueError),
        ),
        (
            "cubo",
            200.0,
            "yaw",
            MultiValue(float, [0.0, 1.0, 0.0, 2]),
            pytest.raises(ValueError),
        ),
    ],
)
def test_rotate_input_origin(struct, angle, key, origin, expected):
    with expected:
        dicom_info2 = Dicominfo(patient)
        n_struct = len(dicom_info2.dicom_struct.StructureSetROISequence)
        dicom_info2.dicom_struct.ROIContourSequence[
            n_struct - 1
        ].ContourSequence[0].ContourData = origin
        dicom_info2.rotate(struct, angle, key)
