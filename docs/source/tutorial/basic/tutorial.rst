========
Tutorial
========

-----------------------
**General information**
-----------------------

In this section, we introduce methods and functionalities of the dicomhandler package.
Its goal is to handle, convert and report data summaries about different DICOM files related to radiation therapy.
DICOM (Digital Imaging and Communications in Medicine) is a format that is used for viewing, storing, sharing and
retrieving medical images of a patient. The medical images can have different modalities, such as:

1. **RT Dose (Radiotherapy Dose):** It contains the patient medical images that describe 2D or 3D radiation dose data,
   generated from treatment planning systems or similar devices. This modality helps the medical staff to view the old
   radiation dose data and storing the new ones.

2. **RT Plan (Radiotherapy Plan):** It contains the patient medical information related to the treatment plans.
   These images help the physicists to control if the requirements for transferring radiation therapy plans
   between devices are satisfied. The images are related, for example, to the positions of the multileaf collimator
   (MLC) during the radiotherapy treatment.

3. **RT Structure (Radiotherapy Structure):** It contains the patient medical information of the structures of
   interest (body, organs and lesions) and related data. This modality includes contour data for the regions of interest
   (ROIs) of the structures. They are relevant to radiation treatment planning.

.. note::

      There are types of DICOM files that are not treated such as computed tomography (CT) and magnetic resonance (MRI)
      images. Future releases will aim to give support also with other type of DICOM files. We can see a complete list here_.

.. _here: https://dicom.innolitics.com/ciods/

The core of our package is the class ``DicomInfo``. The class can be instantiated by means of ``pydicom`` objects
that contain the DICOM files described above. From a practical point of view, a Dicominfo object can be instantiated 
with zero and up to three ``pydicom`` objects that represents the three DICOM files. The goals of the class are the managing, 
format converting and the reporting of data summaries about the ``pydicom`` objects contained in the class.

The ``report`` method, that is not contained in the class ``DicomInfo``, is used for generating a excel file that contains information
about RT Structure file. The *datasets* folder, that contains some DICOM files, is in the directory package
*folder -> docs -> source -> tutorial -> datasets*.

---------------
Dicominfo class
---------------
Now we describe how this ``DicomInfo`` stores, manages and converts DICOM files.

Storing DICOM
-------------

We read the DICOM file before storing it in a instance of ``DicomInfo`` class. The first thing to do, before
storing a DICOM file, is reading it. In order to read it, we import ``os`` package (used for retrieving 
the path in which are the DICOM files) and ``pydicom`` package_ (used for reading a DICOM file). The extension
of a DICOM file is .dcm. In the following example, the variable *patient.dicom_struct* contains a RT Structure. 
The type of this variable is pydicom.dataset.FileDataset.

.. _package: https://pydicom.github.io/pydicom/stable/

.. code-block:: python

      >>> import os
      >>> import pydicom


      >>> path = os.getcwd() 
      >>> dicom_structure_path = str(path) + '/datasets/structure/RS_0.dcm'
      >>> patient_dicom_struct = pydicom.dcmread(dicom_structure_path)
      ...

Now, we can create a instance of ``DicomInfo``. The name of this instance is *di*. For creating a instance of the
class, we need at least one of the three DICOM files described at the beginning of the section. We import
``DicomInfo`` as follows:

.. code-block:: python

      >>> from dicomhandler.dicom_info import DicomInfo


      >>> di = DicomInfo(patient_dicom_struct)
      ...

At this point, *di* stores the RT Structure. For example, we can retrieve the name of the patient:

.. code-block:: python

      >>> di.dicom_struct.PatientName
      'PatientName'
      ...

and the name of the second structure (organ or lesion) of this patient:

.. code-block:: python

      >>> di.dicom_struct.StructureSetROISequence[1].ROIName
      '5 PTV +1.0 mm'
      ...

We can start to see the methods that handling and converting the DICOM files. The methods that
manage this type of DICOM file are ``anonymize``, ``move`` and ``add_margin``.
All these methods can modify the information of the patient's structures.

The object *di.dicom_struct.StructureSetROISequence* contains all the names of the structures.
Its type is *pydicom.sequence.Sequence*. Each element of this sequence is a *pydicom.dataset.Dataset*
``pydicom`` object. We can extract, for example, the name of the third structure.
The third structure has index 2 inside the sequence:

.. code-block:: python

      >>> di.dicom_struct.StructureSetROISequence[2].ROIName
      'Hippocampus Righ'
      ...

