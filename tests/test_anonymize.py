import copy
from unittest.mock import Mock

import pytest

from dicomhandler.dicom_info import Dicominfo

# pydicom mocks

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


# dicominfo mocks

d1 = Dicominfo()
d2 = Dicominfo(m2)
d3 = Dicominfo(m3)
d4 = Dicominfo(m4)
d5 = Dicominfo(m2, m3)
d6 = Dicominfo(m3, m4)
d7 = Dicominfo(m4, m2)
d8 = Dicominfo(m2, m3, m4)


@pytest.mark.filterwarnings("ignore:anonymize")
@pytest.mark.parametrize("patient_name", [True, False])
@pytest.mark.parametrize("patient_birth_date", [True, False])
@pytest.mark.parametrize("operators_name", [True, False])
@pytest.mark.parametrize("instance_creation_date", [True, False])
@pytest.mark.parametrize("di", [d1, d2, d3, d4, d5, d6, d7, d8])
def test_anonymize(
    di,
    patient_name,
    patient_birth_date,
    operators_name,
    instance_creation_date,
):

    di_original = copy.deepcopy(di)

    di = di.anonymize(
        name=patient_name,
        birth=patient_birth_date,
        operator=operators_name,
        creation=instance_creation_date,
    )

    if di.PatientName is not None and patient_name is True:
        assert di.PatientName == "PatientName"
    else:
        assert di.PatientName == di_original.PatientName

    if di.PatientBirthDate is not None and patient_birth_date is True:
        assert di.PatientBirthDate == "19720101"
    else:
        assert di.PatientBirthDate == di_original.PatientBirthDate

    if di.dicom_struct is not None:

        if patient_name is True:
            assert di.dicom_struct.PatientName == "PatientName"
        else:
            assert (
                di.dicom_struct.PatientName
                == di_original.dicom_struct.PatientName
            )

        if patient_birth_date is True:
            assert di.dicom_struct.PatientBirthDate == "19720101"
        else:
            assert (
                di.dicom_struct.PatientBirthDate
                == di_original.dicom_struct.PatientBirthDate
            )

        if operators_name is True:
            assert di.dicom_struct.OperatorsName == "OperatorName"
        else:
            assert (
                di.dicom_struct.OperatorsName
                == di_original.dicom_struct.OperatorsName
            )

        if instance_creation_date is True:
            assert di.dicom_struct.InstanceCreationDate == "19720101"
        else:
            assert (
                di.dicom_struct.InstanceCreationDate
                == di_original.dicom_struct.InstanceCreationDate
            )

    if di.dicom_dose is not None:

        if patient_name is True:
            assert di.dicom_dose.PatientName == "PatientName"
        else:
            assert (
                di.dicom_dose.PatientName == di_original.dicom_dose.PatientName
            )

        if patient_birth_date is True:
            assert di.dicom_dose.PatientBirthDate == "19720101"
        else:
            assert (
                di.dicom_dose.PatientBirthDate
                == di_original.dicom_dose.PatientBirthDate
            )

        if operators_name is True:
            assert di.dicom_dose.OperatorsName == "OperatorName"
        else:
            assert (
                di.dicom_dose.OperatorsName
                == di_original.dicom_dose.OperatorsName
            )

        if instance_creation_date is True:
            assert di.dicom_dose.InstanceCreationDate == "19720101"
        else:
            assert (
                di.dicom_dose.InstanceCreationDate
                == di_original.dicom_dose.InstanceCreationDate
            )

    if di.dicom_plan is not None:

        if patient_name is True:
            assert di.dicom_plan.PatientName == "PatientName"
        else:
            assert (
                di.dicom_plan.PatientName == di_original.dicom_plan.PatientName
            )

        if patient_birth_date is True:
            assert di.dicom_plan.PatientBirthDate == "19720101"
        else:
            assert (
                di.dicom_plan.PatientBirthDate
                == di_original.dicom_plan.PatientBirthDate
            )

        if operators_name is True:
            assert di.dicom_plan.OperatorsName == "OperatorName"
        else:
            assert (
                di.dicom_plan.OperatorsName
                == di_original.dicom_plan.OperatorsName
            )

        if instance_creation_date is True:
            assert di.dicom_plan.InstanceCreationDate == "19720101"
        else:
            assert (
                di.dicom_plan.InstanceCreationDate
                == di_original.dicom_plan.InstanceCreationDate
            )


def test_anonymize_warning():
    with pytest.warns(UserWarning):
        di = Dicominfo()
        di.anonymize()
