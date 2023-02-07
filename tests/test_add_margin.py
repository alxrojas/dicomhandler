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
# These tests verify if the method raises/doesn't raise errors
# in the correct way.
def test_raises(di_1p_fixt, struct, margin, expected):
    with expected:
        dicom_info1 = di_1p_fixt("patient_2_s.gz", "test_add_margin")
        dicom_info1.add_margin(struct, margin)


@pytest.mark.parametrize(
    "struct, margin, index, expected",
    [
        (
            "space1",
            1.0,
            0,
            MultiValue(float, [-0.71, 1.71, 0.0, 1.71, -0.71, 0.0]),
        ),
        (
            "space1",
            -1.0,
            0,
            MultiValue(float, [0.71, 0.29, 0.0, 0.29, 0.71, 0.0]),
        ),
        (
            "space2",
            1.0,
            1,
            MultiValue(float, [0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 4.0, 0.0, 0.0]),
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
                float, [0.29, 1.71, 0.0, 2.0, -2.0, 0.0, 4.0, 0.0, 0.0]
            ),
        ),
        (
            "space3",
            -1.0,
            2,
            MultiValue(float, [1.71, 0.29, 0.0, 2.0, 0.0, 0.0, 2.0, 0.0, 0.0]),
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
# These tests compare the structure with itself with
# increased/reduced margin.
def test_add_margin(di_1p_fixt, struct, margin, index, expected):
    dicom_info1 = di_1p_fixt("patient_2_s.gz", "test_add_margin")
    x = (
        dicom_info1.add_margin(struct, margin)
        .dicom_struct.ROIContourSequence[index]
        .ContourSequence[0]
        .ContourData
    )
    assert len(x) == len(expected)
    assert all([abs(xi - yi) <= 0.00001 for xi, yi in zip(x, expected)])