The object *di.dicom_struct.ROIContourSequence* contains all the spatial coordinates of the structures.
Its type is *pydicom.sequence.Sequence*. Each element of this sequence is a *pydicom.dataset.Dataset*,
so each structure's coordinates are contained in this type of ``pydicom`` object. We can see a structure
as a 3D object, and so each structure is represented by a certain number of slices in 2D. Each element
of *di.dicom_struct.ROIContourSequence* has an attribute called *ContourSequence*. This attribute is a
*pydicom.sequence.Sequence* as well. Each element of this sequence is a *pydicom.dataset.Dataset*, and
contains the contour data for a particular slice.

For example, we can extract the coordinates of the second structure for its second slice (the output is ommited
due to is large).

.. code-block:: python

      >>> di.dicom_struct.ROIContourSequence[1].ContourSequence[1].ContourData
      ...

The contour data of a slice is a sequence of points in three dimension represented in the format
[x0, y0, z0, x1, y1, z1, ...]. For each slice, the z-dimension is fixed.

Handling DICOM
--------------
With the ``anonymize`` method, we can overwrite the private information of the patient such as its name, its
birthday, the operator name that made the radiotherapy treatment and the creation date of the file (that
correspond sometimes to the date of the treatment). For each of these attributes, we can decide which one to
anonymize setting it to True or False. For example, we can anonymize only the patient's birthday. We can see the
birthday before and after the anonymization:

.. code-block:: python

      >>> di_anony = di.anonymize(name=False, birth=True, operator=False, creation=False)
      >>> print(di.dicom_struct.PatientBirthDate)
      '19571018'
      >>> print(di_anony.dicom_struct.PatientName)
      '19720101'
      # This date corresponds to the creation date of the CT device.
      ...

The method ``move`` could perform a rotation_ in pitch, yaw or roll directions of a structure.

.. _rotation: https://en.wikipedia.org/wiki/Aircraft_principal_axes

The instance *di_rotate* will contain the rotated coordinates of the second structure of the DICOM file. We can
extract the rotated structure's coordinates of the first slice (the output is ommited due to is large).

By default, rotations are performed for the isocentre (that is the last structure of the sequence
of *di.dicom_struct.ROIContourSequence*) but they can be performed with respect to an arbitrary point defined
by the user. For example, we want to perform a roll rotation of the second structure by 20º.

.. code-block:: python
      
      >>> struct_name = di.dicom_struct.StructureSetROISequence[1].ROIName
      >>> # Roll rotation of 20.0º in the isocentre
      >>> di_rotate = di.move(struct_name, 20.0, 'roll')
      >>> di_rotate.dicom_struct.ROIContourSequence[1].ContourSequence[1].ContourData

      >>> # For a rotation in an arbritary point
      >>> point = [4.0, -1.2, 100.8]
      >>> di_rotate = di.move(struct_name, 20.0, 'roll', point)
      >>> di_rotate.dicom_struct.ROIContourSequence[1].ContourSequence[1].ContourData
      ...


The ``move`` method is used for displacing a structure along the axes x, y or z. By default, translations
are performed for the isocentre (that is the last structure of the sequence *di.dicom_struct.ROIContourSequence*)
or an arbitrary point defined by the user.

For example, we want to make a translation by 2.0 mm of the second structure along x:

.. code-block:: python

      >>> # x translation of 2.0 mm in the isocentre
      >>> struct_name = di.dicom_struct.StructureSetROISequence[1].ROIName    
      >>> di_translate = di.move(struct_name, 2.0, 'x')
      ...

With the ``add_margin`` method, we can increase/decrease the margin of a specific structure. The
increasing/decreasing of a structure is in mm. We can see the coordinates of original and increased structure first
slice (the output is ommited due to is large).

For example, we can increase the second structure by a margin of 2 mm:

.. code-block:: python

      >>> # Increase the margin in 2.0 mm
      >>> struct_name = di.dicom_struct.StructureSetROISequence[1].ROIName
      >>> di_increased = di.add_margin(struct_name, 2.0)

      >>> # Decrease the margin in 2.0 mm
      >>> di_decreased = di.add_margin(struct_name, -2.0)
      ...

As we have seen, the extraction of the contour data from ``DicomInfo`` object is a bit trivial. The ``DicomInfo``
instance *di* is created using a RT Structure *patient.dicom_struct*. All the information of the RT Structure
are inside the di:

.. code-block:: python

      >>> di.dicom_struct.ROIContourSequence[1].ContourSequence[1].ContourData == \
      ... patient_dicom_struct.ROIContourSequence[1].ContourSequence[1].ContourData
      True

      >>> di.dicom_struct.PatientName == patient_dicom_struct.PatientName
      True
      ...

Format conversion
-----------------

For simplifying the extraction of information from RT Structure and RT Plan, we use the methods
``struct_to_csv``, ``mlc_to_csv``, and ``summarize_to_dataframe`` of ``DicomInfo``. With these methods, we
want to give the user a way to better structure the information contained in RT Structure and RT Plan.
Now, we want to instance a ``DicomInfo`` object which also contains RT Plan. The RT Structure and RT Plan must
refer to the same patient. The ``pydicom`` object *patient.dicom_plan* contains the information of RT Plan.

