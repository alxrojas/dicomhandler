# dicomhandler

<!-- BODY -->

Dicomhandler is a Python tool for integrating [DICOM](https://www.dicomstandard.org/) information and processing DICOM radiotherapy structures. It allows to modify the structures (expand, contract, rotate, translate) and to obtain statistics from these modifications without the need to use CT or MRI images and to create new objects with this information, which are compatible with the commercial systems of treatment planning such as [Eclipse](https://www.varian.com/es/products/radiotherapy/treatment-planning/eclipse) and [Brainlab Elements](https://www.brainlab.com/es/productos-de-cirugia/relacion-de-productos-de-neurocirugia/brainlab-elements/). It is possible to extract the information from the structures in an easy *excelable* form.

Dicomhandler uses DICOM files that belongs to different stages of treatment planning (structures, dose, and plan), by grouping the files of a patient in a single object. DICOM objects have to be created with [Pydicom](https://pydicom.github.io/pydicom/stable/). Also, it allows for the extraction of related information, such as the Cartesian coordinates of structures and multileaf collimator (MLC) positions for each control point in the treatment plan. This is achieved by using the `Dicominfo` class. It receives as input the DICOM radiotherapy structures (RS), dose (RD), and plan (RP) files (or a subset of these) and constructs a single object that contains all the information for a patient.

Dicomhandler is built on [NumPy](https://numpy.org/). NumPy provides an efficient implementation of numerical computations in a high-level language like Python but completely compiled in C, resulting in a significant improvement in speed and code that is clear and easy to maintain.

## Table of Contents
* [Features](#id1)
* [Examples](#id2)
* [Access](#id4)
* [Open and run the project](#id5)
* [Libraries and pre-requisites](#id6)
* [Authors](#id9)
* [License](#id10)
* [Project Status](#id11)
* [Room for Improvement](#id12)
* [Acknowledgements](#id13)
* [More information for potential applications](#id14)
* [Expressions of gratitude](#id15)
<!-- * [License](#license) -->

## Features
The functionalities provided by the package could be divided into three main categories.

- **File transformation:** To modify the files’ information in some
  meaningful way.

- **Format conversion:** DICOM files are neither optimized for data analysis, nor straightforward review by clinical staff, but for hardware. For that reason, the package provides means for both scientific manipulation of data and effortless conversion to clinical-friendly formats.

- **Report data:** To summarize different DICOM files, or even about the comparison between files.

## Examples

### Register DICOM files
It is required to operate on a DICOM object by [Pydicom](https://pydicom.github.io/pydicom/stable/). You can use the DICOM files examples by default in the [repository](https://github.com/alxrojas/dicom2handle/tree/main/Examples)).

You can construct an object with different DICOM files from the same patient as:
```python
di = Dicominfo(dicom_structure, dicom_plan)
```

### Anonymize the information
You can choose the information that it has to be anonymized:
```python
di.anonymize(name=True, birth=True, operator=False, creation=False)
```

### Expand or contract margins
You can expand or subtract margins for a single structure. If you want to expand, the input parameter must be positive. Otherwise, negative.
```python
expanded = di.add_margin('5 GTV', 1.5)
contracted = di.add_margin('5 GTV', -1.5)
```

### Rotate or translate
You can [rotate](https://simple.wikipedia.org/wiki/Pitch,_yaw,_and_roll) or [translate](https://en.wikipedia.org/wiki/Transformation_matrix) a structure (organ or lesion) in an specific direction with respect to an arbitary point or to the isocentre. The keys are: roll, pitch, and yaw (for rotations) and x, y, and z (for translations).

For the isocenter:
```python
di_rotated = di.displace('5 GTV', 0.5, 'pitch')
di_translated = di.displace('5 GTV', 1.0, 'x')
```
Or for an arbritary point:
```python
di_rotated = di.displace('5 GTV', 0.5, 'pitch', [4.0, -50.0, 20.0])
di_translated = di.displace('5 GTV', 1.0, 'x', [4.0, -50.0, 20.0])
```

### Information in dataframe
A dataframe is generated with the main information of the plan and structures, relevant for clinical statistics. By defaults, the dataframe is created for all targets' name from the plan file. Also, you can obtain the calculated areas of multileaf collimator (MLC) modulation.

To obtain general plan information:
```python
di.info_to_dataframe(area=False)
```
To obtain the MLC areas:
```python
di.info_to_dataframe(area=True)
```

### CSV files
A csv file is generated in the current directory with some information.

#### Structures
 The output file provides the information on the coordinates (x, y, z) of all or some structures of a patient. By default the report is generated for all structures.

For all structures this process takes several minutes.
```python
di.dicom_to_csv(structure=True, mlc=False, structures = [])
```
Or you can select some structures to obtain the excel file:
```python
di.dicom_to_csv(structure=True, mlc=False, structures = ['Structure1', 'Structure2'])
```
Also, the output file can provide the information of gantry angle, gantry direction, table angles, and MLC positions for each checkpoint.
```python
di.dicom_to_csv(structure=False, mlc=True)
```

## Access
We encourage the practice of using virtual environments to avoid dependency incompatibilities. The most convenient way to do this, is by using virtualenv, virtualenvwrapper, and pip.

### Install with pip
After setting up and activating the virtualenv, run the following command:
```console
pip install dicomhandler
```
### Install the development version
In case you’d like to be able to update the package code occasionally with the latest bug fixes and improvements, see the source code, or even make your own changes, you can always clone the code directly from the repository:
```console
git clone https://github.com/alxrojas/dicomhandler
cd dicomhandler
pip install -e .
```

## Open and run the project
Run the project as:
```python
from dicomhandler.dicom_info import Dicominfo
from dicomhandler.report import report
```

## Libraries and pre-requisites
The dependencies of the package, that will be automatically installed with the software, are the following:

- [numpy](https://numpy.org/): Data analysis and calculation.
- [pandas](https://pandas.pydata.org/): Report statistics.
- [pydicom](https://pydicom.github.io/pydicom/stable/): DICOM file reader.
- [xlsxwriter](https://pypi.org/project/XlsxWriter/): Write information.

## Authors
- [Alejandro Rojas](https://github.com/alxrojas)
- [Jerónimo Fotinós](https://github.com/JeroFotinos)
- [Nicola Maddalozzo](https://github.com/nicolaMaddalozzo)

## License
This project is licensed under (MIT) - Look the file [LICENSE.md](https://github.com/alxrojas/dicomhandler/blob/main/LICENSE) for details.

## Project Status
Version 0.0.1a1 is _complete_

## Room for Improvement
For future work and improvement:
- A method to provide the assignment of variable margin to a lesion.
- A method to evaluate the dose-volume histogram for the displaced structures.
- The possibility to deform structures.

## Acknowledgements
Many thanks to
- Daniel Venencia, PhD. and Instituto Zunino to provide the resources and the access to data.
- Juan Cabral, PhD. to evaluate and review this project.

## More information for potential applications
- [Beltrán et al. Radiat and Onc (2012)](https://www.sciencedirect.com/science/article/abs/pii/S0167814011003240)
- [Rojas López et al. Phys Med (2021)](https://www.sciencedirect.com/science/article/abs/pii/S1120179721002131)
- [Venencia et al. J Rad in Pract (2022)](https://www.cambridge.org/core/journals/journal-of-radiotherapy-in-practice/article/abs/rotational-effect-and-dosimetric-impact-hdmlc-vs-5mm-mlc-leaf-width-in-single-isocenter-multiple-metastases-radiosurgery-with-brainlab-elements/EFBC35342D49298190BA8381BC729AB1)
- [Zhang et al. SpringerPlus (2016)](https://springerplus.springeropen.com/articles/10.1186/s40064-016-1796-2)

## Expressions of gratitude
* Tell others about this project.
* Cite our project in your paper.
* Invite someone from the team a beer or a coffee.
* Give thanks publicly.
