import pydicom
import pytest
from dicomhandler.dicom_info import Dicominfo
from pydicom.multival import MultiValue

patient = pydicom.dataset.Dataset()
patient.PatientName = "mario rossi"
patient.PatientID = "3"
patient.PatientBirthDate = "20000101"
patient.OperatorsName = "guido rossi"
patient.InstanceCreationDate = "20200101"
patient.Modality = "RTSTRUCT"

ds1 = pydicom.dataset.Dataset()
ds2 = pydicom.dataset.Dataset()
ds1.ROIName = "cuadrado"
ds2.ROIName = "sfera"
patient.StructureSetROISequence = [ds1]
ds33 = pydicom.dataset.Dataset()
ds00 = pydicom.dataset.Dataset()
ds333 = pydicom.dataset.Dataset()
ds000 = pydicom.dataset.Dataset()
a = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0]
b = [0.0, 0.0, 0.0]
ds000.ContourData = MultiValue(float, b)
ds333.ContourData = MultiValue(float, a)
ds33.ContourSequence = [ds333]
ds00.ContourSequence = [ds000]
patient.ROIContourSequence = [ds33, ds00]


@pytest.mark.parametrize(
    "struct, delta, key, patient",
    [
        ("cuadrado", 0.1, "y", patient),
        ("cuadrado", 0.1, "x", patient),
    ],
)
def test_translate(struct, delta, key, patient, *args):
    dicom_info1 = Dicominfo(patient)
    x = (
        dicom_info1.translate(struct, delta, key)
        .dicom_struct.ROIContourSequence[0]
        .ContourSequence[0]
        .ContourData
    )
    y = patient.ROIContourSequence[0].ContourSequence[0].ContourData
    assert len(x) == len(y)
    assert all([abs(xi - yi) <= 1.5 for xi, yi in zip(x, y)])
