import os
from contextlib import nullcontext as does_not_raise

from dicomhandler.report import report

from pandas.testing import assert_frame_equal

import pytest


@pytest.mark.parametrize(
    "patient1, patient2, name, expected",
    [
        ("patient_8_s.gz", "patient_9_s.gz", "point", does_not_raise()),
        ("patient_8_s.gz", "patient_9_s.gz", "cube", does_not_raise()),
        (
            "patient_8_s.gz",
            "patient_12_s.gz",
            "cube",
            pytest.raises(ValueError),
        ),
        (
            "patient_8_s.gz",
            "patient_13_s.gz",
            "cube",
            pytest.raises(ValueError),
        ),
        ("patient_8_s.gz", "patient_9_s.gz", "point", does_not_raise()),
        ("patient_8_s.gz", "patient_9_s.gz", "cube", does_not_raise()),
        (
            "patient_8_s.gz",
            "patient_9_s.gz",
            "POINT",
            pytest.raises(ValueError),
        ),
        ("patient_8_s.gz", "patient_10_s.gz", "", pytest.raises(ValueError)),
        ("patient_8_s.gz", "patient_9_s.gz", "", pytest.raises(ValueError)),
    ],
)
# These tests verify if the method raises/doesn't raise errors
# in the correct way.
def test_raises(di_1p_fixt, patient1, patient2, name, expected, request):
    with expected:
        df_out_1 = di_1p_fixt(patient1, "test_report")
        df_out_2 = di_1p_fixt(patient2, "test_report")
        report(df_out_1, df_out_2, name)


@pytest.mark.parametrize(
    "patient1, patient2, exp_df_c, name",
    [
        ("patient_8_s.gz", "patient_8_s.gz", "exp_df_rep_1.gz", "point"),
        ("patient_8_s.gz", "patient_9_s.gz", "exp_df_rep_1.gz", "point"),
        ("patient_8_s.gz", "patient_9_s.gz", "exp_df_rep_2.gz", "cube"),
        ("patient_8_s.gz", "patient_8_s.gz", "exp_df_rep_2.gz", "cube"),
    ],
)
# These tests verify if the method generates in the correct way
# the dataframes. In order to do it, two dataframes are compared.
def test_equality_df(
    di_1p_fixt, patient1, patient2, exp_df_c, name, load_file
):
    original = di_1p_fixt(patient1, "test_report")
    rotated = di_1p_fixt(patient2, "test_report")
    df_out = report(original, rotated, name)
    exp_df = load_file(os.getcwd() + "/tests/data/test_report/" + exp_df_c)
    assert_frame_equal(df_out, exp_df)


@pytest.mark.parametrize(
    "patient, exp_df_c, name, delta, key",
    [
        ("patient_8_s.gz", "exp_df_rep_3.gz", "point", 1.0, "x"),
        ("patient_8_s.gz", "exp_df_rep_3.gz", "point", 1.0, "y"),
        ("patient_8_s.gz", "exp_df_rep_3.gz", "point", 1.0, "z"),
        ("patient_8_s.gz", "exp_df_rep_3.gz", "point", -1.0, "x"),
        ("patient_8_s.gz", "exp_df_rep_3.gz", "point", -1.0, "y"),
        ("patient_8_s.gz", "exp_df_rep_3.gz", "point", -1.0, "z"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 0.0, "x"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 0.0, "y"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 0.0, "z"),
        ("patient_8_s.gz", "exp_df_rep_4.gz", "cube", 1.0, "x"),
        ("patient_8_s.gz", "exp_df_rep_4.gz", "cube", 1.0, "y"),
        ("patient_8_s.gz", "exp_df_rep_4.gz", "cube", 1.0, "z"),
        ("patient_8_s.gz", "exp_df_rep_4.gz", "cube", -1.0, "x"),
        ("patient_8_s.gz", "exp_df_rep_4.gz", "cube", -1.0, "y"),
        ("patient_8_s.gz", "exp_df_rep_4.gz", "cube", -1.0, "z"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 0.0, "x"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 0.0, "y"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 0.0, "z"),
    ],
)
# These tests verify if the method generates in the correct way
# the dataframes, when comparing one not translated structure,
# with the same translated structure. In order to do it, two dataframes
# are compared.
def test_translations_df(
    di_1p_fixt, patient, exp_df_c, name, delta, key, load_file
):
    original = di_1p_fixt(patient, "test_report")
    translated = original.move(name, delta, key)
    df_out = report(original, translated, name)
    exp_df = load_file(os.getcwd() + "/tests/data/test_report/" + exp_df_c)
    assert_frame_equal(df_out, exp_df)


