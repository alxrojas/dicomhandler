from unittest.mock import Mock

from dicomhandler.dicom_info import Dicominfo

import numpy as np

import pydicom
from pydicom.multival import MultiValue

import pytest


@pytest.fixture()
def patient_1():
    """Method patient_1

    It creates a instance of a pydicom.dataset.Dataset().
    This instance contains the information about the structures
    and the courts. The function return the instance, that is
    used for testing the funcions rotate and translate of
    the class Dicominfo

    Returns
    -------
    pydicom.dataset.Dataset
        Object with information about structures and courts

    """
    patient = pydicom.dataset.Dataset()
    patient.PatientName = "mario rossi"
    patient.PatientID = "3"
    patient.PatientBirthDate = "20000101"
    patient.OperatorsName = "guido rossi"
    patient.InstanceCreationDate = "20200101"
    patient.Modality = "RTSTRUCT"

    # pydicom.StructureROISequence[0].ROIName
    ds_seq_struct_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2 = pydicom.dataset.Dataset()
    ds_seq_struct_3 = pydicom.dataset.Dataset()
    ds_seq_struct_4 = pydicom.dataset.Dataset()
    ds_seq_struct_5 = pydicom.dataset.Dataset()
    ds_seq_struct_1.ROIName = "cubo"
    ds_seq_struct_2.ROIName = "space"
    ds_seq_struct_3.ROIName = "punto"
    ds_seq_struct_4.ROIName = "error"
    ds_seq_struct_5.ROIName = "Coord 1"
    patient.StructureSetROISequence = [
        ds_seq_struct_1,
        ds_seq_struct_2,
        ds_seq_struct_3,
        ds_seq_struct_4,
        ds_seq_struct_5,
    ]

    pyd_corte_1_cubo = pydicom.dataset.Dataset()
    pyd_corte_2_cubo = pydicom.dataset.Dataset()
    pyd_corte_3_cubo = pydicom.dataset.Dataset()
    pyd_corte_4_cubo = pydicom.dataset.Dataset()
    pyd_corte_1_space = pydicom.dataset.Dataset()
    pyd_corte_2_space = pydicom.dataset.Dataset()
    pyd_corte_3_space = pydicom.dataset.Dataset()
    pyd_corte_1_punto = pydicom.dataset.Dataset()
    pyd_corte_1_error = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()

    corte_1_cubo = [0.0, 0.0, 0.0, 2.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 2.0, 0.0]
    corte_2_cubo = [0.0, 0.0, 0.3, 2.0, 0.0, 0.3, 2.0, 2.0, 0.3, 0.0, 2.0, 0.3]
    corte_3_cubo = [0.0, 0.0, 0.6, 2.0, 0.0, 0.6, 2.0, 2.0, 0.6, 0.0, 2.0, 0.6]
    corte_4_cubo = [0.0, 0.0, 1.2, 2.0, 0.0, 1.2, 2.0, 2.0, 1.2, 0.0, 2.0, 1.2]
    corte_1_space = [1.2, 1.3, 1.5, 1.2, 7, 1.5, 1.2, 10, 1.5]
    corte_2_space = [1.2, 1.3, 1.5, 1.2, 7, 1.5, 1.2, 10, 1.5]
    corte_3_space = [1.2, 2.0, 3, 1.2, 3.0, 3, 1.2, 4.5, 3]
    corte_1_punto = [1.0, 1.0, 1.0]
    corte_1_error = [1, 1, 1, 2, 2, 3, 4.0]
    iso = [0.0, 0.0, 0.0]
    pyd_corte_1_cubo.ContourData = MultiValue(float, corte_1_cubo)
    pyd_corte_2_cubo.ContourData = MultiValue(float, corte_2_cubo)
    pyd_corte_3_cubo.ContourData = MultiValue(float, corte_3_cubo)
    pyd_corte_4_cubo.ContourData = MultiValue(float, corte_4_cubo)
    pyd_corte_1_space.ContourData = MultiValue(float, corte_1_space)
    pyd_corte_2_space.ContourData = MultiValue(float, corte_2_space)
    pyd_corte_3_space.ContourData = MultiValue(float, corte_3_space)
    pyd_corte_1_punto.ContourData = MultiValue(float, corte_1_punto)
    pyd_corte_1_error.ContourData = MultiValue(float, corte_1_error)
    ds_vect_iso.ContourData = MultiValue(float, iso)

    ds_cont_struct_1 = pydicom.dataset.Dataset()
    ds_cont_struct_2 = pydicom.dataset.Dataset()
    ds_cont_struct_3 = pydicom.dataset.Dataset()
    ds_cont_struct_4 = pydicom.dataset.Dataset()
    ds_cont_struct_orig = pydicom.dataset.Dataset()
    ds_cont_struct_1.ContourSequence = [
        pyd_corte_1_cubo,
        pyd_corte_2_cubo,
        pyd_corte_3_cubo,
        pyd_corte_4_cubo,
    ]
    ds_cont_struct_2.ContourSequence = [
        pyd_corte_1_space,
        pyd_corte_2_space,
        pyd_corte_3_space,
    ]
    ds_cont_struct_3.ContourSequence = [pyd_corte_1_punto]
    ds_cont_struct_4.ContourSequence = [pyd_corte_1_error]
    ds_cont_struct_orig.ContourSequence = [ds_vect_iso]
    patient.ROIContourSequence = [
        ds_cont_struct_1,
        ds_cont_struct_2,
        ds_cont_struct_3,
        ds_cont_struct_4,
        ds_cont_struct_orig,
    ]
    return patient


