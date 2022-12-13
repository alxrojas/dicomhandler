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
    # Import report.
    >>> import dicomhandler.report as rp
    # Report for the original and displaced lesion.
    >>> rp(dicom, moved, 'tumor')
    """
    n_id1, n_id2 = {}, {}
    for item, _ in enumerate(dicom1.dicom_struct.StructureSetROISequence):
        n_id1[
            (dicom1.dicom_struct.StructureSetROISequence[item].ROIName)
        ] = item
    for item2, _ in enumerate(dicom2.dicom_struct.StructureSetROISequence):
        n_id2[
            (dicom2.dicom_struct.StructureSetROISequence[item2].ROIName)
        ] = item2
    if (struct in n_id1) and (struct in n_id2):
        distances_contour, radius_contour = [], []
        mean_values1, mean_values2 = [], []
        if len(
            dicom1.dicom_struct.ROIContourSequence[
                n_id2[struct]
            ].ContourSequence
        ) == len(
            dicom2.dicom_struct.ROIContourSequence[
                n_id2[struct]
            ].ContourSequence
        ):
            for num, _ in enumerate(
                dicom2.dicom_struct.ROIContourSequence[
                    n_id2[struct]
                ].ContourSequence
            ):
                xmean1, ymean1, zmean1 = [], [], []
                xmean2, ymean2, zmean2 = [], [], []
                counter1 = 0
                counter2 = 0
                while counter1 < int(
                    len(
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                ):
                    xmean1.append(
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * counter1]
                    )
                    ymean1.append(
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * counter1 + 1]
                    )
                    zmean1.append(
                        dicom1.dicom_struct.ROIContourSequence[n_id1[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * counter1 + 2]
                    )
                    counter1 = counter1 + 1
                xmean1 = np.mean(xmean1)
                ymean1 = np.mean(ymean1)
                zmean1 = np.mean(zmean1)
                mean_values1.append([xmean1, ymean1, zmean1])
                while counter2 < int(
                    len(
                        dicom2.dicom_struct.ROIContourSequence[n_id2[struct]]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                ):
                    xmean2.append(
                        dicom2.dicom_struct.ROIContourSequence[n_id2[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * counter2]
                    )
                    ymean2.append(
                        dicom2.dicom_struct.ROIContourSequence[n_id2[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * counter2 + 1]
                    )
                    zmean2.append(
                        dicom2.dicom_struct.ROIContourSequence[n_id2[struct]]
                        .ContourSequence[num]
                        .ContourData[3 * counter2 + 2]
                    )
                    counter2 = counter2 + 1
                xmean2 = np.mean(xmean2)
                ymean2 = np.mean(ymean2)
                zmean2 = np.mean(zmean2)
                mean_values2.append([xmean2, ymean2, zmean2])
            centermass1 = np.mean(mean_values1, axis=0)
            centermass2 = np.mean(mean_values2, axis=0)
            for num, _ in enumerate(
                dicom1.dicom_struct.ROIContourSequence[
                    n_id2[struct]
                ].ContourSequence
            ):
                if (
                    int(
                        len(
                            dicom1.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    )
                ) == (
                    int(
                        len(
                            dicom2.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    )
                ):
                    count = 0
                    while count < int(
                        len(
                            dicom1.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData
                        )
                        / 3
                    ):
                        basepoint = np.array(
                            [
                                (
                                    dicom1.dicom_struct.ROIContourSequence[
                                        n_id1[struct]
                                    ]
                                    .ContourSequence[num]
                                    .ContourData[3 * count]
                                ),
                                (
                                    dicom1.dicom_struct.ROIContourSequence[
                                        n_id1[struct]
                                    ]
                                    .ContourSequence[num]
                                    .ContourData[3 * count + 1]
                                ),
                                (
                                    dicom1.dicom_struct.ROIContourSequence[
                                        n_id1[struct]
                                    ]
                                    .ContourSequence[num]
                                    .ContourData[3 * count + 2]
                                ),
                            ]
                        )
                        movedpoint = np.array(
                            [
                                (
                                    dicom2.dicom_struct.ROIContourSequence[
                                        n_id1[struct]
                                    ]
                                    .ContourSequence[num]
                                    .ContourData[3 * count]
                                ),
                                (
                                    dicom2.dicom_struct.ROIContourSequence[
                                        n_id1[struct]
                                    ]
                                    .ContourSequence[num]
                                    .ContourData[3 * count + 1]
                                ),
                                (
                                    dicom2.dicom_struct.ROIContourSequence[
                                        n_id1[struct]
                                    ]
                                    .ContourSequence[num]
                                    .ContourData[3 * count + 2]
                                ),
                            ]
                        )
                        distance = np.sqrt(
                            sum(np.square(basepoint - movedpoint))
                        )
                        radius = np.sqrt(
                            sum(np.square(basepoint - centermass1))
                        )
                        distances_contour.append(distance)
                        radius_contour.append(radius)
                        count = count + 1
                else:
                    raise ValueError("Contours' length differs")
        else:
            raise ValueError("Number of slices do not correspond")
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
            round(np.max(radius_contour), 3),
            round(np.min(radius_contour), 3),
            round(np.mean(radius_contour), 3),
            round(np.std(radius_contour), 3),
            round(np.var(radius_contour), 3),
            round(np.max(distances_contour), 3),
            round(np.min(distances_contour), 3),
            round(np.mean(distances_contour), 3),
            round(np.std(distances_contour), 3),
            round(np.var(distances_contour), 3),
            round(distance_centermass, 3),
        ],
    }
    return pd.DataFrame(data)
