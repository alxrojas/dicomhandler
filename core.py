import copy

import numpy as np
import pandas as pd
import xlsxwriter
from pydicom.multival import MultiValue


class Dicominfo:
    def __init__(self, *args):
        self.dicom_struct = None
        self.dicom_dose = None
        self.dicom_plan = None
        self.PatientName = None
        self.PatientBirthDate = None
        self.PatientID = None
        if len(args) != 0:
            temp = ""
            for arg in args:
                if temp == "":
                    temp = arg.PatientID
                elif temp == arg.PatientID:
                    pass
                else:
                    raise ValueError("Patient ID's do not match")
            for arg in args:
                if arg.Modality == "RTSTRUCT":
                    self.dicom_struct = arg
                elif arg.Modality == "RTDOSE":
                    self.dicom_dose = arg
                elif arg.Modality == "RTPLAN":
                    self.dicom_plan = arg
                else:
                    raise ValueError("Modality not supported")
            self.PatientName = args[0].PatientName
            self.PatientBirthDate = args[0].PatientBirthDate
            self.PatientID = args[0].PatientID
        else:
            pass

    def anonymize(self, name=True, birth=True, operator=True, creation=True):
        """
        It modifies a dicom object with
        Patient Name 'PatientName',
        Patient Birth Date '19720101',
        Operators Name 'OperatorName',
        Instance Creation Date '19720101'
        """
        dicom_copy = copy.deepcopy(self)

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

    def to_excel(self, name_file, names=[]):
        """
        It creates DICOM contour in excelable form.
        The Contour Data for each organ is set on different sheets.
        The file is created in the same directory with the name name.xlsx
        INPUT:
        name_file -> str, with the name of the file.
        names -> list of str, with the name of the structures to create in
        excel file. By default, [] which corresponds to all structures.
        Warning: for all structures, the (slow) process takes couple of minutes
        OUTPUT:
        Excel file.
        """
        dicom_copy = copy.deepcopy(self)
        extension = ".xlsx"
        if name_file.endswith(extension):
            pass
        else:
            name_file = "".join([name_file, extension])
        names_aux, n_all = {}, {}
        for item in range(len(dicom_copy.dicom_struct.StructureSetROISequence)):
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
        workbook = xlsxwriter.Workbook(name_file)
        for name in n_all:
            worksheet = workbook.add_worksheet(name)
            for num in range(
                len(
                    dicom_copy.dicom_struct.ROIContourSequence[
                        n_all[name]
                    ].ContourSequence
                )
            ):
                worksheet.write_row(1, 3 * num, ["x [mm]", "y [mm]", "z [mm]"])
                for count in range(
                    int(
                        len(
                            dicom_copy.dicom_struct.ROIContourSequence[n_all[name]]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    )
                ):
                    x = float(
                        dicom_copy.dicom_struct.ROIContourSequence[n_all[name]]
                        .ContourSequence[num]
                        .ContourData[3 * count]
                    )
                    y = float(
                        dicom_copy.dicom_struct.ROIContourSequence[n_all[name]]
                        .ContourSequence[num]
                        .ContourData[3 * count + 1]
                    )
                    z = float(
                        dicom_copy.dicom_struct.ROIContourSequence[n_all[name]]
                        .ContourSequence[num]
                        .ContourData[3 * count + 2]
                    )
                    worksheet.write_row(2 + count, 3 * num, [x, y, z])
        workbook.close()

    def rotate(self, struct, angle, key, *args):
        """
        It allows to rotate all the points for a single structure.
        Rotation is in the origin. For that reason it is necessary
        to bring the coordinates to the origin before rotating.
        INPUT:
        name_struct -> Name of the structure to rotate
        angle -> in degrees (positive or negative). Maximum angle allowed:
        360º.
        key -> direction of rotation ('roll', 'pitch' or 'yaw')
        *args -> origin in array [x, y, z]. By default, it is
        considered the isocenter of the structure plan (last
        structure in RS DICOM called Coord 1).
        OUTPUT:
        DICOM file with rotated structure.
        """
        dicom_copy = copy.deepcopy(self)
        if abs(angle) < 360 and isinstance(angle, float):
            angle = np.radians(angle)
        else:
            raise TypeError("Type is not float and angle is > 360º")
        n_id = {}
        length = len(dicom_copy.dicom_struct.StructureSetROISequence)
        if key in ["roll", "pitch", "yaw"]:
            pass
        else:
            raise ValueError("Choose a correct key: roll, pitch, yaw")
        for i in range(length):
            n_id[(dicom_copy.dicom_struct.StructureSetROISequence[i].ROIName)] = i
        if struct in n_id:
            if not args:
                origin = (
                    dicom_copy.dicom_struct.ROIContourSequence[length - 1]
                    .ContourSequence[0]
                    .ContourData
                )
            elif len(args[0]) == 3 and all(isinstance(x, float) for x in args[0]):
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
                "p2iso": np.array(
                    [
                        [1, 0, 0, -origin[0]],
                        [0, 1, 0, -origin[1]],
                        [0, 0, 1, -origin[2]],
                        [0, 0, 0, 1],
                    ]
                ),
                "iso2p": np.array(
                    [
                        [1, 0, 0, origin[0]],
                        [0, 1, 0, origin[1]],
                        [0, 0, 1, origin[2]],
                        [0, 0, 0, 1],
                    ]
                ),
            }
            for num in range(
                len(
                    dicom_copy.dicom_struct.ROIContourSequence[
                        n_id[struct]
                    ].ContourSequence
                )
            ):
                contour_rotated = []
                for counter in range(
                    int(
                        len(
                            dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    )
                ):
                    rotation = (
                        m["iso2p"]
                        @ m[key]
                        @ m["p2iso"]
                        @ [
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * counter]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 1]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 2]
                            ),
                            1.0,
                        ]
                    )
                    contour_rotated.append(rotation[0])
                    contour_rotated.append(rotation[1])
                    contour_rotated.append(rotation[2])
                (
                    dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                    .ContourSequence[num]
                    .ContourData
                ) = MultiValue(float, contour_rotated)
        else:
            raise ValueError("Type a correct name")
        return dicom_copy

    def translate(self, struct, delta, key, *args):
        """
        It allows to translate all the points for a single structure.
        Translation is in the origin. For that reason it is necessary
        to bring the coordinates to the origin before translating.
        INPUT:
        name_struct -> Name of the structure to rotate
        delta -> in mm: float (positive or negative). Maximum displacement
        allowed: 1000 mm (clinical perspective)
        key -> direction of translation ('x', 'y' or 'z')
        *args -> origin in array [x, y, z]. By default, it is
        considered the isocenter of the structure plan (last
        structure in RS DICOM called Coord 1).
        OUTPUT:
        DICOM file with translated structure.
        """
        dicom_copy = copy.deepcopy(self)
        if abs(delta) < 1000 and isinstance(delta, float):
            pass
        else:
            raise ValueError("Type is not float and delta is > 1000 mm")
        n_id = {}
        length = len(dicom_copy.dicom_struct.StructureSetROISequence)
        if key in ["x", "y", "z"]:
            pass
        else:
            raise ValueError("Choose a correct key: x, y, z")
        for i in range(length):
            n_id[(dicom_copy.dicom_struct.StructureSetROISequence[i].ROIName)] = i
        if struct in n_id:
            if not args:
                origin = (
                    dicom_copy.dicom_struct.ROIContourSequence[length - 1]
                    .ContourSequence[0]
                    .ContourData
                )
            elif len(args[0]) == 3 and all(isinstance(x, float) for x in args[0]):
                origin = args[0]
            else:
                raise ValueError("Type an origin [x,y,z] with float elements")
            m = {
                "x": np.array(
                    [[1, 0, 0, delta], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
                ),
                "y": np.array(
                    [[1, 0, 0, 0], [0, 1, 0, delta], [0, 0, 1, 0], [0, 0, 0, 1]]
                ),
                "z": np.array(
                    [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, delta], [0, 0, 0, 1]]
                ),
                "p2iso": np.array(
                    [
                        [1, 0, 0, -origin[0]],
                        [0, 1, 0, -origin[1]],
                        [0, 0, 1, -origin[2]],
                        [0, 0, 0, 1],
                    ]
                ),
                "iso2p": np.array(
                    [
                        [1, 0, 0, origin[0]],
                        [0, 1, 0, origin[1]],
                        [0, 0, 1, origin[2]],
                        [0, 0, 0, 1],
                    ]
                ),
            }
            for num in range(
                len(
                    dicom_copy.dicom_struct.ROIContourSequence[
                        n_id[struct]
                    ].ContourSequence
                )
            ):
                contour_translat = []
                for counter in range(
                    int(
                        len(
                            dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    )
                ):
                    translation = (
                        m["iso2p"]
                        @ m[key]
                        @ m["p2iso"]
                        @ [
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * counter]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 1]
                            ),
                            float(
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * counter + 2]
                            ),
                            1.0,
                        ]
                    )
                    contour_translat.append(translation[0])
                    contour_translat.append(translation[1])
                    contour_translat.append(translation[2])
                (
                    dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                    .ContourSequence[num]
                    .ContourData
                ) = MultiValue(float, contour_translat)
        else:
            raise ValueError("Type a correct name")
        return dicom_copy

    def add_margin(self, struct, margin):
        """
        It allows to expand or substract margin for a single structure.
        For each point is considered the distance between the
        mean center (xmean, ymean) of each its slice plus (minus) a margin.
        By solve a quadratic equation between the circunference
        with centre the point (x0, y0) and radius = margin and the line
        between (xmean, ymean) and (x0, y0) is calculated the point with
        the margin (x, y).
        Equation: x = x0 +- sqrt(margin**2/(1+m**2)), m the slope.
        Equation: y = m(x - x0) + y0
        INPUT:
        name_struct -> Name of the structure to rotate.
        margin -> The expansion or substraction in mm.
        OUTPUT:
        DICOM file with expanded/substracted structure.
        """
        dicom_copy = copy.deepcopy(self)
        n_id = {}
        if isinstance(margin, float):
            pass
        else:
            raise ValueError(f"{margin} must be float")
        longitude = len(dicom_copy.dicom_struct.StructureSetROISequence)
        for item in range(longitude):
            n_id[dicom_copy.dicom_struct.StructureSetROISequence[item].ROIName] = item
        if struct in n_id:
            for num in range(
                len(
                    (
                        dicom_copy.dicom_struct.ROIContourSequence[
                            n_id[struct]
                        ].ContourSequence
                    )
                )
            ):
                contourmargin = []
                lon = int(
                    len(
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                )
                if lon > 1:
                    xmean = np.mean(
                        [
                            (
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * i]
                            )
                            for i in range(lon)
                        ]
                    )
                    ymean = np.mean(
                        [
                            (
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * i + 1]
                            )
                            for i in range(lon)
                        ]
                    )
                    for cont in range(lon):
                        x0 = (
                            dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                            .ContourSequence[num]
                            .ContourData[3 * cont]
                        )
                        y0 = (
                            dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                            .ContourSequence[num]
                            .ContourData[3 * cont + 1]
                        )
                        if x0 != xmean:
                            m = (ymean - y0) / (xmean - x0)
                            sol_x1 = x0 + np.sqrt(margin**2 / (1 + m**2))
                            sol_x2 = x0 - np.sqrt(margin**2 / (1 + m**2))
                            y1 = m * (sol_x1 - x0) + y0
                            y2 = m * (sol_x2 - x0) + y0
                            dist1 = ((xmean - sol_x1) ** 2 + (ymean - y1) ** 2) ** 0.5
                            dist2 = ((xmean - sol_x2) ** 2 + (ymean - y2) ** 2) ** 0.5
                            if margin >= 0 and dist1 >= dist2:
                                contourmargin.append(sol_x1)
                                contourmargin.append(y1)
                            elif margin >= 0 and dist1 < dist2:
                                contourmargin.append(sol_x2)
                                contourmargin.append(y2)
                            elif margin < 0 and dist1 < dist2:
                                contourmargin.append(sol_x1)
                                contourmargin.append(y1)
                            elif margin < 0 and dist1 > dist2:
                                contourmargin.append(sol_x2)
                                contourmargin.append(y2)
                            else:
                                raise ValueError("Invalid margin")
                        else:
                            contourmargin.append(x0)
                            if margin >= 0 and y0 >= ymean:
                                y1 = y0 + margin
                                contourmargin.append(y1)
                            elif margin >= 0 and y0 < ymean:
                                y1 = y0 - margin
                                contourmargin.append(y1)
                            elif margin < 0 and y0 >= ymean:
                                y1 = y0 + margin
                                contourmargin.append(y1)
                            else:
                                y1 = y0 - margin
                                contourmargin.append(y1)
                        contourmargin.append(
                            (
                                dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * cont + 2]
                            )
                        )
                elif lon == 1 and margin > 0:
                    x = (
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                        .ContourSequence[num]
                        .ContourData[0]
                    )
                    y = (
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                        .ContourSequence[num]
                        .ContourData[1]
                    )
                    z = (
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
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
                elif lon == 1 and margin <= 0:
                    contourmargin = (
                        dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                        .ContourSequence[num]
                        .ContourData
                    )
                else:
                    raise ValueError("Contour needs at least 1 point")
                (
                    dicom_copy.dicom_struct.ROIContourSequence[n_id[struct]]
                    .ContourSequence[num]
                    .ContourData
                ) = MultiValue(float, contourmargin)
        else:
            raise ValueError("Type a correct name")
        return dicom_copy


def report(dicom1, dicom2, struct):
    """
    Function that report the maximum, minimum, mean, standard deviation
    and variance of: radius between each point of a structure and its centre
    of mass and the distances between two structures (the same name) in
    different positions. It is reported the distance between the centres of
    mass of the two structures.
    The report is in a dataframe.
    INPUT:
    dicom1 -> First DICOM file with structures.
    dicom1 -> Second DICOM file with structures.
    name_struct -> The name of the structure.
    OUTPUT:
    dataframe with statistics.
    """
    n_id1, n_id2 = {}, {}
    longitude1 = len(dicom1.dicom_struct.StructureSetROISequence)
    longitude2 = len(dicom2.dicom_struct.StructureSetROISequence)
    for item in range(longitude1):
        n_id1[(dicom1.dicom_struct.StructureSetROISequence[item].ROIName)] = item
    for item2 in range(longitude2):
        n_id2[(dicom2.dicom_struct.StructureSetROISequence[item2].ROIName)] = item2
    if (struct in n_id1) and (struct in n_id2):
        distances_contour, radius_contour = [], []
        mean_values1, mean_values2 = [], []
        for num in range(
            len(dicom2.dicom_struct.ROIContourSequence[n_id2[struct]].ContourSequence)
        ):
            vector2 = (
                dicom2.dicom_struct.ROIContourSequence[n_id2[struct]]
                .ContourSequence[num]
                .ContourData
            )
            length1 = int(
                len(
                    dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                    .ContourSequence[num]
                    .ContourData
                )
                / 3
            )
            length2 = int(len(vector2) / 3)
            xmean1 = np.mean(
                [
                    (
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * i]
                    )
                    for i in range(length1)
                ]
            )
            ymean1 = np.mean(
                [
                    (
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * i + 1]
                    )
                    for i in range(length1)
                ]
            )
            zmean1 = np.mean(
                [
                    (
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * i + 2]
                    )
                    for i in range(length1)
                ]
            )
            mean_values1.append([xmean1, ymean1, zmean1])
            xmean2 = np.mean(
                [
                    (
                        dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * i]
                    )
                    for i in range(length2)
                ]
            )
            ymean2 = np.mean(
                [
                    (
                        dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * i + 1]
                    )
                    for i in range(length2)
                ]
            )
            zmean2 = np.mean(
                [
                    (
                        dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * i + 2]
                    )
                    for i in range(length2)
                ]
            )
            mean_values2.append([xmean2, ymean2, zmean2])
        centermass1 = np.mean(mean_values1, axis=0)
        centermass2 = np.mean(mean_values2, axis=0)
        for num in range(
            len(dicom1.dicom_struct.ROIContourSequence[n_id2[struct]].ContourSequence)
        ):
            length1 = int(
                len(
                    dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                    .ContourSequence[num]
                    .ContourData
                )
                / 3
            )
            length2 = int(
                len(
                    dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                    .ContourSequence[num]
                    .ContourData
                )
                / 3
            )
            if length1 == length2:
                for count in range(length1):
                    basepoint = np.array(
                        [
                            (
                                dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * count]
                            ),
                            (
                                dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * count + 1]
                            ),
                            (
                                dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * count + 2]
                            ),
                        ]
                    )
                    movedpoint = np.array(
                        [
                            (
                                dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * count]
                            ),
                            (
                                dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * count + 1]
                            ),
                            (
                                dicom2.dicom_struct.ROIContourSequence[n_id1[struct]]
                                .ContourSequence[num]
                                .ContourData[3 * count + 2]
                            ),
                        ]
                    )
                    distance = np.sqrt(sum(np.square(basepoint - movedpoint)))
                    radius = np.sqrt(sum(np.square(basepoint - centermass1)))
                    distances_contour.append(distance)
                    radius_contour.append(radius)
            else:
                raise ValueError("Contours' length differs")
    else:
        raise ValueError("Wrong name or name must match between two DICOM")
    distance_centermass = np.sqrt(sum(np.square(centermass1 - centermass2)))
    data = {
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
            np.max(radius_contour),
            np.min(radius_contour),
            np.mean(radius_contour),
            np.std(radius_contour),
            np.var(radius_contour),
            np.max(distances_contour),
            np.min(distances_contour),
            np.mean(distances_contour),
            np.std(distances_contour),
            np.var(distances_contour),
            distance_centermass,
        ],
    }
    return pd.DataFrame(data)
