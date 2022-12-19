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
import warnings
from collections import defaultdict
from io import BytesIO

import numpy as np

import pandas as pd

from pydicom.multival import MultiValue


# =============================================================================
# DICOM INFO
# =============================================================================
class Dicominfo:
    r"""Build an object containing DICOM files.

    Allows to integrate the characteristics and properties of the
    different DICOM files, which have complementary information of
    each patient.

    .. note::
        **Important:** ``Dicominfo`` does not allow to merge information from
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
    areas_to_dataframe(self)
        Determines areas from fields defined by multileaf collimator.
    info_to_dataframe(self, targets=[])
        Reports the main information of plan and target structures.
    mlc_to_excel(name_file)
        Creates DICOM plan information in *excelable* form.
    rotate(struct, angle, key, \*args)
        Allows to rotate all the points for a single structure.
    structure_to_excel(name_file, names=[])
        Creates DICOM contour in *excelable* form.
    translate(struct, delta, key, \*args)
        Allows to translate all the points for a single structure.

    Returns
    -------
    pydicom.dataset.FileDataset
        Dicominfo object with DICOM properties.
    pandas.core.frame.DataFrame
        DataFrame reports with specific information and metrics from
        DICOM files.

    """

    def __init__(self, *args):
        """Initialize dicominfo object.

        Initialize ``dicominfo`` objects validating that the information
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
        >>> dicom = dh.Dicom_info(struct, plan)

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
                    raise ValueError("Patient ID's do not match")
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
            dicom_copy.PatientName = "PatientName"
            if dicom_copy.dicom_struct is not None:
                dicom_copy.dicom_struct.PatientName = "PatientName"

            if dicom_copy.dicom_plan is not None:
                dicom_copy.dicom_plan.PatientName = "PatientName"

            if dicom_copy.dicom_dose is not None:
                dicom_copy.dicom_dose.PatientName = "PatientName"

        if birth:
            dicom_copy.PatientBirthDate = "19720101"
            if dicom_copy.dicom_struct is not None:
                (dicom_copy.dicom_struct.PatientBirthDate) = "19720101"

            if dicom_copy.dicom_plan is not None:
                (dicom_copy.dicom_plan.PatientBirthDate) = "19720101"

            if dicom_copy.dicom_dose is not None:
                (dicom_copy.dicom_dose.PatientBirthDate) = "19720101"

        if operator:
            dicom_copy.OperatorsName = "OperatorName"
            if dicom_copy.dicom_struct is not None:
                dicom_copy.dicom_struct.OperatorsName = "OperatorName"

            if dicom_copy.dicom_plan is not None:
                dicom_copy.dicom_plan.OperatorsName = "OperatorName"

            if dicom_copy.dicom_dose is not None:
                dicom_copy.dicom_dose.OperatorsName = "OperatorName"

        if creation:
            dicom_copy.InstanceCreationDate = "19720101"
            if dicom_copy.dicom_struct is not None:
                (dicom_copy.dicom_struct.InstanceCreationDate) = "19720101"

            if dicom_copy.dicom_plan is not None:
                (dicom_copy.dicom_plan.InstanceCreationDate) = "19720101"

            if dicom_copy.dicom_dose is not None:
                (dicom_copy.dicom_dose.InstanceCreationDate) = "19720101"

        return dicom_copy

    def structure_to_excel(self, name_file, names=[]):
        """Create an excel file with the information of the structures.

        The information of the Cartesian coordinates (relative positions)
        for all or some structures is extracted in an .xlsx file
        for pos-processing.

        It creates DICOM contours in *excelable* form.

        The ContourData for each organ is set on different sheets.
        The file is created in the same directory with the
        name name_file.xlsx.

        .. note::
            **Important:** For all structures, it could be a slow process
            to take couple of minutes. The structure BODY or OUTER CONTOUR
            contains a lot of points.

        Parameters
        ----------
        name_file : str
            Name of the output file.
        names : list, default=[]
            List of str, with the name of the structures to create the
            excel file. By default all structures.

        Returns
        -------
        pandas.io.excel._xlsxwriter.XlsxWriter
            Excel file with the coordinates of the selected structures.

        Raises
        ------
        ValueError
            If the name of the structures are not in the files.

        Examples
        --------
        >>> # Extract the coordinates of the structures 1 GTV and Eye Right.
        >>> dicom.structure_to_excel('output', ['1 GTV', 'Eye Right'])
        >>> # Extract the coordinates of the all structures.
        >>> dicom.structure_to_excel('output', [])

        """
        dicom_copy = copy.deepcopy(self)
        extension = ".xlsx"
        name_file = name_file + extension
        names_aux, n_all = {}, {}
        for item, _ in enumerate(
            dicom_copy.dicom_struct.StructureSetROISequence
        ):
            names_aux[
                (dicom_copy.dicom_struct.StructureSetROISequence[item].ROIName)
            ] = item
        if len(names) == 0:
            n_all = names_aux
        else:
            for name in names:
                if name in names_aux.keys():
                    n_all[name] = names_aux[name]
                else:
                    raise ValueError(f"{name} not founded.")
        with pd.ExcelWriter(name_file) as writer:
            for name in n_all:
                array = []
                for num, _ in enumerate(
                    dicom_copy.dicom_struct.ROIContourSequence[
                        n_all[name]
                    ].ContourSequence
                ):
                    count = 0
                    x_values, y_values, z_values = [], [], []
                    while count < int(
                        len(
                            dicom_copy.dicom_struct.ROIContourSequence[
                                n_all[name]
                            ]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    ):
                        x_values.append(
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_all[name]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * count]
                            )
                        )
                        y_values.append(
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_all[name]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * count + 1]
                            )
                        )
                        z_values.append(
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_all[name]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * count + 2]
                            )
                        )
                        seriesx = pd.Series(x_values, name=f"x{num} [mm]")
                        seriesy = pd.Series(y_values, name=f"y{num} [mm]")
                        seriesz = pd.Series(z_values, name=f"z{num} [mm]")
                        count = count + 1
                    array.append(seriesx)
                    array.append(seriesy)
                    array.append(seriesz)
                df = pd.concat(array, axis=1)
                buffer = BytesIO()
                df.to_excel(buffer)
                buffer.getvalue()
                buffer.seek(0)
                df.to_excel(writer, sheet_name=name)
            buffer.close()

    def mlc_to_excel(self, name_file):
        """Create an excel file with the MLC information.

        The information of the multileaf collimator (MLC) positions,
        control points, gantry angles, gantry orientation and table
        angle are reported in an .xlsx file for pos-processing for
        numerical simulations.

        The data for each beam is set on different sheets.

        The file is created at the same directory with the
        name name_file.xlsx. The information contains the principal
        components necessary for Monte Carlo simulations for radiotherapy.

        Parameters
        ----------
        name_file : str
            Name of the output file.

        Returns
        -------
        pandas.io.excel._xlsxwriter.XlsxWriter
            Excel file.

        Raises
        ------
        ValueError
            If the plan file is not loaded.

        References
        ----------
            :cite:p:`calvo2022montecarlo`

        Examples
        --------
        >>> # Extract the MLC relative positions and checkpoints.
        >>> dicom.mlc_to_excel('outputfile')

        """
        dicom_copy = copy.deepcopy(self)
        extension = ".xlsx"
        name_file = name_file + extension
        if dicom_copy.dicom_plan is None:
            raise ValueError("Plan not loaded")
        with pd.ExcelWriter(name_file) as writer:
            for number, _ in enumerate(dicom_copy.dicom_plan.BeamSequence):
                array = []
                for controlpoint, _ in enumerate(
                    dicom_copy.dicom_plan.BeamSequence[
                        number
                    ].ControlPointSequence
                ):
                    gantry_angle = (
                        dicom_copy.dicom_plan.BeamSequence[number]
                        .ControlPointSequence[controlpoint]
                        .GantryAngle
                    )
                    gantry_direction = (
                        dicom_copy.dicom_plan.BeamSequence[number]
                        .ControlPointSequence[controlpoint]
                        .GantryRotationDirection
                    )
                    table_direction = (
                        dicom_copy.dicom_plan.BeamSequence[number]
                        .ControlPointSequence[0]
                        .PatientSupportAngle
                    )
                    if controlpoint == 0:
                        mlc = np.array(
                            dicom_copy.dicom_plan.BeamSequence[number]
                            .ControlPointSequence[controlpoint]
                            .BeamLimitingDevicePositionSequence[2]
                            .LeafJawPositions
                        )
                    else:
                        mlc = list(
                            np.array(
                                dicom_copy.dicom_plan.BeamSequence[number]
                                .ControlPointSequence[controlpoint]
                                .BeamLimitingDevicePositionSequence[0]
                                .LeafJawPositions
                            )
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
                    series = pd.Series(
                        values, name=f"ControlPoint{controlpoint}"
                    )
                    array.append(series)
                df = pd.concat(array, axis=1)
                buffer = BytesIO()
                df.to_excel(buffer)
                buffer.getvalue()
                buffer.seek(0)
                df.to_excel(writer, sheet_name=f"Beam {number}")
            buffer.close()

    def areas_to_dataframe(self):
        """Calculate the areas of multileaf collimator (MLC) modulation.

        The objective of this function is to describe the movements
        of the gantry and MLC during irradiation.

        The output of this function is a pandas dataframe with
        six columns:

            * The code of the beam.
            * The code of the checkpoint.
            * The total area that is under irradiation.
            * The gantry angle.
            * The gantry direction
            * The table angle.

        The total area is calculated as the sum of the areas defined
        between the opposite pair of leaves.

        .. note::
            It is necessary to include at least the plan file.

        Every beam is contains information with the same machine for a patient,
        so the number of leaves of the linear accelerator is the same for
        every beam.

        Returns
        -------
        pandas.core.frame.DataFrame
            Dataframe with information from DICOM plan.

        Raises
        ------
        ValueError
            If the modality is not RTPlan or if the number of
            leaves varies from each checkpoint.
        TypeError
            The direction of gantry is not a string.

        Examples
        --------
        >>> # Obtain dataframe.
        >>> import pydicom
        >>> import os
        >>> # Import the class from the dicomhandler.
        >>> import dicomhandler.dicom_info as dh
        >>> # Construct the object.
        >>> file = os.listdir(os.chdir('path_of_DICOM_plan'))
        >>> plan = pydicom.dcmread(file[0], force = True)
        >>> dicom = dh.Dicom_info(plan)
        >>> # Call method areas_to_dataframe.
        >>> dicom.areas_to_dataframe()

        """
        dicom_copy = copy.deepcopy(self)
        if dicom_copy.dicom_plan is None:
            raise ValueError("Plan not loaded")
        n_laminas = (
            len(
                dicom_copy.dicom_plan.BeamSequence[0]
                .BeamLimitingDeviceSequence[2]
                .LeafPositionBoundaries
            )
            - 1
        )
        for sequences, _ in enumerate(dicom_copy.dicom_plan.BeamSequence):

            if (
                n_laminas
                != len(
                    dicom_copy.dicom_plan.BeamSequence[sequences]
                    .BeamLimitingDeviceSequence[2]
                    .LeafPositionBoundaries
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
        dict_laminas = defaultdict(list)
        leaf_pos = (
            dicom_copy.dicom_plan.BeamSequence[0]
            .BeamLimitingDeviceSequence[2]
            .LeafPositionBoundaries
        )
        for pos1, pos2 in enumerate(leaf_pos[: len(leaf_pos) - 1]):
            dict_laminas[pos1 + 1].append(abs(pos2 - leaf_pos[pos1 + 1]))
        rows_df = []
        for secuencia, _ in enumerate(dicom_copy.dicom_plan.BeamSequence):
            table = (
                dicom_copy.dicom_plan.BeamSequence[secuencia]
                .ControlPointSequence[0]
                .PatientSupportAngle
            )
            gantry_direction = (
                dicom_copy.dicom_plan.BeamSequence[secuencia]
                .ControlPointSequence[0]
                .GantryRotationDirection
            )
            if isinstance(gantry_direction, str) is False:
                raise TypeError("gantry_direction must be a string")
            for control, _ in enumerate(
                dicom_copy.dicom_plan.BeamSequence[
                    secuencia
                ].ControlPointSequence
            ):
                gantry_angle = (
                    dicom_copy.dicom_plan.BeamSequence[secuencia]
                    .ControlPointSequence[control]
                    .GantryAngle
                )
                if control == 0:
                    mlc_positions = (
                        dicom_copy.dicom_plan.BeamSequence[secuencia]
                        .ControlPointSequence[control]
                        .BeamLimitingDevicePositionSequence[2]
                        .LeafJawPositions
                    )
                else:
                    mlc_positions = (
                        dicom_copy.dicom_plan.BeamSequence[secuencia]
                        .ControlPointSequence[control]
                        .BeamLimitingDevicePositionSequence[0]
                        .LeafJawPositions
                    )
                bank_a = np.array(mlc_positions[: len(mlc_positions) // 2])
                lim1 = len(mlc_positions) // 2
                lim2 = len(mlc_positions)
                bank_b = np.array(mlc_positions[lim1:lim2])
                diff = abs(bank_a - bank_b)
                dict_lamina_prov = copy.deepcopy(dict_laminas)
                for z, elem_diff in enumerate(diff):
                    dict_lamina_prov[z + 1].append(elem_diff)
                area = 0
                for values in dict_lamina_prov.values():
                    area += values[0] * values[1]
                rows_df.append(
                    [
                        secuencia + 1,
                        control + 1,
                        round(area, 4),
                        gantry_angle,
                        gantry_direction,
                        table,
                    ]
                )
        df = pd.DataFrame(rows_df, columns=df_cols)
        return df

    def info_to_dataframe(self, targets=[]):
        """Report the main information of the radiotherapy plan.

        The information of the prescribed dose, reference points in targets,
        dose to references points, maximum, minimun and mean radius and
        the center of mass and distance to isocenter for each target
        are summarized in a dataframe.

        The information is reported for all targets in the DICOM plan.
        It is necessary to include at least the structure and plan files.
        Names targets must match. If not, add manually as the examples.
        Please verify that names are in concordance from both files or
        very similar.

        Parameters
        ----------
        targets : list, default = []
            List of names targets. By default, the empty list includes all
            the structures.

        Returns
        -------
        pandas.core.frame.DataFrame
            Dataframe with information from DICOM files.

        Raises
        ------
        ValueError
            If plan dicom and struct dicom are not present, raises ValueError.
            If targets is not a empty list, `len(targets)` have to be igual a
            `len(names_p)`, where `names_p` are the names in the plan.
            The names in targets have to be equal or very similar to
            the names in targets.

        Warns
        -----
        Warning
            If target is an empty list, then it will contain the names in
            the plan, but it is not guaranteed that every element in plan
            has a corresponding element in structures.

        Examples
        --------
        >>> # Obtain dataframe with the names matched.
        >>> import pydicom
        >>> import os
        >>> # import the class from the dicomhandler.
        >>> import dicomhandler.dicom_info as dh
        >>> # construct the object.
        >>> file = os.listdir(os.chdir('path_of_DICOM_files'))
        >>> plan = pydicom.dcmread(file[0], force = True)
        >>> struct = pydicom.dcmread(file[1], force = True)
        >>> dicom = dh.Dicom_info(struct, plan)
        >>> # Call method info_to_dataframe
        >>> dicom.info_to_dataframe()
        >>> # Obtain dataframe with the names missmatched.
        >>> targets = ['1 GTV +2.0 mm',
        ...            '2 GTV +2.0 mm',
        ...            '3 PTV +1.0 mm',
        ...            '4 PTV +1.0 mm',
        ...            '5 PTV +1.0 mm']
        >>> dicom.info_to_dataframe(targets)

        """
        counter = 0
        dictionary_p = {}
        dictionary_s = {}
        names_p, names_s, dose, dose_ref, coordinates = [], [], [], [], []
        dist2iso, dist2iso_struct, radius_contour, centermass = [], [], [], []
        radiusmax, radiusmin, radiusmean = [], [], []
        n_id = {}
        dicom_copy = copy.deepcopy(self)
        df_plan_struct = pd.DataFrame()
        if (dicom_copy.dicom_plan is None) or (
            dicom_copy.dicom_struct is None
        ):
            raise ValueError("You must load plan and structure files.")
        isocenter_plan = np.array(
            dicom_copy.dicom_plan.BeamSequence[0]
            .ControlPointSequence[0]
            .IsocenterPosition
        )
        while counter < len(dicom_copy.dicom_plan.DoseReferenceSequence) / 2:
            names_p.append(
                dicom_copy.dicom_plan.DoseReferenceSequence[
                    counter * 2
                ].DoseReferenceDescription
            )
            dose.append(
                round(
                    dicom_copy.dicom_plan.DoseReferenceSequence[
                        counter * 2
                    ].TargetPrescriptionDose,
                    2,
                )
            )
            dose_ref.append(
                round(
                    dicom_copy.dicom_plan.DoseReferenceSequence[
                        counter * 2 + 1
                    ].TargetPrescriptionDose,
                    2,
                )
            )
            coordinates.append(
                dicom_copy.dicom_plan.DoseReferenceSequence[
                    counter * 2 + 1
                ].DoseReferencePointCoordinates
            )
            dist2iso.append(
                round(
                    np.linalg.norm(
                        np.array(
                            dicom_copy.dicom_plan.DoseReferenceSequence[
                                counter * 2 + 1
                            ].DoseReferencePointCoordinates
                            - isocenter_plan
                        )
                    ),
                    1,
                )
            )
            counter = counter + 1
        for sequence1, _ in enumerate(
            dicom_copy.dicom_struct.StructureSetROISequence
        ):
            n_id[
                (
                    dicom_copy.dicom_struct.StructureSetROISequence[
                        sequence1
                    ].ROIName
                )
            ] = sequence1
            names_s.append(
                dicom_copy.dicom_struct.StructureSetROISequence[
                    sequence1
                ].ROIName
            )
        if len(targets) == 0:
            targets = names_p
            warnings.warn(
                "It is not guaranteed that for each element in the \
                pydicom struct\
                there is the corresponding element in the pydicom plan"
            )
        elif len(targets) != len(names_p):
            raise ValueError(f"Length of target names must be {len(names_p)}.")
        else:
            for value1, target in enumerate(targets):
                nombres = names_p[value1][:4]
                if target.startswith(nombres) is False:
                    raise ValueError(
                        f"{names_p} has not a structure named {target}. \
                        Verify names of the target structures."
                    )
        targets = list(set(names_s).intersection(targets))
        for name in targets:
            mean_values1 = []
            for num, _ in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    n_id[name]
                ].ContourSequence
            ):
                counter1 = 0
                xmean1, ymean1, zmean1 = [], [], []
                while counter1 < int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[name]]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                ):
                    xmean1.append(
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[name]]
                        .ContourSequence[num]
                        .ContourData[3 * counter1]
                    )
                    ymean1.append(
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[name]]
                        .ContourSequence[num]
                        .ContourData[3 * counter1 + 1]
                    )
                    zmean1.append(
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[name]]
                        .ContourSequence[num]
                        .ContourData[3 * counter1 + 2]
                    )
                    counter1 = counter1 + 1
                xmean1 = np.mean(xmean1)
                ymean1 = np.mean(ymean1)
                zmean1 = np.mean(zmean1)
                mean_values1.append([xmean1, ymean1, zmean1])
            centermass1 = np.mean(mean_values1, axis=0)
            for num, _ in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    n_id[name]
                ].ContourSequence
            ):
                counter2 = 0
                while counter2 < int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[name]]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                ):
                    basepoint = np.array(
                        [
                            (
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[name]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter2]
                            ),
                            (
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[name]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter2 + 1]
                            ),
                            (
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[name]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter2 + 2]
                            ),
                        ]
                    )
                    radius_contour.append(
                        round(
                            np.linalg.norm(
                                np.array((basepoint - centermass1))
                            ),
                            2,
                        )
                    )
                    counter2 = counter2 + 1
            for value, _ in enumerate(centermass1):
                centermass1[value] = round(centermass1[value], 3)
            centermass.append(centermass1)
            radiusmax.append(round(np.max(radius_contour), 2))
            radiusmin.append(round(np.min(radius_contour), 2))
            radiusmean.append(round(np.mean(radius_contour), 2))
            radius_contour = []
            dist2iso_struct.append(
                round(
                    np.linalg.norm(np.array(centermass1 - isocenter_plan)), 1
                )
            )
        dictionary_p["Target"] = names_p
        dictionary_p["Prescribed dose [Gy]"] = dose
        dictionary_p["Reference point dose [Gy]"] = dose_ref
        dictionary_p["Reference coordinates [mm]"] = coordinates
        dictionary_p["Distance to iso [mm]"] = dist2iso
        df_plan = pd.DataFrame(dictionary_p)
        for value1, target in enumerate(targets):
            for _, name_p in enumerate(names_p):
                nombres = name_p[:4]
                if target.startswith(nombres):
                    targets[value1] = name_p
        dictionary_s["Target"] = targets
        dictionary_s["Structure coordinates [mm]"] = centermass
        dictionary_s["Max radius [mm]"] = radiusmax
        dictionary_s["Min radius [mm]"] = radiusmin
        dictionary_s["Mean radius [mm]"] = radiusmean
        dictionary_s["Distance to iso (from structure) [mm]"] = dist2iso_struct
        df_struct = pd.DataFrame(dictionary_s)
        df_plan_struct = pd.merge(
            df_plan, df_struct, how="left", on=["Target"]
        )
        return df_plan_struct

    def rotate(self, struct, angle, key, *args):
        r"""Rotate a structure for a reference point.

        Allow to rotate all the points for a single structure.

        Rotation transformations are defined at the origin.
        For that reason it is necessary to bring the coordinates
        to the origin before rotating. You can
        `rotate <https://simple.wikipedia.org/wiki/Pitch,_yaw,_and_roll>`_
        an arbritrary structure (organ at risk, lesion or support
        structure) in any of the 3 degrees of freedom: roll, pitch, or yaw
        with the angle (in degrees) of your choice.

        .. note::
            **Additional advantage:** You can accumulate rotations
            and traslations to study any combination.

        Parameters
        ----------
        struct : str
            Name of the structure to rotate
        angle : float
            Angle in degrees (positive or negative).
            Maximum angle allowed 360º.
        key : str
            Direction of rotation ('roll', 'pitch' or 'yaw')
        \*args : list, optional
            Origin in a list of float elements [x, y, z].
            By default, it is considered the isocenter of the
            structure file (last structure in RS DICOM called Coord 1).
            If not is able this structure, you can add an
            arbritrarly point.

        Returns
        -------
        pydicom.dataset.FileDataset
            Object with DICOM properties of the rotated structure.

        Raises
        ------
        TypeError
            If the angle is a float, int or if angle > 360 degrees.
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
        >>> moved = dicom.rotate('1 GTV', 1.0, 'yaw')
        >>> # rotate lesion 1.0 degree in roll in [0.0, 0.0, 0.0].
        >>> iso = [0.0, 0.0, 0.0]
        >>> dicom.rotate('1 GTV', 1.0, 'yaw', iso)

        """
        dicom_copy = copy.deepcopy(self)
        if (
            isinstance(angle, float) is False
            and isinstance(angle, int) is False
        ):
            raise TypeError("Angle is a float o int!")
        elif abs(angle) > 360:
            raise ValueError("Angle is > 360º")
        else:
            angle = np.radians(angle)
        n_id = {}
        length = len(dicom_copy.dicom_struct.StructureSetROISequence)
        if key in ["roll", "pitch", "yaw"]:
            pass
        else:
            raise ValueError("Choose a correct key: roll, pitch, yaw")
        for i, _ in enumerate(dicom_copy.dicom_struct.StructureSetROISequence):
            n_id[
                (dicom_copy.dicom_struct.StructureSetROISequence[i].ROIName)
            ] = i
        if struct in n_id:
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
                        [0, np.cos(angle), -np.sin(angle), 0],
                        [0, np.sin(angle), np.cos(angle), 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "pitch": np.array(
                    [
                        [np.cos(angle), 0, np.sin(angle), 0],
                        [0, 1, 0, 0],
                        [-np.sin(angle), 0, np.cos(angle), 0],
                        [0, 0, 0, 1],
                    ]
                ),
                "yaw": np.array(
                    [
                        [np.cos(angle), -np.sin(angle), 0, 0],
                        [np.sin(angle), np.cos(angle), 0, 0],
                        [0, 0, 1, 0],
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
            for num, _ in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    n_id[struct]
                ].ContourSequence
            ):
                if (
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData
                    )
                    % 3
                    != 0
                ):
                    raise ValueError(
                        "One slice did not have all points of 3 elements"
                    )
                contour_rotated = []
                counter = 0
                while counter < int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                ):
                    rotation = (
                        m["iso2point"]
                        @ m[key]
                        @ m["point2iso"]
                        @ [
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[struct]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[struct]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 1]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[struct]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 2]
                            ),
                            1.0,
                        ]
                    )
                    contour_rotated.append(rotation[0])
                    contour_rotated.append(rotation[1])
                    contour_rotated.append(rotation[2])
                    counter = counter + 1
                (
                    dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                    .ContourSequence[num]
                    .ContourData
                ) = MultiValue(float, contour_rotated)
        else:
            raise ValueError("Type a correct name")
        return dicom_copy

    def translate(self, struct, delta, key, *args):
        """Translate a structure for a reference point.

        Allow to translate all the points for a single structure.

        Translation transformations are defined at the origin.
        For that reason it is necessary to bring the coordinates
        to the origin before rotating.

        .. note::
            **Additional advantage:** You can accumulate rotations
            and traslations to study any combination.

        Parameters
        ----------
        struct : str
            Name of the structure to translate
        delta : float
            Shift in mm (positive or negative).
            Maximum displacement allowed: 1000 mm (clinical perspective).
            More than 1000 mm has not relevance in patient displacement.
        key : str
            Direction of rotation ('x', 'y' or 'z')
        args : list, optional
            Origin in a list of float elements [x, y, z].
            By default, it is considered the isocenter of the
            structure file (last structure in RS DICOM called Coord 1).
            If not is able this structure, you can add an
            arbritrarly point.

        Returns
        -------
        pydicom.dataset.FileDataset
            Object with DICOM properties of the translated structure.

        Raises
        ------
        TypeError
            If the displacement is not float nor int or if it
            is > 1000 mm.
        ValueError
            If you select an incorrect translation key, incorrect name
            or if you type an origin point with no float.

        Examples
        --------
        >>> # translate tumor 1.0 mm in x in isocenter.
        >>> moved = dicom.translate('1 GTV', 1.0, 'x')
        >>> # translate lesion 1.0 mm in x in [0.0, 0.0, 0.0].
        >>> iso = [0.0, 0.0, 0.0]
        >>> dicom.translate('1 GTV', 1.0, 'x', iso)

        """
        dicom_copy = copy.deepcopy(self)
        if (
            isinstance(delta, float) is False
            and isinstance(delta, int) is False
        ):
            raise TypeError("delta is float or int!")
        elif abs(delta) > 1000:
            raise ValueError("delta is > 1000 mm")
        n_id = {}
        length = len(dicom_copy.dicom_struct.StructureSetROISequence)
        if key in ["x", "y", "z"]:
            pass
        else:
            raise ValueError("Choose a correct key: x, y, z")
        for i, _ in enumerate(dicom_copy.dicom_struct.StructureSetROISequence):
            n_id[
                (dicom_copy.dicom_struct.StructureSetROISequence[i].ROIName)
            ] = i
        if struct in n_id:
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
            for num, _ in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    n_id[struct]
                ].ContourSequence
            ):
                if (
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData
                    )
                    % 3
                    != 0
                ):
                    raise ValueError(
                        "One slice do not have all points of 3 elements"
                    )
                contour_translat = []
                counter = 0
                while counter < int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                ):
                    translation = (
                        m["iso2point"]
                        @ m[key]
                        @ m["point2iso"]
                        @ [
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[struct]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[struct]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 1]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[
                                    n_id[struct]
                                ]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 2]
                            ),
                            1.0,
                        ]
                    )
                    contour_translat.append(translation[0])
                    contour_translat.append(translation[1])
                    contour_translat.append(translation[2])
                    counter = counter + 1
                (
                    dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                    .ContourSequence[num]
                    .ContourData
                ) = MultiValue(float, contour_translat)
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
        name_struct : str
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
        n_id = {}
        if isinstance(margin, float):
            pass
        else:
            raise TypeError(f"{margin} must be float")
        for item, _ in enumerate(
            dicom_copy.dicom_struct.StructureSetROISequence
        ):
            n_id[
                dicom_copy.dicom_struct.StructureSetROISequence[item].ROIName
            ] = item
        if struct in n_id:
            for num1, _ in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    n_id[struct]
                ].ContourSequence
            ):
                x_mean, y_mean, z_mean = [], [], []
                longitud = int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num1]
                        .ContourData
                    )
                    / 3
                )
                if longitud < 1:
                    raise ValueError("Contour needs at least 1 point")
                j = 0
                while j < longitud:
                    x_mean.append(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num1]
                        .ContourData[3 * j]
                    )
                    y_mean.append(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num1]
                        .ContourData[3 * j + 1]
                    )
                    z_mean.append(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num1]
                        .ContourData[3 * j + 2]
                    )
                    j = j + 1
            print(x_mean)
            print(y_mean)
            print(z_mean)
            xmean = np.mean(x_mean)
            ymean = np.mean(y_mean)
            zmean = np.mean(z_mean)
            for num, _ in enumerate(
                dicom_copy.dicom_struct.ROIContourSequence[
                    n_id[struct]
                ].ContourSequence
            ):
                contourmargin = []
                longitude = int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                )
                if longitude > 1:
                    counter = 0
                    while counter < longitude:
                        x0 = (
                            dicom_copy.dicom_struct.ROIContourSequence[
                                n_id[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * counter]
                        )
                        y0 = (
                            dicom_copy.dicom_struct.ROIContourSequence[
                                n_id[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * counter + 1]
                        )
                        z0 = (
                            dicom_copy.dicom_struct.ROIContourSequence[
                                n_id[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * counter + 2]
                        )
                        if (
                            (xmean - x0) ** 2
                            + (ymean - y0) ** 2
                            + (zmean - z0) ** 2
                        ) != 0.0:
                            parameter = (
                                (x0 - xmean) ** 2
                                + (y0 - ymean) ** 2
                                + (z0 - zmean) ** 2
                            )
                            sol_1 = margin / (2 * np.sqrt(parameter))
                            sol_2 = -margin / (2 * np.sqrt(parameter))
                            x_sol1 = round(2 * (xmean - x0) * sol_1 + x0, 2)
                            y_sol1 = round(2 * (ymean - y0) * sol_1 + y0, 2)
                            z_sol1 = round(2 * (zmean - z0) * sol_1 + z0, 2)
                            x_sol2 = round(2 * (xmean - x0) * sol_2 + x0, 2)
                            y_sol2 = round(2 * (ymean - y0) * sol_2 + y0, 2)
                            z_sol2 = round(2 * (zmean - z0) * sol_2 + z0, 2)
                            dist1 = np.sqrt(
                                (xmean - x_sol1) ** 2
                                + (ymean - y_sol1) ** 2
                                + (zmean - z_sol1) ** 2
                            )
                            dist2 = np.sqrt(
                                (xmean - x_sol2) ** 2
                                + (ymean - y_sol2) ** 2
                                + (zmean - z_sol2) ** 2
                            )
                            if margin >= 0 and dist1 >= dist2:
                                contourmargin.append(x_sol1)
                                contourmargin.append(y_sol1)
                                contourmargin.append(z_sol1)
                            elif margin >= 0 and dist1 < dist2:
                                contourmargin.append(x_sol2)
                                contourmargin.append(y_sol2)
                                contourmargin.append(z_sol2)
                            elif margin < 0:
                                contourmargin.append(x_sol2)
                                contourmargin.append(y_sol2)
                                contourmargin.append(z_sol2)
                        else:
                            contourmargin.append(x0)
                            contourmargin.append(y0)
                            contourmargin.append(z0)
                        counter = counter + 1
                elif longitude == 1 and margin > 0:
                    x = (
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData[0]
                    )
                    y = (
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData[1]
                    )
                    z = (
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData[2]
                    )
                    contourmargin = [
                        x,
                        y + margin,
                        z,
                        x + margin,
                        y,
                        z,
                        x,
                        y - margin,
                        z,
                        x - margin,
                        y,
                        z,
                    ]
                elif longitude == 1 and margin <= 0:
                    contourmargin = (
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ]
                        .ContourSequence[num]
                        .ContourData
                    )
                (
                    dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                    .ContourSequence[num]
                    .ContourData
                ) = MultiValue(float, contourmargin)
        else:
            raise ValueError("Type a correct name")
        return dicom_copy
