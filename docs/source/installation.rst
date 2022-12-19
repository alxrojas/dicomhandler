Installation
============


This is the recommended way to install Dicomhandler.

Installing  with pip
^^^^^^^^^^^^^^^^^^^^

.. note::

   We encourage the practice of using virtual environments to avoid dependency incompatibilities. The most convenient way to do this, is by using virtualenv, virtualenvwrapper, and pip.

After setting up and activating the virtualenv, run the following command:

.. code-block:: console

   $ pip install dicomhandler
   ...




Installing the development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In case you'd like to be able to update the package code occasionally with the
latest bug fixes and improvements, see the source code, or even make your own changes, you can always clone the code directly from the repository. To do that, follow these instructions.

First, make sure that you have Git installed and that you can run its commands from a shell.
(Enter *git help* at a shell prompt to test this.)

In order to download the code from the main branch of the repository, the next terminal command will create a folder with the code in your current directory.

.. code-block:: console

   $ git clone https://github.com/alxrojas/dicomhandler
   ...


Then, you can install the package as edditable by doing

.. code-block:: console

   $ cd dicomhandler
   $ pip install -e .
   ...

While a regular installation just enables you to use the package as it was download, an editable installation allows you to modify the source code and have the changes immediately available to use, without needing extra steps.