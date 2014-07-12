=========
Safe File
=========

Part of the
`Using JSON Schema <http://usingjsonschema.github.io>`_
project.

Robust storage using text files is enhanced with support for automated recovery
should an update fail. 

This library provides support for reading and writing files in a recoverable
mode, allowing automated recovery when the program restarts. Normal file
read / write is also supported, enabling a common interface for both files
using automated recovery capabilities and those not using them.

.. image:: https://travis-ci.org/usingjsonschema/ujs-safefile-python.svg?branch=master
    :target: https://travis-ci.org/usingjsonschema/ujs-safefile-python

API
---

readFile
--------

Read a file synchronously from a file system.

**readFile** (filename)

|    arguments:
|        filename *string* Name of file to read (path optional)  
|
|    raises *SafeFileError*  
|    returns *string* Data read

.. code:: python

    data = readFile (filename)

writeFile
---------

Write a file synchronously to a file system.

**writeFile** (filename, data)

| arguments:
|     filename *string* Name of file to write (path optional)  
|     data *string* Data to write to the file
|
| raises *SafeFileError*

.. code:: python

    writeFile (filename, data)

safeReadFile
------------

Read a file synchronously from a file system, inspecting the file system state
and performing recovery processing if needed.

**safeReadFile** (filename)

| Arguments:
|     filename *string* Name of file to read (path optional)  
|
| raises *SafeFileError*  
| returns *string* Data read

.. code:: python

    data = safeReadFile (filename)

safeWriteFile
-------------

Write data to a file synchronously, using a recoverable set of steps. Should
the write processing fail to complete, auto-recovery can perform the steps
required to bring the file content back to a stable state.

**safeWriteFile** (filename, data)

| Arguments:
|     filename *string* Name of file to write (path optional)  
|     data *string* Data to write to the file  
|
| raises *SafeFileError*

.. code:: python

    safeWriteFile (filename, data)

safeGetState
------------

Get the current state of the set of files representing the current file
system contents. Returns one of,

- SAFE_NORMAL, normal state, base and backup files only present
- SAFE_RECOVERABLE, partial write condition that is automatically recoverable
  the next time a read, write or recover function is called
- SAFE_INTERVENE, last write failed before the data being written reached
  a recoverable state. Manual intervention is required if recovery of the last
  write is required, otherwise auto-recovery will recover to the prior stable
  state.

**safeGetState** (filename)

| Arguments:
|     filename *string* Name of file to check (path optional)
|
| returns *integer* State value (SAFE_NORMAL, SAFE_RECOVERABLE or 
  SAFE_INTERVENE) or a file error (INVALID_NAME, DOES_NOT_EXIST or
  IS_NOT_A_FILE)

.. code:: python

    state = safeGetState (filename)

safeRecover
-----------

Initiate the auto-recovery process. This follows the same steps as
``safeReadFile`` follows, but can be called independently.

**safeRecover** (filename)

| Arguments:
|     filename *string* Name of file to recover (path optional)
|
| raises *SafeFileError*

.. code:: python

    safeRecover (file)

SafeFileError
-------------

**SafeFileError** (code, message)

| Arguments:
|    code *integer* Error code (from list below)
|    message *string* Text message associated with code

Constants for the error codes,

- NO_ERROR
- INVALID_NAME
- DOES_NOT_EXIST
- IS_NOT_A_FILE
- READ_ERROR
- WRITE_ERROR
- SAFE_NORMAL
- SAFE_RECOVERABLE
- SAFE_INTERVENE

Installation
------------

The program can be installed using ``pip``, with the command,

.. code:: bash

    pip install ujs-safefile

License
-------

MIT