@pytest.fixture()
def patient_2():
    """Method patient_2

    It creates a instance of a pydicom.dataset.Dataset().
    This instance contains the information about the structures
    and the courts. The function return the instance, that is
    used for testing the funcion add_margin of the class Dicominfo.

    Returns
    -------
    pydicom.dataset.Dataset
        Object with information about structures and courts

    """
    patient = pydicom.dataset.Dataset()
    patient.PatientName = "mario rossi"
    patient.PatientID = "3"
    patient.PatientBirthDate = "20000101"
    patient.OperatorsName = "guido rossi"
    patient.InstanceCreationDate = "20200101"
    patient.Modality = "RTSTRUCT"

    ds_seq_struct_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2 = pydicom.dataset.Dataset()
    ds_seq_struct_3 = pydicom.dataset.Dataset()
    ds_seq_struct_4 = pydicom.dataset.Dataset()
    ds_seq_struct_5 = pydicom.dataset.Dataset()
    ds_seq_struct_6 = pydicom.dataset.Dataset()
    ds_seq_struct_1.ROIName = "space1"
    ds_seq_struct_2.ROIName = "space2"
    ds_seq_struct_3.ROIName = "space3"
    ds_seq_struct_4.ROIName = "space4"
    ds_seq_struct_5.ROIName = "space5"
    ds_seq_struct_6.ROIName = "space6"
    patient.StructureSetROISequence = [
        ds_seq_struct_1,
        ds_seq_struct_2,
        ds_seq_struct_3,
        ds_seq_struct_4,
        ds_seq_struct_5,
        ds_seq_struct_6,
    ]

    pyd_corte_1_space1 = pydicom.dataset.Dataset()
    pyd_corte_1_space2 = pydicom.dataset.Dataset()
    pyd_corte_1_space3 = pydicom.dataset.Dataset()
    pyd_corte_1_space4 = pydicom.dataset.Dataset()
    pyd_corte_1_space5 = pydicom.dataset.Dataset()
    pyd_corte_1_space6 = pydicom.dataset.Dataset()
    corte_1_space1 = [0.0, 1.0, 0.0, 1.0, 0.0, 0.0]
    corte_1_space2 = [1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 3.0, 0.0, 0.0]
    corte_1_space3 = [1.0, 1.0, 0.0, 2.0, -1.0, 0.0, 3.0, 0.0, 0.0]
    corte_1_space4 = [1.0, 0.0, 0.0]
    corte_1_space5 = []
    corte_1_space6 = [1.0, 0.0, 0.0, 1.0, 2.0, 0.0]
    pyd_corte_1_space1.ContourData = MultiValue(float, corte_1_space1)
    pyd_corte_1_space2.ContourData = MultiValue(float, corte_1_space2)
    pyd_corte_1_space3.ContourData = MultiValue(float, corte_1_space3)
    pyd_corte_1_space4.ContourData = MultiValue(float, corte_1_space4)
    pyd_corte_1_space5.ContourData = MultiValue(float, corte_1_space5)
    pyd_corte_1_space6.ContourData = MultiValue(float, corte_1_space6)
    ds_cont_struct_1 = pydicom.dataset.Dataset()
    ds_cont_struct_2 = pydicom.dataset.Dataset()
    ds_cont_struct_3 = pydicom.dataset.Dataset()
    ds_cont_struct_4 = pydicom.dataset.Dataset()
    ds_cont_struct_5 = pydicom.dataset.Dataset()
    ds_cont_struct_6 = pydicom.dataset.Dataset()
    ds_cont_struct_1.ContourSequence = [pyd_corte_1_space1]
    ds_cont_struct_2.ContourSequence = [pyd_corte_1_space2]
    ds_cont_struct_3.ContourSequence = [pyd_corte_1_space3]
    ds_cont_struct_4.ContourSequence = [pyd_corte_1_space4]
    ds_cont_struct_5.ContourSequence = [pyd_corte_1_space5]
    ds_cont_struct_6.ContourSequence = [pyd_corte_1_space6]
    patient.ROIContourSequence = [
        ds_cont_struct_1,
        ds_cont_struct_2,
        ds_cont_struct_3,
        ds_cont_struct_4,
        ds_cont_struct_5,
        ds_cont_struct_6,
    ]
    return patient


