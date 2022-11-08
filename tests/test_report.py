from contextlib import nullcontext as does_not_raise

import pandas as pd
import pydicom
import pytest
from pandas.testing import assert_frame_equal
from pydicom.multival import MultiValue

from dicomhandler.dicom_info import Dicominfo
from dicomhandler.report import report

ds_origin = pydicom.dataset.Dataset()
origin = pydicom.dataset.Dataset()
ds_vect_iso = pydicom.dataset.Dataset()
ds_origin.ROIName = "isocenter"
ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
origin.ContourSequence = [ds_vect_iso]

patient1 = pydicom.dataset.Dataset()
patient1.PatientName = "Mike Wazowski"
patient1.PatientID = "0"
patient1.PatientBirthDate = "20000101"
patient1.OperatorsName = "Mike Wazowski"
patient1.InstanceCreationDate = "20200101"
patient1.Modality = "RTSTRUCT"
ds_seq_struct_1_1 = pydicom.dataset.Dataset()
ds_seq_struct_1_2 = pydicom.dataset.Dataset()
ds_seq_struct_1_1.ROIName = "point"
ds_seq_struct_1_2.ROIName = "cube"
patient1.StructureSetROISequence = [
    ds_seq_struct_1_1,
    ds_seq_struct_1_2,
    ds_origin,
]
pyd_corte_1_punto = pydicom.dataset.Dataset()
pyd_corte_1_1_cube = pydicom.dataset.Dataset()
pyd_corte_1_2_cube = pydicom.dataset.Dataset()
pyd_corte_1_3_cube = pydicom.dataset.Dataset()
corte_1_1_cube = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
corte_1_2_cube = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
corte_1_3_cube = [0.0, 0.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 2.0]
corte_1_1_point = [1.0, 1.0, 1.0]
pyd_corte_1_punto.ContourData = MultiValue(float, corte_1_1_point)
pyd_corte_1_1_cube.ContourData = MultiValue(float, corte_1_1_cube)
pyd_corte_1_2_cube.ContourData = MultiValue(float, corte_1_2_cube)
pyd_corte_1_3_cube.ContourData = MultiValue(float, corte_1_3_cube)
ds_cont_struct_1_1 = pydicom.dataset.Dataset()
ds_cont_struct_1_2 = pydicom.dataset.Dataset()
ds_cont_struct_1_1.ContourSequence = [pyd_corte_1_punto]
ds_cont_struct_1_2.ContourSequence = [
    pyd_corte_1_1_cube,
    pyd_corte_1_2_cube,
    pyd_corte_1_3_cube,
]
patient1.ROIContourSequence = [ds_cont_struct_1_1, ds_cont_struct_1_2, origin]

patient2 = pydicom.dataset.Dataset()
patient2.PatientName = "Mike Wazowski"
patient2.PatientID = "0"
patient2.PatientBirthDate = "20000101"
patient2.OperatorsName = "Mike Wazowski"
patient2.InstanceCreationDate = "20200101"
patient2.Modality = "RTSTRUCT"
ds_seq_struct_2_1 = pydicom.dataset.Dataset()
ds_seq_struct_2_2 = pydicom.dataset.Dataset()
ds_seq_struct_2_1.ROIName = "point"
ds_seq_struct_2_2.ROIName = "cube"
patient2.StructureSetROISequence = [
    ds_seq_struct_2_1,
    ds_seq_struct_2_2,
    ds_origin,
]
pyd_corte_2_punto = pydicom.dataset.Dataset()
pyd_corte_2_1_cube = pydicom.dataset.Dataset()
pyd_corte_2_2_cube = pydicom.dataset.Dataset()
pyd_corte_2_3_cube = pydicom.dataset.Dataset()
corte_2_1_cube = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
corte_2_2_cube = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
corte_2_3_cube = [0.0, 0.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 2.0]
corte_2_1_point = [1.0, 1.0, 1.0]
pyd_corte_2_punto.ContourData = MultiValue(float, corte_2_1_point)
pyd_corte_2_1_cube.ContourData = MultiValue(float, corte_2_1_cube)
pyd_corte_2_2_cube.ContourData = MultiValue(float, corte_2_2_cube)
pyd_corte_2_3_cube.ContourData = MultiValue(float, corte_2_3_cube)
ds_cont_struct_2_1 = pydicom.dataset.Dataset()
ds_cont_struct_2_2 = pydicom.dataset.Dataset()
ds_cont_struct_2_1.ContourSequence = [pyd_corte_2_punto]
ds_cont_struct_2_2.ContourSequence = [
    pyd_corte_2_1_cube,
    pyd_corte_2_2_cube,
    pyd_corte_2_3_cube,
]
patient2.ROIContourSequence = [ds_cont_struct_2_1, ds_cont_struct_2_2, origin]

