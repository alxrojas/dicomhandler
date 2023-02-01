import os
from io import BytesIO

import pandas as pd
from pandas.testing import assert_frame_equal

import pytest


myio1 = BytesIO()

myio1.write(
    b"space1,x0 [mm],y0 [mm],z0 [mm]\n\
0,0.0,1.0,0.0\n\
1,1.0,0.0,0.0\n\
space2,x0 [mm],y0 [mm],z0 [mm]\n\
0,1.0,0.0,0.0\n\
1,2.0,0.0,0.0\n\
2,3.0,0.0,0.0\n\
space3,x0 [mm],y0 [mm],z0 [mm]\n\
0,1.0,1.0,0.0\n\
1,2.0,-1.0,0.0\n\
2,3.0,0.0,0.0\n\
space4,x0 [mm],y0 [mm],z0 [mm]\n\
0,1.0,0.0,0.0\n\
space5,x0 [mm],y0 [mm],z0 [mm]\n\
0,1.0,0.0,0.0\n\
space6,x0 [mm],y0 [mm],z0 [mm]\n\
0,1.0,0.0,0.0\n\
1,1.0,2.0,0.0\
"
)

myio1.seek(0)
df1 = pd.read_csv(myio1)


myio2 = BytesIO()
myio2.write(
    b"Beam 0,CP0,CP1\n\
0,GantryAngle,GantryAngle\n\
1,0.0,10.0\n\
2,GantryDirection,GantryDirection\n\
3,CW,CW\n\
4,TableDirection,TableDirection\n\
5,0.0,0.0\n\
6,MLC,MLC\n\
7,-9.0,-3.0\n\
8,-8.0,-2.0\n\
9,-7.0,-1.0\n\
10,0.0,-3.0\n\
11,0.0,-2.0\n\
12,0.0,-1.0\n\
Beam 1,CP0,CP1\n\
0,GantryAngle,GantryAngle\n\
1,0.0,10.0\n\
2,GantryDirection,GantryDirection\n\
3,CC,CC\n\
4,TableDirection,TableDirection\n\
5,5.0,5.0\n\
6,MLC,MLC\n\
7,-3.0,-3.0\n\
8,-2.0,-2.0\n\
9,-1.0,-1.0\n\
10,1.0,3.0\n\
11,2.0,2.0\n\
12,3.0,1.0"
)
myio2.seek(0)
df2 = pd.read_csv(myio2)


@pytest.mark.parametrize(
    "patient_s, patient_p, struct_b, mlc_b, name_csv, dataframe",
    [
        (
            "patient_0_s.gz",
            "patient_0_p.gz",
            True,
            False,
            "0_PLAN2_struct.csv",
            df1,
        ),
        (
            "patient_0_s.gz",
            "patient_0_p.gz",
            False,
            True,
            "0_PLAN2_MLC.csv",
            df2,
        ),
    ],
)
def test_dataframe(
    dicom_infos_2,
    patient_s,
    patient_p,
    struct_b,
    mlc_b,
    name_csv,
    dataframe,
    request,
):
    di = dicom_infos_2(patient_s, patient_p)
    di.to_csv(structure=struct_b, mlc=mlc_b)
    df = pd.read_csv(name_csv)
    assert_frame_equal(df, dataframe)
    os.remove(name_csv)
