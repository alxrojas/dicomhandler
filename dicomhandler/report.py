"""Report to extract complementary information.

Allows to compare distances from two structures.

"""
import numpy as np

import pandas as pd


def report(dicom1, dicom2, struct):
    """Report metrics from structures.

    This function reports the maximum, minimum, mean, standard deviation
    and variance of: radius between each point of a structure and its centre
    of mass and the distances between two structures (the same name) in
    different positions. It is reported the distance between the centres of
    mass of the two structures.

    The report is in a dataframe.

    Parameters
    ----------
    dicom1 : pydicom.dataset.FileDataset
        First DICOM file with structures.
    dicom2 : pydicom.dataset.FileDataset
        Second DICOM file with structures.
    name_struct : str
        The name of the structure.

    Returns
    -------
    pandas.core.frame.DataFrame
        dataframe with statistics.

    Raises
    ------
    ValueError
        If you type a wrong name or if the name does not
        match between two DICOM files.

    Examples
    --------
    >>> # Import report.
    >>> import dicomhandler.report as rp
    >>> # Report for the original and displaced lesion.
    >>> rp(dicom, moved, 'tumor')
    """
    all_values, radius, distance = [], [], []
    for _, file in enumerate([dicom1, dicom2]):
        for item, name in enumerate(file.dicom_struct.StructureSetROISequence):
            array = []
            if name.ROIName == struct:
                for _, contour in enumerate(
                    file.dicom_struct.ROIContourSequence[item].ContourSequence
                ):
                    count = 0
                    while count < int(len(contour.ContourData) / 3):
                        array.append(
                            [
                                float(contour.ContourData[3 * count]),
                                float(contour.ContourData[3 * count + 1]),
                                float(contour.ContourData[3 * count + 2]),
                            ]
                        )
                        count = count + 1
                all_values.append(array)
    if len(all_values) == 0:
        raise ValueError("Wrong name or name must match between two DICOM")
    elif len(all_values[0][:][:]) == len(all_values[1][:][:]):
        centermass = np.mean(all_values, axis=1)
        difference = np.array(all_values[0][:][:]) - np.array(
            all_values[1][:][:]
        )
        for item, vector in enumerate(np.array(all_values[0][:][:])):
            radius.append(np.linalg.norm(vector - centermass[0]))
            distance.append(np.linalg.norm(difference[item]))
    else:
        raise ValueError("Contours length differs")
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
            round(np.max(radius), 3),
            round(np.min(radius), 3),
            round(np.mean(radius), 3),
            round(np.std(radius), 3),
            round(np.var(radius), 3),
            round(np.max(distance), 3),
            round(np.min(distance), 3),
            round(np.mean(distance), 3),
            round(np.std(distance), 3),
            round(np.var(distance), 3),
            round(np.linalg.norm(centermass[0] - centermass[1]), 3),
        ],
    }
    return pd.DataFrame(data)
