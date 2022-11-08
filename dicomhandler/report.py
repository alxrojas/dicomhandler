import numpy as np
import pandas as pd


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
        n_id1[
            (dicom1.dicom_struct.StructureSetROISequence[item].ROIName)
        ] = item
    for item2 in range(longitude2):
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
            for num in range(
                len(
                    dicom2.dicom_struct.ROIContourSequence[
                        n_id2[struct]
                    ].ContourSequence
                )
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
                        dicom2.dicom_struct.ROIContourSequence[n_id2[struct]]
                        .ContourSequence[num]
                        .ContourData
                    )
                    / 3
                )
                xmean1 = np.mean(
                    [
                        (
                            dicom1.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * i]
                        )
                        for i in range(length1)
                    ]
                )
                ymean1 = np.mean(
                    [
                        (
                            dicom1.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * i + 1]
                        )
                        for i in range(length1)
                    ]
                )
                zmean1 = np.mean(
                    [
                        (
                            dicom1.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
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
                            dicom2.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * i]
                        )
                        for i in range(length2)
                    ]
                )
                ymean2 = np.mean(
                    [
                        (
                            dicom2.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
                            .ContourSequence[num]
                            .ContourData[3 * i + 1]
                        )
                        for i in range(length2)
                    ]
                )
                zmean2 = np.mean(
                    [
                        (
                            dicom2.dicom_struct.ROIContourSequence[
                                n_id1[struct]
                            ]
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
                len(
                    dicom1.dicom_struct.ROIContourSequence[
                        n_id2[struct]
                    ].ContourSequence
                )
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