@pytest.fixture()
def patient_3():
    patient_3 = pydicom.dataset.Dataset()
    patient_3.PatientName = "Mike Wazowski"
    patient_3.PatientID = "0"
    patient_3.PatientBirthDate = "20000101"
    patient_3.OperatorsName = "Mike Wazowski"
    patient_3.InstanceCreationDate = "20200101"
    patient_3.Modality = "RTPLAN"
    leaf_positions_1 = np.zeros(3)
    mlc_1 = pydicom.dataset.Dataset()
    mlc_1.LeafJawPositions = MultiValue(float, leaf_positions_1)
    control_point_1 = pydicom.dataset.Dataset()
    control_point_1.GantryAngle = ["0.0"]
    control_point_1.GantryRotationDirection = ["CW"]
    control_point_1.PatientSupportAngle = ["0.0"]
    control_point_1.BeamLimitingDevicePositionSequence = [mlc_1, mlc_1, mlc_1]
    control_point_seq = pydicom.dataset.Dataset()
    control_point_seq.ControlPointSequence = [control_point_1]
    patient_3.BeamSequence = [control_point_seq]
    return patient_3


@pytest.fixture()
def patient_4():
    patient_4 = pydicom.dataset.Dataset()
    patient_4.PatientName = "Mike Wazowski"
    patient_4.PatientID = "0"
    patient_4.PatientBirthDate = "20000101"
    patient_4.OperatorsName = "Mike Wazowski"
    patient_4.InstanceCreationDate = "20200101"
    patient_4.Modality = "RTSTRUCT"
    return patient_4


@pytest.fixture()
def patient_5():
    """
    Object patient_5

        Instance of a pydicom.dataset.Dataset().
        This instance contains the basic information
        Here, return patient_5 that is
        used for testing the funcion mlc_to_excel of
        the class Dicominfo
    """
    patient_5 = pydicom.dataset.Dataset()
    patient_5.PatientName = "Mike Wazowski"
    patient_5.PatientID = "0"
    patient_5.PatientBirthDate = "20000101"
    patient_5.OperatorsName = "Mike Wazowski"
    patient_5.InstanceCreationDate = "20200101"
    patient_5.Modality = "RTDOSE"
    return patient_5


