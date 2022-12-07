import os
import pathlib
from unittest.mock import Mock

from dicomhandler.dicom_info import Dicominfo

import joblib

import pytest


PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DATA_PATH = PATH / "data"


@pytest.fixture(scope="session")
def dicom_infos():
    def make(name):

        return Dicominfo(joblib.load(DATA_PATH / name))

    return make


@pytest.fixture(scope="session")
def patients():
    def make(name):
        return joblib.load(DATA_PATH / name)

    return make


@pytest.fixture()
def dicom_info_empty():
    d1 = Dicominfo()
    return d1


@pytest.fixture()
def dicom_info_2():
    m2 = Mock()
    m2.PatientName = "Mike Wazowski"
    m2.PatientID = "00"
    m2.PatientBirthDate = "20000102"
    m2.OperatorsName = "Myself"
    m2.InstanceCreationDate = "20220101"
    m2.Modality = "RTPLAN"
    d2 = Dicominfo(m2)
    return d2


@pytest.fixture()
def dicom_info_3():
    m3 = Mock()
    m3.PatientName = "Mike Wazowski"
    m3.PatientID = "00"
    m3.PatientBirthDate = "20000102"
    m3.OperatorsName = "Myself"
    m3.InstanceCreationDate = "20220101"
    m3.Modality = "RTDOSE"
    d3 = Dicominfo(m3)
    return d3


@pytest.fixture()
def dicom_info_4():
    m4 = Mock()
    m4.PatientName = "Mike Wazowski"
    m4.PatientID = "00"
    m4.PatientBirthDate = "20000102"
    m4.OperatorsName = "Myself"
    m4.InstanceCreationDate = "20220101"
    m4.Modality = "RTSTRUCT"
    d4 = Dicominfo(m4)
    return d4


@pytest.fixture()
def dicom_info_5():
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
    d5 = Dicominfo(m2, m3)
    return d5


@pytest.fixture()
def dicom_info_6():
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
    d6 = Dicominfo(m3, m4)
    return d6


@pytest.fixture()
def dicom_info_7():
    m2 = Mock()
    m2.PatientName = "Mike Wazowski"
    m2.PatientID = "00"
    m2.PatientBirthDate = "20000102"
    m2.OperatorsName = "Myself"
    m2.InstanceCreationDate = "20220101"
    m2.Modality = "RTPLAN"
    m4 = Mock()
    m4.PatientName = "Mike Wazowski"
    m4.PatientID = "00"
    m4.PatientBirthDate = "20000102"
    m4.OperatorsName = "Myself"
    m4.InstanceCreationDate = "20220101"
    m4.Modality = "RTSTRUCT"
    d7 = Dicominfo(m4, m2)
    return d7


@pytest.fixture()
def dicom_info_8():
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
    d8 = Dicominfo(m2, m3, m4)
    return d8


@pytest.fixture()
def patient_mock_1():
    m1 = Mock()
    m1.PatientName = "Mike Wazowski"
    m1.PatientID = "00"
    m1.PatientBirthDate = "20000102"
    m1.OperatorsName = "Myself"
    m1.InstanceCreationDate = "20220101"
    m1.Modality = ""
    return m1


@pytest.fixture()
def patient_mock_2():
    m2 = Mock()
    m2.PatientName = "Mike Wazowski"
    m2.PatientID = "00"
    m2.PatientBirthDate = "20000102"
    m2.OperatorsName = "Myself"
    m2.InstanceCreationDate = "20220101"
    m2.Modality = "RTPLAN"
    return m2


@pytest.fixture()
def patient_mock_3():
    m3 = Mock()
    m3.PatientName = "Mike Wazowski"
    m3.PatientID = "00"
    m3.PatientBirthDate = "20000102"
    m3.OperatorsName = "Myself"
    m3.InstanceCreationDate = "20220101"
    m3.Modality = "RTDOSE"
    return m3


@pytest.fixture()
def patient_mock_4():
    m4 = Mock()
    m4.PatientName = "Mike Wazowski"
    m4.PatientID = "00"
    m4.PatientBirthDate = "20000102"
    m4.OperatorsName = "Myself"
    m4.InstanceCreationDate = "20220101"
    m4.Modality = "RTSTRUCT"
    return m4


@pytest.fixture()
def patient_mock_5():
    m5 = Mock()
    m5.PatientName = "Mike Wazowski"
    m5.PatientID = "02"
    m5.PatientBirthDate = "20000102"
    m5.OperatorsName = "Myself"
    m5.InstanceCreationDate = "20220101"
    m5.Modality = "RTDOSE"
    return m5


@pytest.fixture()
def patient_mock_6():
    m6 = Mock()
    m6.PatientName = "Mike Wazowski"
    m6.PatientID = "00"
    m6.PatientBirthDate = "20000102"
    m6.OperatorsName = "Myself"
    m6.InstanceCreationDate = "20220101"
    m6.Modality = "RTDOSE"
    return m6


@pytest.fixture()
def patient_mock_7():
    m7 = Mock()
    m7.PatientName = "Wazowski, Mike"
    m7.PatientID = "00"
    m7.PatientBirthDate = "20000102"
    m7.OperatorsName = "Myself"
    m7.InstanceCreationDate = "20220101"
    m7.Modality = "RTDOSE"
    return m7


@pytest.fixture()
def patient_mock_8():
    m8 = Mock()
    m8.PatientName = "Wazowski, Mike"
    m8.PatientID = "00"
    m8.PatientBirthDate = "20000101"
    m8.OperatorsName = "Myself"
    m8.InstanceCreationDate = "20220101"
    m8.Modality = "RTDOSE"
    return m8
