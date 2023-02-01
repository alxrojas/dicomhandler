from contextlib import nullcontext as does_not_raise

from dicomhandler.report import report

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


data1 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
}

data2 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
}

data3 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
    ],
}

data4 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
    ],
}

data5 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.0,
        2.0,
        2.0,
        0.0,
        0.0,
        2.0,
    ],
}

data6 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        3.162,
        0.0,
        1.803,
        1.040,
        1.082,
        1.581,
    ],
}

data7 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        2.0,
        0.0,
        1.207,
        0.737,
        0.543,
        1.0,
    ],
}

data8 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.828,
        2.828,
        2.828,
        0.0,
        0.0,
        2.828,
    ],
}

data9 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
}

data10 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.828,
        2.828,
        2.828,
        0.0,
        0.0,
        2.828,
    ],
}

data11 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.414,
        1.414,
        1.414,
        0.0,
        0.0,
        1.414,
    ],
}

data12 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        1.0043,
        1.0043,
        1.0043,
        0.0,
        0.0,
        0.0,
    ],
}


@pytest.mark.parametrize(
    "patient1, patient2, name, expected",
    [
        ("patient_8.gz", "patient_9.gz", "point", does_not_raise()),
        ("patient_8.gz", "patient_9.gz", "cube", does_not_raise()),
        ("patient_8.gz", "patient_9.gz", "POINT", pytest.raises(ValueError)),
        ("patient_8.gz", "patient_10.gz", "", pytest.raises(ValueError)),
        ("patient_8.gz", "patient_9.gz", "", pytest.raises(ValueError)),
    ],
)
def test_match_name(dicom_infos, patient1, patient2, name, expected, request):
    with expected:
        original = dicom_infos(patient1)
        rotated = dicom_infos(patient2)
        report(original, rotated, name)


