import os
import pathlib

import joblib

import pydicom


PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
DATA_PATH = PATH / "data"

filename = os.path.join(DATA_PATH, "patient_empty.gz")


def create_patient_pydicom():
    patient = pydicom.dataset.Dataset()
    joblib.dump(patient, filename)


create_patient_pydicom()
