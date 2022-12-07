from pydicom.multival import MultiValue

import pytest


@pytest.mark.parametrize(
    "struct, margin, expected",
    [
        ("space1", "1.0", pytest.raises(TypeError)),
        ("space5", 1.0, pytest.raises(ValueError)),
        ("space", 1.0, pytest.raises(ValueError)),
        ("space1", 1, pytest.raises(TypeError)),
    ],
)
def test_add_margin_cont(dicom_infos, struct, margin, expected):
    with expected:
        dicom_info1 = dicom_infos("patient_2.gz")
        dicom_info1.add_margin(struct, margin)


@pytest.mark.parametrize(
    "struct, margin, index, expected",
    [
        (
            "space1",
            1.0,
            0,
            MultiValue(
                float, [-0.707107, 1.707107, 0.0, 1.707107, -0.707107, 0.0]
            ),
        ),
        (
            "space1",
            -1.0,
            0,
            MultiValue(
                float, [0.707107, 0.292893, 0.0, 0.292893, 0.707107, 0.0]
            ),
        ),
        (
            "space2",
            1.0,
            1,
            MultiValue(float, [0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 4.0, 0.0, 0.0]),
        ),
        (
            "space2",
            0.0,
            1,
            MultiValue(float, [1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 3.0, 0.0, 0.0]),
        ),
        (
            "space3",
            1.0,
            2,
            MultiValue(
                float, [0.292893, 1.707107, 0.0, 2.0, -2.0, 0.0, 4.0, 0.0, 0.0]
            ),
        ),
        (
            "space3",
            -1.0,
            2,
            MultiValue(
                float, [1.707107, 0.292893, 0.0, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0]
            ),
        ),
        (
            "space4",
            1.0,
            3,
            MultiValue(
                float,
                [1.0, 1.0, 0.0, 2.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0],
            ),
        ),
        (
            "space4",
            -1.0,
            3,
            MultiValue(float, [1.0, 0.0, 0.0]),
        ),
        (
            "space6",
            -1.0,
            5,
            MultiValue(float, [1.0, 1.0, 0.0, 1.0, 1.0, 0.0]),
        ),
    ],
)
def test_add_margin(dicom_infos, struct, margin, index, expected):
    dicom_info1 = dicom_infos("patient_2.gz")
    x = (
        dicom_info1.add_margin(struct, margin)
        .dicom_struct.ROIContourSequence[index]
        .ContourSequence[0]
        .ContourData
    )
    y = expected
    assert len(x) == len(y)
    assert all([abs(xi - yi) <= 0.00001 for xi, yi in zip(x, y)])