@pytest.fixture()
def patient_6():
    """
    Object patient_6

    Instance of a pydicom.dataset.Dataset().
    This instance contains the information about BeamSequence
    Here, return patient_6 that is
    used for testing the funcion mlc_to_excel of
    the class Dicominfo
    """
    patient_6 = pydicom.dataset.Dataset()
    patient_6.PatientName = "Mike Wazowski"
    patient_6.PatientID = "0"
    patient_6.PatientBirthDate = "20000101"
    patient_6.OperatorsName = "Mike Wazowski"
    patient_6.InstanceCreationDate = "20200101"
    patient_6.Modality = "RTPLAN"
    leaf_positions_1_4 = np.zeros(3)
    mlc_1_4 = pydicom.dataset.Dataset()
    mlc_1_4.LeafJawPositions = MultiValue(float, leaf_positions_1_4)
    control_point_1_4 = pydicom.dataset.Dataset()
    control_point_1_4.GantryAngle = ["0.0"]
    control_point_1_4.GantryRotationDirection = ["CW"]
    control_point_1_4.PatientSupportAngle = ["0.0"]
    control_point_1_4.BeamLimitingDevicePositionSequence = [
        mlc_1_4,
        mlc_1_4,
        mlc_1_4,
    ]
    leaf_positions_2_4 = np.ones(3)
    mlc_2_4 = pydicom.dataset.Dataset()
    mlc_2_4.LeafJawPositions = MultiValue(float, leaf_positions_2_4)
    control_point_2_4 = pydicom.dataset.Dataset()
    control_point_2_4.GantryAngle = ["10.0"]
    control_point_2_4.GantryRotationDirection = ["CW"]
    control_point_2_4.PatientSupportAngle = ["0.0"]
    control_point_2_4.BeamLimitingDevicePositionSequence = [mlc_2_4]
    control_point_seq_4 = pydicom.dataset.Dataset()
    control_point_seq_4.ControlPointSequence = [
        control_point_1_4,
        control_point_2_4,
    ]
    patient_6.BeamSequence = [control_point_seq_4]
    return patient_6


@pytest.fixture()
def patient_7():
    """
    Object patient_7

    Instance of a pydicom.dataset.Dataset().
    This instance contains the information about BeamSequence
    Here, return patient_7 that is
    used for testing the funcion mlc_to_excel of
    the class Dicominfo
    """
    patient_7 = pydicom.dataset.Dataset()
    patient_7.PatientName = "Mike Wazowski"
    patient_7.PatientID = "0"
    patient_7.PatientBirthDate = "20000101"
    patient_7.OperatorsName = "Mike Wazowski"
    patient_7.InstanceCreationDate = "20200101"
    patient_7.Modality = "RTPLAN"
    leaf_positions_1_5 = np.zeros(3)
    mlc_1_5 = pydicom.dataset.Dataset()
    mlc_1_5.LeafJawPositions = MultiValue(float, leaf_positions_1_5)
    control_point_1_5 = pydicom.dataset.Dataset()
    control_point_1_5.GantryAngle = ["0.0"]
    control_point_1_5.GantryRotationDirection = ["CW"]
    control_point_1_5.PatientSupportAngle = ["0.0"]
    control_point_1_5.BeamLimitingDevicePositionSequence = [
        mlc_1_5,
        mlc_1_5,
        mlc_1_5,
    ]
    leaf_positions_2_5 = np.ones(3)
    mlc_2_5 = pydicom.dataset.Dataset()
    mlc_2_5.LeafJawPositions = MultiValue(float, leaf_positions_2_5)
    control_point_2_5 = pydicom.dataset.Dataset()
    control_point_2_5.GantryAngle = ["10.0"]
    control_point_2_5.GantryRotationDirection = ["CW"]
    control_point_2_5.PatientSupportAngle = ["0.0"]
    control_point_2_5.BeamLimitingDevicePositionSequence = [mlc_2_5]
    control_point_seq_5 = pydicom.dataset.Dataset()
    control_point_seq_5.ControlPointSequence = [
        control_point_1_5,
        control_point_2_5,
    ]
    patient_7.BeamSequence = [control_point_seq_5, control_point_seq_5]
    return patient_7


