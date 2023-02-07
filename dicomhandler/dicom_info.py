#!/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# DOCS
# =============================================================================

"""Build and handle DICOM radiotherapy files.

Python tool for integrating and processing
`DICOM <https://www.dicomstandard.org/>`_
information of radiotherapy structures.

It allows to modify the structures (expand, contract, rotate,
translate) and to obtain statistics from these modifications without
the need to use CT or MRI images and to create new DICOM files with
this information, which are compatible with the commercial of treatment
planning systems such as `Eclipse <https://www.varian.com/>`_
and `Brainlab Elements <https://www.brainlab.com/>`_.

It is possible to extract the information from the structures
in an easy *excelable* form.

.. moduleauthor:: Alejandro Rojas <alexrojas@ciencias.unam.mx>
.. moduleauthor:: Jerónimo Fontinós <jerofoti@gmail.com>
.. moduleauthor:: Nicola Maddalozzo <nicolamaddalozzo95@gmail.com>

"""

# =============================================================================
# IMPORTS
# =============================================================================


import copy
import os
import pathlib
import sys
import warnings
from collections import defaultdict

import numpy as np

import pandas as pd

from pydicom.multival import MultiValue


# =============================================================================
# DICOM INFO
# =============================================================================
class DicomInfo:
    r"""Build an object containing DICOM files.

    Allows to integrate the characteristics and properties of the
    different DICOM files, which have complementary information of
    each patient.

    .. note::
        **Important:** ``DicomInfo`` does not allow to merge information from
        different patients. Only one RS, RP and RD is accepted per patient,
        per instantiation.

    The files accepted are:
        * Structures: RS.dcm.
        * Treatment plan: RP.dcm.
        * Treatment dose: RD.dcm.

    Methods
    -------
    add_margin(struct, margin)
        Allows to expand or subtract margin for a single structure.
    anonymize(name=True, birth=True, operator=True, creation=True)
        Allows to overwrite the patient's information.
    mlc_to_csv(path_or_buff)
        Creates DICOM MLC information in *csv-able* form.
    move(struct, value, key, \*args)
        Allows to move all the points for a single structure.
    struct_to_csv(path_or_buff, names)
        Creates DICOM structure information in *csv-able* form.
    summarize_to_dataframe(self, area)
        Reports the main information of plan and MLC.

    Returns
    -------
    pydicom.dataset.FileDataset
        DicomInfo object with DICOM properties.
    pandas.core.frame.DataFrame
        DataFrame reports with specific information and metrics from
        DICOM files.

    """

    def __init__(self, *args):
        """Initialize dicominfo object.

        Initialize ``DicomInfo`` objects validating that the information
        belongs to the same patient.

        Parameters
        ----------
        args : pydicom.dataset.FileDataset
            DICOM files from a patient.

        Raises
        ------
        ValueError
            If the modality is not supported or if many files has the
            same modality.

        Examples
        --------
        >>> import pydicom
        >>> import os
        >>> # Import the class from the dicomhandler.
        >>> import dicomhandler.dicom_info as dh
        >>> # Construct the object.
        >>> file = os.listdir(os.chdir('path_of_DICOM_files'))
        >>> struct = pydicom.dcmread(file[0])
        >>> plan = pydicom.dcmread(file[1])
        >>> dicom = dh.DicomInfo(struct, plan)

        """
        self.dicom_struct = None
        self.dicom_dose = None
        self.dicom_plan = None
        self.PatientName = None
        self.PatientBirthDate = None
        self.PatientID = None
        if args:
            patient = args[0]
            temp_name = patient.PatientName
            temp_id = patient.PatientID
            temp_birthdate = patient.PatientBirthDate
            temp_modality = patient.Modality
            for files in args[1:]:
                if temp_name != files.PatientName:
                    warnings.warn(
                        "Patients Name do not match,\
                                first argument of patient name will be used"
                    )
                if temp_id != files.PatientID:
                    raise ValueError("Patient IDs do not match")
                if temp_birthdate != files.PatientBirthDate:
                    warnings.warn(
                        "Patients BirthDate do not match,\
                                first argument of birthdate will be used"
                    )
                if temp_modality == files.Modality:
                    raise ValueError("One > dicom of the same modality")
            for files in args[:]:
                if files.Modality == "RTSTRUCT":
                    self.dicom_struct = files
                elif files.Modality == "RTDOSE":
                    self.dicom_dose = files
                elif files.Modality == "RTPLAN":
                    self.dicom_plan = files
                else:
                    raise ValueError("Modality not supported")
            self.PatientName = patient.PatientName
            self.PatientBirthDate = patient.PatientBirthDate
            self.PatientID = patient.PatientID

    def anonymize(self, name=True, birth=True, operator=True, creation=True):
        """Protect the sensitive personal information from files.

        In many cases, it is important to anonymize the patient information
        for research and statistics. ``anonymize`` method allows to overwrite
        the name, birth date of the patient, the operator's name and the
        creation of the plan.

        By default, it modifies a DICOM object with the following values:
            * Patient Name: 'PatientName'
            * Patient Birth Date: '19720101'
            * Operators Name: 'OperatorName'
            * Instance Creation Date: '19720101'

        Parameters
        ----------
        name : bool, default True
            Anonymize the patient name.
        birth : bool, default True
            Anonymize the patient birth date.
        operator : bool, default True
            Anonymize the operator name.
        creation : bool, default True
            Anonymize the instance creation date.

        Returns
        -------
        pydicom.dataset.FileDataset
            Object with DICOM properties of the anonymized files.

        Examples
        --------
        >>> # Anonymize name, birthdate, operator.
        >>> # No anonymize creation date.
        >>> dicom = dicom.anonymize(creation=False)

        """
        dicom_copy = copy.deepcopy(self)
        name_dcm = "PatientName"
        birth_dcm = "19720101"
        operator_dcm = "OperatorName"
        creation_dcm = "19720101"

        empty_di = all(
            [
                self.dicom_struct is None,
                self.dicom_dose is None,
                self.dicom_plan is None,
                self.PatientName is None,
                self.PatientBirthDate is None,
                self.PatientID is None,
            ]
        )

        if empty_di:
            warnings.warn(
                "anonymize should be run after adding data to the object"
            )
            return dicom_copy

        if name:
            dicom_copy.PatientName = name_dcm
            if dicom_copy.dicom_struct is not None:
                dicom_copy.dicom_struct.PatientName = name_dcm

            if dicom_copy.dicom_plan is not None:
                dicom_copy.dicom_plan.PatientName = name_dcm

            if dicom_copy.dicom_dose is not None:
                dicom_copy.dicom_dose.PatientName = name_dcm

        if birth:
            dicom_copy.PatientBirthDate = birth_dcm
            if dicom_copy.dicom_struct is not None:
                (dicom_copy.dicom_struct.PatientBirthDate) = birth_dcm

            if dicom_copy.dicom_plan is not None:
                (dicom_copy.dicom_plan.PatientBirthDate) = birth_dcm

            if dicom_copy.dicom_dose is not None:
                (dicom_copy.dicom_dose.PatientBirthDate) = birth_dcm

        if operator:
            dicom_copy.OperatorsName = operator_dcm
            if dicom_copy.dicom_struct is not None:
                dicom_copy.dicom_struct.OperatorsName = operator_dcm

            if dicom_copy.dicom_plan is not None:
                dicom_copy.dicom_plan.OperatorsName = operator_dcm

            if dicom_copy.dicom_dose is not None:
                dicom_copy.dicom_dose.OperatorsName = operator_dcm

        if creation:
            dicom_copy.InstanceCreationDate = creation_dcm
            if dicom_copy.dicom_struct is not None:
                (dicom_copy.dicom_struct.InstanceCreationDate) = creation_dcm

            if dicom_copy.dicom_plan is not None:
                (dicom_copy.dicom_plan.InstanceCreationDate) = creation_dcm

            if dicom_copy.dicom_dose is not None:
                (dicom_copy.dicom_dose.InstanceCreationDate) = creation_dcm

        return dicom_copy

    def struct_to_csv(self, path_or_buff=None, names=None):
        """Create an csv file with the information of the structure file.

        The information of the Cartesian coordinates (relative positions)
        for all or some structures is extracted in an .csv file
        for pos-processing. The file can be created in any path or by buffer.

        .. note::
            **Important:** For all structures, it could be a slow process
            to take couple of minutes. The structure BODY or OUTER CONTOUR
            contains a lot of points.

        Parameters
        ----------
        path_or_buff : str, pathlib.Path or StringIO, default=None
            Path or buffer to write the information from a dataframe.
        names : list, default=None
            List of strings, with the name of the structures to create
            the csv file. By default all structures.

        Returns
        -------
        csv file
            csv file with the coordinates of the selected structures.

        Raises
        ------
        ValueError
            If the name of the structures are not in the files.
            If the file has not a name.
            If the file has not a .csv o .txt extension.

        References
        ----------
            :cite:p:`calvo2022montecarlo`

        Examples
        --------
        >>> # Extract the coordinates of the structures Eye Right,
        >>> # using path
        >>> dicom.struct_to_csv(path_or_buff='output.csv', ['Eye Right'])
        >>> # using buffer
        >>> dicom.struct_to_csv(path_or_buff=StringIO(), ['Eye Right'])
        >>> # Extract the coordinates of the all structures.
        >>> dicom.struct_to_csv(path_or_buff='output.csv')
        """
        dicom_copy = copy.deepcopy(self)
        if not dicom_copy.dicom_struct:
            raise ValueError("Structure file not loaded")
        elif isinstance(path_or_buff, str):
            name_file = path_or_buff.split("/")[-1].split(".")[0]
            exten = path_or_buff.split("/")[-1].split(".")[1]
            if name_file == "":
                raise ValueError("Enter the file name")
            elif exten not in ["csv", "txt"]:
                raise ValueError(
                    f"The file must have a .csv or .txt extension, \
                     not .{exten}"
                )
        elif isinstance(path_or_buff, pathlib.Path):
            name_file = (
                os.path.splitext(path_or_buff)[0].split("/")[-1].split(".")[0]
            )
            exten = os.path.splitext(path_or_buff)[-1]
            if name_file == "":
                raise ValueError("Enter the file name")
            elif exten not in [".csv", ".txt"]:
                raise ValueError(
                    f"The file must have a .csv or .txt \
                extension, not {exten}"
                )
        names = [] if names is None else names
        names_aux, names_all = {}, {}
        df = []
        for item, value in enumerate(
            dicom_copy.dicom_struct.StructureSetROISequence
        ):
            names_aux[value.ROIName] = item
        if len(names) != 0:
            for name in names:
                if name in names_aux.keys():
                    names_all[name] = names_aux[name]
                else:
                    raise ValueError(f"{name} not founded.")
        else:
            names_all = names_aux
        for roiname in names_all:
            array = []
            for num, contour in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    names_all[roiname]
                ].ContourSequence
            ):
                x, y, z = [], [], []
                counter = 0
                while counter < int(len(contour.ContourData) / 3):
                    x.append(float(contour.ContourData[3 * counter]))
                    y.append(float(contour.ContourData[3 * counter + 1]))
                    z.append(float(contour.ContourData[3 * counter + 2]))
                    seriesx = pd.Series(x, name=f"x{num} [mm]")
                    seriesy = pd.Series(y, name=f"y{num} [mm]")
                    seriesz = pd.Series(z, name=f"z{num} [mm]")
                    counter = counter + 1
                array.append(seriesx)
                array.append(seriesy)
                array.append(seriesz)
            df.append(pd.concat(array, axis=1))
        df_all = pd.concat(df)
        try:
            if path_or_buff is None:
                buffer, close = sys.stdout, False
            elif isinstance(path_or_buff, (str, pathlib.Path)):
                buffer, close = open(path_or_buff, "w"), True
            else:
                buffer, close = path_or_buff, False
            df_all.to_csv(buffer)
        finally:
            if close and not buffer.closed:
                buffer.close()

    def mlc_to_csv(self, path_or_buff=None):
        """Create an csv file with the information of the plan file.

        The information of the multileaf collimator (MLC) positions,
        control points, gantry angles, gantry orientation and table
        angle are reported in an .csv file for pos-processing for
        numerical simulations. The file can be created in any path or by
        buffer. The information contains the principal components
        necessary for Monte Carlo simulations for radiotherapy.

        Parameters
        ----------
        path_or_buff : str, pathlib.Path or StringIO, default=None
            Path or buffer to write the information from a dataframe.

        Returns
        -------
        csv file
            csv file with MLC description.

        Raises
        ------
        ValueError
            If the plan is not loaded.
            If the file has not a name.
            If the file has not a .csv o .txt extension.


        References
        ----------
            :cite:p:`calvo2022montecarlo`

        Examples
        --------
        >>> # Extract MLC positions and checkpoints from a path.
        >>> dicom.mlc_to_csv(path_or_buff='output.csv')
        >>> # Extract MLC positions and checkpoints from a buffer.
        >>> dicom.struct_to_csv(path_or_buff=StringIO())
        """
        dicom_copy = copy.deepcopy(self)
        if not dicom_copy.dicom_plan:
            raise ValueError("Plan file not loaded")
        elif isinstance(path_or_buff, str):
            name_file = path_or_buff.split("/")[-1].split(".")[0]
            exten = path_or_buff.split("/")[-1].split(".")[1]
            if name_file == "":
                raise ValueError("Enter the file name")
            elif exten not in ["csv", "txt"]:
                raise ValueError(
                    f"The file must have a .csv or .txt extension, \
                     not .{exten}"
                )
        elif isinstance(path_or_buff, pathlib.Path):
            name_file = (
                os.path.splitext(path_or_buff)[0].split("/")[-1].split(".")[0]
            )
            exten = os.path.splitext(path_or_buff)[-1]
            if name_file == "":
                raise ValueError("Enter the file name")
            elif exten not in [".csv", ".txt"]:
                raise ValueError(
                    f"The file must have a .csv or .txt extension, not {exten}"
                )
        df = []
        for number, sequence in enumerate(dicom_copy.dicom_plan.BeamSequence):
            array = []
            for item, point in enumerate(sequence.ControlPointSequence):
                gantry_angle = point.GantryAngle
                gantry_direction = point.GantryRotationDirection
                table_direction = sequence.ControlPointSequence[
                    0
                ].PatientSupportAngle
                if item == 0:
                    mlc = np.array(
                        point.BeamLimitingDevicePositionSequence[
                            2
                        ].LeafJawPositions
                    )
                else:
                    mlc = np.array(
                        point.BeamLimitingDevicePositionSequence[
                            0
                        ].LeafJawPositions
                    )
                values = [
                    "GantryAngle",
                    gantry_angle,
                    "GantryDirection",
                    gantry_direction,
                    "TableDirection",
                    table_direction,
                    "MLC",
                ]
                for leaf in mlc:
                    values.append(leaf)
                series = pd.Series(values, name=f"CP{item}")
                array.append(series)
            df.append(pd.concat(array, axis=1))
        df_all = pd.concat(df)
        try:
            if path_or_buff is None:
                buffer, close = sys.stdout, False
            elif isinstance(path_or_buff, (str, pathlib.Path)):
                buffer, close = open(path_or_buff, "w"), True
            else:
                buffer, close = path_or_buff, False
            df_all.to_csv(buffer)
        finally:
            if close and not buffer.closed:
                buffer.close()

    def summarize_to_dataframe(self, area=False):
        """Report the main information of the radiotherapy plan.

        The information of the prescribed dose, reference points in targets,
        dose to references points, the mass centre and distance to isocenter
        for each target are summarized in a dataframe.

        Also, this method calculates the areas of multileaf collimator (MLC)
        modulation. The objective of this method is to describe the movements
        of the gantry and MLC during irradiation. The output is a dataframe
        with six columns:

            * The code of the beam.
            * The code of the checkpoint.
            * The total area that is under irradiation.
            * The gantry angle.
            * The gantry direction
            * The table angle.

        The total area is calculated as the sum of the areas defined
        between the opposite pair of leaves.

        .. note::
            It is necessary to include the plan file.

        Every beam is contains information with the same machine for a
        patient, so the number of leaves of the machine is the same for
        every beam.

        Parameters
        ----------
        areas : bool, default=False
            Areas defined the information reported. By default, the
            dataframe corresponds to general RTPlan information. If
            areas is True, the dataframe corresponds to the MLC areas.

        Returns
        -------
        pandas.core.frame.DataFrame
            Dataframe with information.

        Raises
        ------
        ValueError
            If plan dicom and struct dicom are not present.
            If the modality is not RTPlan or if the number of leaves varies
            from each checkpoint.

        TypeError
            The direction of gantry is not a string.

        Examples
        --------
        >>> # Obtain dataframe for plan information.
        >>> import pydicom
        >>> import os
        >>> # Import the class from the dicomhandler.
        >>> import dicomhandler.dicom_info as dh
        >>> # Construct the object.
        >>> file = os.listdir(os.chdir('path_of_DICOM_files'))
        >>> plan = pydicom.dcmread(file[0], force = True)
        >>> struct = pydicom.dcmread(file[1], force = True)
        >>> dicom = dh.DicomInfo(struct, plan)
        >>> # Obtain dataframe with general plan information.
        >>> dicom.summarize_to_dataframe(area = False)
        >>> # Or, to obtain dataframe with MLC areas.
        >>> dicom.summarize_to_dataframe(area = True)

        """
        dicom_copy = copy.deepcopy(self)
        if dicom_copy.dicom_plan is None:
            raise ValueError("You must load plan and structure files.")
        elif area:
            leaf_pos = (
                dicom_copy.dicom_plan.BeamSequence[0]
                .BeamLimitingDeviceSequence[2]
                .LeafPositionBoundaries
            )
            n_laminas = len(leaf_pos) - 1
            for _, item in enumerate(dicom_copy.dicom_plan.BeamSequence):
                if (
                    n_laminas
                    != len(
                        item.BeamLimitingDeviceSequence[
                            2
                        ].LeafPositionBoundaries
                    )
                    - 1
                ):
                    raise ValueError(
                        "The number of leaves is different among the beams"
                    )
            df_cols = [
                "beam",
                "checkpoint",
                "area",
                "gantry_angle",
                "gantry_direction",
                "table",
            ]
            dict_leaves = defaultdict(list)
            for pos1, pos2 in enumerate(leaf_pos[: len(leaf_pos) - 1]):
                dict_leaves[pos1 + 1].append(abs(pos2 - leaf_pos[pos1 + 1]))
            rows_df = []
            for number, sequence in enumerate(
                dicom_copy.dicom_plan.BeamSequence
            ):
                table = sequence.ControlPointSequence[0].PatientSupportAngle
                gantry_direction = sequence.ControlPointSequence[
                    0
                ].GantryRotationDirection
                if isinstance(gantry_direction, str) is False:
                    raise TypeError("Gantry direction must be a string")
                for control, gantry in enumerate(
                    sequence.ControlPointSequence
                ):
                    gantry_angle = gantry.GantryAngle
                    if control == 0:
                        mlc_positions = (
                            gantry.BeamLimitingDevicePositionSequence[
                                2
                            ].LeafJawPositions
                        )
                    else:
                        mlc_positions = (
                            gantry.BeamLimitingDevicePositionSequence[
                                0
                            ].LeafJawPositions
                        )
                    bank_a = np.array(mlc_positions[: len(mlc_positions) // 2])
                    lim1 = len(mlc_positions) // 2
                    lim2 = len(mlc_positions)
                    bank_b = np.array(mlc_positions[lim1:lim2])
                    diff = abs(bank_a - bank_b)
                    dict_leaf_prov = copy.deepcopy(dict_leaves)
                    for z, elem_diff in enumerate(diff):
                        dict_leaf_prov[z + 1].append(elem_diff)
                    areas = 0
                    for values in dict_leaf_prov.values():
                        areas += values[0] * values[1]
                    rows_df.append(
                        [
                            number + 1,
                            control + 1,
                            round(areas, 1),
                            gantry_angle,
                            gantry_direction,
                            table,
                        ]
                    )
            df = pd.DataFrame(rows_df, columns=df_cols)
        else:
            dict_plan = {}
            names_plan, dose, dose_ref, coordinates, dist2iso = (
                [],
                [],
                [],
                [],
                [],
            )
            isocenter = np.array(
                dicom_copy.dicom_plan.BeamSequence[0]
                .ControlPointSequence[0]
                .IsocenterPosition
            )
            for value, name in enumerate(
                dicom_copy.dicom_plan.DoseReferenceSequence
            ):
                if value % 2 == 0:
                    names_plan.append(name.DoseReferenceDescription)
                    dose.append(round(name.TargetPrescriptionDose, 2))
                if value % 2 == 1:
                    dose_ref.append(round(name.TargetPrescriptionDose, 2))
                    coordinates.append(name.DoseReferencePointCoordinates)
                    dist2iso.append(
                        round(
                            np.linalg.norm(
                                np.array(
                                    name.DoseReferencePointCoordinates
                                    - isocenter
                                )
                            ),
                            1,
                        )
                    )
            dict_plan["Target"] = names_plan
            dict_plan["Prescribed dose [Gy]"] = dose
            dict_plan["Reference point dose [Gy]"] = dose_ref
            dict_plan["Reference coordinates [mm]"] = coordinates
            dict_plan["Distance to iso [mm]"] = dist2iso
            df = pd.DataFrame(dict_plan)
        return df

    def move(self, struct, value, key, *args):
        r"""Moves a structure for a reference point.

        Allow to rotate and translate all the points for a single
        structure.

        The transformations are defined at the origin.
        For that reason it is necessary to bring the coordinates
        to the origin before rotating. You can
        `rotate <https://simple.wikipedia.org/wiki/Pitch,_yaw,_and_roll>`_
        an arbritrary structure (organ at risk, lesion or support
        structure) in any of the 3 degrees of freedom: roll, pitch, or yaw
        with the angle (in degrees) or translate (in mm) in x, y or z axis
        of your choice.

        .. note::
            **Additional advantage:** You can accumulate rotations
            and traslations to study any combination.

        Parameters
        ----------
        struct : str
            Name of the structure to rotate.
        value : float or int
            Value could be positive or negative.
            For rotation, maximum angle allowed 360º.
            For translation, maximum shift allowed 1000 mm.
        key : str
            Direction of rotation ('roll', 'pitch' or 'yaw').
            Direction of translation ('x', 'y' or 'z').
        \*args : list, optional
            Origin in a list of float elements [x, y, z].
            By default, it is considered the isocenter of the
            structure file (last structure in RS DICOM called Coord 1).
            If not is able this structure, you can add an
            arbritrarly point.

        Returns
        -------
        pydicom.dataset.FileDataset
            Object with DICOM properties of the moved structure.

        Raises
        ------
        TypeError
            If the angle is not float or int.
        ValueError
            If you select an incorrect rotation key, incorrect name
            or if you type an origin point with no float.

        References
        ----------
            :cite:p:`rojas2021rot`
            :cite:p:`venencia2022rot`

        Examples
        --------
        >>> # rotate tumor 1.0 degree in yaw in isocenter.
        >>> moved = dicom.move('1 GTV', 1.0, 'yaw')
        >>> # rotate lesion 1.0 degree in roll in [0.0, 0.0, 0.0].
        >>> iso = [0.0, 0.0, 0.0]
        >>> dicom.move('1 GTV', 1.0, 'yaw', iso)
        >>> # translate tumor 1.0 mm in x in isocenter.
        >>> moved = dicom.move('1 GTV', 1.0, 'x')

        """
        dicom_copy = copy.deepcopy(self)
        if not dicom_copy.dicom_struct:
            raise ValueError("Structure file must be loaded")
        elif not isinstance(value, (int, float)):
            raise TypeError("The value of the movement must be float or int")
        elif (key in ["roll", "pitch", "yaw"]) and (abs(value) < 360):
            delta = np.radians(value)
        elif (key in ["x", "y", "z"]) and (abs(value) < 1000):
            delta = value
        else:
            raise ValueError("Choose a correct key or a valid value")

        names_all = {}
        length = len(dicom_copy.dicom_struct.StructureSetROISequence)
        for item, value in enumerate(
            dicom_copy.dicom_struct.StructureSetROISequence
        ):
            names_all[value.ROIName] = item
        if struct in names_all.keys():
            if not args:
                origin = (
                    dicom_copy.dicom_struct.ROIContourSequence[length - 1]
                    .ContourSequence[0]
                    .ContourData
                )
            elif len(args[0]) == 3 and all(
                isinstance(x, float) for x in args[0]
            ):
                origin = args[0]
            else:
                raise ValueError("Type an origin [x,y,z] with float elements")
            m = {
                "roll": np.array(
                    [
                        [1, 0, 0, 0],
                        [0, np.cos(delta), -np.sin(delta), 0],
                        [0, np.sin(delta), np.cos(delta), 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "pitch": np.array(
                    [
                        [np.cos(delta), 0, np.sin(delta), 0],
                        [0, 1, 0, 0],
                        [-np.sin(delta), 0, np.cos(delta), 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "yaw": np.array(
                    [
                        [np.cos(delta), -np.sin(delta), 0, 0],
                        [np.sin(delta), np.cos(delta), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "x": np.array(
                    [
                        [1, 0, 0, delta],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "y": np.array(
                    [
                        [1, 0, 0, 0],
                        [0, 1, 0, delta],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "z": np.array(
                    [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, delta],
                        [0, 0, 0, 1],
                    ]
                ),
                "point2iso": np.array(
                    [
                        [1, 0, 0, -origin[0]],
                        [0, 1, 0, -origin[1]],
                        [0, 0, 1, -origin[2]],
                        [0, 0, 0, 1],
                    ]
                ),
                "iso2point": np.array(
                    [
                        [1, 0, 0, origin[0]],
                        [0, 1, 0, origin[1]],
                        [0, 0, 1, origin[2]],
                        [0, 0, 0, 1],
                    ]
                ),
            }
            for _, contour in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    names_all[struct]
                ].ContourSequence
            ):
                if len(contour.ContourData) % 3 != 0:
                    raise ValueError(
                        "One slice does not have all points of 3 elements"
                    )
                contour_rotated = []
                counter = 0
                while counter < int(len(contour.ContourData) / 3):
                    rotation = (
                        m["iso2point"]
                        @ m[key]
                        @ m["point2iso"]
                        @ [
                            float(contour.ContourData[3 * counter]),
                            float(contour.ContourData[3 * counter + 1]),
                            float(contour.ContourData[3 * counter + 2]),
                            1.0,
                        ]
                    )
                    contour_rotated.append(rotation[0])
                    contour_rotated.append(rotation[1])
                    contour_rotated.append(rotation[2])
                    counter = counter + 1
                contour.ContourData = MultiValue(float, contour_rotated)
        else:
            raise ValueError("Type a correct name")
        return dicom_copy

    def add_margin(self, struct, margin):
        r"""Expand or contract a structure a specified margin.

        Allow to expand or subtract margins for a single structure.

        The margin is calculated by the distance between the
        mean centre :math:`(x_{mean}, y_{mean}, z_{mean})` for each
        point :math:`(x_0, y_0, z_0)` of each its slice plus (minus)
        the desired amount to add (subtract) margins.

        The calculation is performed by solving the parametrized equation
        for the point :math:`(x, y, z)` along the normal vector to the
        tangent plane to the surface of the contour at point
        :math:`(x_0, y_0, z_0)`.

        This parametrized equation is
        :math:`t = \pm \frac{margin}{2*distance}`,
        where :math:`distance` is the Euclidean distance between
        :math:`(x_0, y_0, z_0)` and :math:`(x_{mean}, y_{mean}, z_{mean})`.

        Thus,
            * :math:`x = 2(x_0-x_{mean})t + x_0`.
            * :math:`y = 2(y_0-y_{mean})t + y_0`.
            * :math:`z = 2(z_0-z_{mean})t + z_0`.


        Parameters
        ----------
        struct : str
            Name of the structure to modify the margin.
        margin : float
            The expansion (positive) or substraction
            (negative) in mm.

        Returns
        -------
        pydicom.dataset.FileDataset
            Object with DICOM properties of the structure.

        Raises
        ------
        TypeError
            If the margin is not float.
        ValueError
            If the contour is empty or if its name is
            not founded.

        References
        ----------
            :cite:p:`enwiki:1`
            :cite:p:`beltran2012dosimetry`
            :cite:p:`liu2016gating`
            :cite:p:`zhang2016margin`

        Examples
        --------
        >>> # Add 0.7 mm to the tumor.
        >>> dicom.add_margin('1 GTV', 0.7)
        >>> # Subtract 1.2 mm to the tumor.
        >>> dicom.add_margin('1 GTV', -1.2)

        """
        dicom_copy = copy.deepcopy(self)
        if isinstance(margin, float) is False:
            raise TypeError(f"{margin} must be float")
        for item, name in enumerate(
            dicom_copy.dicom_struct.StructureSetROISequence
        ):
            if struct in name.ROIName:
                array = []
                for items, data in enumerate(
                    dicom_copy.dicom_struct.ROIContourSequence[
                        item
                    ].ContourSequence
                ):
                    if int(len(data.ContourData) / 3) < 1:
                        raise ValueError("Contour needs at least 1 point")
                    else:
                        count = 0
                        while count < int(len(data.ContourData) / 3):
                            array.append(
                                [
                                    float(data.ContourData[3 * count]),
                                    float(data.ContourData[3 * count + 1]),
                                    float(data.ContourData[3 * count + 2]),
                                ]
                            )
                            count = count + 1
                centermass = np.mean(array, axis=0)
                for items, data in enumerate(
                    dicom_copy.dicom_struct.ROIContourSequence[
                        item
                    ].ContourSequence
                ):
                    count = 0
                    contourmargin = []
                    if len(data.ContourData) == 3 and margin > 0:
                        contourmargin = [
                            data.ContourData[0],
                            data.ContourData[1] + margin,
                            data.ContourData[2],
                            data.ContourData[0] + margin,
                            data.ContourData[1],
                            data.ContourData[2],
                            data.ContourData[0],
                            data.ContourData[1] - margin,
                            data.ContourData[2],
                            data.ContourData[0] - margin,
                            data.ContourData[1],
                            data.ContourData[2],
                        ]
                    elif len(data.ContourData) == 3 and margin <= 0:
                        contourmargin = data.ContourData
                    else:
                        while count < int(len(data.ContourData) / 3):
                            vector = [
                                float(data.ContourData[3 * count]),
                                float(data.ContourData[3 * count + 1]),
                                float(data.ContourData[3 * count + 2]),
                            ]
                            parameter = np.linalg.norm(
                                np.array(vector - centermass)
                            )
                            if parameter != 0.0:
                                counter = 0
                                distances, solutions = [], []
                                while counter < 2:
                                    if counter == 0:
                                        sol = margin / (2 * (parameter))
                                    else:
                                        sol = -margin / (2 * (parameter))
                                    solution = []
                                    for value, _ in enumerate(centermass):
                                        solution.append(
                                            round(
                                                2
                                                * (
                                                    centermass[value]
                                                    - vector[value]
                                                )
                                                * sol
                                                + vector[value],
                                                2,
                                            )
                                        )
                                    distance = np.linalg.norm(
                                        np.array(solution - centermass)
                                    )
                                    solutions.append(solution)
                                    distances.append(distance)
                                    counter = counter + 1
                                if (
                                    margin >= 0
                                    and distances[0] >= distances[1]
                                ) or (
                                    margin < 0 and distances[0] < distances[1]
                                ):
                                    contourmargin.append(solutions[0][0])
                                    contourmargin.append(solutions[0][1])
                                    contourmargin.append(solutions[0][2])
                                elif (
                                    (
                                        margin >= 0
                                        and distances[0] < distances[1]
                                    )
                                    or margin < 0
                                    and distances[0] > distances[1]
                                ):
                                    contourmargin.append(solutions[1][0])
                                    contourmargin.append(solutions[1][1])
                                    contourmargin.append(solutions[1][2])
                            else:
                                contourmargin.append(vector[0])
                                contourmargin.append(vector[1])
                                contourmargin.append(vector[2])
                            count = count + 1
                    (
                        dicom_copy.dicom_struct.ROIContourSequence[item]
                        .ContourSequence[items]
                        .ContourData
                    ) = MultiValue(float, contourmargin)
        return dicom_copy
