from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import Dicominfo

import pytest


@pytest.mark.parametrize(
    "dicom,m,expected",
    [
        ("m2", "m6", does_not_raise()),
        ("m3", "m6", pytest.raises(ValueError)),
        ("m4", "m6", does_not_raise()),
    ],
)
def test_repeated_modality(dicom, m, expected, request):
    with expected:
        Dicominfo(request.getfixturevalue(dicom), request.getfixturevalue(m))


@pytest.mark.parametrize(
    "m,dicom,expected",
    [
        ("m4", "m2", does_not_raise()),
        ("m4", "m3", does_not_raise()),
        ("m4", "m5", pytest.raises(ValueError)),
    ],
)
def test_dicominfo_id_match(m, dicom, expected, request):
    with expected:
        assert Dicominfo(
            request.getfixturevalue(m), request.getfixturevalue(dicom)
        )


@pytest.mark.parametrize(
    "dicom_sur_nam, dicom_name_sur",
    [
        ("m2", "m7"),
        ("m4", "m7"),
        ("m7", "m2"),
        ("m7", "m4"),
    ],
)
def test_dicominfo_name_match_2in(dicom_sur_nam, dicom_name_sur, request):
    with pytest.warns(UserWarning):
        Dicominfo(
            request.getfixturevalue(dicom_sur_nam),
            request.getfixturevalue(dicom_name_sur),
        )


@pytest.mark.parametrize(
    "d1, d2, d3",
    [
        ("m2", "m4", "m7"),
        ("m4", "m7", "m2"),
        ("m7", "m2", "m4"),
    ],
)
def test_dicominfo_name_match_3in(d1, d2, d3, request):
    with pytest.warns(UserWarning):
        Dicominfo(
            request.getfixturevalue(d1),
            request.getfixturevalue(d2),
            request.getfixturevalue(d3),
        )


@pytest.mark.parametrize(
    "bd1, bd2",
    [
        ("m2", "m8"),
        ("m4", "m8"),
        ("m8", "m2"),
        ("m8", "m4"),
    ],
)
def test_di_birth_match_2in(bd1, bd2, request):
    with pytest.warns(UserWarning):
        Dicominfo(request.getfixturevalue(bd1), request.getfixturevalue(bd2))


@pytest.mark.parametrize(
    "d1, d2, d3",
    [
        ("m2", "m4", "m8"),
        ("m4", "m8", "m2"),
        ("m8", "m2", "m4"),
    ],
)
def test_di_birth_match_3in(d1, d2, d3, request):
    with pytest.warns(UserWarning):
        Dicominfo(
            request.getfixturevalue(d1),
            request.getfixturevalue(d2),
            request.getfixturevalue(d3),
        )


@pytest.mark.parametrize(
    "dicom,expected",
    [
        ("m1", pytest.raises(ValueError)),
        ("m2", does_not_raise()),
        ("m3", does_not_raise()),
        ("m4", does_not_raise()),
    ],
)
def test_dicominfo_modality_supported_1in(dicom, expected, request):
    with expected:
        di = Dicominfo(request.getfixturevalue(dicom))
        assert di is not None
        assert di.PatientName == request.getfixturevalue(dicom).PatientName
        assert (
            di.PatientBirthDate
            == request.getfixturevalue(dicom).PatientBirthDate
        )
        assert di.PatientID == request.getfixturevalue(dicom).PatientID


@pytest.mark.parametrize(
    "d1, d2",
    [
        ("m1", "m2"),
        ("m1", "m3"),
        ("m1", "m4"),
        ("m2", "m1"),
        ("m3", "m1"),
        ("m4", "m1"),
    ],
)
def test_dicominfo_modality_supported_2in(d1, d2, request):
    with pytest.raises(ValueError):
        Dicominfo(request.getfixturevalue(d1), request.getfixturevalue(d2))


@pytest.mark.parametrize(
    "d1, d2, d3",
    [
        ("m1", "m2", "m3"),
        ("m1", "m3", "m2"),
        ("m2", "m1", "m3"),
        ("m2", "m3", "m1"),
        ("m3", "m1", "m2"),
        ("m3", "m2", "m1"),
        ("m1", "m4", "m3"),
        ("m1", "m3", "m4"),
        ("m4", "m1", "m3"),
        ("m4", "m3", "m1"),
        ("m3", "m1", "m4"),
        ("m3", "m4", "m1"),
        ("m1", "m2", "m4"),
        ("m1", "m4", "m2"),
        ("m2", "m1", "m4"),
        ("m2", "m4", "m1"),
        ("m4", "m1", "m2"),
        ("m4", "m2", "m1"),
    ],
)
def test_dicominfo_modality_supported_3in(d1, d2, d3, request):
    with pytest.raises(ValueError):
        Dicominfo(
            request.getfixturevalue(d1),
            request.getfixturevalue(d2),
            request.getfixturevalue(d3),
        )