@pytest.fixture()
def patient_8():
    ds_origin = pydicom.dataset.Dataset()
    origin = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()
    ds_origin.ROIName = "isocenter"
    ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
    origin.ContourSequence = [ds_vect_iso]
    patient_8 = pydicom.dataset.Dataset()
    patient_8.PatientName = "Mike Wazowski"
    patient_8.PatientID = "0"
    patient_8.PatientBirthDate = "20000101"
    patient_8.OperatorsName = "Mike Wazowski"
    patient_8.InstanceCreationDate = "20200101"
    patient_8.Modality = "RTSTRUCT"
    ds_seq_struct_1_1 = pydicom.dataset.Dataset()
    ds_seq_struct_1_2 = pydicom.dataset.Dataset()
    ds_seq_struct_1_1.ROIName = "point"
    ds_seq_struct_1_2.ROIName = "cube"
    patient_8.StructureSetROISequence = [
        ds_seq_struct_1_1,
        ds_seq_struct_1_2,
        ds_origin,
    ]
    pyd_corte_1_punto = pydicom.dataset.Dataset()
    pyd_corte_1_1_cube = pydicom.dataset.Dataset()
    pyd_corte_1_2_cube = pydicom.dataset.Dataset()
    pyd_corte_1_3_cube = pydicom.dataset.Dataset()
    corte_1_1_cube = [
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        0.0,
        1.0,
        0.0,
        0.0,
    ]
    corte_1_2_cube = [
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        1.0,
    ]
    corte_1_3_cube = [
        0.0,
        0.0,
        2.0,
        0.0,
        1.0,
        2.0,
        1.0,
        1.0,
        2.0,
        1.0,
        0.0,
        2.0,
    ]
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
    patient_8.ROIContourSequence = [
        ds_cont_struct_1_1,
        ds_cont_struct_1_2,
        origin,
    ]
    return patient_8


@pytest.fixture()
def patient_9():
    ds_origin = pydicom.dataset.Dataset()
    origin = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()
    ds_origin.ROIName = "isocenter"
    ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
    origin.ContourSequence = [ds_vect_iso]
    patient_9 = pydicom.dataset.Dataset()
    patient_9.PatientName = "Mike Wazowski"
    patient_9.PatientID = "0"
    patient_9.PatientBirthDate = "20000101"
    patient_9.OperatorsName = "Mike Wazowski"
    patient_9.InstanceCreationDate = "20200101"
    patient_9.Modality = "RTSTRUCT"
    ds_seq_struct_2_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2_2 = pydicom.dataset.Dataset()
    ds_seq_struct_2_1.ROIName = "point"
    ds_seq_struct_2_2.ROIName = "cube"
    patient_9.StructureSetROISequence = [
        ds_seq_struct_2_1,
        ds_seq_struct_2_2,
        ds_origin,
    ]
    pyd_corte_2_punto = pydicom.dataset.Dataset()
    pyd_corte_2_1_cube = pydicom.dataset.Dataset()
    pyd_corte_2_2_cube = pydicom.dataset.Dataset()
    pyd_corte_2_3_cube = pydicom.dataset.Dataset()
    corte_2_1_cube = [
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        0.0,
        1.0,
        0.0,
        0.0,
    ]
    corte_2_2_cube = [
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        1.0,
    ]
    corte_2_3_cube = [
        0.0,
        0.0,
        2.0,
        0.0,
        1.0,
        2.0,
        1.0,
        1.0,
        2.0,
        1.0,
        0.0,
        2.0,
    ]
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
    patient_9.ROIContourSequence = [
        ds_cont_struct_2_1,
        ds_cont_struct_2_2,
        origin,
    ]
    return patient_9


@pytest.fixture()
def patient_10():
    ds_origin = pydicom.dataset.Dataset()
    origin = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()
    ds_origin.ROIName = "isocenter"
    ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
    origin.ContourSequence = [ds_vect_iso]
    patient_10 = pydicom.dataset.Dataset()
    patient_10.PatientName = "Mike Wazowski"
    patient_10.PatientID = "0"
    patient_10.PatientBirthDate = "20000101"
    patient_10.OperatorsName = "Mike Wazowski"
    patient_10.InstanceCreationDate = "20200101"
    patient_10.Modality = "RTSTRUCT"
    ds_seq_struct_3 = pydicom.dataset.Dataset()
    ds_seq_struct_3.ROIName = "point_wrong"
    patient_10.StructureSetROISequence = [ds_seq_struct_3, ds_origin]
    pyd_corte_3_punto = pydicom.dataset.Dataset()
    pyd_corte_3_punto.ContourData = MultiValue(float, [1.0, 1.0, 1.0])
    ds_cont_struct_3 = pydicom.dataset.Dataset()
    ds_cont_struct_3.ContourSequence = [pyd_corte_3_punto]
    patient_10.ROIContourSequence = [ds_cont_struct_3, origin]
    return patient_10


