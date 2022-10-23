<h1 align="center"> dicom2handle </h1>

<h4 align="center">
:construction: Project in development. Men at work :construction:
</h4>

![Badge Development](https://img.shields.io/badge/STATUS-DEVELOPMENT-green)
![GitHub Org's stars](https://img.shields.io/github/stars/alxrojas?style=social)

Python tool for integrating [DICOM](https://www.dicomstandard.org/) information and processing DICOM radiotherapy structures. It allows to modify the structures (expand, contract, rotate, translate) and to obtain statistics from these modifications without the need to use CT or MRI images and to create new DICOM files with this information, which are compatible with the commercial systems of treatment planning such as [Eclipse](https://www.varian.com/es/products/radiotherapy/treatment-planning/eclipse) and [Brainlab Elements](https://www.brainlab.com/es/productos-de-cirugia/relacion-de-productos-de-neurocirugia/brainlab-elements/). It is possible to extract the information from the structures in an easy "excelable" form.


## :hammer: Features

- `Dicominfo`: The `Dicominfo` class allows to integrate the characteristics and data of the different DICOM files, which have complementary information of each patient. The files accepted are: structures (RS.dcm), treatment plan (RP.dcm) and treatment dose (RD.dcm).

- `anonymize`: In many cases, it is important to anonymize the patient's information for research and statistics. `anonymize` method allows to overwrite the name, birthdate of the patient, the operator's name and the creation of the plan.

- `to_excel`: The information of the cartesian coordinates (relative positions) for all or some structures is extracted in an .xlsx file for posprocessing.

- `rotate`: You can rotate an arbritrary structure (organ at risk, lesion or support structure) in any of the 3 degrees of freedom [(roll, pitch or yaw)](https://simple.wikipedia.org/wiki/Pitch,_yaw,_and_roll) with the angle (in grades) of your choice. **Additional advantage: You can accumulate rotations and traslations to study any combination.**

- `translate`: You can translate an arbritrary structure (organ at risk, lesion or support structure) in any of the 3 degrees of freedom (x, y, z) with the shift (in milimeters) of your choice. **Additional advantage: You can accumulate rotations and traslations to study any combination.**

- `add_margin`: You can expand or contract an arbritary structure with the [margin](https://www.aapm.org/meetings/2011SS/documents/MackieUncertainty.pdf) of your choice (in milimeters). This allows to asign new personalized margin for each structure for each patient.

- `report`: After movements (rotations/translations), the original and the displaced structure are compared to show the main metrics involved in the analyisis, such as maximum, mean and mininum local and global displacements and the variances associated.

## 💡Examples

#### Register DICOM file
It is required to operate on a DICOM object (from RS.dcm or RP.dcm), which are called as shown below (you can use the DICOM files by default in the [repository](https://github.com/alxrojas/dicom2handle/tree/main/Examples)):
```python
import os
import pydicom
from core import *

file = os.listdir(os.chdir('./DICOMfiles'))
dcm_structure = pydicom.dcmread(file[0], force = True)
dcm_plan = pydicom.dcmread(file[1], force = True)
```
#### Create the Dicominfo object
Put all dicoms in a single object (containing only the structure's file information as follows:
```python
di = Dicominfo(dcm_structure)
```
or containing structure and plan's information as:
```python
di = Dicominfo(dcm_structure, dcm_plan)
```

#### Anonymize the information
Anonymize the information. By default this function overwrites all the patient's personal data to generic values. You can choose the information that it has to be anonymized: ```anonymize(name=True, birth=True, operator=True, creation=True)```
```python
di.anonymize(name=True, birth=True, operator=False, creation=False)
```

#### Rotate or translate
Input of the functions are: `rotate('Name of the structure', angle=float, key=str, origin = [x, y, z])` with key 'roll', 'pitch' or 'yaw'. By default, the point at which you rotate is the isocenter (center of mass of lesions). `translate('Name of the structure', delta=float, key=str, origin = [x, y, z])` with key 'x', y' or 'z'. By default, the point at which you rotate/translate is the isocenter (center of mass of lesions). You can change the origin for an arbritary point.
For the isocenter:
```python
di_rotated = di.rotate('5 GTV', 0.5, 'pitch')
di_translated = di.translate('5 GTV', 1.0, 'x')
```
or for an arbritary point:
```python
di_rotated = di.rotate('5 GTV', 0.5, 'pitch', [4.0, -50.0, 20.0])
di_translated = di.translate('5 GTV', 1.0, 'x', [4.0, -50, 20.0])
```

#### Statistics report
With the report function you can compare the displacements between two states of the same structure:
```python
report(di, di_rotated, '5 GTV')

	Parameter	Value [mm]
0	Max radius	4.229131
1	Min radius	1.444514
2	Mean radius	3.152265
3	STD radius	0.554659
4	Variance radius	0.307646
5	Max distance	0.170817
6	Min distance	0.113221
7	Mean distance	0.142280
8	STD distance	0.015399
9	Variance distance	0.000237
10	Distance between center mass	0.141891
```

#### Expand or contract margin
Input of the function is: `add_margin('Name of the structure', margin=float)` with the margin in milimeters (positive if expands, negative if contracts).
```python
add_margin('5 GTV', 1.5)
```

#### Excel file
An .xlsx file is generated in the current directory with the information on the coordinates (x, y, z) of all or some structures of a patient. By default the report is generated for all structures.

⚠️ 🐢 For all structures this process takes several minutes (for 40 structures -> 15-20 min) 🐢 ⚠️
```python
di.to_excel('Name of the file', structures = [])
```
Or you can select some structures to obtain the excel file:
```python
di.to_excel('Name of the file', structures = ['Structure1', 'Structure2'])
```

## 📁 Access

Import dicom2handle as

## ⚙️ Open and run the project

Run the project as 

## 🛠️ 📋 Libraries and pre-requisites
Things do you need to install the software:

- [numpy](https://numpy.org/): Data analysis and calculation
- [pandas](https://pandas.pydata.org/): Report statistics
- [pydicom](https://pydicom.github.io/): DICOM file reader
- [xlsxwriter](https://pypi.org/project/XlsxWriter/): Write information

## ✒ Authors

| [<sub>Alejandro Rojas</sub>](https://github.com/alxrojas)| [<sub>Jerónimo Fotinós</sub>](https://github.com/JeroFotinos) | [<sub>Nicola Maddalozzo</sub>](https://github.com/nicolaMaddalozzo) |  [<sub>Martín Núñez</sub>](https://github.com/martinnnuez) |
| :---: | :---: | :---: | :---: |

## 📄 Licencia
This project is licensed under (MIT) - Look the file [LICENSE.md](https://github.com/alxrojas/dicom2handle/blob/main/LICENSE) for details.

## 🤓 More information for potential applications

-[Beltrán et al. Radiat and Onc (2012)](https://www.sciencedirect.com/science/article/abs/pii/S0167814011003240)

-[Rojas López et al. Phys Med (2021)](https://www.sciencedirect.com/science/article/abs/pii/S1120179721002131)

-[Venencia et al. J Rad in Pract (2022)](https://www.cambridge.org/core/journals/journal-of-radiotherapy-in-practice/article/abs/rotational-effect-and-dosimetric-impact-hdmlc-vs-5mm-mlc-leaf-width-in-single-isocenter-multiple-metastases-radiosurgery-with-brainlab-elements/EFBC35342D49298190BA8381BC729AB1)

-[Zhang et al. SpringerPlus (2016)](https://springerplus.springeropen.com/articles/10.1186/s40064-016-1796-2)

## 🎁 Expressions of gratitude

* Tell others about this project 📢
* Cite our project in your paper 📄
* Invite someone from the team a beer 🍺 or a coffee ☕.
* Give thanks publicly 🤓.

---
⌨️ with ❤️ by [AlxRojas](https://github.com/alxrojas) 😊
