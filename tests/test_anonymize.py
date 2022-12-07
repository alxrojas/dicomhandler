import copy

import pytest


@pytest.mark.filterwarnings("ignore:anonymize")
@pytest.mark.parametrize("patient_name", [True, False])
@pytest.mark.parametrize("patient_birth_date", [True, False])
@pytest.mark.parametrize("operators_name", [True, False])
@pytest.mark.parametrize("instance_creation_date", [True, False])
@pytest.mark.parametrize(
    "di",
    [
        "dicom_info_empty",
        "dicom_info_2",
        "dicom_info_3",
        "dicom_info_4",
        "dicom_info_5",
        "dicom_info_6",
        "dicom_info_7",
        "dicom_info_8",
    ],
)
def test_anonymize(
    di,
    patient_name,
    patient_birth_date,
    operators_name,
    instance_creation_date,
    request,
):

    di_original = copy.deepcopy(request.getfixturevalue(di))

    di = request.getfixturevalue(di).anonymize(
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


def test_anonymize_warning(request):
    with pytest.warns(UserWarning):
        di = request.getfixturevalue("dicom_info_empty")
        di.anonymize()