patient3 = pydicom.dataset.Dataset()
patient3.PatientName = "Mike Wazowski"
patient3.PatientID = "0"
patient3.PatientBirthDate = "20000101"
patient3.OperatorsName = "Mike Wazowski"
patient3.InstanceCreationDate = "20200101"
patient3.Modality = "RTSTRUCT"
ds_seq_struct_3 = pydicom.dataset.Dataset()
ds_seq_struct_3.ROIName = "point_wrong"
patient3.StructureSetROISequence = [ds_seq_struct_3, ds_origin]
pyd_corte_3_punto = pydicom.dataset.Dataset()
pyd_corte_3_punto.ContourData = MultiValue(float, [1.0, 1.0, 1.0])
ds_cont_struct_3 = pydicom.dataset.Dataset()
ds_cont_struct_3.ContourSequence = [pyd_corte_3_punto]
patient3.ROIContourSequence = [ds_cont_struct_3, origin]

patient4 = pydicom.dataset.Dataset()
patient4.PatientName = "Mike Wazowski"
patient4.PatientID = "0"
patient4.PatientBirthDate = "20000101"
patient4.OperatorsName = "Mike Wazowski"
patient4.InstanceCreationDate = "20200101"
patient4.Modality = "RTSTRUCT"
ds_seq_struct_4 = pydicom.dataset.Dataset()
ds_seq_struct_4.ROIName = "point_wrong"
patient4.StructureSetROISequence = [ds_seq_struct_4, ds_origin]
pyd_corte_4_punto = pydicom.dataset.Dataset()
pyd_corte_4_punto.ContourData = MultiValue(float, [1.0, 1.0, 1.0, 1.0])
ds_cont_struct_4 = pydicom.dataset.Dataset()
ds_cont_struct_4.ContourSequence = [pyd_corte_4_punto]
patient4.ROIContourSequence = [ds_cont_struct_4, origin]

patient5 = pydicom.dataset.Dataset()
patient5.PatientName = "Mike Wazowski"
patient5.PatientID = "0"
patient5.PatientBirthDate = "20000101"
patient5.OperatorsName = "Mike Wazowski"
patient5.InstanceCreationDate = "20200101"
patient5.Modality = "RTSTRUCT"
ds_seq_struct_5_1 = pydicom.dataset.Dataset()
ds_seq_struct_5_2 = pydicom.dataset.Dataset()
ds_seq_struct_5_1.ROIName = "point"
ds_seq_struct_5_2.ROIName = "cube"
patient5.StructureSetROISequence = [
    ds_seq_struct_5_1,
    ds_seq_struct_5_2,
    ds_origin,
]
pyd_corte_5_punto = pydicom.dataset.Dataset()
pyd_corte_5_1_cube = pydicom.dataset.Dataset()
pyd_corte_5_2_cube = pydicom.dataset.Dataset()
pyd_corte_5_3_cube = pydicom.dataset.Dataset()
pyd_corte_5_4_cube = pydicom.dataset.Dataset()
corte_5_1_cube = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0]
corte_5_2_cube = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
corte_5_3_cube = [0.0, 0.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 2.0]
corte_5_4_cube = [0.0, 0.0, 3.0, 0.0, 1.0, 3.0, 1.0, 1.0, 3.0, 1.0, 0.0, 3.0]
corte_5_1_point = [1.0, 1.0, 1.0]
pyd_corte_5_punto.ContourData = MultiValue(float, corte_5_1_point)
pyd_corte_5_1_cube.ContourData = MultiValue(float, corte_5_1_cube)
pyd_corte_5_2_cube.ContourData = MultiValue(float, corte_5_2_cube)
pyd_corte_5_3_cube.ContourData = MultiValue(float, corte_5_3_cube)
pyd_corte_5_4_cube.ContourData = MultiValue(float, corte_5_4_cube)
ds_cont_struct_5_1 = pydicom.dataset.Dataset()
ds_cont_struct_5_2 = pydicom.dataset.Dataset()
ds_cont_struct_5_1.ContourSequence = [pyd_corte_5_punto]
ds_cont_struct_5_2.ContourSequence = [
    pyd_corte_5_1_cube,
    pyd_corte_5_2_cube,
    pyd_corte_5_3_cube,
    pyd_corte_5_4_cube,
]
patient5.ROIContourSequence = [ds_cont_struct_5_1, ds_cont_struct_5_2, origin]

