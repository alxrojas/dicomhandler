
import numpy as np
import copy
import pydicom
import xlsxwriter
from pydicom.multival import MultiValue


class Dicominfo(pydicom.dataset.Dataset):
    def __init__(self, dicom_struct):
        pydicom.dataset.Dataset.__init__(self, dicom_struct)
        self.dicom_struct = dicom_struct

    def anonymize(self):
        """
        Returns a dicom object with
        Patient Name 'PatientName',
        Patient Birth Date '20000101',
        Operators Name 'OperatorName',
        Instance Creation Date '20000101'
        """
        self.dicom_struct.PatientName = 'PatientName'
        self.dicom_struct.PatientBirthDate = '20000101'
        self.dicom_struct.OperatorsName = 'OperatorName'
        self.dicom_struct.InstanceCreationDate = '20000101'
    #return self.dicom_struct

    def dicom2excel(self, name_file):
        """
        It creates DICOM contour in excelable form.
        The Contour Data for each organ is set on different sheets.
        The file is created in the same directory with the name name.xlsx
        INPUT:
        name_file -> str, with the name of the file.
        OUTPUT:
        Excel file.
        """
        extension = '.xlsx'
        if name_file.endswith(extension):
            pass
        else:
            name_file = ''.join([name_file, extension])
        names = []
        workbook = xlsxwriter.Workbook(name_file)
        merge_format = workbook.add_format({'align': 'center'})
        dicom_contour = self.dicom_struct.ROIContourSequence
        for item in range(len(self.dicom_struct.StructureSetROISequence)):
            name = self.dicom_struct.StructureSetROISequence[item].ROIName
            if name in names:
                pass
            else:
                names.append(name)
                worksheet = workbook.add_worksheet(name)
            for num in range(len(dicom_contour[item].ContourSequence)):
                contour = dicom_contour[item].ContourSequence[num].ContourData
                worksheet.merge_range(0, 3*num, 0, 3*num + 2,
                                      f'Contour {num + 1}', merge_format)
                worksheet.write_row(1, 3*num, ['x [mm]', 'y [mm]', 'z [mm]'])
                for count in range(int(len(contour)/3)):
                    x = float(contour[3*count])
                    y = float(contour[3*count+1])
                    z = float(contour[3*count+2])
                    worksheet.write_row(2+count, 3*num, [x, y, z])
        workbook.close()

    def rotate(self, name_struct, angle, key, *args):
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
        #dicom_struct1 = copy.deepcopy(self.dicom_struct)
        if abs(angle) < 360 and isinstance(angle, float):
            angle = np.radians(angle)
        else:
            raise ValueError("Type is not float and angle is > 360º")
        name_id = {}
        length = len(self.dicom_struct.StructureSetROISequence)
        if key in ['roll', 'pitch', 'yaw']:
            pass
        else:
            raise ValueError("Choose a correct key: roll, pitch, yaw")
        for i in range(length):
            name_id[self.dicom_struct.StructureSetROISequence[i].ROIName] = i
        if name_struct in name_id:
            dicom_contour = self.dicom_struct.ROIContourSequence
            if not args:
                origin = dicom_contour[length-1].ContourSequence[0].ContourData
            elif (len(args[0]) == 3 and
                  all(isinstance(x, float) for x in args[0])):
                origin = args[0]
            else:
                raise ValueError("Type an origin [x,y,z] with float elements")
            m = {'roll': np.array([[1, 0, 0, 0],
                                   [0, np.cos(angle), -np.sin(angle), 0],
                                   [0, np.sin(angle), np.cos(angle), 0],
                                   [0, 0, 0, 1]
                                   ]),
                 'pitch': np.array([[np.cos(angle), 0, np.sin(angle), 0],
                                    [0, 1, 0, 0],
                                    [-np.sin(angle), 0, np.cos(angle), 0],
                                    [0, 0, 0, 1]]),
                 'yaw': np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                                  [np.sin(angle), np.cos(angle), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]
                                  ]),
                 'p2iso': np.array([[1, 0, 0, -origin[0]],
                                    [0, 1, 0, -origin[1]],
                                    [0, 0, 1, -origin[2]],
                                    [0, 0, 0, 1]
                                    ]),
                 'iso2p': np.array([[1, 0, 0, origin[0]],
                                    [0, 1, 0, origin[1]],
                                    [0, 0, 1, origin[2]],
                                    [0, 0, 0, 1]
                                    ])
                 }
            sequence = dicom_contour[name_id[name_struct]].ContourSequence
            for num in range(len(sequence)):
                contour = sequence[num].ContourData
                contour_rotated = []
                for counter in range(int(len(contour)/3)):
                    vector = [float(contour[3*counter]),
                              float(contour[3*counter+1]),
                              float(contour[3*counter+2]), 1.0]
                    rotation = m['iso2p']@m[key]@m['p2iso']@vector
                    contour_rotated.append(rotation[0])
                    contour_rotated.append(rotation[1])
                    contour_rotated.append(rotation[2])
                self.dicom_struct.ROIContourSequence[name_id[name_struct]].ContourSequence[num].ContourData = MultiValue(float, contour_rotated)
        else:
            raise ValueError("Type a correct name")
        #return dicom_struct

    def translate(self, name_struct, delta, key, *args):
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
        #dicom_struct1 = copy.deepcopy(self.dicom_struct)
        if abs(delta) < 1000 and isinstance(delta, float):
            pass
        else:
            raise ValueError("Type is not float and delta is > 1000 mm")
        name_id = {}
        length = len(self.dicom_struct.StructureSetROISequence)
        if key in ['x', 'y', 'z']:
            pass
        else:
            raise ValueError("Choose a correct key: x, y, z")
        for i in range(length):
            name_id[self.dicom_struct.StructureSetROISequence[i].ROIName] = i
        if name_struct in name_id:
            dicom_contour = self.dicom_struct.ROIContourSequence
            if not args:
                origin = dicom_contour[length-1].ContourSequence[0].ContourData
            elif (len(args[0]) == 3 and
                  all(isinstance(x, float) for x in args[0])):
                origin = args[0]
            else:
                raise ValueError("Type an origin [x,y,z] with float elements")
            m = {'x': np.array([[1, 0, 0, delta],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]
                                ]),
                 'y': np.array([[1, 0, 0, 0],
                                [0, 1, 0, delta],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]
                                ]),
                 'z': np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, delta],
                                [0, 0, 0, 1]
                                ]),
                 'p2iso': np.array([[1, 0, 0, -origin[0]],
                                    [0, 1, 0, -origin[1]],
                                    [0, 0, 1, -origin[2]],
                                    [0, 0, 0, 1]
                                    ]),
                 'iso2p': np.array([[1, 0, 0, origin[0]],
                                    [0, 1, 0, origin[1]],
                                    [0, 0, 1, origin[2]],
                                    [0, 0, 0, 1]
                                    ])}
            sequence = dicom_contour[name_id[name_struct]].ContourSequence
            for num in range(len(sequence)):
                contour = sequence[num].ContourData
                contour_translat = []
                for counter in range(int(len(contour)/3)):
                    vector = [float(contour[3*counter]),
                              float(contour[3*counter+1]),
                              float(contour[3*counter+2]), 1.0]
                    translation = m['iso2p']@m[key]@m['p2iso']@vector
                    contour_translat.append(translation[0])
                    contour_translat.append(translation[1])
                    contour_translat.append(translation[2])
                self.dicom_struct.ROIContourSequence[name_id[name_struct]].ContourSequence[num].ContourData = MultiValue(float, contour_translat)
        else:
            raise ValueError("Type a correct name")
        return dicom_struct1

    def add_margin(self, name_struct, margin):
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
        #dicom_struct1 = copy.deepcopy(self.dicom_struct)
        name_id = {}
        if isinstance(margin, float):
            pass
        else:
            raise ValueError(f"{margin} must be float")
        sequence = self.dicom_struct.StructureSetROISequence
        longitude = len(sequence)
        for item in range(longitude):
            name_id[sequence[item].ROIName] = item
        if name_struct in name_id:
            dicom_base = self.dicom_struct
            dicom_contour = dicom_base.ROIContourSequence[name_id[name_struct]]
            for num in range(len(dicom_contour.ContourSequence)):
                contour_margin = []
                vector = dicom_contour.ContourSequence[num].ContourData
                length = int(len(vector)/3)
                if length > 1:
                    xmean = np.mean([vector[3*i] for i in range(length)])
                    ymean = np.mean([vector[3*i+1] for i in range(length)])
                    for cont in range(length):
                        x0 = vector[3*cont]
                        y0 = vector[3*cont + 1]
                        if x0 != xmean:
                            m = (ymean - y0) / (xmean - x0)
                            sol_x1 = x0 + np.sqrt(margin**2 / (1 + m**2))
                            sol_x2 = x0 - np.sqrt(margin**2 / (1 + m**2))
                            y1 = m*(sol_x1 - x0) + y0
                            y2 = m*(sol_x2 - x0) + y0
                            dist1 = ((xmean-sol_x1)**2 + (ymean-y1)**2)**0.5
                            dist2 = ((xmean-sol_x2)**2 + (ymean-y2)**2)**0.5
                            if margin >= 0 and dist1 >= dist2:
                                contour_margin.append(sol_x1)
                                contour_margin.append(y1)
                            elif margin >= 0 and dist1 < dist2:
                                contour_margin.append(sol_x2)
                                contour_margin.append(y2)
                            elif margin < 0 and dist1 < dist2:
                                contour_margin.append(sol_x1)
                                contour_margin.append(y1)
                            elif margin < 0 and dist1 > dist2:
                                contour_margin.append(sol_x2)
                                contour_margin.append(y2)
                            else:
                                raise ValueError("Invalid margin")
                        else:
                            contour_margin.append(x0)
                            if margin >= 0 and x0 >= xmean:
                                y1 = y0 + margin
                                contour_margin.append(y1)
                            elif margin >= 0 and x0 < xmean:
                                y1 = y0 - margin
                                contour_margin.append(y1)
                            elif margin < 0 and x0 >= xmean:
                                y1 = y0 + margin
                                contour_margin.append(y1)
                            else:
                                y1 = y0 - margin
                                contour_margin.append(y1)
                        contour_margin.append(vector[3*cont + 2])
                elif length == 1 and margin > 0:
                    contour_margin = [vector[0], vector[1] + margin, vector[2],
                                      vector[0] + margin, vector[1], vector[2],
                                      vector[0], vector[1] - margin, vector[2],
                                      vector[0] - margin, vector[1], vector[2]]
                elif length == 1 and margin <= 0:
                    contour_margin = vector
                else:
                    raise ValueError("Contour needs at least 1 point")
                sequence = dicom_contour.ContourSequence[num]
                self.dicom_struct.ROIContourSequence[name_id[name_struct]].ContourSequence[num].ContourData = MultiValue(float, contour_margin)
        else:
            raise ValueError("Type a correct name")
#return dicom_struct1
