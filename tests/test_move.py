from contextlib import nullcontext as does_not_raise

from pydicom.multival import MultiValue

import pytest


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
        ("cuadrad", 0, "x", pytest.raises(ValueError)),
        (2, 20.0, "x", pytest.raises(ValueError)),
        ("punto", 20.0, "x", does_not_raise()),
        ("punto", 1001, "x", pytest.raises(ValueError)),
        ("cubo", "1", "x", pytest.raises(TypeError)),
        ("cubo", 200.0, "xx", pytest.raises(ValueError)),
        ("error", 200, "x", pytest.raises(ValueError)),
        ("cubo", 200.1, "x", does_not_raise()),
    ],
)
def test_inputs(dicom_infos, struct, angle, key, expected):
    with expected:
        dicom_info1 = dicom_infos("patient_1_s.gz")
        dicom_info1.move(struct, angle, key)


@pytest.mark.parametrize(
    "struct, angle, key, args, expected",
    [
        ("cubo", 200.0, "yaw", [0.0, 0.0], pytest.raises(ValueError)),
        ("cubo", 200.0, "yaw", [1, 1, 1], pytest.raises(ValueError)),
        ("cubo", 200.0, "yaw", [0.0, 1.0, 0.0], does_not_raise()),
        ("cubo", 200.0, "x", [0.0, 1.0, 0.0], does_not_raise()),
        ("cubo", 200.0, "x", [0.0, 1.0, 0.0, 2], pytest.raises(ValueError)),
        ("cubo", 200.0, "x", [0.0, 0.0], pytest.raises(ValueError)),
    ],
)
def test_move_isocenter(dicom_infos, struct, angle, key, args, expected):
    with expected:
        dicom_info1 = dicom_infos("patient_1_s.gz")
        dicom_info1.move(struct, angle, key, args)


@pytest.mark.parametrize(
    "struct, angle, key",
    [
        ("punto", 359.999, "yaw"),
        ("punto", 359.999, "pitch"),
        ("punto", 359.999, "roll"),
        ("punto", 0.0, "yaw"),
        ("punto", 0.0, "pitch"),
        ("punto", 0.0, "roll"),
        ("punto", 0.0, "x"),
        ("punto", 0.0, "y"),
        ("punto", 0.0, "z"),
    ],
)
def test_move_punto_equal(dicom_infos, patients, struct, angle, key, *args):
    dicom_info1 = dicom_infos("patient_1_s.gz")
    x = (
        dicom_info1.move(struct, angle, key)
        .dicom_struct.ROIContourSequence[1]
        .ContourSequence[0]
        .ContourData
    )
    y = (
        patients("patient_1_s.gz")
        .ROIContourSequence[1]
        .ContourSequence[0]
        .ContourData
    )
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
        ("cubo", 0.0, "x"),
        ("cubo", 0.0, "y"),
        ("cubo", 0.0, "z"),
    ],
)
def test_move_cubo_equal(dicom_infos, patients, struct, angle, key, *args):
    dicom_info = dicom_infos("patient_1_s.gz")
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[0])):
        x = (
            dicom_info.move(struct, angle, key)
            .dicom_struct.ROIContourSequence[0]
            .ContourSequence[i]
            .ContourData
        )
        y = (
            patients("patient_1_s.gz")
            .ROIContourSequence[0]
            .ContourSequence[i]
            .ContourData
        )
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.0001 for xi, yi in zip(x, y)])


@pytest.mark.parametrize(
    "struct, delta1, delta2, delta3, key",
    [
        ("space", 100, 20, -120, "x"),
        ("space", 900, 99, -999, "y"),
        ("space", 19, 21, -40, "z"),
        ("space", 100, -50, -50, "x"),
        ("space", 300, -200, -100, "y"),
        ("space", 200, 0, -200, "z"),
        ("space", 100, 20, -120, "yaw"),
        ("space", 1, 5, -6, "pitch"),
        ("space", 19, 21, -40, "roll"),
        ("space", 100, -50, -50, "yaw"),
        ("space", 300, -200, -100, "pitch"),
        ("space", 200, 0, -200, "roll"),
    ],
)
def test_multi_move_space_equal(
    dicom_infos, patients, struct, delta1, delta2, delta3, key, *args
):
    dicom_info = dicom_infos("patient_1_s.gz")
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[0])):
        x = (
            dicom_info.move(struct, delta1, key)
            .move(struct, delta2, key)
            .move(struct, delta3, key)
            .dicom_struct.ROIContourSequence[1]
            .ContourSequence[i]
            .ContourData
        )
        y = (
            patients("patient_1_s.gz")
            .ROIContourSequence[1]
            .ContourSequence[i]
            .ContourData
        )
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00000001 for xi, yi in zip(x, y)])


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
        ("punto", 1, "x", MultiValue(float, [2.0, 1.0, 1.0])),
        ("punto", 1, "y", MultiValue(float, [1.0, 2.0, 1.0])),
        ("punto", 1, "z", MultiValue(float, [1.0, 1.0, 2.0])),
    ],
)
def test_move_punto(dicom_infos, struct, angle, key, expected):
    dicom_info = dicom_infos("patient_1_s.gz")
    for i in range(len(dicom_info.dicom_struct.ROIContourSequence[2])):
        x = (
            dicom_info.move(struct, angle, key)
            .dicom_struct.ROIContourSequence[2]
            .ContourSequence[i]
            .ContourData
        )
        y = expected
        assert len(x) == len(y)
        assert all([abs(xi - yi) <= 0.00001 for xi, yi in zip(x, y)])
