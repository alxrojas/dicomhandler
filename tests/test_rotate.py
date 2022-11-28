from contextlib import nullcontext as does_not_raise

import pydicom
import pytest
from pydicom.multival import MultiValue

from dicomhandler.dicom_info import Dicominfo




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
def test_rotate_input_struct(struct, angle, key, expected, patient_1):
    with expected:
        dicom_info1 = Dicominfo(patient_1)
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
def test_rotate_input_par_args(struct, angle, key, args, expected, patient_1):
    with expected:
        dicom_info1 = Dicominfo(patient_1)
        dicom_info1.rotate(struct, angle, key, args)


@pytest.mark.parametrize(
    "struct, angle, key",
    [
        ("punto", 359.999, "yaw"),
        ("punto", 359.999, "pitch"),
        ("punto", 359.999, "roll"),
        ("punto", 0.0, "yaw"),
        ("punto", 0.0, "pitch"),
        ("punto", 0.0, "roll"),
    ],
)
def test_rotate_punto_0_360(struct, angle, key, patient_1, *args):
    dicom_info1 = Dicominfo(patient_1)
    x = (
        dicom_info1.rotate(struct, angle, key)
        .dicom_struct.ROIContourSequence[1]
        .ContourSequence[0]
        .ContourData
    )
    y = patient_1.ROIContourSequence[1].ContourSequence[0].ContourData
    print(x)
    print(y)
    assert len(x) == len(y)
    assert all([abs(xi - yi) <= 0.00000001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, angle, key",
    [
        ("cubo", 359.999, "yaw"),
        ("cubo", 359.999, "pitch"),
        ("cubo", 359.999, "roll"),
        ("cubo", 0.0, "yaw"),
        ("cubo", 0.0, "pitch"),
        ("cubo", 0.0, "roll"),
    ],
)
def test_rotate_cubo_0_360(struct, angle, key, patient_1, *args):
    dicom_info = Dicominfo(patient_1)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[0])):
        x = (
            dicom_info.rotate(struct, angle, key)
            .dicom_struct.ROIContourSequence[0]
            .ContourSequence[i]
            .ContourData
        )
        y = patient_1.ROIContourSequence[0].ContourSequence[i].ContourData
        print(x)
        print(y)
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.0001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, angle1, angle2, angle3, key",
    [
        ("space", 100, 20, -120, "yaw"),
        ("space", 1, 5, -6, "pitch"),
        ("space", 19, 21, -40, "roll"),
        ("space", 100, -50, -50, "yaw"),
        ("space", 300, -200, -100, "pitch"),
        ("space", 200, 0, -200, "roll"),
    ],
)
def test_rotate_space(struct, angle1, angle2, angle3, key, patient_1, *args):
    dicom_info = Dicominfo(patient_1)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[1])):
        x = (
            dicom_info.rotate(struct, angle1, key)
            .rotate(struct, angle2, key)
            .rotate(struct, angle3, key)
            .dicom_struct.ROIContourSequence[1]
            .ContourSequence[i]
            .ContourData
        )
        y = patient_1.ROIContourSequence[1].ContourSequence[i].ContourData
        print(x)
        print(y)
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00000001 for xi, yi in zip(x, y)])


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
def test_rotate_input_origin(struct, angle, key, patient_1, origin, expected):
    with expected:
        dicom_info2 = Dicominfo(patient_1)
        dicom_info2.rotate(struct, angle, key, origin)


@pytest.mark.parametrize(
    "struct, angle, key, expected",
    [
        (
            "punto",
            90,
            "roll",

            MultiValue(float, [1.0, -1.00000267, 0.99999533]),
        ),
        (
            "punto",
            90,
            "yaw",
     
            MultiValue(float, [-1.00000267, 0.99999533, 1]),
        ),
        (
            "punto",
            90,
            "pitch",
   
            MultiValue(float, [0.99999533, 1.0, -1.00000267]),
        ),
    ],
)
def test_rotate_punto(struct, angle, key, patient_1, expected):
    dicom_info = Dicominfo(patient_1)
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[2])):
        x = (
            dicom_info.rotate(struct, angle, key)
            .dicom_struct.ROIContourSequence[2]
            .ContourSequence[i]
            .ContourData
        )
        y = expected
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00001 for xi, yi in zip(x, y)])