@pytest.fixture()
def patient_11():
    ds_origin = pydicom.dataset.Dataset()
    origin = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()
    ds_origin.ROIName = "isocenter"
    ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
    origin.ContourSequence = [ds_vect_iso]
    patient_11 = pydicom.dataset.Dataset()
    patient_11.PatientName = "Mike Wazowski"
    patient_11.PatientID = "0"
    patient_11.PatientBirthDate = "20000101"
    patient_11.OperatorsName = "Mike Wazowski"
    patient_11.InstanceCreationDate = "20200101"
    patient_11.Modality = "RTSTRUCT"
    ds_seq_struct_4 = pydicom.dataset.Dataset()
    ds_seq_struct_4.ROIName = "point_wrong"
    patient_11.StructureSetROISequence = [ds_seq_struct_4, ds_origin]
    pyd_corte_4_punto = pydicom.dataset.Dataset()
    pyd_corte_4_punto.ContourData = MultiValue(float, [1.0, 1.0, 1.0, 1.0])
    ds_cont_struct_4 = pydicom.dataset.Dataset()
    ds_cont_struct_4.ContourSequence = [pyd_corte_4_punto]
    patient_11.ROIContourSequence = [ds_cont_struct_4, origin]
    return patient_11


@pytest.fixture()
def patient_12():
    ds_origin = pydicom.dataset.Dataset()
    origin = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()
    ds_origin.ROIName = "isocenter"
    ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
    origin.ContourSequence = [ds_vect_iso]
    patient_12 = pydicom.dataset.Dataset()
    patient_12.PatientName = "Mike Wazowski"
    patient_12.PatientID = "0"
    patient_12.PatientBirthDate = "20000101"
    patient_12.OperatorsName = "Mike Wazowski"
    patient_12.InstanceCreationDate = "20200101"
    patient_12.Modality = "RTSTRUCT"
    ds_seq_struct_5_1 = pydicom.dataset.Dataset()
    ds_seq_struct_5_2 = pydicom.dataset.Dataset()
    ds_seq_struct_5_1.ROIName = "point"
    ds_seq_struct_5_2.ROIName = "cube"
    patient_12.StructureSetROISequence = [
        ds_seq_struct_5_1,
        ds_seq_struct_5_2,
        ds_origin,
    ]
    pyd_corte_5_punto = pydicom.dataset.Dataset()
    pyd_corte_5_1_cube = pydicom.dataset.Dataset()
    pyd_corte_5_2_cube = pydicom.dataset.Dataset()
    pyd_corte_5_3_cube = pydicom.dataset.Dataset()
    pyd_corte_5_4_cube = pydicom.dataset.Dataset()
    corte_5_1_cube = [
        0.0,
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        0.0,
        1.0,
        0.0,
        0.0,
    ]
    corte_5_2_cube = [
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        1.0,
    ]
    corte_5_3_cube = [
        0.0,
        0.0,
        2.0,
        0.0,
        1.0,
        2.0,
        1.0,
        1.0,
        2.0,
        1.0,
        0.0,
        2.0,
    ]
    corte_5_4_cube = [
        0.0,
        0.0,
        3.0,
        0.0,
        1.0,
        3.0,
        1.0,
        1.0,
        3.0,
        1.0,
        0.0,
        3.0,
    ]
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
    patient_12.ROIContourSequence = [
        ds_cont_struct_5_1,
        ds_cont_struct_5_2,
        origin,
    ]
    return patient_12


