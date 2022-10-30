from contextlib import nullcontext as does_not_raise
from unittest.mock import Mock

import pytest

from dicomhandler.dicom_info import Dicominfo

m1 = Mock()
m1.PatientName = "Mike Wazowski"
m1.PatientID = "00"
m1.PatientBirthDate = "20000102"
m1.OperatorsName = "Myself"
m1.InstanceCreationDate = "20220101"
m1.Modality = ""

m2 = Mock()
m2.PatientName = "Mike Wazowski"
m2.PatientID = "00"
m2.PatientBirthDate = "20000102"
m2.OperatorsName = "Myself"
m2.InstanceCreationDate = "20220101"
m2.Modality = "RTPLAN"

m3 = Mock()
m3.PatientName = "Mike Wazowski"
m3.PatientID = "00"
m3.PatientBirthDate = "20000102"
m3.OperatorsName = "Myself"
m3.InstanceCreationDate = "20220101"
m3.Modality = "RTDOSE"

m4 = Mock()
m4.PatientName = "Mike Wazowski"
m4.PatientID = "00"
m4.PatientBirthDate = "20000102"
m4.OperatorsName = "Myself"
m4.InstanceCreationDate = "20220101"
m4.Modality = "RTSTRUCT"

m5 = Mock()
m5.PatientName = "Mike Wazowski"
m5.PatientID = "02"
m5.PatientBirthDate = "20000102"
m5.OperatorsName = "Myself"
m5.InstanceCreationDate = "20220101"
m5.Modality = "RTDOSE"

m6 = Mock()
m6.PatientName = "Mike Wazowski"
m6.PatientID = "00"
m6.PatientBirthDate = "20000102"
m6.OperatorsName = "Myself"
m6.InstanceCreationDate = "20220101"
m6.Modality = "RTDOSE"

m7 = Mock()
m7.PatientName = "Wazowski, Mike"
m7.PatientID = "00"
m7.PatientBirthDate = "20000102"
m7.OperatorsName = "Myself"
m7.InstanceCreationDate = "20220101"
m7.Modality = "RTDOSE"

m8 = Mock()
m8.PatientName = "Wazowski, Mike"
m8.PatientID = "00"
m8.PatientBirthDate = "20000101"
m8.OperatorsName = "Myself"
m8.InstanceCreationDate = "20220101"
m8.Modality = "RTDOSE"


@pytest.mark.parametrize(
    "dicom,m6,expected",
    [
        (m2, m6, does_not_raise()),
        (m3, m6, pytest.raises(ValueError)),
        (m4, m6, does_not_raise()),
    ],
)
def test_repeated_modality(dicom, m6, expected):
    with expected:
        Dicominfo(dicom, m6)


@pytest.mark.parametrize(
    "m4,dicom,expected",
    [
        (m4, m2, does_not_raise()),
        (m4, m3, does_not_raise()),
        (m4, m5, pytest.raises(ValueError)),
    ],
)
def test_dicominfo_id_match(m4, dicom, expected):
    with expected:
        assert Dicominfo(m4, dicom)


@pytest.mark.parametrize(
    "dicom_sur_nam, dicom_name_sur",
    [
        (m2, m7),
        (m4, m7),
        (m7, m2),
        (m7, m4),
    ],
)
def test_dicominfo_name_match_2in(dicom_sur_nam, dicom_name_sur):
    with pytest.warns(UserWarning):
        Dicominfo(dicom_sur_nam, dicom_name_sur)


@pytest.mark.parametrize(
    "d1, d2, d3",
    [
        (m2, m4, m7),
        (m4, m7, m2),
        (m7, m2, m4),
    ],
)
def test_dicominfo_name_match_3in(d1, d2, d3):
    with pytest.warns(UserWarning):
        Dicominfo(d1, d2, d3)


@pytest.mark.parametrize(
    "bd1, bd2",
    [
        (m2, m8),
        (m4, m8),
        (m8, m2),
        (m8, m4),
    ],
)
def test_di_birth_match_2in(bd1, bd2):
    with pytest.warns(UserWarning):
        Dicominfo(bd1, bd2)


@pytest.mark.parametrize(
    "d1, d2, d3",
    [
        (m2, m4, m8),
        (m4, m8, m2),
        (m8, m2, m4),
    ],
)
def test_di_birth_match_3in(d1, d2, d3):
    with pytest.warns(UserWarning):
        Dicominfo(d1, d2, d3)


@pytest.mark.parametrize(
    "dicom,expected",
    [
        (m1, pytest.raises(ValueError)),
        (m2, does_not_raise()),
        (m3, does_not_raise()),
        (m4, does_not_raise()),
    ],
)
def test_dicominfo_modality_supported_1in(dicom, expected):
    with expected:
        di = Dicominfo(dicom)
        assert di is not None
        assert di.PatientName == dicom.PatientName
        assert di.PatientBirthDate == dicom.PatientBirthDate
        assert di.PatientID == dicom.PatientID


@pytest.mark.parametrize(
    "d1, d2",
    [
        (m1, m2),
        (m1, m3),
        (m1, m4),
        (m2, m1),
        (m3, m1),
        (m4, m1),
    ],
)
def test_dicominfo_modality_supported_2in(d1, d2):
    with pytest.raises(ValueError):
        Dicominfo(d1, d2)


@pytest.mark.parametrize(
    "d1, d2, d3",
    [
        (m1, m2, m3),
        (m1, m3, m2),
        (m2, m1, m3),
        (m2, m3, m1),
        (m3, m1, m2),
        (m3, m2, m1),
        (m1, m4, m3),
        (m1, m3, m4),
        (m4, m1, m3),
        (m4, m3, m1),
        (m3, m1, m4),
        (m3, m4, m1),
        (m1, m2, m4),
        (m1, m4, m2),
        (m2, m1, m4),
        (m2, m4, m1),
        (m4, m1, m2),
        (m4, m2, m1),
    ],
)
def test_dicominfo_modality_supported_3in(d1, d2, d3):
    with pytest.raises(ValueError):
        Dicominfo(d1, d2, d3)