patient6 = pydicom.dataset.Dataset()
patient6.PatientName = "Mike Wazowski"
patient6.PatientID = "0"
patient6.PatientBirthDate = "20000101"
patient6.OperatorsName = "Mike Wazowski"
patient6.InstanceCreationDate = "20200101"
patient6.Modality = "RTSTRUCT"
ds_seq_struct_6_1 = pydicom.dataset.Dataset()
ds_seq_struct_6_2 = pydicom.dataset.Dataset()
ds_seq_struct_6_1.ROIName = "point"
ds_seq_struct_6_2.ROIName = "cube"
patient6.StructureSetROISequence = [
    ds_seq_struct_6_1,
    ds_seq_struct_6_2,
    ds_origin,
]
pyd_corte_6_punto = pydicom.dataset.Dataset()
pyd_corte_6_1_cube = pydicom.dataset.Dataset()
pyd_corte_6_2_cube = pydicom.dataset.Dataset()
pyd_corte_6_3_cube = pydicom.dataset.Dataset()
pyd_corte_6_4_cube = pydicom.dataset.Dataset()
corte_6_1_cube = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]
corte_6_2_cube = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
corte_6_3_cube = [0.0, 0.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 2.0]
corte_6_1_point = [1.0, 1.0]
pyd_corte_6_punto.ContourData = MultiValue(float, corte_6_1_point)
pyd_corte_6_1_cube.ContourData = MultiValue(float, corte_6_1_cube)
pyd_corte_6_2_cube.ContourData = MultiValue(float, corte_6_2_cube)
pyd_corte_6_3_cube.ContourData = MultiValue(float, corte_6_3_cube)
ds_cont_struct_6_1 = pydicom.dataset.Dataset()
ds_cont_struct_6_2 = pydicom.dataset.Dataset()
ds_cont_struct_6_1.ContourSequence = [pyd_corte_6_punto]
ds_cont_struct_6_2.ContourSequence = [
    pyd_corte_6_1_cube,
    pyd_corte_6_2_cube,
    pyd_corte_6_3_cube,
]
patient6.ROIContourSequence = [ds_cont_struct_6_1, ds_cont_struct_6_2, origin]

patient7 = pydicom.dataset.Dataset()
patient7.PatientName = "Mike Wazowski"
patient7.PatientID = "0"
patient7.PatientBirthDate = "20000101"
patient7.OperatorsName = "Mike Wazowski"
patient7.InstanceCreationDate = "20200101"
patient7.Modality = "RTSTRUCT"
ds_seq_struct_7_1 = pydicom.dataset.Dataset()
ds_seq_struct_7_2 = pydicom.dataset.Dataset()
ds_seq_struct_7_1.ROIName = "point"
ds_seq_struct_7_2.ROIName = "cube"
patient7.StructureSetROISequence = [
    ds_seq_struct_7_1,
    ds_seq_struct_7_2,
    ds_origin,
]
pyd_corte_7_punto = pydicom.dataset.Dataset()
pyd_corte_7_1_cube = pydicom.dataset.Dataset()
pyd_corte_7_2_cube = pydicom.dataset.Dataset()
pyd_corte_7_3_cube = pydicom.dataset.Dataset()
pyd_corte_7_4_cube = pydicom.dataset.Dataset()
corte_7_1_cube = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
corte_7_2_cube = [0.0, 0.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 0.0, 2.0]
corte_7_3_cube = [0.0, 0.0, 3.0, 0.0, 1.0, 3.0, 1.0, 1.0, 3.0, 1.0, 0.0, 3.0]
corte_7_1_point = [1.0, 1.0, 2.0]
pyd_corte_7_punto.ContourData = MultiValue(float, corte_7_1_point)
pyd_corte_7_1_cube.ContourData = MultiValue(float, corte_7_1_cube)
pyd_corte_7_2_cube.ContourData = MultiValue(float, corte_7_2_cube)
pyd_corte_7_3_cube.ContourData = MultiValue(float, corte_7_3_cube)
ds_cont_struct_7_1 = pydicom.dataset.Dataset()
ds_cont_struct_7_2 = pydicom.dataset.Dataset()
ds_cont_struct_7_1.ContourSequence = [pyd_corte_7_punto]
ds_cont_struct_7_2.ContourSequence = [
    pyd_corte_7_1_cube,
    pyd_corte_7_2_cube,
    pyd_corte_7_3_cube,
]
patient6.ROIContourSequence = [ds_cont_struct_6_1, ds_cont_struct_6_2, origin]