@pytest.fixture()
def patient_13():
    ds_origin = pydicom.dataset.Dataset()
    origin = pydicom.dataset.Dataset()
    ds_vect_iso = pydicom.dataset.Dataset()
    ds_origin.ROIName = "isocenter"
    ds_vect_iso.ContourData = MultiValue(float, [0.0, 0.0, 0.0])
    origin.ContourSequence = [ds_vect_iso]
    patient_13 = pydicom.dataset.Dataset()
    patient_13.PatientName = "Mike Wazowski"
    patient_13.PatientID = "0"
    patient_13.PatientBirthDate = "20000101"
    patient_13.OperatorsName = "Mike Wazowski"
    patient_13.InstanceCreationDate = "20200101"
    patient_13.Modality = "RTSTRUCT"
    ds_seq_struct_6_1 = pydicom.dataset.Dataset()
    ds_seq_struct_6_2 = pydicom.dataset.Dataset()
    ds_seq_struct_6_1.ROIName = "point"
    ds_seq_struct_6_2.ROIName = "cube"
    patient_13.StructureSetROISequence = [
        ds_seq_struct_6_1,
        ds_seq_struct_6_2,
        ds_origin,
    ]
    pyd_corte_6_punto = pydicom.dataset.Dataset()
    pyd_corte_6_1_cube = pydicom.dataset.Dataset()
    pyd_corte_6_2_cube = pydicom.dataset.Dataset()
    pyd_corte_6_3_cube = pydicom.dataset.Dataset()
    corte_6_1_cube = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0]
    corte_6_2_cube = [
        0.0,
        0.0,
        1.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        1.0,
    ]
    corte_6_3_cube = [
        0.0,
        0.0,
        2.0,
        0.0,
        1.0,
        2.0,
        1.0,
        1.0,
        2.0,
        1.0,
        0.0,
        2.0,
    ]
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
    patient_13.ROIContourSequence = [
        ds_cont_struct_6_1,
        ds_cont_struct_6_2,
        origin,
    ]
    return patient_13


@pytest.fixture()
def patient_14():
    patient_14 = pydicom.dataset.Dataset()
    patient_14.PatientName = "Mike Wazowski"
    patient_14.PatientID = "0"
    patient_14.PatientBirthDate = "20000101"
    patient_14.OperatorsName = "Mike Wazowski"
    patient_14.InstanceCreationDate = "20200101"
    patient_14.Modality = "RTSTRUCT"
    ds_seq_struct_1_1 = pydicom.dataset.Dataset()
    ds_seq_struct_1_1.ROIName = "cube"
    patient_14.StructureSetROISequence = [ds_seq_struct_1_1]
    pyd_corte_1_punto = pydicom.dataset.Dataset()
    pyd_corte_2_punto = pydicom.dataset.Dataset()
    corte_1_1_point = [
        0.0,
        0.0,
        0.0,
        1.0,
        0.0,
        0.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
        0.0,
    ]
    corte_1_2_point = [
        0.0,
        0.0,
        1.0,
        1.0,
        0.0,
        1.0,
        1.0,
        1.0,
        1.0,
        0.0,
        1.0,
        1.0,
    ]
    pyd_corte_1_punto.ContourData = MultiValue(float, corte_1_1_point)
    pyd_corte_2_punto.ContourData = MultiValue(float, corte_1_2_point)
    ds_cont_struct_1_1 = pydicom.dataset.Dataset()
    ds_cont_struct_1_1.ContourSequence = [pyd_corte_1_punto, pyd_corte_2_punto]
    patient_14.ROIContourSequence = [
        ds_cont_struct_1_1,
    ]
    return patient_14