@pytest.mark.parametrize(
    "patient, exp_df_c, name, angle, key",
    [
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 0.0, "roll"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 0.0, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 0.0, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 359.99, "roll"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 359.99, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_1.gz", "point", 359.99, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_5.gz", "point", 90.0, "roll"),
        ("patient_8_s.gz", "exp_df_rep_5.gz", "point", 90.0, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_5.gz", "point", 90.0, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_5.gz", "point", -90.0, "roll"),
        ("patient_8_s.gz", "exp_df_rep_5.gz", "point", -90.0, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_5.gz", "point", -90.0, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 0.0, "roll"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 0.0, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 0.0, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 359.99, "roll"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 359.99, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_2.gz", "cube", 359.99, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_6.gz", "cube", 90.0, "roll"),
        ("patient_8_s.gz", "exp_df_rep_6.gz", "cube", 90.0, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_7.gz", "cube", 90.0, "yaw"),
        ("patient_8_s.gz", "exp_df_rep_6.gz", "cube", -90.0, "roll"),
        ("patient_8_s.gz", "exp_df_rep_6.gz", "cube", -90.0, "pitch"),
        ("patient_8_s.gz", "exp_df_rep_7.gz", "cube", -90.0, "yaw"),
    ],
)
# These tests verify if the method generates in the correct way
# the dataframes, when comparing one not rotated structure,
# with the same rotated structure. In order to do it, two dataframes
# are compared.
def test_rotations_df(
    di_1p_fixt, patient, exp_df_c, name, angle, key, load_file
):
    original = di_1p_fixt(patient, "test_report")
    rotated = original.move(name, angle, key)
    df_out = report(original, rotated, name)
    exp_df = load_file(os.getcwd() + "/tests/data/test_report/" + exp_df_c)
    assert_frame_equal(df_out, exp_df)


@pytest.mark.parametrize(
    "patient, exp_df_c, name, angle, key1, key2",
    [
        ("patient_8_s.gz", "exp_df_rep_8.gz", "point", 90.0, "roll", "pitch"),
        ("patient_8_s.gz", "exp_df_rep_9.gz", "point", 90.0, "roll", "yaw"),
        ("patient_8_s.gz", "exp_df_rep_10.gz", "point", 90.0, "pitch", "yaw"),
    ],
)
# These tests verify if the method generates in the correct way
# the dataframes, when comparing one not rotated structure,
# with the same multi-rotated structure. In order to do it, two dataframes
# are compared.
def test_cumulated_rotations(
    di_1p_fixt, patient, exp_df_c, name, angle, key1, key2, load_file
):
    original = di_1p_fixt(patient, "test_report")
    rotated = original.move(name, angle, key1)
    rotated2 = rotated.move(name, angle, key2)
    df_out = report(original, rotated2, name)
    exp_df = load_file(os.getcwd() + "/tests/data/test_report/" + exp_df_c)
    assert_frame_equal(df_out, exp_df)


@pytest.mark.parametrize(
    "patient, exp_df_c, name, delta, key1, key2",
    [
        ("patient_8_s.gz", "exp_df_rep_11.gz", "point", 1.0, "x", "y"),
        ("patient_8_s.gz", "exp_df_rep_11.gz", "point", 1.0, "x", "z"),
        ("patient_8_s.gz", "exp_df_rep_11.gz", "point", 1.0, "z", "y"),
    ],
)
# These tests verify if the method generates in the correct way
# the dataframes, when comparing one not translated structure,
# with the same multi-translated structure. In order to do it, two dataframes
# are compared.
def test_cumulated_translations(
    di_1p_fixt, patient, exp_df_c, name, delta, key1, key2, load_file
):
    original = di_1p_fixt(patient, "test_report")
    translated = original.move(name, delta, key1)
    translated2 = translated.move(name, delta, key2)
    df_out = report(original, translated2, name)
    exp_df = load_file(os.getcwd() + "/tests/data/test_report/" + exp_df_c)
    assert_frame_equal(df_out, exp_df)


@pytest.mark.parametrize(
    "patient, exp_df_c, name, margin",
    [
        ("patient_8_s.gz", "exp_df_rep_12.gz", "cube", 1.0),
        ("patient_8_s.gz", "exp_df_rep_12.gz", "cube", -1.0),
    ],
)
# These tests verify if the method generates in the correct way
# the dataframes, when comparing one structure with original margin,
# with the same structure with increased/reduced margin.
# In order to do it, two dataframes
def test_margins_df(di_1p_fixt, patient, exp_df_c, name, margin, load_file):
    original = di_1p_fixt(patient, "test_report")
    expanded = original.add_margin(name, margin)
    df_out = report(original, expanded, name)
    exp_df = load_file(os.getcwd() + "/tests/data/test_report/" + exp_df_c)
    assert_frame_equal(df_out, exp_df, atol=0.001)
