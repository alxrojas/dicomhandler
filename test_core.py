from contextlib import nullcontext as does_not_raise
from unittest.mock import Mock

import pytest

import core

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


@pytest.mark.parametrize(
    "dicom,expected",
    [
        (m1, pytest.raises(ValueError)),
        (m2, does_not_raise()),
        (m3, does_not_raise()),
        (m4, does_not_raise()),
    ],
)
def test_dicominfo_modality_supported(dicom, expected):
    with expected:
        assert core.Dicominfo(dicom) is not None


@pytest.mark.parametrize(
    "dicom,expected",
    [
        (m2, does_not_raise()),
        (m3, does_not_raise()),
        (m4, does_not_raise()),
        (m5, pytest.raises(ValueError)),
    ],
)
def test_dicominfo_id_match(dicom, expected):
    with expected:
        assert core.Dicominfo(m4, dicom)