data1 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
}

data2 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
}

data3 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
    ],
}

data4 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
    ],
}

data5 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.0,
        2.0,
        2.0,
        0.0,
        0.0,
        2.0,
    ],
}

data6 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        3.162,
        0.0,
        1.803,
        1.040,
        1.082,
        1.581,
    ],
}

data7 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        2.0,
        0.0,
        1.207,
        0.737,
        0.543,
        1.0,
    ],
}

data8 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.828,
        2.828,
        2.828,
        0.0,
        0.0,
        2.828,
    ],
}

data9 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ],
}

data10 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        2.828,
        2.828,
        2.828,
        0.0,
        0.0,
        2.828,
    ],
}

data11 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        1.414,
        1.414,
        1.414,
        0.0,
        0.0,
        1.414,
    ],
}

data12 = {
    "Parameter": [
        "Max radius",
        "Min radius",
        "Mean radius",
        "STD radius",
        "Variance radius",
        "Max distance",
        "Min distance",
        "Mean distance",
        "STD distance",
        "Variance distance",
        "Distance between center mass",
    ],
    "Value [mm]": [
        1.225,
        0.707,
        1.052,
        0.244,
        0.06,
        1.0,
        1.0,
        1.0,
        0.0,
        0.0,
        0.0,
    ],
}


@pytest.mark.parametrize(
    "dicom1,dicom2,name,expected",
    [
        (patient1, patient2, "point", does_not_raise()),
        (patient1, patient2, "cube", does_not_raise()),
        (patient1, patient2, "POINT", pytest.raises(ValueError)),
        (patient1, patient3, "", pytest.raises(ValueError)),
        (patient1, patient2, "", pytest.raises(ValueError)),
        (patient1, patient3, "point", pytest.raises(ValueError)),
        (patient1, patient3, "cube", pytest.raises(ValueError)),
    ],
)
def test_match_name(dicom1, dicom2, name, expected):
    with expected:
        original = Dicominfo(dicom1)
        rotated = Dicominfo(dicom2)
        report(original, rotated, name)


@pytest.mark.parametrize(
    "dicom1,dicom2,name,expected",
    [
        (patient1, patient2, "point", does_not_raise()),
        (patient1, patient2, "cube", does_not_raise()),
        (patient1, patient4, "point", pytest.raises(ValueError)),
        (patient1, patient5, "cube", pytest.raises(ValueError)),
        (patient1, patient6, "cube", pytest.raises(ValueError)),
    ],
)
def test_length_contours(dicom1, dicom2, name, expected):
    with expected:
        original = Dicominfo(dicom1)
        rotated = Dicominfo(dicom2)
        report(original, rotated, name)


