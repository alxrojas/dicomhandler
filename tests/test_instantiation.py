from contextlib import nullcontext as does_not_raise

from dicomhandler.dicom_info import DicomInfo

import pytest


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2, expected",
    [
        ("patient_mock_2", "patient_mock_6", does_not_raise()),
        ("patient_mock_3", "patient_mock_6", pytest.raises(ValueError)),
        ("patient_mock_4", "patient_mock_6", does_not_raise()),
    ],
)
def test_repeated_modality(patient_mock1, patient_mock2, expected, request):
    with expected:
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
        )


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2,expected",
    [
        ("patient_mock_4", "patient_mock_2", does_not_raise()),
        ("patient_mock_4", "patient_mock_3", does_not_raise()),
        ("patient_mock_4", "patient_mock_5", pytest.raises(ValueError)),
    ],
)
def test_dicominfo_id_match(patient_mock1, patient_mock2, expected, request):
    with expected:
        assert DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
        )


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2",
    [
        ("patient_mock_2", "patient_mock_7"),
        ("patient_mock_4", "patient_mock_7"),
        ("patient_mock_7", "patient_mock_2"),
        ("patient_mock_7", "patient_mock_4"),
    ],
)
def test_dicominfo_name_match_2in(patient_mock1, patient_mock2, request):
    with pytest.warns(UserWarning):
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
        )


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2, patient_mock3",
    [
        ("patient_mock_2", "patient_mock_4", "patient_mock_7"),
        ("patient_mock_4", "patient_mock_7", "patient_mock_2"),
        ("patient_mock_7", "patient_mock_2", "patient_mock_4"),
    ],
)
def test_dicominfo_name_match_3in(
    patient_mock1, patient_mock2, patient_mock3, request
):
    with pytest.warns(UserWarning):
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
            request.getfixturevalue(patient_mock3),
        )


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2",
    [
        ("patient_mock_2", "patient_mock_8"),
        ("patient_mock_4", "patient_mock_8"),
        ("patient_mock_8", "patient_mock_2"),
        ("patient_mock_8", "patient_mock_4"),
    ],
)
def test_di_birth_match_2in(patient_mock1, patient_mock2, request):
    with pytest.warns(UserWarning):
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
        )


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2, patient_mock3",
    [
        ("patient_mock_2", "patient_mock_4", "patient_mock_8"),
        ("patient_mock_4", "patient_mock_8", "patient_mock_2"),
        ("patient_mock_8", "patient_mock_2", "patient_mock_4"),
    ],
)
def test_di_birth_match_3in(
    patient_mock1, patient_mock2, patient_mock3, request
):
    with pytest.warns(UserWarning):
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
            request.getfixturevalue(patient_mock3),
        )


@pytest.mark.parametrize(
    "patient_mock,expected",
    [
        ("patient_mock_1", pytest.raises(ValueError)),
        ("patient_mock_2", does_not_raise()),
        ("patient_mock_3", does_not_raise()),
        ("patient_mock_4", does_not_raise()),
    ],
)
def test_dicominfo_modality_supported_1in(patient_mock, expected, request):
    with expected:
        di = DicomInfo(request.getfixturevalue(patient_mock))
        assert di is not None
        assert (
            di.PatientName == request.getfixturevalue(patient_mock).PatientName
        )
        assert (
            di.PatientBirthDate
            == request.getfixturevalue(patient_mock).PatientBirthDate
        )
        assert di.PatientID == request.getfixturevalue(patient_mock).PatientID


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2",
    [
        ("patient_mock_1", "patient_mock_2"),
        ("patient_mock_1", "patient_mock_3"),
        ("patient_mock_1", "patient_mock_4"),
        ("patient_mock_2", "patient_mock_1"),
        ("patient_mock_3", "patient_mock_1"),
        ("patient_mock_4", "patient_mock_1"),
    ],
)
def test_dicominfo_modality_supported_2in(
    patient_mock1, patient_mock2, request
):
    with pytest.raises(ValueError):
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
        )


@pytest.mark.parametrize(
    "patient_mock1, patient_mock2, patient_mock3",
    [
        ("patient_mock_1", "patient_mock_2", "patient_mock_3"),
        ("patient_mock_1", "patient_mock_3", "patient_mock_2"),
        ("patient_mock_2", "patient_mock_1", "patient_mock_3"),
        ("patient_mock_2", "patient_mock_3", "patient_mock_1"),
        ("patient_mock_3", "patient_mock_1", "patient_mock_2"),
        ("patient_mock_3", "patient_mock_2", "patient_mock_1"),
        ("patient_mock_1", "patient_mock_4", "patient_mock_3"),
        ("patient_mock_1", "patient_mock_3", "patient_mock_4"),
        ("patient_mock_4", "patient_mock_1", "patient_mock_3"),
        ("patient_mock_4", "patient_mock_3", "patient_mock_1"),
        ("patient_mock_3", "patient_mock_1", "patient_mock_4"),
        ("patient_mock_3", "patient_mock_4", "patient_mock_1"),
        ("patient_mock_1", "patient_mock_2", "patient_mock_4"),
        ("patient_mock_1", "patient_mock_4", "patient_mock_2"),
        ("patient_mock_2", "patient_mock_1", "patient_mock_4"),
        ("patient_mock_2", "patient_mock_4", "patient_mock_1"),
        ("patient_mock_4", "patient_mock_1", "patient_mock_2"),
        ("patient_mock_4", "patient_mock_2", "patient_mock_1"),
    ],
)
def test_dicominfo_modality_supported_3in(
    patient_mock1, patient_mock2, patient_mock3, request
):
    with pytest.raises(ValueError):
        DicomInfo(
            request.getfixturevalue(patient_mock1),
            request.getfixturevalue(patient_mock2),
            request.getfixturevalue(patient_mock3),
        )