.. code-block:: python
      
      >>> path = os.getcwd()
      >>> dicom_structure_path = str(path) + '/datasets/structure/RS_0.dcm'
      >>> # RT structure
      >>> patient_dicom_struct = pydicom.dcmread(dicom_structure_path)
      >>> dicom_plan_path = str(path) + '/datasets/plan/RP_0.dcm'
      >>> # RT plan
      >>> patient_dicom_plan = pydicom.dcmread(dicom_plan_path)
      >>> di = Dicominfo(patient_dicom_struct, patient_dicom_plan)
      ...

Now, *di* stores the information that were in *patient.dicom_struct* and *patient.dicom_plan*.

The ``struct_to_csv`` method extracts the information of the cartesian coordinates (relative positions)
for all or some structures. The output file provides the coordinates of each structure in its own sheet.

For example, we want to extract the information for the second and third structure. The method return a file
as follows:

.. code-block:: python

      >>> struct_name_1 = di.dicom_struct.StructureSetROISequence[1].ROIName
      >>> struct_name_2 = di.dicom_struct.StructureSetROISequence[2].ROIName
      >>> # The output file has the name: name_file.csv
      >>> di.struct_to_csv('name_file', names = [struct_name_1, struct_name_2])
      ...

The RT Plan contains information about multileaf collimator (MLC) positions, control points, gantry angles,
gantry orientation and patient table angle. A visualization of MLC device is shown in the next link_.

.. _link: https://en.wikipedia.org/wiki/Multileaf_collimator

The MLC modulates the photon beam that passes through the collimator by irregular shapes created by the
leaves. The photom beam irradiates the lesions of the patient. The gantry_ is the mechanical support for
delivering the photon beam. The gantry is able to move with respect to the isocentre.

.. _gantry: https://en.wikipedia.org/wiki/Gantry_(medical)

During a radiotherapy treatment, a lot of information about the gantry movements and leaves of MLC are
stored in the RT Plan. During a treatment, we have a lot of differents movements of gantry, collimator,
MLC, and table. For each movement, we have some control points in which we save the information about the
MLC leaves positions, gantry angles, gantry orientation and table angle.

The ``mlc_to_csv`` method extracts these information. It returns a file as follows:

.. code-block:: python
      
      >>> # The output file has the name: name_file.csv
      >>> di.mlc_to_csv('name_file')
      ...

The ``summarize_to_dataframe`` method extracts information about the RT Plan of a patient.
It returns all the information about the lesions/organs structures that are contained in the RT Plan.
This information is prescribed dose, reference points, dose to references points, maximum, minimun, and
mean radius, the mass centre and distance to isocentre.

This method searches the information in the RT Structure that correspond to the structures in the RT
Plan. This information is represented in a DataFrame as follows:

.. code-block:: python
      
      >>> df = di.summarize_to_dataframe(area=False)
      ...

Also, the ``summarize_to_dataframe`` method extracts the areas of the irregular forms created by the MLC leaves
during a treatment for each control control for each beam. It returns a pandas DataFrame.

.. code-block:: python

      >>> df_areas = di.summarize_to_dataframe(area=True)
      ...

Reporting data
--------------
The ``report`` method performs a comparison between the a structure in two states (for example,
non-displaced and displaced) of a single patient. This method provides some metrics such as the maximum,
minimum, and mean displacement between the structure in both states. Also, the maximum, minimum, and mean
radius of the structure is reported.

For example, if we consider the third structure and we rotate it 5.0º in yaw direction:

.. code-block:: python

      >>> import pydicom

      >>> from dicomhandler.dicom_info import DicomInfo
      >>> from dicomhandler.report import report
      

      >>> path = os.getcwd()
      >>> dicom_structure_path = str(path) + '/datasets/structure/RS_0.dcm'
      >>> patient_struct = pydicom.dcmread(dicom_structure_path)
      >>> di = Dicominfo(patient_struct)
      >>> struct_name = di.dicom_struct.StructureSetROISequence[2].ROIName
      >>> di_rotated = di.move(struct_name, 5.0, 'yaw')
      >>> report(di_1, di_rotated, struct_name)
      Parameter	Value [mm]
      0	Max radius	21.828
      1	Min radius	0.704
      2	Mean radius	12.412
      3	STD radius	4.775
      4	Variance radius	22.802
      5	Max distance	5.833
      6	Min distance	2.734
      7	Mean distance	4.454
      8	STD distance	0.800
      9	Variance distance	0.640
      10    Distance between center mass	4.119
      ...