@pytest.fixture()
def patient_15():
    patient_15 = pydicom.dataset.Dataset()
    patient_15.PatientName = "Mike Wazowski"
    patient_15.PatientID = "0"
    patient_15.PatientBirthDate = "20000101"
    patient_15.OperatorsName = "Mike Wazowski"
    patient_15.InstanceCreationDate = "20200101"
    patient_15.Modality = "RTSTRUCT"
    ds_seq_struct_2_1 = pydicom.dataset.Dataset()
    ds_seq_struct_2_1.ROIName = "point"
    ds_seq_struct_2_2 = pydicom.dataset.Dataset()
    ds_seq_struct_2_2.ROIName = "point2"
    patient_15.StructureSetROISequence = [ds_seq_struct_2_1, ds_seq_struct_2_2]
    pyd_corte_2_punto = pydicom.dataset.Dataset()
    corte_2_1_point = [1.0, 1.0, 1.0]
    pyd_corte_22_punto = pydicom.dataset.Dataset()
    corte_2_2_point = [2.0, 2.0, 2.0]
    pyd_corte_2_punto.ContourData = MultiValue(float, corte_2_1_point)
    pyd_corte_22_punto.ContourData = MultiValue(float, corte_2_2_point)
    ds_cont_struct_2_1 = pydicom.dataset.Dataset()
    ds_cont_struct_2_1.ContourSequence = [pyd_corte_2_punto]
    ds_cont_struct_2_2 = pydicom.dataset.Dataset()
    ds_cont_struct_2_2.ContourSequence = [pyd_corte_22_punto]
    patient_15.ROIContourSequence = [ds_cont_struct_2_1, ds_cont_struct_2_2]
    return patient_15


@pytest.fixture()
def d1():
    d1 = Dicominfo()
    return d1


@pytest.fixture()
def d2():
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
def d3():
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
def d4():
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
def d5():
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
def d6():
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
def d7():
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
def d8():
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
def m1():
    m1 = Mock()
    m1.PatientName = "Mike Wazowski"
    m1.PatientID = "00"
    m1.PatientBirthDate = "20000102"
    m1.OperatorsName = "Myself"
    m1.InstanceCreationDate = "20220101"
    m1.Modality = ""
    return m1


@pytest.fixture()
def m2():
    m2 = Mock()
    m2.PatientName = "Mike Wazowski"
    m2.PatientID = "00"
    m2.PatientBirthDate = "20000102"
    m2.OperatorsName = "Myself"
    m2.InstanceCreationDate = "20220101"
    m2.Modality = "RTPLAN"
    return m2


@pytest.fixture()
def m3():
    m3 = Mock()
    m3.PatientName = "Mike Wazowski"
    m3.PatientID = "00"
    m3.PatientBirthDate = "20000102"
    m3.OperatorsName = "Myself"
    m3.InstanceCreationDate = "20220101"
    m3.Modality = "RTDOSE"
    return m3


@pytest.fixture()
def m4():
    m4 = Mock()
    m4.PatientName = "Mike Wazowski"
    m4.PatientID = "00"
    m4.PatientBirthDate = "20000102"
    m4.OperatorsName = "Myself"
    m4.InstanceCreationDate = "20220101"
    m4.Modality = "RTSTRUCT"
    return m4


@pytest.fixture()
def m5():
    m5 = Mock()
    m5.PatientName = "Mike Wazowski"
    m5.PatientID = "02"
    m5.PatientBirthDate = "20000102"
    m5.OperatorsName = "Myself"
    m5.InstanceCreationDate = "20220101"
    m5.Modality = "RTDOSE"
    return m5


@pytest.fixture()
def m6():
    m6 = Mock()
    m6.PatientName = "Mike Wazowski"
    m6.PatientID = "00"
    m6.PatientBirthDate = "20000102"
    m6.OperatorsName = "Myself"
    m6.InstanceCreationDate = "20220101"
    m6.Modality = "RTDOSE"
    return m6


@pytest.fixture()
def m7():
    m7 = Mock()
    m7.PatientName = "Wazowski, Mike"
    m7.PatientID = "00"
    m7.PatientBirthDate = "20000102"
    m7.OperatorsName = "Myself"
    m7.InstanceCreationDate = "20220101"
    m7.Modality = "RTDOSE"
    return m7


@pytest.fixture()
def m8():
    m8 = Mock()
    m8.PatientName = "Wazowski, Mike"
    m8.PatientID = "00"
    m8.PatientBirthDate = "20000101"
    m8.OperatorsName = "Myself"
    m8.InstanceCreationDate = "20220101"
    m8.Modality = "RTDOSE"
    return m8