@pytest.mark.parametrize(
    "dicom1,dicom2, dataframe, name",
    [
        (patient1, patient1, data1, "point"),
        (patient1, patient2, data1, "point"),
        (patient1, patient2, data2, "cube"),
        (patient1, patient1, data2, "cube"),
    ],
)
def test_dataframe(dicom1, dicom2, dataframe, name):
    original = Dicominfo(dicom1)
    rotated = Dicominfo(dicom2)
    df1 = report(original, rotated, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "dicom1, dataframe, name, delta, key",
    [
        (patient1, data3, "point", 1.0, "x"),
        (patient1, data3, "point", 1.0, "y"),
        (patient1, data3, "point", 1.0, "z"),
        (patient1, data3, "point", -1.0, "x"),
        (patient1, data3, "point", -1.0, "y"),
        (patient1, data3, "point", -1.0, "z"),
        (patient1, data1, "point", 0.0, "x"),
        (patient1, data1, "point", 0.0, "y"),
        (patient1, data1, "point", 0.0, "z"),
        (patient1, data4, "cube", 1.0, "x"),
        (patient1, data4, "cube", 1.0, "y"),
        (patient1, data4, "cube", 1.0, "z"),
        (patient1, data4, "cube", -1.0, "x"),
        (patient1, data4, "cube", -1.0, "y"),
        (patient1, data4, "cube", -1.0, "z"),
        (patient1, data2, "cube", 0.0, "x"),
        (patient1, data2, "cube", 0.0, "y"),
        (patient1, data2, "cube", 0.0, "z"),
    ],
)
def test_translations(dicom1, dataframe, name, delta, key):
    original = Dicominfo(dicom1)
    translated = original.translate(name, delta, key)
    df1 = report(original, translated, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "dicom1, dataframe, name, angle, key",
    [
        (patient1, data1, "point", 0.0, "roll"),
        (patient1, data1, "point", 0.0, "pitch"),
        (patient1, data1, "point", 0.0, "yaw"),
        (patient1, data1, "point", 359.99, "roll"),
        (patient1, data1, "point", 359.99, "pitch"),
        (patient1, data1, "point", 359.99, "yaw"),
        (patient1, data5, "point", 90.0, "roll"),
        (patient1, data5, "point", 90.0, "pitch"),
        (patient1, data5, "point", 90.0, "yaw"),
        (patient1, data5, "point", -90.0, "roll"),
        (patient1, data5, "point", -90.0, "pitch"),
        (patient1, data5, "point", -90.0, "yaw"),
        (patient1, data2, "cube", 0.0, "roll"),
        (patient1, data2, "cube", 0.0, "pitch"),
        (patient1, data2, "cube", 0.0, "yaw"),
        (patient1, data2, "cube", 359.99, "roll"),
        (patient1, data2, "cube", 359.99, "pitch"),
        (patient1, data2, "cube", 359.99, "yaw"),
        (patient1, data6, "cube", 90.0, "roll"),
        (patient1, data6, "cube", 90.0, "pitch"),
        (patient1, data7, "cube", 90.0, "yaw"),
        (patient1, data6, "cube", -90.0, "roll"),
        (patient1, data6, "cube", -90.0, "pitch"),
        (patient1, data7, "cube", -90.0, "yaw"),
    ],
)
def test_rotations(dicom1, dataframe, name, angle, key):
    original = Dicominfo(dicom1)
    rotated = original.rotate(name, angle, key)
    df1 = report(original, rotated, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "dicom1, dataframe, name, angle, key1, key2",
    [
        (patient1, data8, "point", 90.0, "roll", "pitch"),
        (patient1, data9, "point", 90.0, "roll", "yaw"),
        (patient1, data10, "point", 90.0, "pitch", "yaw"),
    ],
)
def test_cumulated_rotations(dicom1, dataframe, name, angle, key1, key2):
    original = Dicominfo(dicom1)
    rotated = original.rotate(name, angle, key1)
    rotated2 = rotated.rotate(name, angle, key2)
    df1 = report(original, rotated2, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "dicom1, dataframe, name, delta, key1, key2",
    [
        (patient1, data11, "point", 1.0, "x", "y"),
        (patient1, data11, "point", 1.0, "x", "z"),
        (patient1, data11, "point", 1.0, "z", "y"),
    ],
)
def test_cumulated_translations(dicom1, dataframe, name, delta, key1, key2):
    original = Dicominfo(dicom1)
    translated = original.translate(name, delta, key1)
    translated2 = translated.translate(name, delta, key2)
    df1 = report(original, translated2, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)


@pytest.mark.parametrize(
    "dicom1, dataframe, name, margin",
    [
        (patient1, data12, "cube", 1.0),
        (patient1, data12, "cube", -1.0),
    ],
)
def test_margins(dicom1, dataframe, name, margin):
    original = Dicominfo(dicom1)
    expanded = original.add_margin(name, margin)
    df1 = report(original, expanded, name)
    df2 = pd.DataFrame(dataframe)
    assert_frame_equal(df1, df2)