@pytest.mark.parametrize(
    "patient1, patient2, dataframe, name",
    [
        ("patient_8.gz", "patient_8.gz", data1, "point"),
        ("patient_8.gz", "patient_9.gz", data1, "point"),
        ("patient_8.gz", "patient_9.gz", data2, "cube"),
        ("patient_8.gz", "patient_8.gz", data2, "cube"),
    ],
)
def test_dataframe(dicom_infos, patient1, patient2, dataframe, name, request):
    original = dicom_infos(patient1)
    rotated = dicom_infos(patient2)
    df1 = report(original, rotated, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "patient1, dataframe, name, delta, key",
    [
        ("patient_8.gz", data3, "point", 1.0, "x"),
        ("patient_8.gz", data3, "point", 1.0, "y"),
        ("patient_8.gz", data3, "point", 1.0, "z"),
        ("patient_8.gz", data3, "point", -1.0, "x"),
        ("patient_8.gz", data3, "point", -1.0, "y"),
        ("patient_8.gz", data3, "point", -1.0, "z"),
        ("patient_8.gz", data1, "point", 0.0, "x"),
        ("patient_8.gz", data1, "point", 0.0, "y"),
        ("patient_8.gz", data1, "point", 0.0, "z"),
        ("patient_8.gz", data4, "cube", 1.0, "x"),
        ("patient_8.gz", data4, "cube", 1.0, "y"),
        ("patient_8.gz", data4, "cube", 1.0, "z"),
        ("patient_8.gz", data4, "cube", -1.0, "x"),
        ("patient_8.gz", data4, "cube", -1.0, "y"),
        ("patient_8.gz", data4, "cube", -1.0, "z"),
        ("patient_8.gz", data2, "cube", 0.0, "x"),
        ("patient_8.gz", data2, "cube", 0.0, "y"),
        ("patient_8.gz", data2, "cube", 0.0, "z"),
    ],
)
def test_translations(
    dicom_infos, patient1, dataframe, name, delta, key, request
):
    original = dicom_infos(patient1)
    translated = original.move(name, delta, key)
    df1 = report(original, translated, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "patient1, dataframe, name, angle, key",
    [
        ("patient_8.gz", data1, "point", 0.0, "roll"),
        ("patient_8.gz", data1, "point", 0.0, "pitch"),
        ("patient_8.gz", data1, "point", 0.0, "yaw"),
        ("patient_8.gz", data1, "point", 359.99, "roll"),
        ("patient_8.gz", data1, "point", 359.99, "pitch"),
        ("patient_8.gz", data1, "point", 359.99, "yaw"),
        ("patient_8.gz", data5, "point", 90.0, "roll"),
        ("patient_8.gz", data5, "point", 90.0, "pitch"),
        ("patient_8.gz", data5, "point", 90.0, "yaw"),
        ("patient_8.gz", data5, "point", -90.0, "roll"),
        ("patient_8.gz", data5, "point", -90.0, "pitch"),
        ("patient_8.gz", data5, "point", -90.0, "yaw"),
        ("patient_8.gz", data2, "cube", 0.0, "roll"),
        ("patient_8.gz", data2, "cube", 0.0, "pitch"),
        ("patient_8.gz", data2, "cube", 0.0, "yaw"),
        ("patient_8.gz", data2, "cube", 359.99, "roll"),
        ("patient_8.gz", data2, "cube", 359.99, "pitch"),
        ("patient_8.gz", data2, "cube", 359.99, "yaw"),
        ("patient_8.gz", data6, "cube", 90.0, "roll"),
        ("patient_8.gz", data6, "cube", 90.0, "pitch"),
        ("patient_8.gz", data7, "cube", 90.0, "yaw"),
        ("patient_8.gz", data6, "cube", -90.0, "roll"),
        ("patient_8.gz", data6, "cube", -90.0, "pitch"),
        ("patient_8.gz", data7, "cube", -90.0, "yaw"),
    ],
)
def test_rotations(
    dicom_infos, patient1, dataframe, name, angle, key, request
):
    original = dicom_infos(patient1)
    rotated = original.move(name, angle, key)
    df1 = report(original, rotated, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "patient1, dataframe, name, angle, key1, key2",
    [
        ("patient_8.gz", data8, "point", 90.0, "roll", "pitch"),
        ("patient_8.gz", data9, "point", 90.0, "roll", "yaw"),
        ("patient_8.gz", data10, "point", 90.0, "pitch", "yaw"),
    ],
)
def test_cumulated_rotations(
    dicom_infos, patient1, dataframe, name, angle, key1, key2, request
):
    original = dicom_infos(patient1)
    rotated = original.move(name, angle, key1)
    rotated2 = rotated.move(name, angle, key2)
    df1 = report(original, rotated2, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "patient1, dataframe, name, delta, key1, key2",
    [
        ("patient_8.gz", data11, "point", 1.0, "x", "y"),
        ("patient_8.gz", data11, "point", 1.0, "x", "z"),
        ("patient_8.gz", data11, "point", 1.0, "z", "y"),
    ],
)
def test_cumulated_translations(
    dicom_infos, patient1, dataframe, name, delta, key1, key2, request
):
    original = dicom_infos(patient1)
    translated = original.move(name, delta, key1)
    translated2 = translated.move(name, delta, key2)
    df1 = report(original, translated2, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "patient1, dataframe, name, margin",
    [
        ("patient_8.gz", data12, "cube", 1.0),
        ("patient_8.gz", data12, "cube", -1.0),
    ],
)
def test_margins(dicom_infos, patient1, dataframe, name, margin, request):
    original = dicom_infos(patient1)
    expanded = original.add_margin(name, margin)
    df1 = report(original, expanded, name)
    df2 = pd.DataFrame(dataframe)
    print(df1)
    print(df2)
    assert_frame_equal(df1, df2, atol=0.001)


@pytest.mark.parametrize(
    "patient1,patient2,name,expected",
    [
        ("patient_8.gz", "patient_9.gz", "point", does_not_raise()),
        ("patient_8.gz", "patient_9.gz", "cube", does_not_raise()),
        ("patient_8.gz", "patient_12.gz", "cube", pytest.raises(ValueError)),
        ("patient_8.gz", "patient_13.gz", "cube", pytest.raises(ValueError)),
    ],
)
def test_length_contours(
    dicom_infos, patient1, patient2, name, expected, request
):
    with expected:
        original = dicom_infos(patient1)
        rotated = dicom_infos(patient2)
        report(original, rotated, name)
