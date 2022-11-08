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
    "struct, delta, key, expected",
    [
        ("cuadrad", 0, "x", ValueError),
        (2, 20.0, "x", ValueError),
        ("punto", 20.0, "x", True),
        ("punto", 1001, "x", ValueError),
        ("cubo", "1", "x", TypeError),
        ("cubo", 200.0, "xx", ValueError),
        ("error", 200, "x", ValueError),
        ("cubo", 200.1, "x", False),
    ],
)
def test_translate_input_struct(struct, delta, key, expected):
    try:
        dicom_info1 = Dicominfo(patient)
        dicom_info1.translate(struct, delta, key)
        expected = True
    except ValueError:
        assert ValueError == expected
    except TypeError:
        assert TypeError == expected


@pytest.mark.parametrize(
    "struct, delta, key, args, expected",
    [
        ("cubo", 200.0, "x", [0.0, 0.0], ValueError),
        ("cubo", 200.0, "x", [1, 1, 1], ValueError),
        ("cubo", 200.0, "x", [0.0, 1.0, 0.0], True),
    ],
)
def test_translate_input_par_args(struct, delta, key, args, expected):
    try:
        dicom_info1 = Dicominfo(patient)
        dicom_info1.translate(struct, delta, key, args)
        assert expected is True
    except ValueError:
        assert expected == ValueError


@pytest.mark.parametrize(
    "struct, delta, key, patient",
    [
        ("punto", 0.0, "x", patient),
        ("punto", 0.0, "y", patient),
        ("punto", 0.0, "z", patient),
    ],
)
def test_translate_punto_0_360(struct, delta, key, patient, *args):
    dicom_info1 = Dicominfo(patient)
    x = (
        dicom_info1.translate(struct, delta, key)
        .dicom_struct.ROIContourSequence[1]
        .ContourSequence[0]
        .ContourData
    )
    y = patient.ROIContourSequence[1].ContourSequence[0].ContourData
    print(x)
    print(y)
    assert len(x) == len(y)
    assert all([abs(xi - yi) <= 0.001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, delta, key, patient",
    [
        ("cubo", 0.0, "x", patient),
        ("cubo", 0.0, "y", patient),
        ("cubo", 0.0, "z", patient),
    ],
)
def test_translate_cubo_0_360(struct, delta, key, patient, *args):
    dicom_info = Dicominfo(patient)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[0])):
        x = (
            dicom_info.translate(struct, delta, key)
            .dicom_struct.ROIContourSequence[0]
            .ContourSequence[i]
            .ContourData
        )
        y = patient.ROIContourSequence[0].ContourSequence[i].ContourData
        print(x)
        print(y)
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00000001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, delta1, delta2, delta3, key, patient",
    [
        ("space", 100, 20, -120, "x", patient),
        ("space", 999, 1, -1000, "y", patient),
        ("space", 19, 21, -40, "z", patient),
        ("space", 100, -50, -50, "x", patient),
        ("space", 300, -200, -100, "y", patient),
        ("space", 200, 0, -200, "z", patient),
    ],
)
def test_translate_space(struct, delta1, delta2, delta3, key, patient, *args):
    dicom_info = Dicominfo(patient)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[0])):
        x = (
            dicom_info.translate(struct, delta1, key)
            .translate(struct, delta2, key)
            .translate(struct, delta3, key)
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
    "struct, delta, key, patient, expected",
    [
        ("punto", 1, "x", patient, MultiValue(float, [2.0, 1.0, 1.0])),
        ("punto", 1, "y", patient, MultiValue(float, [1.0, 2.0, 1.0])),
        ("punto", 1, "z", patient, MultiValue(float, [1.0, 1.0, 2.0])),
    ],
)
def test_rotate_punto(struct, delta, key, patient, expected):
    dicom_info = Dicominfo(patient)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[2])):
        x = (
            dicom_info.translate(struct, delta, key)
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
    "struct, delta, key, origin, expected",
    [
        ("cubo", 200.0, "z", MultiValue(float, [0.0, 0.0, 0.0]), True),
        (
            "cubo",
            200.0,
            "z",
            MultiValue(float, [0.0, 0.0, 0.0, 1]),
            ValueError,
        ),
        (
            "cubo",
            200.0,
            "z",
            MultiValue(float, [0.0, 1.0, 0.0, 2]),
            ValueError,
        ),
    ],
)
def test_translate_input_origin(struct, delta, key, origin, expected):
    try:
        dicom_info2 = Dicominfo(patient)
        n_struct = len(dicom_info2.dicom_struct.StructureSetROISequence)
        dicom_info2.dicom_struct.ROIContourSequence[
            n_struct - 1
        ].ContourSequence[0].ContourData = origin
        dicom_info2.translate(struct, delta, key)
        assert expected is True
    except ValueError:
        assert expected == ValueError
