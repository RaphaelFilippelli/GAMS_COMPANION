# GAMS Python API Documentation (v49)

Complete documentation for the GAMS Python API, converted from HTML to clean Markdown for optimal consumption by Large Language Models including ChatGPT.

## Table of Contents

1. API: Overview
2. API: Getting Started
3. API: Control
4. API: Gamstransfer
5. API: Gamstransfer Main Classes
6. API: Gamstransfer Additional Topics
7. API: Magic
8. User Guide: Gamsconnect
9. T Main
10. Engine Api
11. Class: gams .Control .Database .Gamsdatabase
12. Class: gams .Control .Database .Gamsdatabase Members
13. Class: gams .Control .Database . Gamssymbol
14. Class: gams .Control .Database . Gamssymbol Members
15. Class: gams .Control .Execution .Gamsjob
16. Class: gams .Control .Execution .Gamsjob Members
17. Class: gams .Control .Execution .Gamsmodelinstance
18. Class: gams .Control .Execution .Gamsmodelinstance Members
19. Class: gams .Control .Execution .Symbolupdatetype
20. Class: gams .Control .Execution .Symbolupdatetype Members
21. Class: gams .Control .Options .Gamsoptions
22. Class: gams .Control .Options .Gamsoptions Members
23. Class: gams .Control .Workspace .Debuglevel
24. Class: gams .Control .Workspace .Debuglevel Members
25. Class: gams .Control .Workspace .Gamsworkspace
26. Class: gams .Control .Workspace .Gamsworkspace Members

---

## 1. API: Overview

# Python API
The GAMS API is a Python package that contains several sub-modules that enable the control of the GAMS system as well as the movement of data between GAMS and Python. Currently the API supports the Python versions 3.9 to 3.13. The following table gives an overview of all available sub-modules:

Sub-Module | Description
---|---
[connect](UG_GAMSCONNECT.html) | Used primarily by GMSPython to digest YAML syntax to Extract, Transform and Load (ETL) data into GAMS, but can be used in native Python environments.
[control](API_PY_CONTROL.html) | Enables full control of the GAMS System
[core](API_MAIN.html#GAMS_LLAPIS) | Core GAMS API tools used to connect to GDX, GMD, GMO and other GAMS objects. Requires expert level knowledge.
[engine](https://www.gams.com/engine/engine-api.html) | GAMS Engine API (OpenAPI compliant), manages jobs with GAMS Engine
[magic](API_PY_MAGIC.html) (beta) | Enables the use of GAMS from within Jupyter notebooks
[tools](T_MAIN.html#GAMS_TOOLS_LIBRARY) (beta) | Code base for the GAMS tools library
[transfer](API_PY_GAMSTRANSFER.html) | Data Only API – Allows GAMS data to be maintained outside a GAMS script

**Note:** Due to compatibility issues the GAMS Python API does not work with the Python interpreter from the Microsoft Store.

To install the API please visit: [Getting Started](API_PY_GETTING_STARTED.html).

# Migrate import statements
With the release of GAMS 42 the GAMS Python ecosystem has been restructured – the new structure has many benefits (easier/safer (un)installs, cleaner module namespaces, etc.).

**Attention:** The new API structure cannot be used to simply "update" previous versions – users should build new python environments from scratch before attempting to install.

Restructuring of the GAMS python API ecosystem was confined to the creation of the new nested structure – class, method and other variables names were not modified. The import statements in legacy code will need to be updated if using the new system. Best practice will be to use the new package structure to import different sub-modules as needed (and avoid `from <module_name> import *` syntax). We provide a mapping between the old syntax and the new to aid in the transition to the new API structure:

Old `import` statement | New `import` recommendation(s)
---|---
`from gams import GamsWorkspace` | `from gams import GamsWorkspace`
`from gams import *` | `import gams`
`from gdxcc import *` | `from gams.core import gdx`
-or-
`import gams.core.gdx as gdx`
`from optcc import *` | `from gams.core import opt`
-or-
`import gams.core.opt as opt`
`import gamstransfer as gt` | `from gams import transfer as gt`
-or-
`import gams.transfer as gt`
`import gams_engine` | ‘import gams.engine’

**Note:** Jupyter users will need to migrate their `reload_ext gams_magic` -> `reload_ext gams.magic` and `load_ext gams_magic` -> `load_ext gams.magic`

## Testing for Old vs New API
Users may be running the same python code with different versions of the Python API. If this is the case, it might be beneficial to include conditional import statements. It is possible to test for the GAMS major version number with the `GamsWorkspace.api_major_rel_number` property:

from gams import GamsWorkspace

if GamsWorkspace.api_major_rel_number<42: # old API structure

import gdxcc as gdx

from gams import *

import gamstransfer as gt

else: # new API structure

import gams.core.gdx as gdx

from [gams.control](apis/python/classgams_1_1control_1_1database_1_1__GamsSymbol.html) import *

import gams.transfer as gt

[gams::control](apis/python/classgams_1_1control_1_1database_1_1__GamsSymbol.html)

**Attention:** While conditional import statements can be helpful, users are strongly encouraged to modify their code to use the new structure.

# GAMS Python API Structure
```
    gams
    â
    âââ connect (previously: gams_connect)
    â
    âââ control (previously: gams)
    â
    âââ core (new)
    â    âââ gdx (previously: gdxcc)
    â    âââ gmd (previously: gmdcc)
    â    âââ opt (previously: optcc)
    â    âââ idx (previously: idxcc)
    â    âââ dct (previously: dctmcc)
    â    âââ gmo (previously: gmomcc)
    â    âââ gev (previously: gevmcc)
    â    âââ cfg (previously: cfgmcc)
    â    âââ emp (previously: emplexer, empyacc)
    â    âââ embedded (previously: gamsemb)
    â
    âââ engine (previously: gams_engine)
    â
    âââ magic (previously: gams_magic)
    â
    âââ transfer (previously: gamstransfer)
```

---

## 2. API: Getting Started

### Table of Contents
* Verify Conda Installation
* Create a New Conda Environment
* Install
* macOS Compatibility
* Apple M1/M2
* Verify the GAMS API
* Uninstall the GAMS API
* Remove Conda Environment
* Other Useful Conda Commands
* Python Virtual Environment (venv)
* Working with Python and multiple GAMS Installations
* A note on using Python site package

Users have many options to manage their Python installation; in many cases it is advantageous to create a Python "environment" to sandbox an instance of Python (something which can be done with `venv` or `conda`). We recommend that users download a version of [`miniconda`](https://docs.conda.io/en/latest/miniconda.html). We direct users to the `conda` documentation for installation issues. After the user has installed `miniconda` (or `conda`) we will:
* Verify that `conda` is working
* Create a new scratch Python environment
* Enter the new environment and verify the `python` version
* Install the GAMS API with `pip`

**Note:** `miniconda` and `conda` are synonymous – both are package + environment managers – however, `conda` comes preloaded with a number of useful data science-related packages. We emphasize `miniconda` because of the smaller install size. The terminal commands we used here apply to both `miniconda` and `conda` versions. The remaining documentation will only use the term `conda`.

**Attention:** The new API structure cannot be used to simply "update" previous versions – users should build new Python environments from scratch before attempting to install.

# Verify Conda Installation
To verify that `conda` is accessible from the terminal we simply need to check for the version number. Your version of `conda` may differ. The installation of the GAMS API does not depend on the `conda` version.
```
    $  conda --version
    conda 22.9.0
```

# Create a New Conda Environment
`Conda` can create, manage, and delete Python environments easily – this flexibility allows users to experiment quickly with different tools. If experiments fail, the entire environment can be removed without damaging the rest of the system. In short, each `conda` environment is an isolated sandbox. We will now create a new `conda` environment called `gams` that we will used when installing the GAMS API.

**Note:** Best practice is to use an environment rather than install into conda's base environment
```
    $  conda create --name gams python=3.10
    [verbose conda output]
    #
    # To activate this environment, use
    #
    #     $ conda activate gams
    #
    # To deactivate an active environment, use
    #
    #     $ conda deactivate
    Retrieving notices: ...working... done
    $
```

**Note:** It is necessary to specify the version of Python to install into the new `conda` environment. The GAMS API currently supports Python 3.9 to 3.13.

We must now "activate" the `conda` environment (i.e., enter the Python sandbox).
```
    $  conda activate gams
    (gams)$
```

Once in the activated environment we should verify the Python version is the one that was specified at creation.
```
    (gams)$  python --version
    Python 3.10.8
```

# Install
The GAMS Python API is distributed through the [Python Package Index](https://pypi.org/project/gamsapi/). The `gamsapi` package comes with several install options (via `pip` `extras`) that change how dependencies are resolved. `pip` will not install any third-party dependencies if an `extra` label was not provided. For example, to install the `transfer` data tool (and its dependencies to `pandas` and `scipy`).
```
    (gams)$  pip install gamsapi[transfer]==xx.y.z
```

**Note:** `xx.y.z` represents your installed GAMS version number (e.g., 49.6.1). To specifically install a `gamsapi` release candidate (released with a GAMS beta version) the user will need to use the pattern `xx.0.0rcN`, where `N` is the number of the release candidate.

The `extras` that are available for the GAMS Python API are:

`extra` | Third-party Dependencies to Install
---|---
`connect` | `pandas`, `pyyaml`, `openpyxl`, `sqlalchemy`, `cerberus`, `pyodbc`, `psycopg2-binary`, `pymysql`, `pymssql`
`control` | `certifi`, `urllib3`
`core` | `ply`, `numpy`
`engine` | `python_dateutil`, `urllib3`
`magic` | `ipython`, `pandas`
`tools` | `pandas`
`transfer` | `pandas`, `scipy`
`all` | installs all third-party dependencies for all sub-modules – a complete install

**Attention:** Users can chain several `extras` together (separated by commas) in one `pip` install command to install dependencies from several sub-modules at once.

**Note:** On certain platforms `psycopg2-binary` needs to be built from source (e.g. for Python 3.13 on Windows and for Python 3.9 on macOS on ARM64). This requires additional build dependencies that might need to be installed manually.

# macOS Compatibility
The default shell for macOS 10.15+ (Catalina) is `zsh`. Users that wish to install the `gamsapi` will need to modify their install syntax slightly (note the quotations).
```
    (gams)$  pip install 'gamsapi[transfer]'==xx.y.z
```

**Note:** `xx.y.z` represents your installed GAMS version number (e.g., 49.6.1)

## Apple M1/M2
Apple users that have a M1/M2 (`arm`) chipset must be careful to match build architectures (i.e., `x86` or `arm`) of both the GAMS system and miniconda (Python). Ideally, M1/M2 users will only install native `arm` compatible programs. Apple's Rosetta 2 does allow users to install and run `x86` compiled programs on M1/M2. However, mixed installations (i.e., an `arm` GAMS system but a `x86` miniconda or vice versa) will fail because the `gamsapi` will not be able to properly load the necessary shared libraries.

The `gams audit` tool will return the GAMS build architecture (`x86` or `arm` will be in the returned string):
```
    (gams)$  gams audit
    GAMSX            45.1.0 88bbff72 Oct 14, 2023          DAC arm 64bit/macOS
```

The build architecture of the Python installation is available with the following command:
```
    (gams)$  python -c "import platform; print(platform.processor())"
    arm
```

**Attention:** The user must reinstall either a GAMS or Python system if these two returns do not match.

# Verify the GAMS API
`pip` provides feedback that suggests that the GAMS API was successfully installed, however, it is still wise to verify this. The best way to test is to actually create a short Python script that imports `gams`. The following 1 line will run an `import` operation and, if successful, will output the API version number. The API was not successfully installed if an import error is raised.
```
    (gams)$  python -c "import gams; print(f'API OK -- Version {gams.__version__}')"
    API OK -- Version 45.2.0
```

**Attention:** Example problems can be found in the `[PATH TO GAMS]/api/python/examples` folder (organized by sub-module).

# Uninstall the GAMS API
Removal of the GAMS API is straightforward with `pip`:
```
    (gams)$  pip uninstall gamsapi
    Found existing installation: gamsapi 45.2.0
    Uninstalling gamsapi-45.2.0:
      Would remove:
        /Users/gams_user/miniconda3/envs/gams/lib/python3.10/site-packages/gamsapi-45.2.0.dist-info/*
        /Users/gams_user/miniconda3/envs/gams/lib/python3.10/site-packages/gamsapi/*
    Proceed (Y/n)? y
      Successfully uninstalled gamsapi-45.2.0
```

# Remove Conda Environment
Removal of the entire `conda` environment is also straightforward with the following operations:
```
    (gams)$  conda deactivate
    (base)$  conda remove --name gams --all
    [verbose conda output]
    Proceed ([y]/n)? y

    Preparing transaction: done
    Verifying transaction: done
    Executing transaction: done
    (base)$
```

# Other Useful Conda Commands
Users are directed to the full `conda` [documentation](https://docs.conda.io/projects/conda/en/stable/) but some useful commands are provided here as a quick reference.

Conda Command | Description
---|---
`conda env list` | List all conda environments
`conda list` | List all installed packages in the active environment
`conda deactivate` | Deactivate the current Python environment
`conda remove --name XXX --all` | Remove the `XXX` environment, must be deactivated first
`conda install XXX` | Install package `XXX` with the conda system, not all packages can be installed from `conda` directly

# Python Virtual Environment (venv)
This documentation assumed users will want to use `conda` to manage their Python environments, but other tools such as `venv` can be used to manage separate Python environments. The details of the `venv` setup, activation, deactivation and removal differ from `conda`, but the `pip` install commands are the same as in `conda`. Interested users are referred to the official [`venv`](https://docs.python.org/3/library/venv.html) documentation for details on how to create a virtual environment. Users are also directed to additional documentation on: [`Installing packages using pip and virtual environments`](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#).

# Working with Python and multiple GAMS Installations
Some users may want to run multiple versions of GAMS on their system – we recommend that users create separate Python environments in order to compare the behavior between versions of the Python API.

# A note on using Python site package
Previous API versions could be used by a Python interpreter if the path to the API directory was included in a `sitecustomize.py` script that resided in the `site-packages` directory. This type of installation allows customized packages to be found and used, but not necessarily copied into Python's directory structure. Previous versions of the API benefited from this type of installation, we recommend that users create a separate Python environment and actually install the GAMS API into the environment with `pip`. Users that were using the `sitecustomize.py` installation method might experience issues with `pip` installations if their Python finds an old `sitecustomize.py` file that includes a path to old GAMS API files (`pip` might report that the `requirement is already satisfied`). Users can find out where the `USER_SITE` directory is located by running the following command:
```
    (gams)$  python -m site
```

Once this directory has been found, it is necessary to remove all paths (in the `sitecustomize.py` file) that point to previous GAMS API folders and reattempt the `pip` install process.

---

## 3. API: Control

### Table of Contents
* Recommended Import
* Specifying a GAMS System Directory
* Important Classes of the API
* How to use the API
* How to import packages/modules from the GAMS control API (transport1.py)
* How to choose the GAMS system (transport1.py)
* How to export data to GDX (transport_gdx.py)
* How to import data from GDX (transport_gdx.py)
* How to run a GamsJob from file (transport1.py)
* How to retrieve a solution from an output database (transport1.py)
* How to specify the solver using GamsOptions (transport1.py)
* How to run a job with a solver option file and capture its log output (transport1.py)
* How to use include files (transport2.py)
* How to read data from string and export to GDX (transport3.py)
* How to run a job using data from GDX (transport3.py)
* How to run a job using implicit database communication (transport3.py)
* How to define data using Python data structures (transport4.py)
* How to prepare a GamsDatabase from Python data structures (transport4.py)
* How to initialize a GamsCheckpoint by running a GamsJob (transport5.py)
* How to initialize a GamsJob from a GamsCheckpoint (transport5.py)
* How to run multiple GamsJobs in parallel using a GamsCheckpoint (transport6.py)
* How to create a GamsModelInstance from a GamsCheckpoint (transport7.py)
* How to modify a parameter of a GamsModelInstance using GamsModifier (transport7.py)
* How to modify a variable of a GamsModelInstance using GamsModifier (transport7.py)
* How to use a queue to solve multiple GamsModelInstances in parallel (transport8.py)
* How to fill a GamsDatabase by reading from MS Access (transport9.py)
* How to fill a GamsDatabase by reading from MS Excel (transport10.py)
* How to create and use a save/restart file (transport11.py)

GAMS `control` is a sub-module of the Python API that allows for full control over the GAMS system (data, model instances, and solving). It can be used in conjunction with other Python API sub-modules (`numpy` and `transfer`) to boost performance when pushing/pulling data to/from a GAMS model. The `gams.control` package provides objects to interact with the General Algebraic Modeling System (GAMS). Objects in this package allow convenient exchange of input data and model results (`GamsDatabase`), help to create and run GAMS models (`GamsJob`), that can be customized by GAMS options (`GamsOptions`). Furthermore, it introduces a way to solve a sequence of closely related model instances in the most efficient way (`GamsModelInstance`).

A GAMS program can include other source files (e.g. $include), load data from GDX files (e.g. $GDXIN or execute_load), and create PUT files. All these files can be specified with a (relative) path and therefore an anchor into the file system is required. The base class GamsWorkspace manages the anchor to the file system. If external file communication is not an issue in a particular Python application, temporary directories and files will be managed by objects in the namespace.

With the exception of GamsWorkspace the objects in the `gams.control` package cannot be accessed across different threads unless the instance is locked. The classes themself are thread safe and multiple objects of the class can be used from different threads (see below for restrictions on solvers that are not thread safe within the GamsModelInstance class).

**Note:** If you use multiple instances of the GamsWorkspace in parallel, you should avoid using the same working directory. Otherwise you may end up with conflicting file names.

The GAMS `control` Python API lacks support for the following GAMS components: Acronyms, support for GAMS compilation/execution errors (GamsJob.run just throws an exception), structured access to listing file, and proper support for solver options.

Currently only Cplex, Gurobi, and SoPlex fully utilize the power of solving GamsModelInstances. Some solvers will not even work in a multi-threaded application using GamsModelInstances. For some solvers this is unavoidable because the solver library is not thread safe (e.g. MINOS), other solvers are in principle thread safe but the GAMS link is not (e.g. SNOPT). Moreover, GamsModelInstances are not available for quadratic model types (QCP, MIQCP, RMIQCP).

# Recommended Import
GAMS `control` is available with the following import statement once the API has been installed:
```
    >>> import gams
```

Other sub-modules must be imported with separate import statements.

## Specifying a GAMS System Directory
There are several ways to specify which system directory should be used. On all platforms, the system directory can be specified in the GamsWorkspace constructor. If no system directory is specified by the user, The API tries to find one automatically:
* Windows: Try to find a system directory in the Windows registry.
* Linux: Try to find a system directory in the `PATH` first. If none was found, search `LD_LIBRARY_PATH`.
* OS X: Try to find a system directory in the `PATH` first. If none was found, search `DYLD_LIBRARY_PATH`.

The environment variable `PATH` can be set as follows on Linux and macOS:

export PATH=<Path/To/[GAMS](apis/dotnet/namespaceGAMS.html)>:$PATH

[GAMS](apis/dotnet/namespaceGAMS.html)

**Note:** On Linux and macOS it is recommended to specify the `PATH` only instead of `(DY)LD_LIBRARY_PATH` since this might cause problems loading the correct version of certain modules (e.g. gdx).

# Important Classes of the API
This section provides a quick overview of some fundamental classes of the GAMS `control` API. Their usage is demonstrated by an extensive set of examples in the How to use the API section.
* [gams::control::workspace::GamsWorkspace](apis/python/classgams_1_1control_1_1workspace_1_1GamsWorkspace.html) Class
* [gams::control::execution::GamsJob](apis/python/classgams_1_1control_1_1execution_1_1GamsJob.html) Class
* [gams::control::database::GamsDatabase](apis/python/classgams_1_1control_1_1database_1_1GamsDatabase.html) Class
* [gams::control::options::GamsOptions](apis/python/classgams_1_1control_1_1options_1_1GamsOptions.html) Class
* [gams::control::execution::GamsModelInstance](apis/python/classgams_1_1control_1_1execution_1_1GamsModelInstance.html) Class

# How to use the API
The GAMS distribution provides several examples that illustrate the usage of the API. `[GAMSDIR]\api\python\examples\control` contains multiple examples dealing with the well-known [transportation problem](https://www.gams.com/products/gams/gams-language/#the-gams-language-at-a-glance). In further course of this tutorial we discuss these examples step by step and introduce new elements of the API in detail.

We recommend to open the aforementioned files to gain a complete overview of the examples. Down below we explain the examples with the help of selected code snippets.
* How to import packages/modules from the GAMS control API (transport1.py)
* How to choose the GAMS system (transport1.py)
* How to export data to GDX (transport_gdx.py)
* How to import data from GDX (transport_gdx.py)
* How to run a GamsJob from file (transport1.py)
* How to retrieve a solution from an output database (transport1.py)
* How to specify the solver using GamsOptions (transport1.py)
* How to run a job with a solver option file and capture its log output (transport1.py)
* How to use include files (transport2.py)
* How to read data from string and export to GDX (transport3.py)
* How to run a job using data from GDX (transport3.py)
* How to run a job using implicit database communication (transport3.py)
* How to define data using Python data structures (transport4.py)
* How to prepare a GamsDatabase from Python data structures (transport4.py)
* How to initialize a GamsCheckpoint by running a GamsJob (transport5.py)
* How to initialize a GamsJob from a GamsCheckpoint (transport5.py)
* How to run multiple GamsJobs in parallel using a GamsCheckpoint (transport6.py)
* How to create a GamsModelInstance from a GamsCheckpoint (transport7.py)
* How to modify a parameter of a GamsModelInstance using GamsModifier (transport7.py)
* How to modify a variable of a GamsModelInstance using GamsModifier (transport7.py)
* How to use a queue to solve multiple GamsModelInstances in parallel (transport8.py)
* How to fill a GamsDatabase by reading from MS Access (transport9.py)
* How to fill a GamsDatabase by reading from MS Excel (transport10.py)
* How to create and use a save/restart file (transport11.py)

## How to import packages/modules from the GAMS control API (transport1.py)
Before we can start using the GAMS `control` API, it needs to be installed by following the instructions from the [Getting Started](API_PY_GETTING_STARTED.html) section. Afterwards we can use the API by importing the `GamsWorkspace` class like this:

from gams import GamsWorkspace

Conventional Python packages/modules can by imported like that:

import os

import sys

## How to choose the GAMS system (transport1.py)
By default the GAMS system is determined automatically. In case of having multiple GAMS systems on your machine, the desired system can be specified via an additional argument when the workspace is created. If we type `python transport1.py` C:/GAMS/42 we use `GAMS 42` to run `transport1.py` even if our default GAMS system might be a different one. This is managed by the following code:

...

sys_dir = sys.argv[1] if len(sys.argv) > 1 else None

ws = GamsWorkspace(system_directory=sys_dir)

...

## How to export data to GDX (transport_gdx.py)
Although the GAMS `control` Python API offers much more than exchanging data between Python and GDX, a common use case is the export and import of GDX files. The central class for this purpose is GamsDatabase. We assume that the data to be exported is available in Python data structures.

...

plants = ["Seattle", "San-Diego"]

markets = ["New-York", "Chicago", "Topeka"]

capacity = {"Seattle": 350.0, "San-Diego": 600.0}

demand = {"New-York": 325.0, "Chicago": 300.0, "Topeka": 275.0}

distance = {

("Seattle", "New-York"): 2.5,

("Seattle", "Chicago"): 1.7,

("Seattle", "Topeka"): 1.8,

("San-Diego", "New-York"): 2.5,

("San-Diego", "Chicago"): 1.8,

("San-Diego", "Topeka"): 1.4,

}

...

Different GAMS symbols are represented using different Python data structures. The data for the GAMS sets is represented using Python lists of strings (e.g. `plants` and `markets`). On the other hand, GAMS parameters are represented by Python dictionaries (e.g. `capacity` and `demand`). Note that the representation of the two dimensional parameter `distance` uses Python tuples for storing the keys. The choice of data structures can also be different, but the used structures in this example fit well for representing GAMS data with standard Python data structures.

A new GamsDatabase instance can be created using GamsWorkspace.add_database.

...

# create new GamsDatabase instance
db = ws.add_database()

...

We start adding GAMS sets using the method GamsDatabase.add_set which takes the name and the dimension as arguments. The third argument is an optional explanatory text. A for-loop iterates through `plants` and adds new records to the recently created GamsSet instance `i` using GamsSet.add_record.

...

# add 1-dimensional set 'i' with explanatory text 'canning plants' to the GamsDatabase
i = db.add_set("i", 1, "canning plants")

for p in plants:

i.add_record(p)

...

GamsParameter instances can be added by using the method GamsDatabase.add_parameter. It has the same signature as GamsDatabase.add_set. Anyhow, in this example we use GamsDatabase.add_parameter_dc instead which takes a list of GamsSet instances instead of the dimension for creating a parameter with domain information.

...

# add parameter 'a' with domain 'i'
a = db.add_parameter_dc("a", [i], "capacity of plant i in cases")

for p in plants:

a.add_record(p).value = capacity[p]

...

As soon as all data is prepared in the GamsDatabase, the method GamsDatabase.export can be used to create a GDX file.

...

# export the GamsDatabase to a GDX file with name 'data.gdx' located in the 'working_directory' of the GamsWorkspace
db.export("data.gdx")

...

## How to import data from GDX (transport_gdx.py)
Data can be imported from a GDX file using GamsWorkspace.add_database_from_gdx. The method takes a path to a GDX file and creates a GamsDatabase instance.

...

# add a new GamsDatabase and initialize it from the GDX file just created
db2 = ws.add_database_from_gdx("data.gdx")

...

Reading the data from the GamsSet `i` into a list can be done as follows:

...

# read data from symbols into Python data structures
i = [rec.keys[0] for rec in db2["i"]]

...

A Python list is created using list comprehensions. `i` is retrieved by querying the GamsDatabase `db2`. The returned GamsSet object can be iterated using a for-loop to access the records of the set. Each record is of type GamsSetRecord and can be asked for its keys.

You can do the same for GamsParameters. Instead of creating a Python list, we want to have the data in the form of a Python dictionary. GamsParameterRecords can not only be asked for their keys, but also for their value. The following code snippet shows how to read the one dimensional parameter `a` into a Python dictionary using dict comprehensions.

...

a = {rec.keys[0]: rec.value for rec in db2["a"]}

...

For multi dimensional symbols, we choose the Python dictionary keys to be tuples instead of string. We access the keys as usual, but do not address a specific key. Instead, we take the whole list of keys and turn it into a tuple.

...

d = {tuple(rec.keys): rec.value for rec in db2["d"]}

...

Scalars can be read into a Python identifier by accessing the value of the first and only record.

...

f = db2["f"].first_record().value

...

## How to run a GamsJob from file (transport1.py)
At first we create our workspace using `ws = GamsWorkspace()`. Afterwards we load the `trnsport` model from the GAMS model library which puts the corresponding gms file in our working directory. Note that you can create a GamsJob with any other gms file you might have created on your own as long as it is located in the current working directory. Then the GamsJob `job` can be defined using the add_job_from_file method and afterwards we run the job.

...

ws.gamslib("trnsport")

job = ws.add_job_from_file("trnsport.gms")

job.run()

...

## How to retrieve a solution from an output database (transport1.py)
The following lines create the solution output and illustrate the usage of the GamsJob.out_db property to get access to the GamsDatabase created by the run method. To retrieve the content of variable `x` we use squared brackets that internally call the get_symbol method.

...

for rec in job.out_db["x"]:

print(

f"x({rec.key(0)},{rec.key(1)}): level={rec.level} marginal={rec.marginal}"

)

...

Note that instead of using the squared brackets we could also use

...

for rec in job.out_db.get_symbol("x"):

...

## How to specify the solver using GamsOptions (transport1.py)
The solver can be specified via the GamsOptions class and the GamsWorkspace.add_options method. The GamsOptions.all_model_types property sets xpress as default solver for all model types that can be handled by the solver. Then we run our GamsJob `job` with the new GamsOption.

...

opt = ws.add_options()

opt.all_model_types = "xpress"

job.run(opt)

...

## How to run a job with a solver option file and capture its log output (transport1.py)
At first we create the file `xpress.opt` with content `algorithm=barrier` which will be used as solver option file and is stored in the current working directory. Afterwards we use a GamsOption just like in the preceding example and set GamsOption.optfile property to 1 to tell the solver to look for a solver option file. In addition, we specify the argument `output` in order to write the log of the GamsJob into the file `transport1_xpress.log`.

...

with open(os.path.join(ws.working_directory, "xpress.opt"), "w") as file:

file.write("algorithm=barrier")

opt.optfile = 1

with open("transport1_xpress.log", "w") as log:

job.run(opt, output=log)

...

Instead of writing the log output to a file, any object that provides the functions `write` and `flush` can be used. In order to write the log directly to `stdout`, we can use the following code:

...

job.run(opt, output=sys.stdout)

...

## How to use include files (transport2.py)
In this example, as in many succeeding, the data text and the model text are separated into two different strings. Note that these strings accessed via `GAMS_DATA` and `GAMS_MODEL` are using GAMS syntax. At first we write an include file `tdata.gms` that contains the data but not the model text and save it in our current working directory.

...

with open(os.path.join(ws.working_directory, "tdata.gms"), "w") as file:

file.write(GAMS_DATA)

...

Afterwards we create a GamsJob using the GamsWorkspace.add_job_from_string method. GamsOptions.defines is used like the 'double dash' GAMS parameters, i.e. it corresponds to `--incname=tdata` on the command line where `incname` is used as name for the include file in `GAMS_MODEL` as shown below.

...

job = ws.add_job_from_string(GAMS_MODEL)

opt = ws.add_options()

opt.defines["incname"] = "tdata"

job.run(opt)

...

The string `GAMS_MODEL` contains the following lines to read in the data.

...

$if not set incname $abort 'no include file name for data file provided'

$include %incname%

...

## How to read data from string and export to GDX (transport3.py)
We read the data from the string `GAMS_DATA`. Note that this contains no model but only data definition in GAMS syntax. By running the corresponding GamsJob a GamsDatabase is created that is available via the GamsJob.out_db property. We can use the GamsDatabase.export method to write the content of this database to a GDX file `tdata.gdx` in the current working directory.

...

job = ws.add_job_from_string(GAMS_DATA)

job.run()

job.out_db.export(os.path.join(ws.working_directory, "tdata.gdx"))

...

## How to run a job using data from GDX (transport3.py)
This works quite similar to the usage of an include file explained in How to use include files (transport2.py).

...

job = ws.add_job_from_string(GAMS_MODEL)

opt = ws.add_options()

opt.defines["gdxincname"] = "tdata"

opt.all_model_types = "xpress"

job.run(opt)

...

Note that there are some minor changes in `GAMS_MODEL` compared to preceding examples due to the usage of a GDX instead of an include file.

...

$if not set gdxincname $abort 'no include file name for data file provided'

$gdxIn %gdxincname%

$load i j a b d f

$gdxIn

...

## How to run a job using implicit database communication (transport3.py)
This example does basically the same as the two preceding examples together. We create two GamsJobs `job_data` and `job_model` where the first one contains only the data and the second one contains only the model without data. After running `job_data` the corresponding `out_db` can be read in directly just like a GDX file. Note that the database needs to be passed to the GamsJob.run method as additional argument.

...

job_data = ws.add_job_from_string(GAMS_DATA)

job_model = ws.add_job_from_string(GAMS_MODEL)

job_data.run()

opt.defines["gdxincname"] = job_data.out_db.name

job_model.run(opt, databases=job_data.out_db)

...

## How to define data using Python data structures (transport4.py)
We use Python lists to define the sets and Python dictionaries for the parameter definition.

...

plants = ["Seattle", "San-Diego"]

markets = ["New-York", "Chicago", "Topeka"]

capacity = {"Seattle": 350.0, "San-Diego": 600.0}

demand = {"New-York": 325.0, "Chicago": 300.0, "Topeka": 275.0}

distance = {

("Seattle", "New-York"): 2.5,

("Seattle", "Chicago"): 1.7,

("Seattle", "Topeka"): 1.8,

("San-Diego", "New-York"): 2.5,

("San-Diego", "Chicago"): 1.8,

("San-Diego", "Topeka"): 1.4,

}

...

## How to prepare a GamsDatabase from Python data structures (transport4.py)
At first we create an empty GamsDatabase db using the GamsWorkspace.add_database method. Afterwards we prepare the database. To add a set to the database we use the GamsSet class and the GamsDatabase.add_set method with arguments describing the identifier, dimension and explanatory text. To add the records to the database we iterate over the elements of our Python data structure and add them by using the GamsSet.add_record method.

For parameters the procedure is pretty much the same. Note that the table that specifies the distances in GAMS can be treated as parameter with dimension 2.

The GamsJob can be run like explained in the preceding example How to run a job using implicit database communication (transport3.py).

...

db = ws.add_database()

i = db.add_set("i", 1, "canning plants")

for p in plants:

i.add_record(p)

j = db.add_set("j", 1, "markets")

for m in markets:

j.add_record(m)

a = db.add_parameter_dc("a", [i], "capacity of plant i in cases")

for p in plants:

a.add_record(p).value = capacity[p]

b = db.add_parameter_dc("b", [j], "demand at market j in cases")

for m in markets:

b.add_record(m).value = demand[m]

d = db.add_parameter_dc("d", [i, j], "distance in thousands of miles")

for k, v in distance.items():

d.add_record(k).value = v

f = db.add_parameter("f", 0, "freight in dollars per case per thousand miles")

f.add_record().value = 90

job = ws.add_job_from_string(GAMS_MODEL)

opt = ws.add_options()

opt.defines["gdxincname"] = db.name

opt.all_model_types = "xpress"

job.run(opt, databases=db)

...

## How to initialize a GamsCheckpoint by running a GamsJob (transport5.py)
The following lines of code conduct several operations. While the first line simply creates a GamsCheckpoint, the second one uses the GamsWorkspace.add_job_from_string method to create a GamsJob containing the model text and data but no solve statement. Afterwards the run method gets the GamsCheckpoint as argument. That means the GamsCheckpoint `cp` captures the state of the GamsJob.

...

cp = ws.add_checkpoint()

job = ws.add_job_from_string(GAMS_MODEL)

job.run(checkpoint=cp)

...

## How to initialize a GamsJob from a GamsCheckpoint (transport5.py)
Note that the string `GAMS_MODEL` contains the entire model and data definition plus an additional demand multiplier and scalars for model and solve status but no solve statement:

...

bmult 'demand multiplier' / 1 /;

...

demand(j) 'satisfy demand at market j';

...

Scalar ms 'model status', ss 'solve status';

...

In transport5.py we create a list with eight different values for this demand multiplier.

...

bmult = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

...

For each entry of that list we create a GamsJob using the GamsWorkspace.add_job_from_string method. Besides another string which resets the demand multiplier `bmult`, specifies the solve statement and assigns values to the scalars `ms` and `ss` we pass the checkpoint `cp` as additional argument. This results in a GamsJob combined from the checkpoint plus the content provided by the string.

We run the GamsJob and print some interesting data from the out_db.

...

for b in bmult:

job = ws.add_job_from_string(

f"bmult={b}; solve transport min z use lp; ms=transport.modelstat; ss=transport.solvestat;",

cp,

)

job.run()

print(f"Scenario bmult={b}:")

print(f" Modelstatus: {job.out_db['ms'].find_record().value}")

print(f" Solvestatus: {job.out_db['ss'].find_record().value}")

print(f" Obj: {job.out_db['z'].find_record().level}")

...

NOTE: Some of the demand multipliers cause infeasibility. Nevertheless, GAMS keeps the incumbent objective function value. Therefore the [model status](UG_GamsCall.html#GAMSAOmodelstat) and the [solve status](UG_GamsCall.html#GAMSAOsolvestat) provide important information for a correct solution interpretation.

## How to run multiple GamsJobs in parallel using a GamsCheckpoint (transport6.py)
With the exception of GamsWorkspace the objects in the `gams.control` package cannot be accessed across different threads unless the instance is locked. The classes themselves are thread safe and multiple objects of the class can be used from different threads (see below for restrictions on solvers that are not thread safe within the `GamsModelInstance` class).

**Note:** If you use multiple instances of the `GamsWorkspace` in parallel, you should avoid using the same working directory. Otherwise you may end up with conflicting file names.

Currently only Cplex, Gurobi, and SoPlex fully utilize the power of solving GamsModelInstances. Some solvers will not even work in a multi-threaded application using GamsModelInstances. For some solvers this is unavoidable because the solver library is not thread safe (e.g. MINOS), other solvers are in principle thread safe but the GAMS link is not (e.g. SNOPT). Moreover, GamsModelInstances are not available for quadratic model types (QCP, MIQCP, RMIQCP).

This example illustrates how to run the jobs known from transport5.py in parallel. We initialize the GamsCheckpoint `cp` and introduce a demand multiplier as we did before:

...

cp = ws.add_checkpoint()

job = ws.add_job_from_string(GAMS_MODEL)

job.run(checkpoint=cp)

bmult = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

...

Furthermore, we introduce a lock object `io_lock` that will be used to avoid mixed up output from the parallel jobs. We create one scenario for each entry of `bmultlist` and cause a thread to begin execution.

...

io_lock = Lock()

threads = {}

for b in bmult:

threads[b] = Thread(target=run_scenario, args=(ws, cp, io_lock, b))

threads[b].start()

for b in bmult:

threads[b].join()

...

In function `run_scenario` a GamsJob is created and run just like in the preceding example of transport5.py. The output section is also the same except for the fact that it is 'locked' by the object `io_lock` which means that the output section cannot be executed simultaneously for multiple demand multipliers.

...

def run_scenario(workspace, checkpoint, io_lock, b):

job = workspace.add_job_from_string(

f"bmult={b}; solve transport min z use lp; ms=transport.modelstat; ss=transport.solvestat;",

checkpoint,

)

job.run()

# we need to make the output a critical section to avoid messed up report informations
io_lock.acquire()

print(f"Scenario bmult={b}:")

print(f" Modelstatus: {job.out_db['ms'].first_record().value}")

print(f" Solvestatus: {job.out_db['ss'].first_record().value}")

print(f" Obj: {job.out_db['z'].first_record().level}")

io_lock.release()

...

While the output in transport5.py is strictly ordered subject to the order of the elements of `bmult` in transport6.py the output blocks might change their order but the blocks describing one scenario are still appearing together due to the `io_lock` object.

## How to create a GamsModelInstance from a GamsCheckpoint (transport7.py)
In transport7.py the usage of GamsModelInstance is demonstrated.

At first checkpoint `cp` is created as in the preceding examples. Note that the GamsJob `job` again contains no solve statement and the demand multiplier is already included with default value 1. We create the GamsModelInstance `mi` using the GamsCheckpoint.add_modelinstance method.

...

cp = ws.add_checkpoint()

job = ws.add_job_from_string(GAMS_MODEL)

job.run(checkpoint=cp)

mi = cp.add_modelinstance()

...

## How to modify a parameter of a GamsModelInstance using GamsModifier (transport7.py)
A GamsModelInstance uses a sync_db to maintain the data. We define `bmult` as GamsParameter using the GamsDatabase.add_parameter method and specify gurobi as solver. Afterwards the GamsModelInstance is instantiated with 3 arguments, the solve statement, GamsModifier `bmult` and GamsOptions `opt`. The GamsModifier means that `bmult` is modifiable while all other parameters, variables and equations of GamsModelInstance `mi` stay unchanged. We use the GamsParameter.add_record method to assign a value to `bmult`. That value can be varied afterwards using the GamsParameter.first_record method to reproduce our well-known example with different demand multipliers.

...

bmult = mi.sync_db.add_parameter("bmult", 0, "demand multiplier")

opt = ws.add_options()

opt.all_model_types = "cplex"

mi.instantiate("transport use lp min z", GamsModifier(bmult), opt)

bmult.add_record().value = 1.0

bmult_list = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3]

for b in bmult_list:

bmult.first_record().value = b

mi.solve()

print(f"Scenario bmult={b}:")

print(f" Modelstatus: {mi.model_status}")

print(f" Solvestatus: {mi.solver_status}")

print(f" Obj: {mi.sync_db['z'].first_record().level}")

...

## How to modify a variable of a GamsModelInstance using GamsModifier (transport7.py)
We create a GamsModelInstance using the GamsCheckpoint.add_modelinstance method. Afterwards we define `x` as GamsVariable and a GamsParameter `xup` that will be used as upper bound for `x`. At the following instantiate method GamsModifier has 3 arguments. The first one says that `x` is modifiable, the second determines which part of the variable (lower bound, upper bound or level) can be modified and the third specifies the GamsParameter that holds the new value, in this case `xup`.

In the following loops we set the upper bound of one link of the network to zero, which means that no transportation between the corresponding plant and market is possible, and solve the modified transportation problem.

...

mi = cp.add_modelinstance()

x = mi.sync_db.add_variable("x", 2, VarType.Positive)

xup = mi.sync_db.add_parameter("xup", 2, "upper bound on x")

# instantiate the GamsModelInstance and pass a model definition and GamsModifier to declare upper bound of x mutable
mi.instantiate("transport use lp min z", GamsModifier(x, UpdateAction.Upper, xup))

mi.solve()

for i in job.out_db["i"]:

for j in job.out_db["j"]:

xup.clear()

xup.add_record((i.key(0), j.key(0))).value = 0

mi.solve()

print(f"Scenario link blocked: {i.key(0)} - {j.key(0)}")

print(f" Modelstatus: {mi.model_status}")

print(f" Solvestatus: {mi.solver_status}")

print(f" Obj: {mi.sync_db['z'].find_record().level}")

...

## How to use a queue to solve multiple GamsModelInstances in parallel (transport8.py)
We initialize a GamsCheckpoint `cp` from a GamsJob. Then we define a list that represents the different values of the demand multiplier. That list will be used like a queue where we extract the last element first. The objects `list_lock` and `io_lock` are used later to avoid multiple reading of one demand multiplier and messed up output. Then we call function `scen_solve` multiple times in parallel. The number of parallel calls is specified by `nr_workers`.

...

cp = ws.add_checkpoint()

job = ws.add_job_from_string(GAMS_MODEL)

job.run(checkpoint=cp)

bmult_list = [1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6]

list_lock = Lock()

io_lock = Lock()

# start 2 threads
nr_workers = 2

threads = {}

for i in range(nr_workers):

threads[i] = Thread(

target=scen_solve, args=(cp, bmult_list, list_lock, io_lock)

)

threads[i].start()

for i in range(nr_workers):

threads[i].join()

In function `scen_solve` we create and instantiate a GamsModelInstance as in the preceding examples and make parameter `bmult` modifiable. Note that we choose `cplex` as solver because it is thread safe (gurobi would also be possible).

We have two critical sections that are locked by the objects `list_lock` and `io_lock`. Note that the pop method removes and returns the last element from the list and deletes it. Once the list is empty the loop terminates.

...

def scen_solve(checkpoint, bmult_list, list_lock, io_lock):

list_lock.acquire()

mi = checkpoint.add_modelinstance()

list_lock.release()

bmult = mi.sync_db.add_parameter("bmult", 0, "demand multiplier")

opt = ws.add_options()

opt.all_model_types = "cplex"

# instantiate the GamsModelInstance and pass a model definition and GamsModifier to declare bmult mutable
mi.instantiate("transport use lp min z", GamsModifier(bmult), opt)

bmult.add_record().value = 1.0

while True:

# dynamically get a bmult value from the queue instead of passing it to the different threads at creation time
list_lock.acquire()

if not bmult_list:

list_lock.release()

return

b = bmult_list.pop()

list_lock.release()

bmult.first_record().value = b

mi.solve()

# we need to make the output a critical section to avoid messed up report informations
io_lock.acquire()

print(f"Scenario bmult={b}:")

print(f" Modelstatus: {mi.model_status}")

print(f" Solvestatus: {mi.solver_status}")

print(f" Obj: {mi.sync_db['z'].first_record().level}")

io_lock.release()

...

## How to fill a GamsDatabase by reading from MS Access (transport9.py)
This example illustrates how to import data from Microsoft Access to a GamsDatabase. There are a few prerequisites required to run transport9.py successfully.
* We import `pyodbc`.
* Note that an architecture mismatch might cause problems. The bitness of your MS Access, Python, pyodbc and GAMS should be identical (64 bit).

We call a function `read_data_from_access` that finally returns a GamsDatabase as shown below.

...

db = read_from_access(ws)

...

The function `read_from_access` begins with the creation of an empty database. Afterwards we set up a connection to the MS Access database `transport.accdb` which can be found in `[GAMSDIR]\apifiles\Data`. To finally read in GAMS sets and parameters we call the functions `read_set` and `read_parameter` that are explained down below.

...

def read_from_access(ws):

db = ws.add_database()

# connect to database
str_access_conn = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=..\\..\\..\\..\apifiles\Data\transport.accdb"

try:

connection = pyodbc.connect(str_access_conn)

except Exception as e:

raise Exception(f"Error: Failed to create a database connection.\n{e}")

# read GAMS sets
read_set(connection, db, "SELECT Plant FROM plant", "i", 1, "canning plants")

read_set(connection, db, "SELECT Market FROM Market", "j", 1, "markets")

# read GAMS parameters
read_parameter(

connection,

db,

"SELECT Plant,Capacity FROM Plant",

"a",

1,

"capacity of plant i in cases",

)

read_parameter(

connection,

db,

"SELECT Market,Demand FROM Market",

"b",

1,

"demand at market j in cases",

)

read_parameter(

connection,

db,

"SELECT Plant,Market,Distance FROM Distance",

"d",

2,

"distance in thousands of miles",

)

connection.close()

return db

...

The function `read_set` adds a set to the GamsDatabase that is filled with the data from the MS Access file afterwards. The function `read_parameter` works quite similar.

...

def read_set(connection, db, query_string, set_name, set_dim, set_exp=""):

try:

cursor = connection.cursor()

cursor.execute(query_string)

data = cursor.fetchall()

if len(data[0]) != set_dim:

raise Exception(

"Number of fields in select statement does not match setDim"

)

i = db.add_set(set_name, set_dim, set_exp)

for row in data:

keys = []

for key in row:

keys.append(str(key))

i.add_record(keys)

except Exception as ex:

raise Exception(

"Error: Failed to retrieve the required data from the database.\n{0}".format(

ex

)

)

finally:

cursor.close()

...

Once we read in all the data we can create a GamsJob from the GamsDatabase and run it as usual.

## How to fill a GamsDatabase by reading from MS Excel (transport10.py)
This example illustrates how to read data from Excel, or to be more specific, from `[GAMSDIR]\apifiles\Data\transport.xlsx`.

At first you have to download the `openpyxl` package:

`pip install openpyxl`

Now you should be able to run transport10.py.

In transport10.py the model is given as string without data like in many examples before and the Excel file `transport.xlsx` is located at `[GAMSDIR]\apifiles\Data`. At first we define the workbook to read from and the different sheet names. To ensure to have the same number of markets and plants in all spreadsheets, we conduct a little test that checks for the number of rows and columns. Our workspace is only created if this test yields no errors.

...

wb = load_workbook(

os.path.join(*[os.pardir] * 4, "apifiles", "Data", "transport.xlsx")

)

capacity = wb["capacity"]

demand = wb["demand"]

distance = wb["distance"]

# number of markets/plants have to be the same in all spreadsheets
if (

distance.max_column - 1 != demand.max_column

or distance.max_row - 1 != capacity.max_row

):

raise Exception("Size of the spreadsheets doesn't match")

...

Now we can create a GamsDatabase and read in the data contained in the different worksheets. We iterate over the columns and read in the set names and the corresponding parameter values.

...

db = ws.add_database()

i = db.add_set("i", 1, "Plants")

j = db.add_set("j", 1, "Markets")

capacity_param = db.add_parameter_dc("a", [i], "Capacity")

demand_param = db.add_parameter_dc("b", [j], "Demand")

distance_param = db.add_parameter_dc("d", [i, j], "Distance")

for c in capacity.iter_cols():

key = c[0].value

i.add_record(key)

capacity_param.add_record(key).value = c[1].value

for c in demand.iter_cols():

key = c[0].value

j.add_record(key)

demand_param.add_record(key).value = c[1].value

for c in range(2, distance.max_column + 1):

for r in range(2, distance.max_row + 1):

keys = (

distance.cell(row=r, column=1).value,

distance.cell(row=1, column=c).value,

)

v = distance.cell(row=r, column=c).value

distance_param.add_record(keys).value = v

...

Note that we can name sets and parameters just like in the database but we don't have to. Now we can run our GamsJob as usual.

...

job = ws.add_job_from_string(GAMS_MODEL)

opt = ws.add_options()

opt.defines["gdxincname"] = db.name

opt.all_model_types = "xpress"

job.run(opt, databases=db)

for rec in job.out_db["x"]:

print(

f"x({rec.key(0)},{rec.key(1)}): level={rec.level} marginal={rec.marginal}"

)

...

## How to create and use a save/restart file (transport11.py)
In transport11.py we demonstrate how to create and use a save/restart file. Usually such a file should be supplied by an application provider but in this example we create one for demonstration purpose. Note that the restart is launched from a GamsCheckpoint.

We create a directory `tmp` with internal identifier `w_dir` in the directory we are currently in. This file will be used as working directory later. From the main function we call the function `create_save_restart` giving it directory `tmp` and the desired name for the save/restart file (`tbase`) as arguments.

...

working_dir = os.path.join(os.curdir, "tmp")

create_save_restart(sys_dir, os.path.join(working_dir, "tbase"))

...

In function `create_save_restart` we create a workspace with the given working directory (`w_dir` refers to `tmp`). Then we create a GamsJob from a string. Note that the string given via `get_base_model_text` contains the basic definitions of sets without giving them a content (that is what `$onempty` is used for). Afterwards we specify a GamsOption to only compile the job but do not execute it. Then we create a checkpoint `cp` that is initialized by the following run of the GamsJob and stored in the file given as argument to the function, in our case `tbase`. This becomes possible because the add_checkpoint method accepts identifiers as well as file names as argument.

...

def create_save_restart(sys_dir, cp_file_name):

ws = GamsWorkspace(os.path.dirname(cp_file_name), sys_dir)

job_1 = ws.add_job_from_string(GAMS_BASE_MODEL)

opt = ws.add_options()

opt.action = Action.CompileOnly

cp = ws.add_checkpoint(os.path.basename(cp_file_name))

job_1.run(opt, cp)

...

So what you should keep in mind before we return to further explanations of the main function is, that the file `tbase` is now in the current working directory and contains a checkpoint that will work exactly like a restart file.

In the main function we define some data using Python data structures as we already did in [transport4.py] (How to define data using Python data structures (transport4.py)) before we create the GamsWorkspace and a GamsDatabase.

...

sys_dir = sys.argv[1] if len(sys.argv) > 1 else None

working_dir = os.path.join(os.curdir, "tmp")

ws = GamsWorkspace(working_dir, sys_dir)

db = ws.add_database()

...

Afterwards we set up the GamsDatabase like we already did in [transport4.py] (How to prepare a GamsDatabase from Python data structures (transport4.py)). Once this is done we run a GamsJob using this data plus the checkpoint stored in file `tbase`.

...

cp_base = ws.add_checkpoint("tbase")

job = ws.add_job_from_string(GAMS_MODEL, cp_base)

opt = ws.add_options()

opt.defines["gdxincname"] = db.name

opt.all_model_types = "xpress"

job.run(opt, databases=db)

...

Note that the string from which we create `job` is different to the one used to prepare the checkpoint stored in `tbase` and is only responsible for reading in the data from the GamsDatabase correctly. The entire model definition is delivered by the checkpoint `cp_base` which is equal to the one we saved in `tbase`.

---

## 4. API: Gamstransfer

### Table of Contents
* Recommended Import
* Design
* Naming Conventions
* Install
* Examples
* GDX Read
* Write Symbol to CSV
* Write a New GDX
* Full Example
* Extended Examples
* Get HTML data
* Get PostgreSQL data (w/ sqlalchemy)

`transfer` is a tool to maintain GAMS data outside a GAMS script in a programming language like Python or Matlab. It allows the user to add GAMS symbols (Sets, Aliases, Parameters, Variables and Equations), to manipulate GAMS symbols, as well as read/write symbols to different data endpoints. `transfer`âs main focus is the highly efficient transfer of data between GAMS and the target programming language, while keeping those operations as simple as possible for the user. In order to achieve this, symbol records â the actual and potentially large-scale data sets â are stored in native data structures of the corresponding programming languages. The benefits of this approach are threefold: (1) The user is usually very familiar with these data structures, (2) these data structures come with a large tool box for various data operations, and (3) optimized methods for reading from and writing to GAMS can transfer the data as a bulk â resulting in the high performance of this package. This documentation describes, in detail, the use of `transfer` within a Python environment.

Data within `transfer` will be stored as Pandas DataFrame. The flexible nature of Pandas DataFrames makes them ideal for storing/manipulating sparse data. Pandas includes advanced operations for [indexing and slicing](https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html), [reshaping](https://pandas.pydata.org/docs/user_guide/reshaping.html), [merging](https://pandas.pydata.org/docs/user_guide/merging.html) and even [visualization](https://pandas.pydata.org/docs/user_guide/visualization.html).

Pandas also includes a number of advanced data [I/O tools](https://pandas.pydata.org/docs/user_guide/io.html) that allow users to generate DataFrames directly from CSV (`.csv`), JSON (`.json`), HTML (`.html`), Microsoft Excel (`.xls`, `.xlsx`), SQL , pickle (.`pkl`), SPSS (`.sav`, `.zsav`), SAS (`.xpt`, `.sas7bdat`), etc.

Centering `transfer` around the Pandas DataFrame gives GAMS users (on a variety of platforms – macOS, Windows, Linux) access to tools to move data back and forth between their favorite environments for use in their GAMS models.

The goal of this documentation is to introduce the user to `transfer` and its functionality. This documentation is not designed to teach the user how to effectively manipulate Pandas DataFrames; users seeking a deeper understanding of Pandas are referred to the extensive [documentation](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html).

Experienced GAMS API users seeking detailed documentation and examples are directed to [Main Classes](API_PY_GAMSTRANSFER_MAIN_CLASSES.html) and [Additional Topics](API_PY_GAMSTRANSFER_ADDITIONAL_TOPICS.html).

# Recommended Import
Users can access the `transfer` sub-module with either of the following (equivalent) import statements once the GAMS Python API has been installed:

import gams.transfer as gt

from gams import transfer as gt

# Design
Storing, manipulating, and transforming sparse data requires that it lives within an environment – this data can then be linked together to enable various operations. In `transfer` we refer to this "environment" as the `Container`, it is the main repository for storing and linking our sparse data. Symbols can be added to the `Container` from a variety of GAMS starting points but they can also be generated directly within the Python environment using convenient function calls that are part of the `transfer` package; a symbol can only belong to one container at a time.

The process of linking symbols together within a container was inspired by typical GAMS workflows but leverages aspects of object oriented programming to make linking data a natural process. Linking data enables data operations like implicit set growth, domain checking, data format transformations (to dense/sparse matrix formats), etc – all of these features are enabled by the use of ordered [pandas.CategoricalDtype](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.CategoricalDtype.html) data types. All of these details will be discussed in the following sections.

# Naming Conventions
Methods – functions that operate on a object – are all verbs (i.e., `getMaxAbsValue()`, `getUELs()`, etc.) and use camel case for identification purposes. Methods are, by convention, tools that "do things"; that is they involve some, potentially expensive, computations. Some `transfer` methods accept arguments, while others are simply called using the `()` notation. Plural arguments (`columns`) hint that they can accept lists of inputs (i.e., a list of symbol names) while singular arguments (`column`) will only accept one input at a time.

Properties – inherent attributes of an object – are all nouns (i.e., `name`, `number_records`, etc.) and use snake case (lower case words separated by underscores) for identification purposes. Object properties (or "object attributes") are fundamental to the object and therefore they are not called like methods; object properties are simply accessed by other methods or user calls. By convention, properties only require trival amounts of computation to access.

Classes – the basic structure of an object – are all singular nouns and use camel case (starting with a capital first letter) for identification purposes.

# Install
The user must download and install the latest version of GAMS in order to install `transfer`. `transfer` is installed when the GAMS Python API is built and installed. The user is referred [HERE](API_PY_GETTING_STARTED.html) for instructions on how to install the Python API files. `transfer` and all GAMS Python API files are compatible with environment managers such as Anaconda.

# Examples
## GDX Read
Reading in all symbols can be accomplished with one line of code (we reference data from the [`trnsport.gms`](../gamslib_ml/libhtml/gamslib_trnsport.html) example).

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

All symbol data is organized in the data attribute – `m.data[<symbol_name>].records` (the `Container` is also subscriptable, `m[<symbol_name>].records` is an equivalent statement) – records are stored as Pandas DataFrames.

## Write Symbol to CSV
Writing symbol records to a CSV can also be accomplished with one line.

m["x"].records.to_csv("x.csv")

## Write a New GDX
There are six symbol classes within `transfer`: 1) Sets, 2) Parameters, 3) Variables, 4) Equations, 5) Aliases and 6) UniverseAliases. For purposes of this quick start, we show how to recreate the `distance` data structure from the [`trnsport.gms`](../gamslib_ml/libhtml/gamslib_trnsport.html) model (the parameter `d`). This brief example shows how users can achieve "GAMS-like" functionality, but within a Python environment – `transfer` leverages the object oriented programming to simplify syntax.

import gams.transfer as gt

import pandas as pd

m = gt.Container()

# create the sets i, j
i = gt.Set(m, "i", records=["seattle", "san-diego"], description="supply")

j = gt.Set(m, "j", records=["new-york", "chicago", "topeka"], description="markets")

# add "d" parameter -- domain linked to set objects i and j
d = gt.Parameter(m, "d", [i, j], description="distance in thousands of miles")

# create some data as a generic DataFrame
dist = pd.DataFrame(

[

("seattle", "new-york", 2.5),

("seattle", "chicago", 1.7),

("seattle", "topeka", 1.8),

("san-diego", "new-york", 2.5),

("san-diego", "chicago", 1.8),

("san-diego", "topeka", 1.4),

],

columns=["from", "to", "thousand_miles"],

)

# setRecords will automatically convert the dist DataFrame into a standard DataFrame format
d.setRecords(dist)

# write the GDX
m.write("out.gdx")

This example shows a few fundamental features of `transfer`:

  1. An empty Container is analogous to an empty GDX file
  2. Symbols will always be linked to a Container (notice that we always pass the Container reference `m` to the symbol constructor)
  3. Records can be added to a symbol with the `setRecords()` method or through the `records` constructor argument (internally calls `setRecords()`). `transfer` will convert many common Python data structures into a standard format.
  4. Domain linking is possible by passing domain set objects to other symbols
  5. Writing a GDX file can be accomplished in one line with the `write()` method.

## Full Example
It is possible to use everything we now know about `transfer` to recreate the [`trnsport.gms`](../gamslib_ml/libhtml/gamslib_trnsport.html) results in GDX form. As part of this example we also introduce the `write` method (and generate `new.gdx`). We will discuss it in more detail in the following section: [GDX Read/Write](API_PY_GAMSTRANSFER_ADDITIONAL_TOPICS.html#PY_GAMSTRANSFER_GDX).

import gams.transfer as gt

# create an empty Container object
m = gt.Container()

# add sets
i = gt.Set(m, "i", records=["seattle", "san-diego"], description="supply")

j = gt.Set(m, "j", records=["new-york", "chicago", "topeka"], description="markets")

# add parameters
a = gt.Parameter(m, "a", ["*"], description="capacity of plant i in cases")

b = gt.Parameter(m, "b", j, description="demand at market j in cases")

d = gt.Parameter(m, "d", [i, j], description="distance in thousands of miles")

f = gt.Parameter(

m, "f", records=90, description="freight in dollars per case per thousand miles"

)

c = gt.Parameter(

m, "c", [i, j], description="transport cost in thousands of dollars per case"

)

# set parameter records
cap = pd.DataFrame([("seattle", 350), ("san-diego", 600)], columns=["plant", "n_cases"])

a.setRecords(cap)

dem = pd.DataFrame(

[("new-york", 325), ("chicago", 300), ("topeka", 275)],

columns=["market", "n_cases"],

)

b.setRecords(dem)

dist = pd.DataFrame(

[

("seattle", "new-york", 2.5),

("seattle", "chicago", 1.7),

("seattle", "topeka", 1.8),

("san-diego", "new-york", 2.5),

("san-diego", "chicago", 1.8),

("san-diego", "topeka", 1.4),

],

columns=["from", "to", "thousand_miles"],

)

d.setRecords(dist)

# c(i,j) = f * d(i,j) / 1000;
cost = d.records.copy(deep=True)

cost["value"] = f.records.loc[0, "value"] * cost["value"] / 1000

c.setRecords(cost)

# add variables
q = pd.DataFrame(

[

("seattle", "new-york", 50, 0),

("seattle", "chicago", 300, 0),

("seattle", "topeka", 0, 0.036),

("san-diego", "new-york", 275, 0),

("san-diego", "chicago", 0, 0.009),

("san-diego", "topeka", 275, 0),

],

columns=["from", "to", "level", "marginal"],

)

x = gt.Variable(

m, "x", "positive", [i, j], records=q, description="shipment quantities in cases",

)

z = gt.Variable(

m,

"z",

records=pd.DataFrame(data=[153.675], columns=["level"]),

description="total transportation costs in thousands of dollars",

)

# add equations
cost = gt.Equation(m, "cost", "eq", description="define objective function")

supply = gt.Equation(m, "supply", "leq", i, description="observe supply limit at plant i")

demand = gt.Equation(m, "demand", "geq", j, description="satisfy demand at market j")

# set equation records
cost.setRecords(

pd.DataFrame(data=[[0, 1, 0, 0]], columns=["level", "marginal", "lower", "upper"])

)

supplies = pd.DataFrame(

[

("seattle", 350, "eps", float("-inf"), 350),

("san-diego", 550, 0, float("-inf"), 600),

],

columns=["from", "level", "marginal", "lower", "upper"],

)

supply.setRecords(supplies)

demands = pd.DataFrame(

[

("new-york", 325, 0.225, 325),

("chicago", 300, 0.153, 300),

("topeka", 275, 0.126, 275),

],

columns=["from", "level", "marginal", "lower"],

)

demand.setRecords(demands)

m.write("new.gdx")

# Extended Examples
## Get HTML data
import gams.transfer as gt

import pandas as pd

url = "https://www.fdic.gov/resources/resolutions/bank-failures/failed-bank-list"

dfs = pd.read_html(url)

# pandas will create a list of dataframes depending on the target URL, we just need the first one
df = dfs[0]

m = gt.Container()

b = gt.Set(m, "b", ["*"], records=df["Bank NameBank"].unique(), description="Bank Name")

s = gt.Set(

m,

"s",

["*"],

records=df["StateSt"].sort_values().unique(),

description="States (alphabetical order)",

)

c = gt.Set(

m,

"c",

["*"],

records=df["CityCity"].sort_values().unique(),

description="Cities (alphabetical order)",

)

c_to_s = gt.Set(

m,

"c_to_s",

[c, s],

records=df[["CityCity", "StateSt"]]

.drop_duplicates()

.sort_values(by=["StateSt", "CityCity"]),

description="City/State pair",

)

bf = gt.Parameter(

m,

"bf",

b,

records=df[["Bank NameBank", "FundFund"]]

.drop_duplicates(subset="Bank NameBank")

.sort_values(by=["Bank NameBank"]),

description="Bank Namd & Fund #",

)

In [1]: m.isValid()

Out[1]: True

**Note:** Users can chain Pandas operations together and pass those operations through to the `records` argument or the `setRecords` method.

## Get PostgreSQL data (w/ sqlalchemy)
import gams.transfer as gt

from sqlalchemy import create_engine

import pandas as pd

# connect to postgres (assuming a localhost)
engine = create_engine("postgresql://localhost:5432/" \+ <database_name>)

df = pd.read_sql(<sql_table_name>, con=engine, index_col=0)

# create the Container and add symbol
m = Container()

p = Parameter(m, <sql_table_name>)

# we need to figure out the symbol dimensionality (potentially from the shape of the dataframe)
r, c = df.shape

p.dimension = c - 1

# set the records
p.setRecords(df)

# write out the GDX file
m.write("out.gdx")

---

## 5. API: Gamstransfer Main Classes

### Table of Contents
* Container
* Constructor
* Properties
* Methods
* Set
* Constructor
* Properties
* Methods
* Adding Set Records
* Directly Set Records
* Generate Set Records
* Parameter
* Constructor
* Properties
* Methods
* Adding Parameter Records
* Directly Set Records
* Generate Parameter Records
* Variable
* Constructor
* Properties
* Methods
* Adding Variable Records
* Directly Set Records
* Generate Variable Records
* Equation
* Constructor
* Properties
* Methods
* Adding Equation Records
* Directly Set Records
* Generate Equation Records
* Alias
* Constructor
* Properties
* Methods
* Adding Alias Records
* UniverseAlias
* Constructor
* Properties
* Methods
* DomainViolation
* Constructor

# Container
The main object class within `transfer` is called `Container`. The `Container` is the vessel that allows symbols to be linked together (through their domain definitions), it enables implicit set definitions, it enables structural manipulations of the data (matrix generation), and it allows the user to perform different read/write operations.

## Constructor
Constructor Arguments

Argument | Type | Description | Required | Default
---|---|---|---|---
`load_from` | `str` or `PathLike` object, GMD Object Handle, `GamsDatabase` object, `Container` | Points to the source of the data being read into the `Container` | No | None
`system_directory` | `str` | Absolute path to GAMS system directory | No | Attempts to find the GAMS installation by creating a `GamsWorkspace` object and loading the `system_directory` attribute.

Creating a `Container` is a simple matter of initializing an object. For example:

import gams.transfer as gt

m = gt.Container()

This new `Container` object, here called `m`, contains a number of convenient properties and methods that allow the user to interact with the symbols that are in the `Container`. Some of these methods are used to filter out different types of symbols, other methods are used to numerically characterize the data within each symbol.

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`data` | main dictionary that is used to store all symbol data (case preserving) | `CasePreservingDict` | \-
`modified` | Flag that identifies if the `Container` has been modified in some way. `Container.modified=False` will reset this flag for all symbols in the container as well as the container itself. | `bool` | \-
`summary` | returns a brief summary of the `Container` | `dict` | \-

Symbols are organized in the `Container` under the `data` `Container` attribute. The dot notation (`m.data`) is used to access the underlying dictionary. Symbols in this dictionary can then be retrieved with the standard bracket notation (`m.data[<symbol_name>]`). The `Container` is also subscriptable (i.e., `m["i"]` will return the `i` Set object just as if the user called `m.data["i"]`). The behavior of the `data` dictionary is has been customized to be case-insensitive (which mimics the behavior of GAMS) – `m["i"]` and `m["I"]` will return the same object.

In [1]: m.data

Out[1]:

{'i': <Set `i` (0x7f95b8d63e80)>,

'j': <Set `j` (0x7f95b8d63a60)>,

'a': <Parameter `a` (0x7f95b8d63ee0)>,

'b': <Parameter `b` (0x7f95b8d63d00)>,

'd': <Parameter `d` (0x7f95b8da86a0)>,

'f': <Parameter `f` (0x7f95b8da8670)>,

'c': <Parameter `c` (0x7f95b8da83d0)>,

'x': <Positive Variable `x` (0x7f95b8da83a0)>,

'z': <Free Variable `z` (0x7f95b8da8400)>,

'cost': <Eq Equation `cost` (0x7f95b8da82b0)>,

'supply': <Leq Equation `supply` (0x7f95b8da8280)>,

'demand': <Geq Equation `demand` (0x7f95b8da8580)>}

Symbol existence in the `Container` can be tested with an overloaded Python `in` operator. The following (case-insensitive) syntax is possible:

In [1]: 'i' in m

Out[1]: True

In [2]: 'I' in m

Out[2]: True

In [3]: i in m

Out[3]: True

**Note:** The final example assumes the existence of a separate symbol object called `i`.

The `Container` can also iterate through the symbols (will return a tuple of `(symbol_name, symbol_object)` using a `for-loop` as in the following example. The `list` and `dict` methods can be useful in creating lists and dictionaries of all symbols in the `Container`.

In [1]: m = gt.Container("out.gdx")

In [2]: for name, obj in m:

...: print(name, obj)

...:

i <Set `i` (0x7f9038533fa0)>

j <Set `j` (0x7f9038533fd0)>

a <Parameter `a` (0x7f9038533340)>

b <Parameter `b` (0x7f9038533f10)>

d <Parameter `d` (0x7f9038533f70)>

f <Parameter `f` (0x7f9038533160)>

c <Parameter `c` (0x7f90583b4bb0)>

x <Positive Variable `x` (0x7f90583b4070)>

z <Free Variable `z` (0x7f90583b5570)>

cost <Eq Equation `cost` (0x7f90583b44f0)>

supply <Leq Equation `supply` (0x7f9008c33df0)>

demand <Geq Equation `demand` (0x7f9008c33b80)>

In [3]: list(m)

Out[3]:

[('i', <Set `i` (0x7fced87d3790)>),

('j', <Set `j` (0x7fced882e530)>),

('a', <Parameter `a` (0x7fced882e9b0)>),

('b', <Parameter `b` (0x7fced882ebf0)>),

('d', <Parameter `d` (0x7fced882e800)>),

('f', <Parameter `f` (0x7fced882e9e0)>),

('c', <Parameter `c` (0x7fced882e320)>),

('x', <Positive Variable `x` (0x7fced882e650)>),

('z', <Free Variable `z` (0x7fced882e410)>),

('cost', <Eq Equation `cost` (0x7fcec8918640)>),

('supply', <Leq Equation `supply` (0x7fcec8918610)>),

('demand', <Geq Equation `demand` (0x7fcec89183a0)>)]

In [5]: dict(m)

Out[5]:

{'i': <Set `i` (0x7fced87d3790)>,

'j': <Set `j` (0x7fced882e530)>,

'a': <Parameter `a` (0x7fced882e9b0)>,

'b': <Parameter `b` (0x7fced882ebf0)>,

'd': <Parameter `d` (0x7fced882e800)>,

'f': <Parameter `f` (0x7fced882e9e0)>,

'c': <Parameter `c` (0x7fced882e320)>,

'x': <Positive Variable `x` (0x7fced882e650)>,

'z': <Free Variable `z` (0x7fced882e410)>,

'cost': <Eq Equation `cost` (0x7fcec8918640)>,

'supply': <Leq Equation `supply` (0x7fcec8918610)>,

'demand': <Geq Equation `demand` (0x7fcec89183a0)>}

**Note:** The `len` (length) function can be used to quickly find out how many symbols exist in the `Container` (`len(m)`).

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`addAlias` | `Container` method to add an `Alias` | `name` (`str`)
`alias_with` (`Set`, `Alias`) | `Alias` object
`addEquation` | `Container` method to add an `Equation` | `name` (`str`)
`type` (`str`)
`domain=[]` (`str`, `list`)
`records=None` (`pandas.DataFrame`, `numpy.ndarry`, `None`)
`domain_forwarding=False` (`bool`)
`description=""` (`str`)
`uels_on_axes=False` (`bool`) | `Equation` object
`addParameter` | `Container` method to add a `Parameter` | `name` (`str`)
`domain=None` (`str`, `list`, `None`)
`records=None` (`pandas.DataFrame`, `numpy.ndarry`, `None`)
`domain_forwarding=False` (`bool`)
`description=""` (`str`)
`uels_on_axes=False` (`bool`) | `Parameter` object
`addSet` | `Container` method to add a `Set` | `name` (`str`)
`domain=None` (`str`, `list`, `None`)
`is_singleton=False` (`bool`)
`records=None` (`pandas.DataFrame`, `numpy.ndarry`, `None`)
`domain_forwarding=False` (`bool`)
`description=""` (`str`)
`uels_on_axes=False` (`bool`) | `Set` object
`addUniverseAlias` | `Container` method to add a `UniverseAlias` | `name` (`str`) | `UniverseAlias` object
`addVariable` | `Container` method to add an `Variable` | `name` (`str`)
`type="free"` (`str`)
`domain=[]` (`str`, `list`)
`records=None` (`pandas.DataFrame`, `numpy.ndarry`, `None`)
`domain_forwarding=False` (`bool`)
`description=""` (`str`)
`uels_on_axes=False` (`bool`) | `Variable` object
`capitalizeUELs` | will capitalize all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`casefoldUELs` | will casefold all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`countDomainViolations` | get the count of how many records contain at least one domain violation for `symbols` (if `symbols=None` assume all symbols) | `symbols=None` (`str`, `list`, `None`) | `dict`
`countDuplicateRecords` | returns the count of how many duplicate records exist for `symbols` (if `symbols=None` assume all symbols) | `symbols=None` (`str`, `list`, `None`) | `dict`
`describeAliases` | create a summary table with descriptive statistics for `Aliases` | `symbols=None` (`None`, `str`, `list`) - if `None`, assumes all aliases | `pandas.DataFrame`
`describEquations` | create a summary table with descriptive statistics for `Equations` | `symbols=None` (`None`, `str`, `list`) - if `None`, assumes all equations | `pandas.DataFrame`
`describeParameters` | create a summary table with descriptive statistics for `Parameters` | `symbols=None` (`None`, `str`, `list`) - if `None`, assumes all parameters | `pandas.DataFrame`
`describeSets` | create a summary table with descriptive statistics for `Sets` | `symbols=None` (`None`, `str`, `list`) - if `None`, assumes all sets | `pandas.DataFrame`
`describeVariables` | create a summary table with descriptive statistics for `Variables` | `symbols=None` (`None`, `str`, `list`) - if `None`, assumes all variables | `pandas.DataFrame`
`dropDomainViolations` | drop records that have domain violations for `symbols` (if `symbols=None` assume all symbols) | `symbols=None` (`str`, `list`, `None`) | `None`
`dropDuplicateRecords` | drop records with duplicate domains from `symbols` in the Container – `keep` argument can take values of "first" (keeps the first instance of a duplicate record), "last" (keeps the last instance of a record), or `False` (drops all duplicates including the first and last) | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols
`keep="first"` (str, `False`) | `None`
`getAliases` | return all alias objects in the container (`is_valid=None`), return all valid alias objects (`is_valid=True`), return all invalid alias objects (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`getDomainViolations` | gets domain violations that exist in the data for `symbols` (if `symbols=None` assume all symbols); returns a `list` of `DomainViolation` objects (or `None` if no violations) | `symbols=None` (`str`, `list`, `None`) | `list` or `None`
`getEquations` | return all equation objects (`is_valid=None`), return all valid equation objects (`is_valid=True`), return all invalid equation objects (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`)
`types=None` (`list` of equation types) - if `None`, assumes all types | `list`
`getParameters` | return all parameter objects in the container (`is_valid=None`), return all valid parameter objects (`is_valid=True`), return all invalid parameter objects (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`getSets` | return all set objects in the container (`is_valid=None`), return all valid set objects (`is_valid=True`), return all invalid set objects (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`getSymbols` | returns a list of object references for `symbols` | `symbols` (`str`, `list`) | `list`
`getUELs` | gets UELs from all `symbols`. If `symbols=None` and `ignore_unused=False`, return the full universe set. If `symbols=None` and `ignore_unused=True`, return a universe set that contains UELs that only appear in data. | `symbols=None` (`str`, `list`, `None`)
`ignore_unused=False` (`bool`) | `list`
`getVariables` | return all variable objects (`is_valid=None`), return all valid variable objects (`is_valid=True`), return all invalid variable objects (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`)
`types=None` (`list` of variable types) - if `None`, assumes all types | `list`
`hasDomainViolations` | returns `True` if there are domain violations in the records for `symbols` (if `symbols=None` assume all symbols), returns `False` if not. | `symbols=None` (`str`, `list`, `None`) | `bool`
`hasDuplicateRecords` | returns `True` if there are duplicate records for `symbols` (if `symbols=None` assume all symbols), `False` if not. | `symbols=None` (`str`, `list`, `None`) | `bool`
`isValid` | `True` if `symbols` in the Container are valid (if `symbols=None` assume all symbols) | `symbols=None` (`str`, `list`, `None`) | `bool`
`ljustUELs` | will left justify all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`symbols=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`listAliases` | list all aliases (`is_valid=None`), list all valid aliases (`is_valid=True`), list all invalid aliases (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`listEquations` | list all equations (`is_valid=None`), list all valid equations (`is_valid=True`), list all invalid equations (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`)
`types=None` (`list` of equation types) - if `None`, assumes all types | `list`
`listParameters` | list all parameters (`is_valid=None`), list all valid parameters (`is_valid=True`), list all invalid parameters (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`listSets` | list all sets (`is_valid=None`), list all valid sets (`is_valid=True`), list all invalid sets (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`listSymbols` | list all symbols (`is_valid=None`), list all valid symbols (`is_valid=True`), list all invalid symbols (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`) | `list`
`listVariables` | list all variables (`is_valid=None`), list all valid variables (`is_valid=True`), list all invalid variables (`is_valid=False`) in the container | `is_valid=None` (`bool`, `None`)
`types=None` (`list` of variable types) - if `None`, assumes all types | `list`
`lowerUELs` | will lowercase all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`lstripUELs` | will left strip whitespace from all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`read` | main method to read `load_from`, can be provided with a list of `symbols` to read in subsets, `records` controls if symbol records are loaded or just metadata, `mode` controls if data is first read into categorical data structures or object type structures, `encoding` specifies the original file [encoding](https://docs.python.org/3/library/codecs.html#standard-encodings) and to properly decode special characters | `load_from` (`str` or `PathLike` object, GMD Object Handle, `GamsDatabase` object, `Container`)
`symbols="all"` (`str`, `list`)
`records=True` (`bool`)
`mode="category"` (`category` or `string`)
`encoding=None` (`str` or `None`) | `None`
`removeSymbols` | symbols to remove from the Container, also sets the symbols `container` to None. If `symbols=None`, will remove all symbols. | `symbols=None` (`str`, `list`, `None`) | `None`
`removeUELs` | removes UELs from all `symbols` in all dimensions. If `uels` is `None` only unused UELs will be removed. If `symbols` is `None` UELs will be removed from all symbols. | `uels` (`str`, `list`, `None`)
`symbols=None` (`str`, `list`, `None`) | `None`
`renameSymbol` | rename a symbol in the `Container` | `old_name` (`str`), `new_name` (`str`) | `None`
`renameUELs` | renames UELs (case-sensitive) that appear in `symbols` (for all dimensions). If `symbols=None`, rename UELs in all symbols. If `allow_merge=True`, the categorical object will be re-created to offer additional data flexibility. ** All trailing whitespace is trimmed ** | `uels` (`dict`)
`symbols=None` (`str`, `list`, `None`)
`allow_merge=False` (`bool`) | `None`
`reorderSymbols` | reorder symbols in order to avoid domain violations | \- | `None`
`rjustUELs` | will right justify all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`symbols=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`rstripUELs` | will right strip whitespace from all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`stripUELs` | will strip whitespace from all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`titleUELs` | will title (capitalize all individual words) in all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`upperUELs` | will uppercase all UELs in the `Container` or a subset of specified `symbols`, can be chained with other `*UELs` string operations | `symbols=None` (`str`, `list`, `None`) - if `None`, assumes all symbols | `self`
`write` | main bulk write method to a `write_to` target | `write_to` (`str`, `PathLike` object, `GamsDatabase` object, GMD Object)
`symbols=None` (`None`, `str`, `list`) - if `None`, assumes all symbols
`compress=False` (`bool`)
`uel_priority=None` (`str`, `list`)
`merge_symbols=None` (`None`, `str`, `list`)
`mode=None` (`None`, `string`, `category`) - if `None`, assumes `string` mode writing
`eps_to_zero=True` (`bool`) - default behavior will convert all `-0.0` (`EPS`) values into `0.0` (drop the sign bit) | `None`

# Set
There are two different ways to create a GAMS set and add it to a `Container`.

  1. Use `Set` constructor
  2. Use the `Container` method `addSet` (which internally calls the `Set` constructor)

## Constructor
Argument | Type | Description | Required | Default
---|---|---|---|---
`container` | `Container` | A reference to the `Container` object that the symbol is being added to | Yes | \-
`description` | `str` | Description of symbol | No | ""
`domain` | `list`, `str`, or `Set/Alias` | List of domains given either as string ('*' for universe set) or as reference to a Set/Alias object | No | `["*"]`
`domain_forwarding` | `bool` or `list` | Flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | No | False
`is_singleton` | `bool` | Indicates if set is a singleton set (`True`) or not (`False`) | No | False
`name` | `str` | Name of symbol | Yes | \-
`records` | many | Symbol records | No | None
`uels_on_axes` | `bool` | Instructs `setRecords` to assume symbol domain information is contained in the axes of the Pandas object | No | False

**Note:** Set records can be updated through the object constructor (a new object will not be created) if a symbol of the same name already exists in the container, has the same domain, and has the same `is_singleton` and `domain_forwarding` state. The symbol description will only be updated if new text is provided.

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`container` | reference to the `Container` that the symbol belongs to | `Container` | \-
`description` | description of symbol | `str` | \-
`dimension` | dimension of symbol | `int` | setting is a shorthand notation to create `["*"] * n` domains in symbol
`domain` | list of domains given either as string (`*` for universe set) or as reference to the Set/Alias object | `list`, `str`, or `Set/Alias` | \-
`domain_forwarding` | flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | `bool` or `list` | no effect after records have been set
`domain_labels` | column headings for the `records` DataFrame | `list` of `str` | will add a `_<dimension>` tag to user supplied column names (if not unique)
`domain_names` | string version of domain names | `list` of `str` | \-
`domain_type` | `none`, `relaxed` or `regular` depending on state of domain links | `str` | \-
`is_singleton` | `bool` if symbol is a singleton set | `bool` | \-
`modified` | Flag that identifies if the `Set` has been modified | `bool` | \-
`name` | name of symbol | `str` | sets the GAMS name of the symbol
`number_records` | number of symbol records (i.e., returns `len(self.records)` if not `None`) | `int` | \-
`records` | the main symbol records | `pandas.DataFrame` | responsive to `domain_forwarding` state
`summary` | output a `dict` of only the metadata | `dict` | \-

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`addUELs` | adds UELs to the symbol `dimensions`. If `dimensions` is `None` then add UELs to all dimensions. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`) | `None`
`capitalizeUELs` | will capitalize all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`casefoldUELs` | will casefold all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`countDomainViolations` | returns the count of how many records contain at least one domain violation | \- | `int`
`countDuplicateRecords` | returns the count of how many (case insensitive) duplicate records exist | \- | `int`
`dropDomainViolations` | drop records from the symbol that contain a domain violation | \- | `None`
`dropDuplicateRecords` | drop records with (case insensitive) duplicate domains from the symbol – `keep` argument can take values of "first" (keeps the first instance of a duplicate record), "last" (keeps the last instance of a record), or `False` (drops all duplicates including the first and last) | `keep="first"` (str, `False`) | `None`
`equals` | Used to compare the symbol to another symbol. If `check_uels=True` then check both used and unused UELs and confirm same order, otherwise only check used UELs in data and do not check UEL order. If `check_element_text=True` then check that all set elements have the same descriptive element text, otherwise skip. If `check_meta_data=True` then check that symbol name and description are the same, otherwise skip. If `verbose=True` will return an exception from the asserter describing the nature of the difference. | `check_uels=True` (`bool`)
`check_element_text=True` (`bool`)
`check_meta_data=True` (`bool`)
`verbose=False` (`bool`) | `bool`
`findDomainViolations` | get a view of the records DataFrame that contain any domain violations | \- | `pandas.DataFrame`
`findDuplicateRecords` | get a view of the records DataFrame that contain any (case insensitive) duplicate domains – `keep` argument can take values of "first" (finds all duplicates while keeping the first instance as unique), "last" (finds all duplicates while keeping the last instance as unique), or `False` (finds all duplicates) | `keep="first"` (str, `False`) | `pandas.DataFrame`
`generateRecords` | convenience method to set standard `pandas.DataFrame` formatted records given domain set information. Will generate records with the Cartesian product of all domain sets. The `density` argument can take any value on the interval `[0,1]`. If `density` is <1 then randomly selected records will be removed. `density` will accept a `list` of length `dimension` -- allows users to specify a density per symbol dimension. Random number state can be set with `seed` argument. | `density=1.0` (`float`, `list`)
`seed=None` (`int`, `None`) | `None`
`getDomainViolations` | returns a `list` of `DomainViolation` objects if any (`None` otherwise) | \- | `list` or `None`
`getSparsity` | get the sparsity of the symbol w.r.t the cardinality | \- | `float`
`getUELs` | gets UELs from symbol `dimensions`. If `dimensions` is `None` then get UELs from all dimensions (maintains order). The argument `codes` accepts a list of `str` UELs and will return the corresponding `int`; must specify a single dimension if passing `codes`. Returns only UELs in the data if `ignore_unused=True`, otherwise return all UELs. | `dimensions=None` (`int`, `list`, `None`)
`codes=None` (`int`, `list`, `None`)
`ignore_unused=False` (`bool`) | `list`
`hasDomainViolations` | returns `True` if there are domain violations in the records, returns `False` if not. | \- | `bool`
`hasDuplicateRecords` | returns `True` if there are (case insensitive) duplicate records in the symbol, returns `False` if not. | \- | `bool`
`isValid` | checks if the symbol is in a valid format, throw exceptions if `verbose=True`, recheck a symbol if `force=True` | `verbose=False`
`force=True` | `bool`
`ljustUELs` | will left justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lowerUELs` | will lowercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lstripUELs` | will left strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`pivot` | Convenience function to pivot `records` into a new shape (only symbols with >1D can be pivoted). If `index` is `None` then it is set to dimensions `[0..dimension-1]`. If `columns` is `None` then it is set to the last dimension. Missing values in the pivot will take the value provided by `fill_value` | `index=None` (`str`, `list`, `None`)
`columns=None` (`str`, `list`, `None`)
`fill_value=None` (`int`, `float`, `str`) | `pd.DataFrame`
`renameUELs` | renames UELs (case-sensitive) that appear in the symbol `dimensions`. If `dimensions` is `None` then operate on all dimensions of the symbol. If `allow_merge=True`, the categorical object will be re-created to offer additional data flexibility. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`, `dict`)
`dimensions` (`int`, `list`, `None`)
`allow_merge=False` (`bool`) | `None`
`reorderUELs` | reorders the UELs in the symbol `dimensions`. If `uels` is `None`, reorder UELs to data order and append any unused categories. If `dimensions` is `None` then reorder UELs in all dimensions of the symbol. | `uels` (`str`, `list`, `dict`, `None`)
`dimensions` (`int`, `list`, `None`) | `None`
`removeUELs` | removes UELs that appear in the symbol `dimensions`, If `uels` is `None` then remove all unused UELs (categories). If `dimensions` is `None` then operate on all dimensions. | `uels=None` (`str`, `list`, `None`)
`dimensions=None` (`int`, `list`, `None`) | `bool`
`rjustUELs` | will right justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`rstripUELs` | will right strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`setRecords` | main convenience method to set standard `pandas.DataFrame` formatted records. If `uels_on_axes=True` `setRecords` will assume that all domain information is contained in the axes of the pandas object – data will be flattened (if necessary). | `records` (many types) | `None`
`setUELs` | set the UELs for symbol `dimensions`. If `dimensions` is `None` then set UELs for all dimensions. If `rename=True`, then the old UEL names will be renamed with the new UEL names. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`)
`rename=False` (`bool`) | `None`
`stripUELs` | will strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`titleUELs` | will title (capitalize all individual words) in all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`toList` | convenience method to return symbol records as a Python list | `include_element_text=False` (bool) | `list`
`upperUELs` | will uppercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`

## Adding Set Records
Three possibilities exist to assign symbol records to a set (roughly ordered in complexity):

  1. Setting the argument `records` in the set constructor/container method (internally calls `setRecords`) - creates a data copy
  2. Using the symbol method `setRecords` \- creates a data copy
  3. Setting the property `records` directly - does not create a data copy

If the data is in a convenient format, a user may want to pass the records directly within the set constructor. This is an optional keyword argument and internally the set constructor will simply call the `setRecords` method. The symbol method `setRecords` is a convenience method that transforms the given data into an approved Pandas DataFrame format (see [Standard Data Formats](API_PY_GAMSTRANSFER_ADDITIONAL_TOPICS.html#PY_GAMSTRANSFER_STANDARD_FORMAT)). Many native Python data types can be easily transformed into DataFrames, so the `setRecords` method for `Set` objects will accept a number of different types for input. The `setRecords` method is called internally on any data structure that is passed through the `records` argument. We show a few examples of ways to create differently structured sets:

Example #1 - Create a 1D set from a list

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego"])

# NOTE: the above syntax is equivalent to -
# i = gt.Set(m, "i")
# i.setRecords(["seattle", "san-diego"])
# NOTE: the above syntax is also equivalent to -
# m.addSet("i", records=["seattle", "san-diego"])
# NOTE: the above syntax is also equivalent to -
# i = m.addSet("i")
# i.setRecords(["seattle", "san-diego"])
# NOTE: the above syntax is also equivalent to -
# m.addSet("i")
# m["i"].setRecords(["seattle", "san-diego"])
In [1]: i.records

Out[1]:

uni element_text

0 seattle

1 san-diego

Example #2 - Create a 1D set from a tuple

import gams.transfer as gt

m = gt.Container()

j = gt.Set(m, "j", records=("seattle", "san-diego"))

# NOTE: the above syntax is equivalent to -
# j = gt.Set(m, "j")
# j.setRecords(("seattle", "san-diego"))
# NOTE: the above syntax is also equivalent to -
# m.addSet("j", records=("seattle", "san-diego"))
# NOTE: the above syntax is also equivalent to -
# j = m.addSet("j")
# j.setRecords(("seattle", "san-diego"))
# NOTE: the above syntax is also equivalent to -
# m.addSet("j")
# m["j"].setRecords(("seattle", "san-diego"))
In [1]: j.records

Out[1]:

uni element_text

0 seattle

1 san-diego

Example #3 - Create a 2D set from a list of tuples

import gams.transfer as gt

m = gt.Container()

k = gt.Set(m, "k", ["*", "*"], records=[("seattle", "san-diego")])

# NOTE: the above syntax is equivalent to -
# k = gt.Set(m, "k", ["*", "*"])
# k.setRecords([("seattle", "san-diego")])
# NOTE: the above syntax is also equivalent to -
# m.addSet("k", ["*","*"], records=[("seattle", "san-diego")])
# NOTE: the above syntax is also equivalent to -
# k = m.addSet("k", ["*","*"])
# k.setRecords([("seattle", "san-diego")])
# NOTE: the above syntax is also equivalent to -
# m.addSet("k", ["*","*"])
# m["k"].setRecords([("seattle", "san-diego")])
In [1]: k.records

Out[1]:

uni_0 uni_1 element_text

0 seattle san-diego

Example #4 - Create a 1D set from a DataFrame slice + .unique()

import gams.transfer as gt

m = gt.Container()

# note that the raw data is convenient to hold in a DataFrame
dist = pd.DataFrame(

[

("seattle", "new-york", 2.5),

("seattle", "chicago", 1.7),

("seattle", "topeka", 1.8),

("san-diego", "new-york", 2.5),

("san-diego", "chicago", 1.8),

("san-diego", "topeka", 1.4),

],

columns=["from", "to", "thousand_miles"],

)

l = gt.Set(m, "l", records=dist["from"].unique())

# NOTE: the above syntax is equivalent to -
# l = gt.Set(m, "l")
# l.setRecords(dist["from"].unique())
# NOTE: the above syntax is also equivalent to -
# m.addSet("l", records=dist["from"].unique())
# NOTE: the above syntax is also equivalent to -
# l = m.addSet("l")
# l.setRecords(dist["from"].unique())
# NOTE: the above syntax is also equivalent to -
# m.addSet("l")
# m["l"].setRecords(dist["from"].unique())
In [1]: l.records

Out[1]:

uni element_text

0 seattle

1 san-diego

**Note:** The `.unique()` method preserves the order of appearance, unlike `set()`.

Set element text is very handy when labeling specific set elements within a set. A user can add a set element text directly with a set element. Note that it is not required to label all set elements, as can be seen in the following example.

Example #5 - Add set element text

import gams.transfer as gt

m = gt.Container()

i = gt.Set(

m,

"i",

records=[

("seattle", "home of sub pop records"),

("san-diego",),

("washington_dc", "former gams hq"),

],

)

# NOTE: the above syntax is equivalent to -
# # i = gt.Set(m, "i")
# i_recs = [
# ("seattle", "home of sub pop records"),
# ("san-diego",),
# ("washington_dc", "former gams hq"),
# ]
# # i.setRecords(i_recs)
# NOTE: the above syntax is also equivalent to -
# m.addSet("i", records=i_recs)
# NOTE: the above syntax is also equivalent to -
# i = m.addSet("i")
# i.setRecords(i_recs)
# NOTE: the above syntax is also equivalent to -
# m.addSet("i")
# m["i"].setRecords(i_recs)
In [1]: i.records

Out[1]:

uni element_text

0 seattle home of sub pop records

1 san-diego

2 washington_dc former gams hq

Example #6 - Create a 1D set from a Pandas Series

import gams.transfer as gt

import pandas as pd

s = pd.Series(index=["a", "b"])

m = gt.Container()

i = gt.Set(m, "i", records=s, uels_on_axes=True)

# NOTE: We pass the uels_on_axes=True argument in order to tell setRecords to reshape the data
In [1]: i.records

Out[1]:

uni element_text

0 a

1 b

# Now let's add in some element_text
s = pd.Series(index=["a", "b"], data=["node_1", "node_2"])

m = gt.Container()

i = gt.Set(m, "i", records=s, uels_on_axes=True)

In [2]: i.records

Out[2]:

uni element_text

0 a node_1

1 b node_2

# If uels_on_axes=False, setRecords will attempt to create a categorical data structure from s.values -- which cannot be done successfully if there are NaN values in s.values.
s = pd.Series(index=["a", "b"])

m = gt.Container()

i = gt.Set(m, "i", records=s)

ValueError: Categorical categories cannot be null

Example #7 - Create a 2D set from a Pandas Series

s = pd.Series(

index=pd.MultiIndex.from_tuples([("a", "b"), ("c", "d")]),

data=["link_1", "link_2"],

)

m = gt.Container()

i = gt.Set(m, "i", ["*", "*"], records=s, uels_on_axes=True)

# Here is the raw pandas.Series object
In [1]: s

Out[1]:

a b link_1

c d link_2

dtype: object

# When setting records the pandas.Series object will get converted into a pandas.DataFrame
In [2]: i.records

Out[2]:

uni_0 uni_1 element_text

0 a b link_1

1 c d link_2

**Attention:** The order of the set element could be surprising depending on how the pandas MultiIndex is created. Users should take care that the order of the elements returned from the `getUELs` method is correct.

Example #8 - Create a 2D set from a Pandas DataFrame with uels_on_axes=True

import gams.transfer as gt

import pandas as pd

# Create some data first
dim1 = ["a", "b"]

dim2 = ["e", "f"]

dim3 = ["z", "x", "y"]

df = pd.DataFrame(

index=dim1, columns=pd.MultiIndex.from_product([dim2, dim3]), dtype=bool

)

# now remove all set elements that contain the "z" element in the 3rd dimension
df.loc[:, (slice(None), "z")] = False

# now remove all set elements that contain the "a" element in the 1st dimension
df.loc["a", :] = False

In [1]: df

Out[1]:

e f

z x y z x y

a False False False False False False

b False True True False True True

# create the Container and add records
m = gt.Container()

i = gt.Set(m, "i", ["*"] * 3, records=df, uels_on_axes=True)

In [2]: i.records

Out[2]:

uni_0 uni_1 uni_2 element_text

0 b e x

1 b e y

2 b f x

3 b f y

**Note:** It not possible to set `element_text` when `uels_on_axes=True`

## Directly Set Records
The primary advantage of the `setRecords` method is that `transfer` will convert many different (and convenient) data types into the standard data format (a Pandas DataFrame). Users that require higher performance will want to directly pass the `Container` a reference to a valid Pandas DataFrame, thereby skipping some of these computational steps. This places more burden on the user to pass the data in a valid standard form, but it speeds the records setting process and it avoids making a copy of the data in memory. In this section we walk the user through an example of how to set records directly.

Example #1 - Directly set records (1D set)

import gams.transfer as gt

import pandas as pd

m = gt.Container()

i = gt.Set(m, "i", description="supply")

# create a standard format dataframe
df_i = pd.DataFrame(

data=[("seattle", ""), ("san-diego", "")], columns=["uni", "element_text"]

)

# need to create categorical column type, referencing elements already in df_i
df_i["uni"] = df_i["uni"].astype(

pd.CategoricalDtype(categories=df_i["uni"].unique(), ordered=True)

)

# set the records directly
i.records = df_i

In [1]: i.isValid()

Out[1]: True

Stepping through this example we take the following steps:

  1. Create an empty `Container`
  2. Create a GAMS set `i` in the Container, but do not set the `records`
  3. Create a Pandas DataFrame (manually, in this example) taking care to follow the [standard format](API_PY_GAMSTRANSFER_ADDITIONAL_TOPICS.html#PY_GAMSTRANSFER_STANDARD_FORMAT)
  4. The DataFrame has the right shape and column labels so we can proceed to set the records.
  5. We need to cast the `uni` column as a `categorical` data type, so we create a custom ordered category type using `pandas.CategoricalDtype`
  6. Finally, we set the records directly by passing a reference to `df_i` into the symbol records attribute. The setter function of `.records` checks that a DataFrame is being set, but does not check validity. Thus, as a final step we call the `.isValid()` method to verify that the symbol is valid.

**Attention:** Users can debug their DataFrames by running `<symbol_name>.isValid(verbose=True)` to get feedback about their data.

Example #2 - Directly set records (1D subset)

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego"], description="supply")

j = gt.Set(m, "j", i, description="supply")

# create a standard format dataframe
df_j = pd.DataFrame(data=[("seattle", "")], columns=["i", "element_text"])

# create the categorical column type
df_j["i"] = df_j["i"].astype(i.records["uni"].dtype)

# set the records
j.records = df_j

In [1]: j.isValid()

Out[1]: True

This example is more subtle in that we want to create a set `j` that is a subset of `i`. We create the set `i` using the `setRecords` method but then set the records directly for `j`. There are two important details to note: 1) the column labels in `df_j` now reflect the standard format for a symbol with a domain set (as opposed to the universe) and 2) we create the categorical dtype by referencing the parent set (`i`) for the categories (instead of referencing itself).

## Generate Set Records
Generating the initial `pandas.DataFrame` object could be difficult for `Set` symbols that have a large number of records and a small number of UELs – these higher dimensional symbols will benefit from the `generateRecords` convenience function. Internally, `generateRecords` computes the dense Cartesian product of all the domain sets that define a symbol (`generateRecords` will only work on symbols where `<symbol>.domain_type == "regular"`).

Example #1 - Create a large (dense) 4D set

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Set(m, "a", [i, j, k, l])

# generate the records
a.generateRecords()

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l element_text

0 i0 j0 k0 l0

1 i0 j0 k0 l1

2 i0 j0 k0 l2

3 i0 j0 k0 l3

4 i0 j0 k0 l4

... ... ... ... ... ...

6249995 i49 j49 k49 l45

6249996 i49 j49 k49 l46

6249997 i49 j49 k49 l47

6249998 i49 j49 k49 l48

6249999 i49 j49 k49 l49

[6250000 rows x 5 columns]

It is also possible to generate a sparse set (randomly selected rows are removed from the dense dataframe) with the `density` argument to `generateRecords`.

Example #2 - Create a large (sparse) 4D set

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Set(m, "a", [i, j, k, l])

# generate the records
a.generateRecords(density=0.05)

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l element_text

0 i0 j0 k1 l4

1 i0 j0 k1 l13

2 i0 j0 k1 l19

3 i0 j0 k1 l23

4 i0 j0 k2 l1

... ... ... ... ... ...

312495 i49 j49 k48 l27

312496 i49 j49 k48 l30

312497 i49 j49 k49 l7

312498 i49 j49 k49 l32

312499 i49 j49 k49 l42

[312500 rows x 5 columns]

Example #3 - Create a large 4D set w/ only 1 sparse dimension

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Set(m, "a", [i, j, k, l])

# generate the records
a.generateRecords(density=[1, 0.05, 1, 1])

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l element_text

0 i0 j22 k0 l0

1 i0 j22 k0 l1

2 i0 j22 k0 l2

3 i0 j22 k0 l3

4 i0 j22 k0 l4

... ... ... ... ... ...

249995 i49 j36 k49 l45

249996 i49 j36 k49 l46

249997 i49 j36 k49 l47

249998 i49 j36 k49 l48

249999 i49 j36 k49 l49

[250000 rows x 5 columns]

# Parameter
There are two different ways to create a GAMS parameter and add it to a `Container`.

  1. Use `Parameter` constructor
  2. Use the `Container` method `addParameter` (which internally calls the `Parameter` constructor)

## Constructor
Constructor Arguments

Argument | Type | Description | Required | Default
---|---|---|---|---
`container` | `Container` | A reference to the `Container` object that the symbol is being added to | Yes | \-
`description` | `str` | Description of symbol | No | ""
`domain` | `list`, `str`, or `Set/Alias` | List of domains given either as string ('*' for universe set) or as reference to a Set/Alias object, an empty domain list will create a scalar parameter | No | []
`domain_forwarding` | `bool` or `list` | Flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | No | False
`name` | `str` | Name of symbol | Yes | \-
`records` | many | Symbol records | No | None
`uels_on_axes` | `bool` | Instructs `setRecords` to assume symbol domain information is contained in the axes of the Pandas object | No | False

**Note:** Parameter records can be updated through the object constructor (a new object will not be created) if a symbol of the same name already exists in the container, has the same domain, and has the same `domain_forwarding` state. The symbol description will only be updated if new text is provided.

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`container` | reference to the `Container` that the symbol belongs to | `Container` | \-
`description` | description of symbol | `str` | \-
`dimension` | dimension of symbol | `int` | setting is a shorthand notation to create `["*"] * n` domains in symbol
`domain` | list of domains given either as string (`*` for universe set) or as reference to the Set/Alias object | `list`, `str`, or `Set/Alias` | \-
`domain_forwarding` | flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | `bool` or `list` | no effect after records have been set
`domain_labels` | column headings for the `records` DataFrame | `list` of `str` | will add a `_<dimension>` tag to user supplied column names (if not unique)
`domain_names` | string version of domain names | `list` of `str` | \-
`domain_type` | `none`, `relaxed` or `regular` depending on state of domain links | `str` | \-
`is_scalar` | True if the `len(self.domain) = 0` | `bool` | \-
`modified` | Flag that identifies if the `Parameter` has been modified | `bool` | \-
`name` | name of symbol | `str` | sets the GAMS name of the symbol
`number_records` | number of symbol records (i.e., returns `len(self.records)` if not `None`) | `int` | \-
`records` | the main symbol records | `pandas.DataFrame` | responsive to `domain_forwarding` state
`shape` | a tuple describing the array dimensions if `records` were converted with `.toDense()` | `tuple` | \-
`summary` | output a `dict` of only the metadata | `dict` | \-

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`addUELs` | adds UELs to the symbol `dimensions`. If `dimensions` is `None` then add UELs to all dimensions. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`) | `None`
`capitalizeUELs` | will capitalize all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`casefoldUELs` | will casefold all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`countDomainViolations` | returns the count of how many records contain at least one domain violation | \- | `int`
`countDuplicateRecords` | returns the count of how many (case insensitive) duplicate records exist | \- | `int`
`countEps` | total number of `SpecialValues.EPS` in `value` column | \- | `int` or `None`
`countNA` | total number of `SpecialValues.NA` in `value` column | \- | `int` or `None`
`countNegInf` | total number of `SpecialValues.NEGINF` in `value` column | \- | `int` or `None`
`countPosInf` | total number of `SpecialValues.POSINF` in `value` column | \- | `int` or `None`
`countUndef` | total number of `SpecialValues.UNDEF` in `value` column | \- | `int` or `None`
`dropDefaults` | an alias to `dropZeros` | \- | `None`
`dropDomainViolations` | drop records from the symbol that contain a domain violation | \- | `None`
`dropDuplicateRecords` | drop records with (case insensitive) duplicate domains from the symbol – `keep` argument can take values of "first" (keeps the first instance of a duplicate record), "last" (keeps the last instance of a record), or `False` (drops all duplicates including the first and last) | `keep="first"` (str, `False`) | `None`
`dropEps` | drop records from the symbol that are `GAMS EPS` (zero `0.0` records will be retained) | \- | `None`
`dropMissing` | drop records from the symbol that are `NaN` (includes both `NA` and `Undef` special values) | \- | `None`
`dropNA` | drop records from the symbol that are `GAMS NA` | \- | `None`
`dropUndef` | drop records from the symbol that are `GAMS Undef` | \- | `None`
`dropZeros` | drop records from the symbol that are zero (GAMS EPS (`-0.0`) will not be dropped) | \- | `None`
`equals` | Used to compare the symbol to another symbol. If `check_uels=True` then check both used and unused UELs and confirm same order, otherwise only check used UELs in data and do not check UEL order. If `check_meta_data=True` then check that symbol name and description are the same, otherwise skip. `rtol` (relative tolerance) and `atol` (absolute tolerance) set equality tolerances. If `verbose=True` will return an exception from the asserter describing the nature of the difference. | `check_uels=True` (`bool`)
`check_meta_data=True` (`bool`)
`rtol=0.0` (`float`, `None`)
`atol=0.0` (`float`, `None`)
`verbose=False` (`bool`) | `bool`
`findDomainViolations` | get a view of the records DataFrame that contain any domain violations | \- | `pandas.DataFrame`
`findDuplicateRecords` | get a view of the records DataFrame that contain any (case insensitive) duplicate domains – `keep` argument can take values of "first" (finds all duplicates while keeping the first instance as unique), "last" (finds all duplicates while keeping the last instance as unique), or `False` (finds all duplicates) | `keep="first"` (str, `False`) | `pandas.DataFrame`
`findEps` | find positions of `SpecialValues.EPS` in `value` column | \- | `pandas.DataFrame` or `None`
`findNA` | find positions of `SpecialValues.NA` in `value` column | \- | `pandas.DataFrame` or `None`
`findNegInf` | find positions of `SpecialValues.NEGINF` in `value` column | \- | `pandas.DataFrame` or `None`
`findPosInf` | find positions of `SpecialValues.POSINF` in `value` column | \- | `pandas.DataFrame` or `None`
`findUndef` | find positions of `SpecialValues.Undef` in `value` column | \- | `pandas.DataFrame` or `None`
`generateRecords` | convenience method to set standard `pandas.DataFrame` formatted records given domain set information. Will generate records with the Cartesian product of all domain sets. The `density` argument can take any value on the interval `[0,1]`. If `density` is <1 then randomly selected records will be removed. `density` will accept a `list` of length `dimension` -- allows users to specify a density per symbol dimension. Random number state can be set with `seed` argument. | `density=1.0` (`float`, `list`)
`func=numpy.random.uniform(0,1)` (callable)
`seed=None` (`int`, `None`) | `None`
`getMaxAbsValue` | get the maximum absolute value in `value` column | \- | `float` or `None`
`getMaxValue` | get the maximum value in `value` column | \- | `float` or `None`
`getMeanValue` | get the mean value in `value` column | \- | `float` or `None`
`getMinValue` | get the minimum value in `value` column | \- | `float` or `None`
`getSparsity` | get the sparsity of the symbol w.r.t the cardinality | \- | `float`
`getUELs` | gets UELs from symbol `dimensions`. If `dimensions` is `None` then get UELs from all dimensions (maintains order). The argument `codes` accepts a list of `str` UELs and will return the corresponding `int`; must specify a single dimension if passing `codes`. Returns only UELs in the data if `ignore_unused=True`, otherwise return all UELs. | `dimensions=None` (`int`, `list`, `None`)
`codes=None` (`int`, `list`, `None`)
`ignore_unused=False` (`bool`) | `list`
`hasDomainViolations` | returns `True` if there are domain violations in the records, returns `False` if not. | \- | `bool`
`hasDuplicateRecords` | returns `True` if there are (case insensitive) duplicate records in the symbol, returns `False` if not. | \- | `bool`
`isValid` | checks if the symbol is in a valid format, throw exceptions if `verbose=True`, recheck a symbol if `force=True` | `verbose=False`
`force=True` | `bool`
`ljustUELs` | will left justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lowerUELs` | will lowercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lstripUELs` | will left strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`pivot` | Convenience function to pivot `records` into a new shape (only symbols with >1D can be pivoted). If `index` is `None` then it is set to dimensions `[0..dimension-1]`. If `columns` is `None` then it is set to the last dimension. Missing values in the pivot will take the value provided by `fill_value` | `index=None` (`str`, `list`, `None`)
`columns=None` (`str`, `list`, `None`)
`fill_value=None` (`int`, `float`, `str`) | `pd.DataFrame`
`removeUELs` | removes UELs that appear in the symbol `dimensions`, If `uels` is `None` then remove all unused UELs (categories). If `dimensions` is `None` then operate on all dimensions. | `uels=None` (`str`, `list`, `None`)
`dimensions=None` (`int`, `list`, `None`) | `bool`
`renameUELs` | renames UELs (case-sensitive) that appear in the symbol `dimensions`. If `dimensions` is `None` then operate on all dimensions of the symbol. If `allow_merge=True`, the categorical object will be re-created to offer additional data flexibility. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`, `dict`)
`dimensions` (`int`, `list`, `None`)
`allow_merge=False` (`bool`) | `None`
`reorderUELs` | reorders the UELs in the symbol `dimensions`. If `uels` is `None`, reorder UELs to data order and append any unused categories. If `dimensions` is `None` then reorder UELs in all dimensions of the symbol. | `uels` (`str`, `list`, `dict`, `None`)
`dimensions` (`int`, `list`, `None`) | `None`
`rjustUELs` | will right justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`rstripUELs` | will right strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`setRecords` | main convenience method to set standard `pandas.DataFrame` records. If `uels_on_axes=True` `setRecords` will assume that all domain information is contained in the axes of the pandas object – data will be flattened (if necessary). | `records` (many types). | `None`
`setUELs` | set the UELs for symbol `dimensions`. If `dimensions` is `None` then set UELs for all dimensions. If `rename=True`, then the old UEL names will be renamed with the new UEL names. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`)
`rename=False` (`bool`) | `None`
`stripUELs` | will strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`titleUELs` | will title (capitalize all individual words) in all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`toDense` | convert symbol to a dense `numpy.array` format | \- | `numpy.array` or `None`
`toDict` | convenience method to return symbol records as a Python dictionary, `orient` can take values `natural` or `columns` and will control the shape of the `dict`. Must use `orient="columns"` if attempting to set symbol records with `setRecords` | `orient="natural"` | `dict`
`toList` | convenience method to return symbol records as a Python list | \- | `list`
`toSparseCoo` | convert symbol to a sparse COOrdinate `numpy.array` format | \- | sparse matrix format or `None`
`toValue` | convenience method to return symbol records as a Python float. Only possible with scalar symbols. | \- | `float`
`upperUELs` | will uppercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`whereMax` | find the domain entry of records with a maximum value (return first instance only) | \- | `list` of `str` or `None`
`whereMaxAbs` | find the domain entry of records with a maximum absolute value (return first instance only) | \- | `list` of `str` or `None`
`whereMin` | find the domain entry of records with a minimum value (return first instance only) | \- | `list` of `str` or `None`

## Adding Parameter Records
Three possibilities exist to assign symbol records to a parameter (roughly ordered in complexity):

  1. Setting the argument `records` in the set constructor/container method (internally calls `setRecords`) - creates a data copy
  2. Using the symbol method `setRecords` \- creates a data copy
  3. Setting the property `records` directly - does not create a data copy

If the data is in a convenient format, a user may want to pass the records directly within the parameter constructor. This is an optional keyword argument and internally the parameter constructor will simply call the `setRecords` method. The symbol method `setRecords` is a convenience method that transforms the given data into an approved Pandas DataFrame format (see [Standard Data Formats](API_PY_GAMSTRANSFER_ADDITIONAL_TOPICS.html#PY_GAMSTRANSFER_STANDARD_FORMAT)). Many native Python data types can be easily transformed into DataFrames, so the `setRecords` method for `Set` objects will accept a number of different types for input. The `setRecords` method is called internally on any data structure that is passed through the `records` argument. We show a few examples of ways to create differently structured parameters:

Example #1 - Create a GAMS scalar

import gams.transfer as gt

m = gt.Container()

pi = gt.Parameter(m, "pi", records=3.14159)

# NOTE: the above syntax is equivalent to -
# pi = gt.Parameter(m, "pi")
# pi.setRecords(3.14159)
# NOTE: the above syntax is also equivalent to -
# m.addParameter("pi", records=3.14159)
# NOTE: the above syntax is also equivalent to -
# pi = m.addParameter("pi")
# pi.setRecords(3.14159)
# NOTE: the above syntax is also equivalent to -
# m.addParameter("pi")
# m["pi"].setRecords(3.14159)
In [14]: pi.records

Out[14]:

value

0 3.14159

**Note:** `transfer` will still convert scalar values to a standard format (i.e., a Pandas DataFrame with a single row and column).

Example #2 - Create a 1D parameter (defined over `*`) from a list of tuples

import gams.transfer as gt

m = gt.Container()

i = gt.Parameter(m, "i", ["*"], records=[("i" \+ str(i), i) for i in range(5)])

# NOTE: the above syntax is equivalent to -
# i = gt.Parameter(m, "i")
# i.setRecords([("i" + str(i), i) for i in range(5)])
# NOTE: the above syntax is also equivalent to -
# m.addParameter("i", records=[("i" + str(i), i) for i in range(5)])
# NOTE: the above syntax is also equivalent to -
# i = m.addParameter("i")
# i.setRecords([("i" + str(i), i) for i in range(5)])
# NOTE: the above syntax is also equivalent to -
# m.addParameter("i")
# m["i"].setRecords([("i" + str(i), i) for i in range(5)])
In [1]: i.records

Out[1]:

uni value

0 i0 0.0

1 i1 1.0

2 i2 2.0

3 i3 3.0

4 i4 4.0

Example #3 - Create a 1D parameter (defined over a set) from a list of tuples

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=["i" \+ str(i) for i in range(5)])

a = gt.Parameter(m, "a", i, records=[("i" \+ str(i), i) for i in range(5)])

# NOTE: the above syntax is equivalent to -
# i = gt.Set(m, "i")
# i.setRecords(["i" + str(i) for i in range(5)])
# a = gt.Parameter(m, "a", i)
# a.setRecords([("i" + str(i), i) for i in range(5)])
# NOTE: the above syntax is also equivalent to -
# m.addSet("i", records=["i" + str(i) for i in range(5)])
# m.addParameter("a", i, records=[("i" + str(i), i) for i in range(5)])
# NOTE: the above syntax is also equivalent to -
# i = m.addSet("i")
# i.setRecords(["i" + str(i) for i in range(5)])
# a = m.addParameter("a", i)
# a.setRecords([("i" + str(i), i) for i in range(5)])
# NOTE: the above syntax is also equivalent to -
# m.addSet("i")
# m["i"].setRecords(["i" + str(i) for i in range(5)])
# m.addParameter("a", i)
# m["a"].setRecords([("i" + str(i), i) for i in range(5)])
In [1]: a.records

Out[1]:

i value

0 i0 0.0

1 i1 1.0

2 i2 2.0

3 i3 3.0

4 i4 4.0

Example #4 - Create a 2D parameter (defined over a set) from a DataFrame slice

import gams.transfer as gt

import pandas as pd

dist = pd.DataFrame(

[

("seattle", "new-york", 2.5),

("seattle", "chicago", 1.7),

("seattle", "topeka", 1.8),

("san-diego", "new-york", 2.5),

("san-diego", "chicago", 1.8),

("san-diego", "topeka", 1.4),

],

columns=["from", "to", "thousand_miles"],

)

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=dist["from"].unique())

j = gt.Set(m, "j", ["*"], records=dist["to"].unique())

a = gt.Parameter(m, "a", [i, j], records=dist.loc[[0, 3], :])

# NOTE: the above syntax is equivalent to -
# i = gt.Set(m, "i")
# i.setRecords(dist["from"].unique())
# j = gt.Set(m, "j")
# j.setRecords(dist["to"].unique())
# a = gt.Parameter(m, "a", [i, j])
# a.setRecords(dist.loc[[0, 3], :])
# NOTE: the above syntax is also equivalent to -
# m.addSet("i", records=dist["from"].unique())
# m.addSet("j", records=dist["to"].unique())
# m.addParameter("a", i, records=dist.loc[[0, 3], :])
In [1]: a.records

Out[1]:

i j value

0 seattle new-york 2.5

3 san-diego new-york 2.5

**Note:** The original indexing is preserved when a user slices rows out of a reference dataframe.

Example #5 - Create a 2D parameter (defined over a set) from a matrix

import gams.transfer as gt

import pandas as pd

dist = pd.DataFrame(

[

("seattle", "new-york", 2.5),

("seattle", "chicago", 1.7),

("seattle", "topeka", 1.8),

("san-diego", "new-york", 2.5),

("san-diego", "chicago", 1.8),

("san-diego", "topeka", 1.4),

],

columns=["from", "to", "thousand_miles"],

)

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=dist["from"].unique())

j = gt.Set(m, "j", ["*"], records=dist["to"].unique())

a = gt.Parameter(m, "a", [i, j], records=dist)

In [1]: a.toDense()

Out[1]:

array([[2.5, 1.7, 1.8],

[2.5, 1.8, 1.4]])

# use a.toDense() to create a new (and identical) parameter a2
a2 = gt.Parameter(m, "a2", [i, j], records=a.toDense())

# check that a is identical to a2
In [1]: a.equals(a2, check_meta_data=False)

Out[1]: True

Example #6 - Create a 2D parameter from an array using setRecords

import gams.transfer as gt

import numpy as np

import pandas as pd

m = gt.Container()

i = gt.Set(m, "i", records=["i" \+ str(i) for i in range(5)])

j = gt.Set(m, "j", records=["j" \+ str(j) for j in range(5)])

# create the parameter with linked domains (these will control the .shape of the symbol)
a = gt.Parameter(m, "a", [i, j])

# here we use the .shape property to easily generate a dense random array in numpy
a.setRecords(np.random.uniform(low=1, high=10, size=a.shape))

In [1]: a.toDense()

Out[1]:

array([[3.6694495 , 5.17395381, 1.99129484, 3.28315433, 1.44793791],

[1.06953243, 6.56331121, 5.26162554, 5.98098795, 8.30006 ],

[3.77213221, 5.82144901, 9.30035479, 9.12534285, 8.51970747],

[8.47965504, 7.84426304, 5.2442471 , 6.96666622, 6.55194415],

[5.62682779, 4.92509183, 8.94579609, 2.7724934 , 9.99576081]])

Example #7 - Create a 1D parameter from a pandas Series

import gams.transfer as gt

import pandas as pd

s = pd.Series(index=["a", "b", "c"], data=[i + 1 for i in range(3)])

m = gt.Container()

i = gt.Parameter(m, "i", ["*"], records=s, uels_on_axes=True)

In [1]: i.records

Out[1]:

uni value

0 a 1.0

1 b 2.0

2 c 3.0

Example #8 - Create a 2D parameter from a pandas Series

import gams.transfer as gt

import pandas as pd

dim1 = ["a", "b", "c"]

dim2 = ["z", "y", "x"]

s = pd.Series(

index=pd.MultiIndex.from_product([dim1, dim2]),

data=[i + 1 for i in range(len(dim1) * len(dim2))],

)

m = gt.Container()

i = gt.Parameter(m, "i", ["*", "*"], records=s, uels_on_axes=True)

In [1]: i.records

Out[1]:

uni_0 uni_1 value

0 a z 1.0

1 a y 2.0

2 a x 3.0

3 b z 4.0

4 b y 5.0

5 b x 6.0

6 c z 7.0

7 c y 8.0

8 c x 9.0

# NOTE: the order of the second dimension is automatically put into lexicographical order by Pandas
# This can be unexpected and undesirable from a GAMS perspective.
In [2]: s.index.levels[1]

Out[2]: Index(['x', 'y', 'z'], dtype='object')

# gams.transfer goes through extra work to maintain data order in the categorical data structures
# this can be see here where "z" is mapped to integer 0, "y" is mapped to 1 and "x" is mapped to 2
In [3]: i.records["uni_1"]

Out[3]:

0 z

1 y

2 x

3 z

4 y

5 x

6 z

7 y

8 x

Name: uni_1, dtype: category

Categories (3, object): ['z' < 'y' < 'x']

In [4]: i.records["uni_1"].cat.codes

Out[4]:

0 0

1 1

2 2

3 0

4 1

5 2

6 0

7 1

8 2

dtype: int8

Example #9 - Create a 2D parameter from a DataFrame (uels_on_axes=True)

import gams.transfer as gt

import pandas as pd

import numpy as np

dim1 = [f"d{i}" for i in range(2)]

dim2 = [f"d{i}" for i in range(2)]

dim3 = [f"d{i}" for i in range(2)]

dim4 = [f"d{i}" for i in range(2)]

rng = np.random.default_rng(seed=100)

df = pd.DataFrame(

data=rng.uniform(size=(2, 8)),

index=dim1,

columns=pd.MultiIndex.from_product([dim2, dim3, dim4]),

)

In [1]: df

Out[1]:

d0 d1

d0 d1 d0 d1

d0 d1 d0 d1 d0 d1 d0 d1

d0 0.834982 0.596554 0.288863 0.042952 0.973654 0.596472 0.790263 0.910339

d1 0.688154 0.189991 0.981479 0.284740 0.629273 0.581036 0.599912 0.535248

m = gt.Container()

i = gt.Parameter(m, "i", ["*"] * 4, records=df, uels_on_axes=True)

In [2]: i.records

Out[2]:

uni_0 uni_1 uni_2 uni_3 value

0 d0 d0 d0 d0 0.834982

1 d0 d0 d0 d1 0.596554

2 d0 d0 d1 d0 0.288863

3 d0 d0 d1 d1 0.042952

4 d0 d1 d0 d0 0.973654

5 d0 d1 d0 d1 0.596472

6 d0 d1 d1 d0 0.790263

7 d0 d1 d1 d1 0.910339

8 d1 d0 d0 d0 0.688154

9 d1 d0 d0 d1 0.189991

10 d1 d0 d1 d0 0.981479

11 d1 d0 d1 d1 0.284740

12 d1 d1 d0 d0 0.629273

13 d1 d1 d0 d1 0.581036

14 d1 d1 d1 d0 0.599912

15 d1 d1 d1 d1 0.535248

## Directly Set Records
As with sets, the primary advantage of the `setRecords` method is that `transfer` will convert many different (and convenient) data types into the standard data format (a Pandas DataFrame). Users that require higher performance will want to directly pass the `Container` a reference to a valid Pandas DataFrame, thereby skipping some of these computational steps. This places more burden on the user to pass the data in a valid standard form, but it speeds the records setting process and it avoids making a copy of the data in memory. In this section we walk the user through an example of how to set records directly.

Example #1 - Correctly set records (directly)

import gams.transfer as gt

import pandas as pd

import numpy as np

df = pd.DataFrame(

data=[

("h" \+ str(h), "m" \+ str(m), "s" \+ str(s))

for h in range(8760)

for m in range(60)

for s in range(60)

],

columns=["h", "m", "s"],

)

df["value"] = np.random.uniform(0, 100, len(df))

m = gt.Container()

hrs = gt.Set(m, "h", records=df["h"].unique())

mins = gt.Set(m, "m", records=df["m"].unique())

secs = gt.Set(m, "s", records=df["s"].unique())

df["h"] = df["h"].astype(hrs.records["uni"].dtype)

df["m"] = df["m"].astype(mins.records["uni"].dtype)

df["s"] = df["s"].astype(secs.records["uni"].dtype)

a = gt.Parameter(m, "a", [hrs, mins, secs])

# set records
a.records = df

In [1]: a.isValid()

Out[1]: True

In this example we create a large parameter (31,536,000 records and 8880 unique domain elements – we mimic data that is labeled for every second in one year) and assign it to a parameter with `a.records`. `transfer` requires that all domain columns must be a categorical data type, furthermore, this categorical must be ordered. The `records` setter function does very little work other than checking if the object being set is a DataFrame. This places more responsibility on the user to create a DataFrame that complies with the standard format. In Example #1 we take care to properly reference the categorical data types from the domain sets – and in the end `a.isValid() = True`.

Users will need to use the `.isValid(verbose=True)` method to debug any structural issues. As an example we incorrectly generate categorical data types by passing the DataFrame constructor the generic `dtype="category"` argument. This creates categorical column types but they are not ordered and they do not reference the underlying domain set. These errors result in `a` being invalid.

Example #2 - Incorrectly set records (directly)

import gams.transfer as gt

import pandas as pd

import numpy as np

df = pd.DataFrame(

data=[

("h" \+ str(h), "m" \+ str(m), "s" \+ str(s))

for h in range(8760)

for m in range(60)

for s in range(60)

],

columns=["h", "m", "s"],

dtype="category"

)

df["value"] = np.random.uniform(0, 100, len(df))

m = gt.Container()

hrs = gt.Set(m, "h", records=df["h"].unique())

mins = gt.Set(m, "m", records=df["m"].unique())

secs = gt.Set(m, "s", records=df["s"].unique())

a = gt.Parameter(m, "a", [hrs, mins, secs])

# set the records directly
a.records = df

In [1]: a.isValid()

Out[1]: False

In [2]: a.isValid(verbose=True)

Out[2]: Exception: Domain information in column 'h' for 'records' must be an ORDERED categorical type (i.e., <symbol_object>.records["h"].dtype.ordered = True)

## Generate Parameter Records
Generating the initial `pandas.DataFrame` object could be difficult for `Parameter` symbols that have a large number of records and a small number of UELs – these higher dimensional symbols will benefit from the `generateRecords` convenience function. Internally, `generateRecords` computes the dense Cartesian product of all the domain sets that define a symbol (`generateRecords` will only work on symbols where `<symbol>.domain_type == "regular"`).

Example #1 - Create a large (dense) 4D parameter

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Parameter(m, "a", [i, j, k, l])

# generate the records
a.generateRecords()

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l value

0 i0 j0 k0 l0 0.386390

1 i0 j0 k0 l1 0.671253

2 i0 j0 k0 l2 0.522057

3 i0 j0 k0 l3 0.037694

4 i0 j0 k0 l4 0.564205

... ... ... ... ... ...

6249995 i49 j49 k49 l45 0.573354

6249996 i49 j49 k49 l46 0.033717

6249997 i49 j49 k49 l47 0.410322

6249998 i49 j49 k49 l48 0.758310

6249999 i49 j49 k49 l49 0.920708

[6250000 rows x 5 columns]

**Note:** In Example #1 a large 4D parameter was generated – by default, the value of these records are randomly drawn numbers from the interval `[0,1]` (uniform distribution).

As with `Sets`, it is possible to generate a sparse parameter with the `density` argument to `generateRecords`. We extend this example by passing our own custom `func` argument that will control the behavior of the `value` columns. The `func` argument accepts a `callable` (i.e., a reference to a function).

Example #2 - Create a large (sparse) 4D parameter with normally distributed values

import gams.transfer as gt

import numpy as np

# create a custom function to pass to `generateRecords`
def value_dist(size, seed):

rng = np.random.default_rng(seed=seed)

return rng.normal(loc=10.0, scale=2.3, size=size)

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Parameter(m, "a", [i, j, k, l])

# generate the records
a.generateRecords(density=0.05, func=value_dist)

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l value

0 i0 j0 k0 l33 12.490579

1 i0 j0 k0 l43 9.460560

2 i0 j0 k0 l44 7.660337

3 i0 j0 k0 l47 8.811967

4 i0 j0 k1 l5 11.103291

... ... ... ... ... ...

312495 i49 j49 k48 l38 10.619791

312496 i49 j49 k48 l41 14.208250

312497 i49 j49 k48 l47 6.104145

312498 i49 j49 k49 l0 10.216812

312499 i49 j49 k49 l39 9.739771

[312500 rows x 5 columns]

In [3]: a.records["value"].mean()

Out[3]: 10.004072307451391

In [4]: a.records["value"].std()

Out[4]: 2.292569938350144

**Note:** The custom `callable` function reference must expose a `size` argument. It might be tedious to know the exact number of the records that will be generated, especially if a fractional density is specified; therefore, the `generateRecords` method will pass in the correct size automatically. Users are encouraged to use the Numpy suite of random distributions when generating samples – custom functions have the potential to be computationally burdensome if a symbol has a large number of records.

Example #3 - Create a large 4D parameter with 1 sparse dimension

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Parameter(m, "a", [i, j, k, l])

# generate the records
a.generateRecords(density=[1, 0.05, 1, 1])

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l value

0 i0 j30 k0 l0 0.473084

1 i0 j30 k0 l1 0.192571

2 i0 j30 k0 l2 0.060711

3 i0 j30 k0 l3 0.655477

4 i0 j30 k0 l4 0.629535

... ... ... ... ... ...

249995 i49 j32 k49 l45 0.442380

249996 i49 j32 k49 l46 0.002444

249997 i49 j32 k49 l47 0.332731

249998 i49 j32 k49 l48 0.983800

249999 i49 j32 k49 l49 0.984322

[250000 rows x 5 columns]

Example #4 - Create a large 4D parameter with a random number seed

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Parameter(m, "a", [i, j, k, l])

a2 = gt.Parameter(m, "a2", [i, j, k, l])

# generate the records
a.generateRecords(density=0.05, seed=123)

a2.generateRecords(density=0.05)

In [1]: a.equals(a2, check_meta_data=False)

Out[1]: False

In [2]: a2.generateRecords(density=0.05, seed=123)

In [3]: a.equals(a2, check_meta_data=False)

Out[3]: True

**Note:** The `seed` is an `int` that will set the random number generator state (enables reproducible sequences of random numbers).

# Variable
There are two different ways to create a GAMS variable and add it to a `Container`.

  1. Use `Variable` constructor
  2. Use the `Container` method `addVariable` (which internally calls the `Variable` constructor)

## Constructor
Constructor Arguments

Argument | Type | Description | Required | Default
---|---|---|---|---
`container` | `Container` | A reference to the `Container` object that the symbol is being added to | Yes | \-
`description` | `str` | Description of symbol | No | ""
`domain` | `list`, `str`, or `Set/Alias` | List of domains given either as string (`*` for universe set) or as reference to a Set/Alias object, an empty domain list will create a scalar variable | No | []
`domain_forwarding` | `bool` or `list` | Flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | No | False
`name` | `str` | Name of symbol | Yes | \-
`records` | many | Symbol records | No | None
`type` | `str` | Type of variable being created [`binary`, `integer`, `positive`, `negative`, `free`, `sos1`, `sos2`, `semicont`, `semiint`] | No | `free`
`uels_on_axes` | `bool` | Instructs `setRecords` to assume symbol domain information is contained in the axes of the Pandas object | No | False

**Note:** Variable records can be updated through the object constructor (a new object will not be created) if a symbol of the same name already exists in the container, has the same domain, has the same `type`, and has the same `domain_forwarding` state. The symbol description will only be updated if new text is provided.

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`container` | reference to the `Container` that the symbol belongs to | `Container` | \-
`description` | description of symbol | `str` | \-
`dimension` | dimension of symbol | `int` | setting is a shorthand notation to create `["*"] * n` domains in symbol
`domain` | list of domains given either as string (`*` for universe set) or as reference to the Set/Alias object | `list`, `str`, or `Set/Alias` | \-
`domain_forwarding` | flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | `bool` or `list` | no effect after records have been set
`domain_labels` | column headings for the `records` DataFrame | `list` of `str` | will add a `_<dimension>` tag to user supplied column names (if not unique)
`domain_names` | string version of domain names | `list` of `str` | \-
`domain_type` | `none`, `relaxed` or `regular` depending on state of domain links | `str` | \-
`is_scalar` | `True` if the `len(self.domain) = 0` | `bool` | \-
`modified` | Flag that identifies if the `Variable` has been modified | `bool` | \-
`name` | name of symbol | `str` | sets the GAMS name of the symbol
`number_records` | number of symbol records (i.e., returns `len(self.records)` if not `None`) | `int` | \-
`records` | the main symbol records | `pandas.DataFrame` | responsive to `domain_forwarding` state
`shape` | a tuple describing the array dimensions if `records` were converted with `.toDense()` | `tuple` | \-
`summary` | output a `dict` of only the metadata | `dict` | \-
`type` | `str` type of variable | `str` | \-

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`addUELs` | adds UELs to the symbol `dimensions`. If `dimensions` is `None` then add UELs to all dimensions. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`) | `None`
`capitalizeUELs` | will capitalize all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`casefoldUELs` | will casefold all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`countDomainViolations` | returns the count of how many records contain at least one domain violation | \- | `int`
`countDuplicateRecords` | returns the count of how many (case insensitive) duplicate records exist | \- | `int`
`countEps` | total number of `SpecialValues.EPS` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countNA` | total number of `SpecialValues.NA` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countNegInf` | total number of `SpecialValues.NEGINF` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countPosInf` | total number of `SpecialValues.POSINF` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countUndef` | total number of `SpecialValues.UNDEF` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`dropDefaults` | drop records that are set to GAMS default records (check `.default_records` property for values) | \- | `None`
`dropDomainViolations` | drop records from the symbol that contain a domain violation | \- | `None`
`dropDuplicateRecords` | drop records with (case insensitive) duplicate domains from the symbol – `keep` argument can take values of "first" (keeps the first instance of a duplicate record), "last" (keeps the last instance of a record), or `False` (drops all duplicates including the first and last) | `keep="first"` (str, `False`) | `None`
`dropEps` | drop records from the symbol that are `GAMS EPS` (zero `0.0` records will be retained) | \- | `None`
`dropMissing` | drop records from the symbol that are `NaN` (includes both `NA` and `Undef` special values) | \- | `None`
`dropNA` | drop records from the symbol that are `GAMS NA` | \- | `None`
`dropUndef` | drop records from the symbol that are `GAMS Undef` | \- | `None`
`equals` | Used to compare the symbol to another symbol. The `columns` argument allows the user to numerically compare only specified variable attributes (default is to compare all). If `check_uels=True` then check both used and unused UELs and confirm same order, otherwise only check used UELs in data and do not check UEL order. If `check_meta_data=True` then check that symbol name, description and variable type are the same, otherwise skip. `rtol` (relative tolerance) and `atol` (absolute tolerance) set equality tolerances; can be different tolerances for different variable attributes (if specified as a `dict`). If `verbose=True` will return an exception from the asserter describing the nature of the difference. | `columns=["level", "marginal", "lower", "upper", "scale"]`
`check_uels=True` (`bool`)
`check_meta_data=True` (`bool`)
`rtol=0.0` (`int`, `float`, `None`)
`atol=0.0` (`int`, `float`, `None`)
`verbose=False` (`bool`) | `bool`
`findDomainViolations` | get a view of the records DataFrame that contain any domain violations | \- | `pandas.DataFrame`
`findDuplicateRecords` | get a view of the records DataFrame that contain any (case insensitive) duplicate domains – `keep` argument can take values of "first" (finds all duplicates while keeping the first instance as unique), "last" (finds all duplicates while keeping the last instance as unique), or `False` (finds all duplicates) | `keep="first"` (str, `False`) | `pandas.DataFrame`
`findEps` | find positions of `SpecialValues.EPS` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findNA` | find positions of `SpecialValues.NA` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findNegInf` | find positions of `SpecialValues.NEGINF` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findPosInf` | find positions of `SpecialValues.POSINF` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findUndef` | find positions of `SpecialValues.Undef` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`generateRecords` | convenience method to set standard `pandas.DataFrame` formatted records given domain set information. Will generate records with the Cartesian product of all domain sets. The `density` argument can take any value on the interval `[0,1]`. If `density` is <1 then randomly selected records will be removed. `density` will accept a `list` of length `dimension` -- allows users to specify a density per symbol dimension. Random number state can be set with `seed` argument. | `density=1.0` (`float`, `list`)
`func=numpy.random.uniform(0,1)` (`dict` of `callables`)
`seed=None` (`int`, `None`) | `None`
`getMaxValue` | get the maximum value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getMinValue` | get the minimum value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getMeanValue` | get the mean value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getMaxAbsValue` | get the maximum absolute value across all `columns` | `columns="level"` (`str`, `list`) | `float`
`getSparsity` | get the sparsity of the symbol w.r.t the cardinality | \- | `float`
`getUELs` | gets UELs from symbol `dimensions`. If `dimensions` is `None` then get UELs from all dimensions (maintains order). The argument `codes` accepts a list of `str` UELs and will return the corresponding `int`; must specify a single dimension if passing `codes`. Returns only UELs in the data if `ignore_unused=True`, otherwise return all UELs. | `dimensions=None` (`int`, `list`, `None`)
`codes=None` (`int`, `list`, `None`)
`ignore_unused=False` (`bool`) | `list`
`hasDomainViolations` | returns `True` if there are domain violations in the records, returns `False` if not. | \- | `bool`
`hasDuplicateRecords` | returns `True` if there are (case insensitive) duplicate records in the symbol, returns `False` if not. | \- | `bool`
`isValid` | checks if the symbol is in a valid format, throw exceptions if `verbose=True`, recheck a symbol if `force=True` | `verbose=False`
`force=True` | `bool`
`ljustUELs` | will left justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lowerUELs` | will lowercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lstripUELs` | will left strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`pivot` | Convenience function to pivot `records` into a new shape (only symbols with >1D can be pivoted). If `index` is `None` then it is set to dimensions `[0..dimension-1]`. If `columns` is `None` then it is set to the last dimension. If `value` is `None` then the `level` values will be pivoted. Missing values in the pivot will take the value provided by `fill_value` | `index=None` (`str`, `list`, `None`)
`columns=None` (`str`, `list`, `None`)
`value` (`str`)
`fill_value=None` (`int`, `float`, `str`) | `pd.DataFrame`
`removeUELs` | removes UELs that appear in the symbol `dimensions`, If `uels` is `None` then remove all unused UELs (categories). If `dimensions` is `None` then operate on all dimensions. | `uels=None` (`str`, `list`, `None`)
`dimensions=None` (`int`, `list`, `None`) | `bool`
`renameUELs` | renames UELs (case-sensitive) that appear in the symbol `dimensions`. If `dimensions` is `None` then operate on all dimensions of the symbol. If `allow_merge=True`, the categorical object will be re-created to offer additional data flexibility. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`, `dict`)
`dimensions` (`int`, `list`, `None`)
`allow_merge=False` (`bool`) | `None`
`reorderUELs` | reorders the UELs in the symbol `dimensions`. If `uels` is `None`, reorder UELs to data order and append any unused categories. If `dimensions` is `None` then reorder UELs in all dimensions of the symbol. | `uels` (`str`, `list`, `dict`, `None`)
`dimensions` (`int`, `list`, `None`) | `None`
`rjustUELs` | will right justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`rstripUELs` | will right strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`setRecords` | main convenience method to set standard `pandas.DataFrame` records. If `uels_on_axes=True` `setRecords` will assume that all domain information is contained in the axes of the pandas object – data will be flattened (if necessary). | `records` (many types) | `None`
`setUELs` | set the UELs for symbol `dimensions`. If `dimensions` is `None` then set UELs for all dimensions. If `rename=True`, then the old UEL names will be renamed with the new UEL names. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`)
`rename=False` (`bool`) | `None`
`stripUELs` | will strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`titleUELs` | will title (capitalize all individual words) in all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`toDense` | convert `column` to a dense `numpy.array` format | `column="level"` (`str`) | `numpy.array` or `None`
`toDict` | convenience method to return symbol records as a Python dictionary. `columns` will control which attributes to include in the `dict`. `orient` can take values `natural` or `columns` and will control the shape of the `dict`. Must use `orient="columns"` if attempting to set symbol records with `setRecords`. | `columns="level"` (str)
`orient="natural"` (str) | `dict`
`toList` | convenience method to return symbol records as a Python list, the `columns` argument will control with attributes to include in the list | `columns="level"` (str) | `list`
`toSparseCoo` | convert `column` to a sparse COOrdinate `numpy.array` format | `column="level"` (`str`) | sparse matrix format or `None`
`toValue` | convenience method to return symbol records as a Python float. Only possible with scalar symbols. Attribute can be specified with `column` argument. | `column="level"` (str) | `float`
`upperUELs` | will uppercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`whereMax` | find the domain entry of records with a maximum value (return first instance only) | `column="level"` (`str`) | `list` of `str` or `None`
`whereMaxAbs` | find the domain entry of records with a maximum absolute value (return first instance only) | `column="level"` (`str`) | `list` of `str` or `None`
`whereMin` | find the domain entry of records with a minimum value (return first instance only) | `column="level"` (`str`) | `list` of `str` or `None`

## Adding Variable Records
Three possibilities exist to assign symbol records to a variable (roughly ordered in complexity):

  1. Setting the argument `records` in the set constructor/container method (internally calls `setRecords`) - creates a data copy
  2. Using the symbol method `setRecords` \- creates a data copy
  3. Setting the property `records` directly - does not create a data copy

If the data is in a convenient format, a user may want to pass the records directly within the variable constructor. This is an optional keyword argument and internally the variable constructor will simply call the `setRecords` method. In contrast to the `setRecords` methods in in either the Set or Parameter classes the `setRecords` method for variables will only accept Pandas DataFrames and specially structured `dict` for creating records from matrices. This restriction is out of necessity because to properly set a record for a Variable the user must pass data for the `level`, `marginal`, `lower`, `upper` and `scale` attributes. That said, any missing attributes will be filled in with the GAMS default record values (see: [Variable Types](UG_Variables.html#UG_Variables_VariableTypes)), default `scale` value is always 1, and the default `level` and `marginal` values are 0 for all variable types). We show a few examples of ways to create differently structured variables:

Example #1 - Create a GAMS scalar variable

import gams.transfer as gt

m = gt.Container()

pi = gt.Variable(m, "pi", records=pd.DataFrame(data=[3.14159], columns=["level"]))

# NOTE: the above syntax is equivalent to -
# pi = gt.Variable(m, "pi", "free")
# pi.setRecords(pd.DataFrame(data=[3.14159], columns=["level"]))
# NOTE: the above syntax is also equivalent to -
# m.addVariable("pi", "free", records=pd.DataFrame(data=[3.14159], columns=["level"]))
In [1]: pi.records

Out[1]:

level marginal lower upper scale

0 3.14159 0.0 -inf inf 1.0

Example #2 - Create a 1D variable (defined over `*`) from a list of tuples

In this example we only set the `marginal` values.

import gams.transfer as gt

m = gt.Container()

v = gt.Variable(

m,

"v",

"free",

domain=["*"],

records=pd.DataFrame(

data=[("i" \+ str(i), i) for i in range(5)], columns=["domain", "marginal"]

),

)

In [1]: v.records

Out[1]:

uni level marginal lower upper scale

0 i0 0.0 0.0 -inf inf 1.0

1 i1 0.0 1.0 -inf inf 1.0

2 i2 0.0 2.0 -inf inf 1.0

3 i3 0.0 3.0 -inf inf 1.0

4 i4 0.0 4.0 -inf inf 1.0

Example #3 - Create a 1D variable (defined over a set) from a list of tuples

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=["i" \+ str(i) for i in range(5)])

v = gt.Variable(

m,

"v",

"free",

domain=i,

records=pd.DataFrame(

data=[("i" \+ str(i), i) for i in range(5)], columns=["domain", "marginal"]

),

)

In [1]: v.records

Out[1]:

i level marginal lower upper scale

0 i0 0.0 0.0 -inf inf 1.0

1 i1 0.0 1.0 -inf inf 1.0

2 i2 0.0 2.0 -inf inf 1.0

3 i3 0.0 3.0 -inf inf 1.0

4 i4 0.0 4.0 -inf inf 1.0

Example #4 - Create a 2D positive variable, specifying no numerical data

import gams.transfer as gt

import pandas as pd

m = gt.Container()

v = gt.Variable(

m,

"v",

"positive",

["*", "*"],

records=pd.DataFrame([("seattle", "san-diego"), ("chicago", "madison")]),

)

In [1]: v.records

Out[1]:

uni_0 uni_1 level marginal lower upper scale

0 seattle san-diego 0.0 0.0 0.0 inf 1.0

1 chicago madison 0.0 0.0 0.0 inf 1.0

Example #5 - Create a 2D variable (defined over a set) from a matrix

import gams.transfer as gt

import pandas as pd

import numpy as np

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=["i" \+ str(i) for i in range(5)])

j = gt.Set(m, "j", ["*"], records=["j" \+ str(i) for i in range(5)])

a = gt.Parameter(

m,

"a",

[i, j],

records=[("i" \+ str(i), "j" \+ str(j), i + j) for i in range(5) for j in range(5)],

)

# create a free variable and set the level and marginal attributes from matricies
v = gt.Variable(

m, "v", domain=[i, j], records={"level": a.toDense(), "marginal": a.toDense()}

)

# if not specified, the toDense() method will convert the level values to a matrix
In [1]: v.toDense()

Out[1]:

array([[0., 1., 2., 3., 4.],

[1., 2., 3., 4., 5.],

[2., 3., 4., 5., 6.],

[3., 4., 5., 6., 7.],

[4., 5., 6., 7., 8.]])

Example #6 - Create a 1D variable from a pandas Series

import gams.transfer as gt

import pandas as pd

s = pd.Series(index=["a", "b", "c"], data=[i + 1 for i in range(3)])

m = gt.Container()

v = gt.Variable(m, "v", domain=["*"], records=s, uels_on_axes=True)

In [1]: v.records

Out[1]:

uni level marginal lower upper scale

0 a 1.0 0.0 -inf inf 1.0

1 b 2.0 0.0 -inf inf 1.0

2 c 3.0 0.0 -inf inf 1.0

**Note:** `transfer` will assume that the `level` value is being set if attributes cannot be found in the axes

Example #7 - Create a 1D variable from a pandas Series (set only the marginal)

import gams.transfer as gt

import pandas as pd

# NOTE: we include the "marginal" label in level 1 of the MultiIndex
s = pd.Series(

index=pd.MultiIndex.from_product([["a", "b", "c"], ["marginal"]]),

data=[i + 1 for i in range(3)],

)

m = gt.Container()

v = gt.Variable(m, "v", domain=["*"], records=s, uels_on_axes=True)

In [1]: v.records

Out[1]:

uni level marginal lower upper scale

0 a 0.0 1.0 -inf inf 1.0

1 b 0.0 2.0 -inf inf 1.0

2 c 0.0 3.0 -inf inf 1.0

**Note:** `transfer` will search the axes for any variable attributes and set those attributes provided. It is necessary to include all attributes into the same axes level (if a MultiIndex) without any other UELs – if other UELs are found in the same level then all element will be interpreted as UELs and could result in GAMS domain violations.

Example #8 - Create a 2D variable from a DataFrame (uels_on_axes=True)

import gams.transfer as gt

import pandas as pd

import numpy as np

dim1 = [f"d{i}" for i in range(2)]

dim2 = [f"e{i}" for i in range(2)]

dim3 = [f"f{i}" for i in range(2)]

dim4 = [f"g{i}" for i in range(2)]

rng = np.random.default_rng(seed=100)

df = pd.DataFrame(

data=rng.uniform(size=(4, 4)),

index=pd.MultiIndex.from_product([dim1, dim2]),

columns=pd.MultiIndex.from_product([dim3, dim4]),

)

In [1]: df

Out[1]:

f0 f1

g0 g1 g0 g1

d0 e0 0.834982 0.596554 0.288863 0.042952

e1 0.973654 0.596472 0.790263 0.910339

d1 e0 0.688154 0.189991 0.981479 0.284740

e1 0.629273 0.581036 0.599912 0.535248

m = gt.Container()

v = gt.Variable(m, "v", domain=["*"] * 4, records=df, uels_on_axes=True)

In [8]: v.records

Out[8]:

uni_0 uni_1 uni_2 uni_3 level marginal lower upper scale

0 d0 e0 f0 g0 0.834982 0.0 -inf inf 1.0

1 d0 e0 f0 g1 0.596554 0.0 -inf inf 1.0

2 d0 e0 f1 g0 0.288863 0.0 -inf inf 1.0

3 d0 e0 f1 g1 0.042952 0.0 -inf inf 1.0

4 d0 e1 f0 g0 0.973654 0.0 -inf inf 1.0

5 d0 e1 f0 g1 0.596472 0.0 -inf inf 1.0

6 d0 e1 f1 g0 0.790263 0.0 -inf inf 1.0

7 d0 e1 f1 g1 0.910339 0.0 -inf inf 1.0

8 d1 e0 f0 g0 0.688154 0.0 -inf inf 1.0

9 d1 e0 f0 g1 0.189991 0.0 -inf inf 1.0

10 d1 e0 f1 g0 0.981479 0.0 -inf inf 1.0

11 d1 e0 f1 g1 0.284740 0.0 -inf inf 1.0

12 d1 e1 f0 g0 0.629273 0.0 -inf inf 1.0

13 d1 e1 f0 g1 0.581036 0.0 -inf inf 1.0

14 d1 e1 f1 g0 0.599912 0.0 -inf inf 1.0

15 d1 e1 f1 g1 0.535248 0.0 -inf inf 1.0

## Directly Set Records
As with sets, the primary advantage of the `setRecords` method is that `transfer` will convert many different (and convenient) data types into the standard data format (a Pandas DataFrame). Users that require higher performance will want to directly pass the `Container` a reference to a valid Pandas DataFrame, thereby skipping some of these computational steps. This places more burden on the user to pass the data in a valid standard form, but it speeds the records setting process and it avoids making a copy of the data in memory. In this section we walk the user through an example of how to set records directly.

Example #1 - Correctly set records (directly)

import gams.transfer as gt

import pandas as pd

import numpy as np

df = pd.DataFrame(

data=[

("h" \+ str(h), "m" \+ str(m), "s" \+ str(s))

for h in range(8760)

for m in range(60)

for s in range(60)

],

columns=["h", "m", "s"],

)

# it is necessary to specify all variable attributes if setting records directly
# NOTE: all numeric data must be type float
df["level"] = np.random.uniform(0, 100, len(df))

df["marginal"] = 0.0

df["lower"] = gt.SpecialValues.NEGINF

df["upper"] = gt.SpecialValues.POSINF

df["scale"] = 1.0

m = gt.Container()

hrs = gt.Set(m, "h", records=df["h"].unique())

mins = gt.Set(m, "m", records=df["m"].unique())

secs = gt.Set(m, "s", records=df["s"].unique())

df["h"] = df["h"].astype(hrs.records["uni"].dtype)

df["m"] = df["m"].astype(mins.records["uni"].dtype)

df["s"] = df["s"].astype(secs.records["uni"].dtype)

a = gt.Variable(m, "a", domain=[hrs, mins, secs])

# set records
a.records = df

In [1]: a.isValid()

Out[1]: True

**Attention:** All numeric data in the records will need to be type `float` in order to maintain a valid symbol.

In this example we create a large variable (31,536,000 records and 8880 unique domain elements – we mimic data that is labeled for every second in one year) and assign it to a variable with `a.records`. `transfer` requires that all domain columns must be a categorical data type, furthermore this categorical must be ordered. The `records` setter function does very little work other than checking if the object being set is a DataFrame. This places more responsibility on the user to create a DataFrame that complies with the standard format. In Example #1 we take care to properly reference the categorical data types from the domain sets – and in the end `a.isValid() = True`. As with Set and Parameters, users can use the `.isValid(verbose=True)` method to debug any structural issues.

## Generate Variable Records
Generating the initial `pandas.DataFrame` object could be difficult for `Variable` symbols that have a large number of records and a small number of UELs – these higher dimensional symbols will benefit from the `generateRecords` convenience function. Internally, `generateRecords` computes the dense Cartesian product of all the domain sets that define a symbol (`generateRecords` will only work on symbols where `<symbol>.domain_type == "regular"`).

Example #1 - Create a large (dense) 4D variable

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Variable(m, "a", "free", [i, j, k, l])

# generate the records
a.generateRecords()

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l level marginal lower upper scale

0 i0 j0 k0 l0 0.470248 0.0 -inf inf 1.0

1 i0 j0 k0 l1 0.924286 0.0 -inf inf 1.0

2 i0 j0 k0 l2 0.347550 0.0 -inf inf 1.0

3 i0 j0 k0 l3 0.937009 0.0 -inf inf 1.0

4 i0 j0 k0 l4 0.050716 0.0 -inf inf 1.0

... ... ... ... ... ... ... ... ... ...

6249995 i49 j49 k49 l45 0.385032 0.0 -inf inf 1.0

6249996 i49 j49 k49 l46 0.029305 0.0 -inf inf 1.0

6249997 i49 j49 k49 l47 0.440716 0.0 -inf inf 1.0

6249998 i49 j49 k49 l48 0.432931 0.0 -inf inf 1.0

6249999 i49 j49 k49 l49 0.157107 0.0 -inf inf 1.0

[6250000 rows x 9 columns]

**Note:** In Example #1 a large 4D variable was generated – by default, only the `level` value of these records are randomly drawn from the interval `[0,1]` (uniform distribution). Other variable attributes take the default record value.

As with `Parameters`, it is possible to generate a sparse variable with the `density` argument to `generateRecords`. We extend this example by passing our own custom `func` argument that will control the behavior of the `value` columns. The `func` argument accepts a `dict` of `callables` (i.e., a reference to a function).

Example #2 - Create a large (sparse) 4D variable with normally distributed values

import gams.transfer as gt

import numpy as np

# create a custom function to pass to `generateRecords`
def level_dist(size):

return np.random.normal(loc=10.0, scale=2.3, size=size)

def marginal_dist(size):

return np.random.normal(loc=0.5, scale=0.1, size=size)

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Variable(m, "a", "free", [i, j, k, l])

# generate the records
a.generateRecords(density=0.05, func={"level":level_dist, "marginal":marginal_dist})

In [1]: a.isValid()

Out[1]: True

In [12]: a.records

Out[12]:

i j k l level marginal lower upper scale

0 i0 j0 k0 l36 11.105235 0.468989 -inf inf 1.0

1 i0 j0 k0 l40 5.697361 0.478019 -inf inf 1.0

2 i0 j0 k1 l17 11.900784 0.473814 -inf inf 1.0

3 i0 j0 k1 l24 10.105931 0.456925 -inf inf 1.0

4 i0 j0 k1 l31 8.444142 0.490966 -inf inf 1.0

... ... ... ... ... ... ... ... ... ...

312495 i49 j49 k47 l17 11.523186 0.508001 -inf inf 1.0

312496 i49 j49 k47 l20 9.341183 0.739237 -inf inf 1.0

312497 i49 j49 k47 l26 10.705808 0.581103 -inf inf 1.0

312498 i49 j49 k47 l32 7.910963 0.479655 -inf inf 1.0

312499 i49 j49 k49 l8 11.800414 0.628040 -inf inf 1.0

[312500 rows x 9 columns]

In [3]: a.records["level"].mean()

Out[3]: 10.004072307451391

In [4]: a.records["level"].std()

Out[4]: 2.292569938350144

In [5]: a.records["marginal"].mean()

Out[5]: 0.49970172269778

In [6]: a.records["marginal"].std()

Out[6]: 0.09998772109802055

**Note:** The custom `callable` function reference must expose a `size` argument. It might be tedious to know the exact number of the records that will be generated, especially if a fractional density is specified; therefore, the `generateRecords` method will pass in the correct size automatically. Users are encouraged to use the Numpy suite of random distributions when generating samples – custom functions have the potential to be computationally burdensome if a symbol has a large number of records.

# Equation
There are two different ways to create a GAMS equation and add it to a `Container`.

  1. Use `Equation` constructor
  2. Use the `Container` method `addEquation` (which internally calls the `Equation` constructor)

## Constructor
Constructor Arguments

Argument | Type | Description | Required | Default
---|---|---|---|---
`container` | `Container` | A reference to the `Container` object that the symbol is being added to | Yes | \-
`description` | `str` | Description of symbol | No | ""
`domain` | `list`, `str`, or `Set/Alias` | List of domains given either as string (`*` for universe set) or as reference to a Set/Alias object, an empty domain list will create a scalar equation | No | []
`domain_forwarding` | `bool` or `list` | Flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | No | False
`name` | `str` | Name of symbol | Yes | \-
`records` | many | Symbol records | No | None
`type` | `str` | Type of equation being created [`eq` (or `E`/`e`), `geq` (or `G`/`g`), `leq` (or `L`/`l`), `nonbinding` (or `N`/`n`), `external` (or `X`/`x`)] | Yes | \-
`uels_on_axes` | `bool` | Instructs `setRecords` to assume symbol domain information is contained in the axes of the Pandas object | No | False

**Note:** Equation records can be updated through the object constructor (a new object will not be created) if a symbol of the same name already exists in the container, has the same domain, has the same `type`, and has the same `domain_forwarding` state. The symbol description will only be updated if new text is provided.

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`container` | reference to the `Container` that the symbol belongs to | `Container` | \-
`description` | description of symbol | `str` | \-
`dimension` | dimension of symbol | `int` | setting is a shorthand notation to create `["*"] * n` domains in symbol
`domain` | list of domains given either as string (`*` for universe set) or as reference to the Set/Alias object | `list`, `str`, or `Set/Alias` | \-
`domain_forwarding` | flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | `bool` or `list` | no effect after records have been set
`domain_labels` | column headings for the `records` DataFrame | `list` of `str` | will add a `_<dimension>` tag to user supplied column names (if not unique)
`domain_names` | string version of domain names | `list` of `str` | \-
`domain_type` | `none`, `relaxed` or `regular` depending on state of domain links | `str` | \-
`is_scalar` | `True` if the `len(self.domain) = 0` | `bool` | \-
`modified` | Flag that identifies if the `Equation` has been modified | `bool` | \-
`name` | name of symbol | `str` | sets the GAMS name of the symbol
`number_records` | number of symbol records (i.e., returns `len(self.records)` if not `None`) | `int` | \-
`records` | the main symbol records | `pandas.DataFrame` | responsive to `domain_forwarding` state
`shape` | a tuple describing the array dimensions if `records` were converted with `.toDense()` | `tuple` | \-
`summary` | output a `dict` of only the metadata | `dict` | \-
`type` | `str` type of variable | `str` | \-

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`addUELs` | adds UELs to the symbol `dimensions`. If `dimensions` is `None` then add UELs to all dimensions. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`) | `None`
`capitalizeUELs` | will capitalize all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`casefoldUELs` | will casefold all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`countDomainViolations` | returns the count of how many records contain at least one domain violation | \- | `int`
`countDuplicateRecords` | returns the count of how many (case insensitive) duplicate records exist | \- | `int`
`countEps` | total number of `SpecialValues.EPS` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countNA` | total number of `SpecialValues.NA` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countNegInf` | total number of `SpecialValues.NEGINF` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countPosInf` | total number of `SpecialValues.POSINF` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`countUndef` | total number of `SpecialValues.UNDEF` across all `columns` | `columns="level"` (`str`, `list`) | `int` or `None`
`dropDefaults` | drop records that are set to GAMS default records (check `.default_records` property for values) | \- | `None`
`dropDomainViolations` | drop records from the symbol that contain a domain violation | \- | `None`
`dropDuplicateRecords` | drop records with (case insensitive) duplicate domains from the symbol – `keep` argument can take values of "first" (keeps the first instance of a duplicate record), "last" (keeps the last instance of a record), or `False` (drops all duplicates including the first and last) | `keep="first"` (str, `False`) | `None`
`dropEps` | drop records from the symbol that are `GAMS EPS` (zero `0.0` records will be retained) | \- | `None`
`dropMissing` | drop records from the symbol that are `NaN` (includes both `NA` and `Undef` special values) | \- | `None`
`dropNA` | drop records from the symbol that are `GAMS NA` | \- | `None`
`dropUndef` | drop records from the symbol that are `GAMS Undef` | \- | `None`
`equals` | Used to compare the symbol to another symbol. The `columns` argument allows the user to numerically compare only specified equation attributes (default is to compare all). If `check_uels=True` then check both used and unused UELs and confirm same order, otherwise only check used UELs in data and do not check UEL order. If `check_meta_data=True` then check that symbol name, description and equation type are the same, otherwise skip. `rtol` (relative tolerance) and `atol` (absolute tolerance) set equality tolerances; can be different tolerances for different equation attributes (if specified as a `dict`). If `verbose=True` will return an exception from the asserter describing the nature of the difference. | `columns=["level", "marginal", "lower", "upper", "scale"]`
`check_uels=True` (`bool`)
`check_meta_data=True` (`bool`)
`rtol=0.0` (`int`, `float`, `None`)
`atol=0.0` (`int`, `float`, `None`)
`verbose=False` (`bool`) | `bool`
`findDomainViolations` | get a view of the records DataFrame that contain any domain violations | \- | `pandas.DataFrame`
`findDuplicateRecords` | get a view of the records DataFrame that contain any (case insensitive) duplicate domains – `keep` argument can take values of "first" (finds all duplicates while keeping the first instance as unique), "last" (finds all duplicates while keeping the last instance as unique), or `False` (finds all duplicates) | `keep="first"` (str, `False`) | `pandas.DataFrame`
`findEps` | find positions of `SpecialValues.EPS` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findNA` | find positions of `SpecialValues.NA` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findNegInf` | find positions of `SpecialValues.NEGINF` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findPosInf` | find positions of `SpecialValues.POSINF` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`findUndef` | find positions of `SpecialValues.Undef` in `column` | `column="level"` (`str`) | `pandas.DataFrame` or `None`
`generateRecords` | convenience method to set standard `pandas.DataFrame` formatted records given domain set information. Will generate records with the Cartesian product of all domain sets. The `density` argument can take any value on the interval `[0,1]`. If `density` is <1 then randomly selected records will be removed. `density` will accept a `list` of length `dimension` -- allows users to specify a density per symbol dimension. Random number state can be set with `seed` argument. | `density=1.0` (`float`, `list`)
`func=numpy.random.uniform(0,1)` (`dict` of `callables`)
`seed=None` (`int`, `None`) | `None`
`getMaxAbsValue` | get the maximum absolute value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getMaxValue` | get the maximum value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getMeanValue` | get the mean value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getMinValue` | get the minimum value across all `columns` | `columns="level"` (`str`, `list`) | `float` or `None`
`getSparsity` | get the sparsity of the symbol w.r.t the cardinality | \- | `float`
`getUELs` | gets UELs from symbol `dimensions`. If `dimensions` is `None` then get UELs from all dimensions (maintains order). The argument `codes` accepts a list of `str` UELs and will return the corresponding `int`; must specify a single dimension if passing `codes`. Returns only UELs in the data if `ignore_unused=True`, otherwise return all UELs. | `dimensions=None` (`int`, `list`, `None`)
`codes=None` (`int`, `list`, `None`)
`ignore_unused=False` (`bool`) | `list`
`hasDomainViolations` | returns `True` if there are domain violations in the records, returns `False` if not. | \- | `bool`
`hasDuplicateRecords` | returns `True` if there are (case insensitive) duplicate records in the symbol, returns `False` if not. | \- | `bool`
`isValid` | checks if the symbol is in a valid format, throw exceptions if `verbose=True`, recheck a symbol if `force=True` | `verbose=False`
`force=True` | `bool`
`ljustUELs` | will left justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lowerUELs` | will lowercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lstripUELs` | will left strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`pivot` | Convenience function to pivot `records` into a new shape (only symbols with >1D can be pivoted). If `index` is `None` then it is set to dimensions `[0..dimension-1]`. If `columns` is `None` then it is set to the last dimension. If `value` is `None` then the `level` values will be pivoted. Missing values in the pivot will take the value provided by `fill_value` | `index=None` (`str`, `list`, `None`)
`columns=None` (`str`, `list`, `None`)
`value` (`str`)
`fill_value=None` (`int`, `float`, `str`) | `pd.DataFrame`
`removeUELs` | removes UELs that appear in the symbol `dimensions`, If `uels` is `None` then remove all unused UELs (categories). If `dimensions` is `None` then operate on all dimensions. | `uels=None` (`str`, `list`, `None`)
`dimensions=None` (`int`, `list`, `None`) | `bool`
`renameUELs` | renames UELs (case-sensitive) that appear in the symbol `dimensions`. If `dimensions` is `None` then operate on all dimensions of the symbol. If `allow_merge=True`, the categorical object will be re-created to offer additional data flexibility. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`, `dict`)
`dimensions` (`int`, `list`, `None`)
`allow_merge=False` (`bool`) | `None`
`reorderUELs` | reorders the UELs in the symbol `dimensions`. If `uels` is `None`, reorder UELs to data order and append any unused categories. If `dimensions` is `None` then reorder UELs in all dimensions of the symbol. | `uels` (`str`, `list`, `dict`, `None`)
`dimensions` (`int`, `list`, `None`) | `None`
`rjustUELs` | will right justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`rstripUELs` | will right strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`setRecords` | main convenience method to set standard `pandas.DataFrame` records. If `uels_on_axes=True` `setRecords` will assume that all domain information is contained in the axes of the pandas object – data will be flattened (if necessary). | `records` (many types) | `None`
`setUELs` | set the UELs for symbol `dimensions`. If `dimensions` is `None` then set UELs for all dimensions. If `rename=True`, then the old UEL names will be renamed with the new UEL names. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`)
`rename=False` (`bool`) | `None`
`stripUELs` | will strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`titleUELs` | will title (capitalize all individual words) in all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`toDense` | convert `column` to a dense `numpy.array` format | `column="level"` (`str`) | `numpy.array` or `None`
`toDict` | convenience method to return symbol records as a Python dictionary. `columns` will control which attributes to include in the `dict`. `orient` can take values `natural` or `columns` and will control the shape of the `dict`. Must use `orient="columns"` if attempting to set symbol records with `setRecords`. | `columns="level"` (str)
`orient="natural"` (str) | `dict`
`toList` | convenience method to return symbol records as a Python list, the `columns` argument will control with attributes to include in the list | `columns="level"` (str) | `list`
`toSparseCoo` | convert `column` to a sparse COOrdinate `numpy.array` format | `column="level"` (`str`) | sparse matrix format or `None`
`toValue` | convenience method to return symbol records as a Python float. Only possible with scalar symbols. Attribute can be specified with `column` argument. | `column="level"` (str) | `float`
`upperUELs` | will uppercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`whereMax` | find the domain entry of records with a maximum value (return first instance only) | `column="level"` (`str`) | `list` of `str` or `None`
`whereMaxAbs` | find the domain entry of records with a maximum absolute value (return first instance only) | `column="level"` (`str`) | `list` of `str` or `None`
`whereMin` | find the domain entry of records with a minimum value (return first instance only) | `column="level"` (`str`) | `list` of `str` or `None`

## Adding Equation Records
Adding equation records mimics that of variables – three possibilities exist to assign symbol records to an equation (roughly ordered in complexity):

  1. Setting the argument `records` in the set constructor/container method (internally calls `setRecords`) - creates a data copy
  2. Using the symbol method `setRecords` \- creates a data copy
  3. Setting the property `records` directly - does not create a data copy

Setting equation records require the user to be explicit with the type of equation that is being created; in contrast to setting variable records (where the default variable is considered to be `free`).

If the data is in a convenient format, a user may want to pass the records directly within the equation constructor. This is an optional keyword argument and internally the equation constructor will simply call the `setRecords` method. In contrast to the `setRecords` methods in in either the Set or Parameter classes the `setRecords` method for variables will only accept Pandas DataFrames and specially structured `dict` for creating records from matrices. This restriction is out of necessity because to properly set a record for an Equation the user must pass data for the `level`, `marginal`, `lower`, `upper` and `scale` attributes. That said, any missing attributes will be filled in with the GAMS default record values (`level = 0.0`, `marginal = 0.0`, `lower = -inf`, `upper = inf`, `scale = 1.0`). We show a few examples of ways to create differently structured variables:

Example #1 - Create a GAMS scalar equation

import gams.transfer as gt

m = gt.Container()

# here we create an equality (=E=) equation
z = gt.Equation(m, "z", "eq", records=pd.DataFrame(data=[3.14159], columns=["level"]))

# NOTE: the above syntax is equivalent to -
# pi = gt.Equation(m, "pi", "eq")
# pi.setRecords(pd.DataFrame(data=[3.14159], columns=["level"]))
# NOTE: the above syntax is also equivalent to -
# m.addEquation("pi", "eq", records=pd.DataFrame(data=[3.14159], columns=["level"]))
In [1]: pi.records

Out[1]:

level marginal lower upper scale

0 3.14159 0.0 -inf inf 1.0

Example #2 - Create a 1D Equation (defined over `*`) from a list of tuples

In this example we only set the `marginal` values.

import gams.transfer as gt

m = gt.Container()

# here we define a greater than or equal (=G=) equation
i = gt.Equation(

m,

"i",

"geq",

domain=["*"],

records=pd.DataFrame(

data=[("i" \+ str(i), i) for i in range(5)], columns=["domain", "marginal"]

),

)

In [1]: i.type

Out[1]: 'geq'

In [2]: i.records

Out[2]:

uni level marginal lower upper scale

0 i0 0.0 0.0 -inf inf 1.0

1 i1 0.0 1.0 -inf inf 1.0

2 i2 0.0 2.0 -inf inf 1.0

3 i3 0.0 3.0 -inf inf 1.0

4 i4 0.0 4.0 -inf inf 1.0

Example #3 - Create a 1D Equation (defined over a set) from a list of tuples

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=["i" \+ str(i) for i in range(5)])

# here we define a less than or equal (=L=) equation
e = gt.Equation(

m,

"e",

"leq",

domain=i,

records=pd.DataFrame(

data=[("i" \+ str(i), i) for i in range(5)], columns=["domain", "marginal"]

),

)

In [1]: i.type

Out[1]: 'leq'

In [5]: e.records

Out[5]:

i level marginal lower upper scale

0 i0 0.0 0.0 -inf inf 1.0

1 i1 0.0 1.0 -inf inf 1.0

2 i2 0.0 2.0 -inf inf 1.0

3 i3 0.0 3.0 -inf inf 1.0

4 i4 0.0 4.0 -inf inf 1.0

Example #4 - Create a 2D equation, specifying no numerical data

import gams.transfer as gt

import pandas as pd

m = gt.Container()

e = gt.Equation(

m,

"e",

"eq",

["*", "*"],

records=pd.DataFrame([("seattle", "san-diego"), ("chicago", "madison")]),

)

In [1]: e.records

Out[1]:

uni_0 uni_1 level marginal lower upper scale

0 seattle san-diego 0.0 0.0 -inf inf 1.0

1 chicago madison 0.0 0.0 -inf inf 1.0

Example #5 - Create a 2D equation (defined over a set) from a matrix

import gams.transfer as gt

import pandas as pd

import numpy as np

m = gt.Container()

i = gt.Set(m, "i", ["*"], records=["i" \+ str(i) for i in range(5)])

j = gt.Set(m, "j", ["*"], records=["j" \+ str(i) for i in range(5)])

a = gt.Parameter(

m,

"a",

[i, j],

records=[("i" \+ str(i), "j" \+ str(j), i + j) for i in range(5) for j in range(5)],

)

# create a nonbinding (=N=) equation and set the level and marginal attributes from matricies
e = gt.Equation(

m, "e", "nonbinding", domain=[i, j], records={"level": a.toDense(), "marginal": a.toDense()}

)

In [1]: e.records

Out[1]:

i j level marginal lower upper scale

0 i0 j1 1.0 1.0 -inf inf 1.0

1 i0 j2 2.0 2.0 -inf inf 1.0

2 i0 j3 3.0 3.0 -inf inf 1.0

3 i0 j4 4.0 4.0 -inf inf 1.0

4 i1 j0 1.0 1.0 -inf inf 1.0

5 i1 j1 2.0 2.0 -inf inf 1.0

6 i1 j2 3.0 3.0 -inf inf 1.0

7 i1 j3 4.0 4.0 -inf inf 1.0

8 i1 j4 5.0 5.0 -inf inf 1.0

9 i2 j0 2.0 2.0 -inf inf 1.0

10 i2 j1 3.0 3.0 -inf inf 1.0

11 i2 j2 4.0 4.0 -inf inf 1.0

12 i2 j3 5.0 5.0 -inf inf 1.0

13 i2 j4 6.0 6.0 -inf inf 1.0

14 i3 j0 3.0 3.0 -inf inf 1.0

15 i3 j1 4.0 4.0 -inf inf 1.0

16 i3 j2 5.0 5.0 -inf inf 1.0

17 i3 j3 6.0 6.0 -inf inf 1.0

18 i3 j4 7.0 7.0 -inf inf 1.0

19 i4 j0 4.0 4.0 -inf inf 1.0

20 i4 j1 5.0 5.0 -inf inf 1.0

21 i4 j2 6.0 6.0 -inf inf 1.0

22 i4 j3 7.0 7.0 -inf inf 1.0

23 i4 j4 8.0 8.0 -inf inf 1.0

# if not specified, the toDense() method will convert the level values to a matrix
In [2]: e.toDense()

Out[2]:

array([[0., 1., 2., 3., 4.],

[1., 2., 3., 4., 5.],

[2., 3., 4., 5., 6.],

[3., 4., 5., 6., 7.],

[4., 5., 6., 7., 8.]])

Example #6 - Create a 1D equation from a pandas Series

import gams.transfer as gt

import pandas as pd

s = pd.Series(index=["a", "b", "c"], data=[i + 1 for i in range(3)])

m = gt.Container()

e = gt.Equation(m, "e", "eq", domain=["*"], records=s, uels_on_axes=True)

In [1]: e.records

Out[1]:

uni level marginal lower upper scale

0 a 1.0 0.0 -inf inf 1.0

1 b 2.0 0.0 -inf inf 1.0

2 c 3.0 0.0 -inf inf 1.0

**Note:** `transfer` will assume that the `level` value is being set if attributes cannot be found in the axes (same behavior when setting `Variables`)

Example #7 - Create a 1D equation from a pandas Series (set only the marginal)

import gams.transfer as gt

import pandas as pd

# NOTE: we include the "marginal" label in level 1 of the MultiIndex
s = pd.Series(

index=pd.MultiIndex.from_product([["a", "b", "c"], ["marginal"]]),

data=[i + 1 for i in range(3)],

)

m = gt.Container()

e = gt.Equation(m, "e", "eq", domain=["*"], records=s, uels_on_axes=True)

In [1]: v.records

Out[1]:

uni level marginal lower upper scale

0 a 0.0 1.0 -inf inf 1.0

1 b 0.0 2.0 -inf inf 1.0

2 c 0.0 3.0 -inf inf 1.0

Example #8 - Create a 2D equation from a DataFrame (uels_on_axes=True)

import gams.transfer as gt

import pandas as pd

import numpy as np

dim1 = [f"d{i}" for i in range(2)]

dim2 = [f"e{i}" for i in range(2)]

dim3 = [f"f{i}" for i in range(2)]

dim4 = [f"g{i}" for i in range(2)]

rng = np.random.default_rng(seed=100)

df = pd.DataFrame(

data=rng.uniform(size=(4, 4)),

index=pd.MultiIndex.from_product([dim1, dim2]),

columns=pd.MultiIndex.from_product([dim3, dim4]),

)

In [1]: df

Out[1]:

f0 f1

g0 g1 g0 g1

d0 e0 0.834982 0.596554 0.288863 0.042952

e1 0.973654 0.596472 0.790263 0.910339

d1 e0 0.688154 0.189991 0.981479 0.284740

e1 0.629273 0.581036 0.599912 0.535248

m = gt.Container()

e = gt.Equation(m, "e", "eq", domain=["*"] * 4, records=df, uels_on_axes=True)

In [8]: e.records

Out[8]:

uni_0 uni_1 uni_2 uni_3 level marginal lower upper scale

0 d0 e0 f0 g0 0.834982 0.0 -inf inf 1.0

1 d0 e0 f0 g1 0.596554 0.0 -inf inf 1.0

2 d0 e0 f1 g0 0.288863 0.0 -inf inf 1.0

3 d0 e0 f1 g1 0.042952 0.0 -inf inf 1.0

4 d0 e1 f0 g0 0.973654 0.0 -inf inf 1.0

5 d0 e1 f0 g1 0.596472 0.0 -inf inf 1.0

6 d0 e1 f1 g0 0.790263 0.0 -inf inf 1.0

7 d0 e1 f1 g1 0.910339 0.0 -inf inf 1.0

8 d1 e0 f0 g0 0.688154 0.0 -inf inf 1.0

9 d1 e0 f0 g1 0.189991 0.0 -inf inf 1.0

10 d1 e0 f1 g0 0.981479 0.0 -inf inf 1.0

11 d1 e0 f1 g1 0.284740 0.0 -inf inf 1.0

12 d1 e1 f0 g0 0.629273 0.0 -inf inf 1.0

13 d1 e1 f0 g1 0.581036 0.0 -inf inf 1.0

14 d1 e1 f1 g0 0.599912 0.0 -inf inf 1.0

15 d1 e1 f1 g1 0.535248 0.0 -inf inf 1.0

## Directly Set Records
As with set, parameters and variables, the primary advantage of the `setRecords` method is that `transfer` will convert many different (and convenient) data types into the standard data format (a Pandas DataFrame). Users that require higher performance will want to directly pass the `Container` a reference to a valid Pandas DataFrame, thereby skipping some of these computational steps. This places more burden on the user to pass the data in a valid standard form, but it speeds the records setting process and it avoids making a copy of the data in memory. In this section we walk the user through an example of how to set records directly.

Example #1 - Correctly set records (directly)

import gams.transfer as gt

import pandas as pd

import numpy as np

df = pd.DataFrame(

data=[

("h" \+ str(h), "m" \+ str(m), "s" \+ str(s))

for h in range(8760)

for m in range(60)

for s in range(60)

],

columns=["h", "m", "s"],

)

# it is necessary to specify all variable attributes if setting records directly
# NOTE: all numeric data must be type float
df["level"] = np.random.uniform(0, 100, len(df))

df["marginal"] = 0.0

df["lower"] = gt.SpecialValues.NEGINF

df["upper"] = gt.SpecialValues.POSINF

df["scale"] = 1.0

m = gt.Container()

hrs = gt.Set(m, "h", records=df["h"].unique())

mins = gt.Set(m, "m", records=df["m"].unique())

secs = gt.Set(m, "s", records=df["s"].unique())

df["h"] = df["h"].astype(hrs.records["uni"].dtype)

df["m"] = df["m"].astype(mins.records["uni"].dtype)

df["s"] = df["s"].astype(secs.records["uni"].dtype)

a = gt.Equation(m, "a", "eq", domain=[hrs, mins, secs])

# set records
a.records = df

In [1]: e.isValid()

Out[1]: True

**Attention:** All numeric data in the records will need to be type `float` in order to maintain a valid symbol.

In this example we create a large equation (31,536,000 records and 8880 unique domain elements) and assign it to a variable with `a.records`. `transfer` requires that all domain columns must be a categorical data type, furthermore this categorical must be ordered. The `records` setter function does very little work other than checking if the object being set is a DataFrame. This places more responsibility on the user to create a DataFrame that complies with the standard format. In Example #1 we take care to properly reference the categorical data types from the domain sets – and in the end `a.isValid() = True`. As with Set and Parameters, users can use the `.isValid(verbose=True)` method to debug any structural issues.

## Generate Equation Records
Generating the initial `pandas.DataFrame` object could be difficult for `Equation` symbols that have a large number of records and a small number of UELs – these higher dimensional symbols will benefit from the `generateRecords` convenience function. Internally, `generateRecords` computes the dense Cartesian product of all the domain sets that define a symbol (`generateRecords` will only work on symbols where `<symbol>.domain_type == "regular"`).

Example #1 - Create a large (dense) 4D equation

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Equation(m, "a", "eq", [i, j, k, l])

# generate the records
a.generateRecords()

In [1]: a.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

i j k l level marginal lower upper scale

0 i0 j0 k0 l0 0.470248 0.0 -inf inf 1.0

1 i0 j0 k0 l1 0.924286 0.0 -inf inf 1.0

2 i0 j0 k0 l2 0.347550 0.0 -inf inf 1.0

3 i0 j0 k0 l3 0.937009 0.0 -inf inf 1.0

4 i0 j0 k0 l4 0.050716 0.0 -inf inf 1.0

... ... ... ... ... ... ... ... ... ...

6249995 i49 j49 k49 l45 0.385032 0.0 -inf inf 1.0

6249996 i49 j49 k49 l46 0.029305 0.0 -inf inf 1.0

6249997 i49 j49 k49 l47 0.440716 0.0 -inf inf 1.0

6249998 i49 j49 k49 l48 0.432931 0.0 -inf inf 1.0

6249999 i49 j49 k49 l49 0.157107 0.0 -inf inf 1.0

[6250000 rows x 9 columns]

**Note:** In Example #1 a large 4D equation was generated – by default, only the `level` value of these records are randomly drawn from the interval `[0,1]` (uniform distribution). Other variable attributes take the default record value.

As with `Variables`, it is possible to generate a sparse variable with the `density` argument to `generateRecords`. We extend this example by passing our own custom `func` argument that will control the behavior of the `value` columns. The `func` argument accepts a `dict` of `callables` (i.e., a reference to a function).

Example #2 - Create a large (sparse) 4D equation with normally distributed values

import gams.transfer as gt

import numpy as np

# create a custom function to pass to `generateRecords`
def level_dist(size):

return np.random.normal(loc=10.0, scale=2.3, size=size)

def marginal_dist(size):

return np.random.normal(loc=0.5, scale=0.1, size=size)

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(50)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(50)])

k = gt.Set(m, "k", records=[f"k{i}" for i in range(50)])

l = gt.Set(m, "l", records=[f"l{i}" for i in range(50)])

# create and define the symbol `a` with `regular` domains
a = gt.Equation(m, "a", "eq", [i, j, k, l])

# generate the records
a.generateRecords(density=0.05, func={"level":level_dist, "marginal":marginal_dist})

In [1]: a.isValid()

Out[1]: True

In [12]: a.records

Out[12]:

i j k l level marginal lower upper scale

0 i0 j0 k0 l36 11.105235 0.468989 -inf inf 1.0

1 i0 j0 k0 l40 5.697361 0.478019 -inf inf 1.0

2 i0 j0 k1 l17 11.900784 0.473814 -inf inf 1.0

3 i0 j0 k1 l24 10.105931 0.456925 -inf inf 1.0

4 i0 j0 k1 l31 8.444142 0.490966 -inf inf 1.0

... ... ... ... ... ... ... ... ... ...

312495 i49 j49 k47 l17 11.523186 0.508001 -inf inf 1.0

312496 i49 j49 k47 l20 9.341183 0.739237 -inf inf 1.0

312497 i49 j49 k47 l26 10.705808 0.581103 -inf inf 1.0

312498 i49 j49 k47 l32 7.910963 0.479655 -inf inf 1.0

312499 i49 j49 k49 l8 11.800414 0.628040 -inf inf 1.0

[312500 rows x 9 columns]

In [3]: a.records["level"].mean()

Out[3]: 10.004072307451391

In [4]: a.records["level"].std()

Out[4]: 2.292569938350144

In [5]: a.records["marginal"].mean()

Out[5]: 0.49970172269778

In [6]: a.records["marginal"].std()

Out[6]: 0.09998772109802055

**Note:** The custom `callable` function reference must expose a `size` argument. It might be tedious to know the exact number of the records that will be generated, especially if a fractional density is specified; therefore, the `generateRecords` method will pass in the correct size automatically. Users are encouraged to use the Numpy suite of random distributions when generating samples – custom functions have the potential to be computationally burdensome if a symbol has a large number of records.

# Alias
There are two different ways to create a GAMS alias and add it to a `Container`.

  1. Use `Alias` constructor
  2. Use the `Container` method `addAlias` (which internally calls the `Alias` constructor)

## Constructor
Constructor Arguments

Argument | Type | Description | Required | Default
---|---|---|---|---
`alias_with` | `Set` object | set object from which to create an alias | Yes | \-
`container` | `Container` | A reference to the `Container` object that the symbol is being added to | Yes | \-
`name` | `str` | Name of symbol | Yes | \-

**Note:** The Alias property `alias_with` can be updated through the object constructor (a new object will not be created) if a symbol of the same name already exists in the container.

Example - Creating an alias from a set

`transfer` only stores the reference to the parent set as part of the alias structure – most properties that are called from an alias object simply point to the properties of the parent set (with the exception of `container`, `name`, and `alias_with`). It is possible to create an alias from another alias object. In this case a recursive search will be performed to find the root parent set – this is the set that will ultimately be stored as the `alias_with` property. We can see this behavior in the following example:

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i" \+ str(i) for i in range(5)])

ip = gt.Alias(m, "ip", i)

ipp = gt.Alias(m, "ipp", ip)

In [1]: ip.alias_with.name

Out[1]: 'i'

In [2]: ipp.alias_with.name

Out[2]: 'i'

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`alias_with` | aliased object | `Set` | \-
`container` | reference to the `Container` that the symbol belongs to | `Container` | \-
`description` | description of symbol | `str` | \-
`dimension` | dimension of symbol | `int` | setting is a shorthand notation to create `["*"] * n` domains in symbol
`domain` | list of domains given either as string (`*` for universe set) or as reference to the Set/Alias object | `list`, `str`, or `Set/Alias` | \-
`domain_forwarding` | flag that forces set elements to be recursively included in all parent sets (i.e., implicit set growth). Can pass as a list of `bool` to control which domains to forward. | `bool` or `list` | no effect after records have been set
`domain_labels` | column headings for the `records` DataFrame | `list` of `str` | will add a `_<dimension>` tag to user supplied column names (if not unique)
`domain_names` | string version of domain names | `list` of `str` | \-
`domain_type` | `none`, `relaxed` or `regular` depending on state of domain links | `str` | \-
`is_singleton` | if symbol is a singleton set | `bool` | \-
`modified` | Flag that identifies if the `Alias` has been modified | `bool` | \-
`name` | name of symbol | `str` | sets the GAMS name of the symbol
`number_records` | number of symbol records (i.e., returns `len(self.records)` if not `None`) | `int` | \-
`records` | the main symbol records | `pandas.DataFrame` | responsive to `domain_forwarding` state
`summary` | output a `dict` of only the metadata | `dict` | \-

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`addUELs` | adds UELs to the parent set `dimensions`. If `dimensions` is `None` then add UELs to all dimensions. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`) | `None`
`equals` | Used to compare the symbol to another symbol. If `check_uels=True` then check both used and unused UELs and confirm same order, otherwise only check used UELs in data and do not check UEL order. If `check_element_text=True` then check that all set elements have the same descriptive element text, otherwise skip. If `check_meta_data=True` then check that symbol name and description are the same, otherwise skip. If `verbose=True` will return an exception from the asserter describing the nature of the difference. | `check_uels=True` (`bool`)
`check_element_text=True` (`bool`)
`check_meta_data=True` (`bool`)
`verbose=False` (`bool`) | `bool`
`capitalizeUELs` | will capitalize all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`casefoldUELs` | will casefold all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`countDomainViolations` | returns the count of how many records in the parent set contain at least one domain violation | \- | `int`
`countDuplicateRecords` | returns the count of how many (case insensitive) duplicate records exist in the parent set | \- | `int`
`dropDomainViolations` | drop records from the parent set that contain a domain violation | \- | `None`
`dropDuplicateRecords` | drop records with (case insensitive) duplicate domains from the parent set – `keep` argument can take values of "first" (keeps the first instance of a duplicate record), "last" (keeps the last instance of a record), or `False` (drops all duplicates including the first and last) | `keep="first"` (str, `False`) | `None`
`findDomainViolations` | get a view of the records DataFrame that contain any domain violations | \- | `pandas.DataFrame`
`findDuplicateRecords` | get a view of the records DataFrame from the parent set that contain any (case insensitive) duplicate domains – `keep` argument can take values of "first" (finds all duplicates while keeping the first instance as unique), "last" (finds all duplicates while keeping the last instance as unique), or `False` (finds all duplicates) | `keep="first"` (str, `False`) | `pandas.DataFrame`
`getDomainViolations` | returns a `list` of `DomainViolation` objects if any (`None` otherwise) | \- | `list` or `None`
`getSparsity` | get the sparsity of the symbol w.r.t the cardinality | \- | `float`
`getUELs` | gets UELs from the parent set `dimensions`. If `dimensions` is `None` then get UELs from all dimensions (maintains order). The argument `codes` accepts a list of `str` UELs and will return the corresponding `int`; must specify a single dimension if passing `codes`. Returns only UELs in the data if `ignore_unused=True`, otherwise return all UELs. | `dimensions=None` (`int`, `list`, `None`)
`codes=None` (`int`, `list`, `None`)
`ignore_unused=False` (`bool`) | `list`
`hasDomainViolations` | returns `True` if there are domain violations in the records of the parent set, returns `False` if not. | \- | `bool`
`hasDuplicateRecords` | returns `True` if there are (case insensitive) duplicate records in the parent set, returns `False` if not. | \- | `bool`
`isValid` | checks if the symbol is in a valid format, throw exceptions if `verbose=True`, re-check a symbol if `force=True` | `verbose=False`
`force=True` | `bool`
`ljustUELs` | will left justify all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lowerUELs` | will lowercase all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`lstripUELs` | will left strip whitespace from all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`pivot` | Convenience function to pivot `records` into a new shape (only symbols with >1D can be pivoted). If `index` is `None` then it is set to dimensions `[0..dimension-1]`. If `columns` is `None` then it is set to the last dimension. Missing values in the pivot will take the value provided by `fill_value` | `index=None` (`str`, `list`, `None`)
`columns=None` (`str`, `list`, `None`)
`fill_value=None` (`int`, `float`, `str`) | `pd.DataFrame`
`removeUELs` | removes UELs that appear in the parent set `dimensions`, If `uels` is `None` then remove all unused UELs (categories). If `dimensions` is `None` then operate on all dimensions. | `uels=None` (`str`, `list`, `None`)
`dimensions=None` (`int`, `list`, `None`) | `bool`
`renameUELs` | renames UELs (case-sensitive) that appear in the parent set `dimensions`. If `dimensions` is `None` then operate on all dimensions of the symbol. If `allow_merge=True`, the categorical object will be re-created to offer additional data flexibility. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`, `dict`)
`dimensions` (`int`, `list`, `None`)
`allow_merge=False` (`bool`) | `None`
`reorderUELs` | reorders the UELs in the parent set `dimensions`. If `uels` is `None`, reorder UELs to data order and append any unused categories. If `dimensions` is `None` then reorder UELs in all dimensions of the parent set. | `uels` (`str`, `list`, `dict`, `None`)
`dimensions` (`int`, `list`, `None`) | `None`
`rjustUELs` | will right justify all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `length` (`int`)
`fill_character=None` \- if `None`, assumes `" "`
`dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`rstripUELs` | will right strip whitespace from all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`setRecords` | main convenience method to set standard `pandas.DataFrame` formatted records. If `uels_on_axes=True` `setRecords` will assume that all domain information is contained in the axes of the pandas object – data will be flattened (if necessary). | `records` (many types) | `None`
`setUELs` | set the UELs for parent set `dimensions`. If `dimensions` is `None` then set UELs for all dimensions. If `rename=True`, then the old UEL names will be renamed with the new UEL names. ** All trailing whitespace is trimmed ** | `uels` (`str`, `list`)
`dimensions=None` (`int`, `list`, `None`)
`rename=False` (`bool`) | `None`
`stripUELs` | will strip whitespace from all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`titleUELs` | will title (capitalize all individual words) in all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`
`toList` | convenience method to return symbol records as a Python list | `include_element_text=False` (bool) | `list`
`upperUELs` | will uppercase all UELs in the parent set or a subset of specified `dimensions` in the parent set, can be chain with other `*UELs` string operations | `dimensions=None` (`int`, `list`, or `None`) - if `None`, assumes all symbols | `self`

## Adding Alias Records
The linked structure of Aliases offers some unique opportunities to access some of the setter functionality of the parent set. Specifically, `transfer` allows the user to change the `domain`, `description`, `dimension`, and `records` of the underlying parent set as a shorthand notation. We can see this behavior if we look at a modified Example #1 from Adding Set Records.

Example - Creating set records through an alias link

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i")

ip = gt.Alias(m, "ip",i)

ip.description = "adding new descriptive set text"

ip.domain = ["*", "*"]

ip.setRecords([("i" \+ str(i), "j" \+ str(j)) for i in range(3) for j in range(3)])

In [1]: i.description

Out[1]: 'adding new descriptive set text'

In [2]: i.domain

Out[2]: ['*', '*']

In [3]: i.records

Out[3]:

uni_0 uni_1 element_text

0 i0 j0

1 i0 j1

2 i0 j2

3 i1 j0

4 i1 j1

5 i1 j2

6 i2 j0

7 i2 j1

8 i2 j2

**Note:** An alias `.isValid()=True` when the underlying parent set is also valid – if the parent set is removed from the Container the alias will no longer be valid.

# UniverseAlias
There are two different ways to create a GAMS UniverseAlias (an alias to the universe) and add it to a `Container`.

  1. Use `UniverseAlias` constructor
  2. Use the `Container` method `addUniverseAlias` (which internally calls the `UniverseAlias` constructor)

## Constructor
Constructor Arguments

Argument | Type | Description | Required | Default
---|---|---|---|---
`container` | `Container` | A reference to the `Container` object that the symbol is being added to | Yes | \-
`name` | `str` | Name of symbol | Yes | \-

Example - Creating an alias to the universe

In GAMS it is possible to create aliases to the universe (i.e., the entire list of UELs) with the syntax:
```
    set i / i1, i2 /;
    alias(h,*);
    set j / j1, j2 /;
```

In this small example, `h` would be associated with all four UELs (`i1`, `i2`, `j1` and `j2`) even though set `j` was defined after the alias declaration. `transfer` mimics this behavior with the `UniverseAlias` class. Internally, the `records` attribute will always call the `<Container>.getUELs()` and build the Pandas `DataFrame` on the fly. The `UniverseAlias` class is fundamentally different from the `Alias` class because it does not point to a parent set at all; it is not possible to perform operations (like `setRecords` or `findDomainViolations`) on the parent set through a `UniverseAlias` (because there is no parent set). This means that a `UniverseAlias` can be created by only defining the symbol name. We can see this behavior in the following example:

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2"])

h = gt.UniverseAlias(m, "h")

j = gt.Set(m, "j", records=["j1", "j2"])

# -- alternative syntax --
# m = gt.Container()
# m.addSet("i", records=["i1", "i2"])
# m.addUniverseAlias("h")
# m.addSet("j", records=["j1", "j2"])
In [1]: m.data

Out[1]:

{'i': <Set `i` (0x7f9598a3bd90)>,

'h': <UniverseAlias `h` (0x7f9598a61690)>,

'j': <Set `j` (0x7f95b9359cc0)>}

In [2]: h.records

Out[2]:

uni

0 i1

1 i2

2 j1

3 j2

**Note:** Unlike other sets, the universe does not hold on to set `element_text`, thus the returned `DataFrame` for the `UniverseAlias` will only have 1 column.

## Properties
Property | Description | Type | Special Setter Behavior
---|---|---|---
`alias_with` | always `*` | `str` | \-
`container` | reference to the `Container` that the symbol belongs to | `Container` | \-
`description` | always `Aliased with *` | `str` | \-
`dimension` | always `1` | `int` | \-
`domain` | always `["*"]` | `list` of `str` | \-
`domain_labels` | always `["*"]` | `list` of `str` | \-
`domain_names` | always `["*"]` | `list` of `str` | \-
`domain_type` | always `none` | `str` | \-
`is_singleton` | always `False` | `bool` | \-
`modified` | flag that identifies if the `UniverseAlias` has been modified | `bool` | \-
`name` | name of symbol | `str` | sets the GAMS name of the symbol
`number_records` | number of symbol records (i.e., returns `len(records)` if not `None`) | `int` | \-
`records` | the main symbol records | `pandas.DataFrame` | \-
`summary` | output a `dict` of only the metadata | `dict` | \-

## Methods
Method | Description | Arguments/Defaults | Returns
---|---|---|---
`equals` | Used to compare the symbol to another symbol. If `check_uels=True` then check both used and unused UELs and confirm same order, otherwise only check used UELs in data and do not check UEL order. If `check_element_text=True` then check that all set elements have the same descriptive element text, otherwise skip. If `check_meta_data=True` then check that symbol name and description are the same, otherwise skip. If `verbose=True` will return an exception from the asserter describing the nature of the difference. | `check_uels=True` (`bool`)
`check_element_text=True` (`bool`)
`check_meta_data=True` (`bool`)
`verbose=False` (`bool`) | `bool`
`getSparsity` | always `0.0` | \- | `float`
`getUELs` | gets UELs from the `Container`. Returns only UELs in the data if `ignore_unused=True`, otherwise return all UELs. | `ignore_unused=False` (`bool`) | `list`
`isValid` | checks if the symbol is in a valid format, throw exceptions if `verbose=True`, re-check a symbol if `force=True` | `verbose=False`
`force=True` | `bool`
`pivot` | Convenience function to pivot `records` into a new shape (only symbols with >1D can be pivoted). If `index` is `None` then it is set to dimensions `[0..dimension-1]`. If `columns` is `None` then it is set to the last dimension. Missing values in the pivot will take the value provided by `fill_value` | `index=None` (`str`, `list`, `None`)
`columns=None` (`str`, `list`, `None`)
`fill_value=None` (`int`, `float`, `str`) | `pd.DataFrame`
`toList` | convenience method to return symbol records as a Python list | \- | `list`

# DomainViolation
`DomainViolation` objects are convenient containers that store information about the location of domain violations in a symbol. These objects are computed dynamically with the `getDomainViolations` method and should not be instantiated by the user (they are read-only, to the extent that this is possible in Python). However, the user may be interested in some of the information that they contain.

## Constructor
Constructor Arguments/Properties

Argument | Type | Description | Required | Default
---|---|---|---|---
`symbol` | `_Symbol` | A reference to the `_Symbol` object that has a domain violation | Yes | \-
`dimension` | `int` | An index to the dimension of the `symbol` where the domain violation exists | Yes | \-
`domain` | `Set`, `Alias` or `UniverseAlias` | A reference to the symbol domain that is the source of the domain violation | Yes | \-
`violations` | `list` | A list of all the domain elements that are causing violations | Yes | \-

---

## 6. API: Gamstransfer Additional Topics

### Table of Contents
* Validating Data
* Custom Column Headings
* Converting Records
* Comparing Symbols
* Domain Forwarding
* Domain Violations
* Duplicate Records
* Pivoting Data
* Describing Data
* describeSets
* describeParameters
* describeVariables
* describeEquations
* describeAliases
* Matrix Generation
* The Universe Set
* Customize the Universe Set
* getUELs Examples
* addUELs Examples
* removeUELs Examples
* renameUELs Examples
* reorderUELs Examples
* setUELs Examples
* String Manipulation on UELs
* Reordering Symbols
* Rename Symbols
* Removing Symbols
* GAMS Special Values
* Standard Data Formats
* GDX Read/Write
* Read GDX
* Write GDX
* GamsDatabase Read/Write
* Read GamsDatabases
* Write to GamsDatabases
* Container Read

# Validating Data
`transfer` requires that the records for all symbols exist in a standard format (Standard Data Formats) in order for them to be understood by the `Container`. It is certainly possible that the data could end up in a state that is inconsistent with the standard format (especially if setting symbol attributes directly). `transfer` includes the `.isValid()` method in order to determine if a symbol is structurally valid – this method returns a `bool`. This method does not guarantee that a symbol will be successfully written to either GDX or GMD, other data errors (duplicate records, long UEL names, or domain violations) could exist that are not tested in `.isValid()`.

For example, we create two valid sets and then check them with `.isValid()` to be sure.

**Note:** It is possible to run `.isValid()` on both the `Container` as well as the symbol object – `.isValid()` will also return a `bool` if there are any invalid symbols in the `Container` object.

Example (valid data)

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego", "washington_dc"])

j = gt.Set(m, "j", i, records=["san-diego", "washington_dc"])

In [1]: i.isValid()

Out[1]: True

In [2]: j.isValid()

Out[2]: True

In [3]: m.isValid()

Out[3]: True

The `.isValid()` method checks:

  1. If the symbol belongs to a Container
  2. If all domain set symbols exist in the Container
  3. If all domain set symbols objects are valid
  4. If any domain set is also a singleton set (not allowed in GAMS)
  5. If records are a DataFrame (or `None`)
  6. If the records DataFrame is the right number of columns (based on symbol dimension)
  7. If the symbol is a scalar, then ensure there is only one record (row) in the DataFrame
  8. If records column headings are unique
  9. If any symbol attribute columns are missing or out of order
  10. If all domain columns are type `category`
  11. If all domain categories are type `str`
  12. If all data columns are type `float`

# Custom Column Headings
The names of the domain columns are flexible, but `transfer` requires unique column names. Users are encouraged to change the column headings of the underlying dataframe by using the `domain_labels` property. Using this property will ensure that unique column names are generated by adding a `_<dimension>` tag to the end of any user supplied column names. The following examples show this behavior.

**Attention:** All `*` domains are recast as `uni`. This allows users to access the column data with both the Pandas bracket and/or dot notation (i.e., `df["uni"]` or `df.uni`).

Column heading behavior at symbol instantiation

The `setRecords` (which is called internally at symbol instantiation) method will set default `domain_labels` if they were not provided by the user. The only way for a user to provide domain labels with `setRecords` is by passing in a Pandas DataFrame object. The `_<dimension>` tag will be added to all domain labels in order to make all domain names unique – this tag is added to all dimensions if any subset of the domain names are non-unique.

import gams.transfer as gt

import pandas as pd

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

# define a symbol with unique domain names
a = gt.Parameter(

m, "a", [i, "*"], records=[("i1", "u1", 1), ("i2", "u2", 1), ("i3", "u3", 1)]

)

# define a symbol with NON-unique domain names
b = gt.Parameter(

m, "b", [i, i], records=[("i1", "i1", 1), ("i2", "i2", 1), ("i3", "i3", 1)]

)

# define a symbol from a dataframe that already has column names
df = pd.DataFrame(

[("i1", "i1", 1), ("i2", "i2", 1), ("i3", "i3", 1)],

columns=["from", "to", "distance"],

)

c = gt.Parameter(m, "c", [i, i], records=df)

In [1]: m.isValid()

Out[1]: True

In [2]: i.records

Out[2]:

uni element_text

0 i1

1 i2

2 i3

In [3]: a.records

Out[3]:

i uni value

0 i1 u1 1.0

1 i2 u2 1.0

2 i3 u3 1.0

In [4]: b.records

Out[4]:

i_0 i_1 value

0 i1 i1 1.0

1 i2 i2 1.0

2 i3 i3 1.0

In [5]: c.records

Out[5]:

from to value

0 i1 i1 1.0

1 i2 i2 1.0

2 i3 i3 1.0

Customizing column headings

Many users may want to output the GAMS DataFrame directly to another format (CSV, etc.) and may wish to create customized DataFrame column headings for readability. User can do this by directly setting the `domain_labels` property, as seen in the following example.

**Attention:** Users are encouraged to use the `<symbol>.domain_labels` property instead of setting the `<DataFrame>.columns` directly. The avoids the possibility of out-of-sync symbol validity. The `domain_labels` property does not store anything, calling this property simply returns the exact domain labels from the DataFrame.

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

# define a symbol with unique domain names
a = gt.Parameter(

m, "a", [i, "*"], records=[("i1", "u1", 1), ("i2", "u2", 1), ("i3", "u3", 1)]

)

# customize the headings to allow more friendly output (to csv, etc.)
a.domain_labels = ["start", "destination"]

In [1]: m.isValid()

Out[1]: True

In [2]: a.records

Out[2]:

start destination value

0 i1 u1 1.0

1 i2 u2 1.0

2 i3 u3 1.0

# Converting Records
All data in `transfer` will be stored as a Pandas DataFrame – however, it is desirable to have easy access to data without the additional infrastructure that comes with the DataFrame object. We include `to*` methods (available for all symbol types) that will return other data structures. The following examples show the behavior of `toValue`, `toList`, and `toDict` (previous examples showed examples of `toDense` and `toSparseCoo`).

Examples of toList

import gams.transfer as gt

import pandas as pd

m = gt.Container()

i = gt.Set(m, "i", records=["i0", "i1", "i2"])

ii = gt.Set(

m, "ii", ["*", "*"], records=[(f"i{i}", f"i{i}", f"element_text for i{i}") for i in range(3)]

)

s = gt.Set(m, "s", i, is_singleton=True, records="i1")

u = gt.UniverseAlias(m, "u")

ip = gt.Alias(m, "ip", i)

a0 = gt.Parameter(m, "a0", records=1)

a1 = gt.Parameter(m, "a1", i, records=[("i1", 1), ("i2", 2)])

a2 = gt.Parameter(m, "a2", [i, i], records=[("i1", "i1", 1), ("i2", "i1", 2)])

v0 = gt.Variable(m, "v0", "free", records=1)

v1 = gt.Variable(

m,

"v1",

"free",

i,

records=pd.DataFrame([("i1", 1), ("i2", 2)], columns=["i", "level"]),

)

v2 = gt.Variable(

m,

"v2",

"free",

[i, i],

records=(

pd.DataFrame(

[("i1", "i1", 1), ("i2", "i1", 2)],

columns=["i", "i", "level"],

)

),

)

In [1]: i.toList()

Out[1]: ['i0', 'i1', 'i2']

In [2]: ii.toList()

Out[2]: [('i0', 'i0'), ('i1', 'i1'), ('i2', 'i2')]

In [3]: ii.toList(include_element_text=True)

Out[3]:

[('i0', 'i0', 'element_text for i0'),

('i1', 'i1', 'element_text for i1'),

('i2', 'i2', 'element_text for i2')]

In [4]: s.toList()

Out[4]: ['i1']

In [5]: u.toList()

Out[5]: ['i0', 'i1', 'i2']

In [6]: ip.toList()

Out[6]: ['i0', 'i1', 'i2']

In [7]: a0.toList()

Out[7]: [1.0]

In [8]: a1.toList()

Out[8]: [('i1', 1.0), ('i2', 2.0)]

In [9]: a2.toList()

Out[9]: [('i1', 'i1', 1.0), ('i2', 'i1', 2.0)]

In [10]: v0.toList() # default is to include only the "level"

Out[10]: [1.0]

In [11]: v0.toList("marginal")

Out[11]: [0.0]

In [12]: v1.toList() # default is to include only the "level"

Out[12]: [('i1', 1.0), ('i2', 2.0)]

In [13]: v1.toList(["level", "marginal"])

Out[13]: [('i1', 1.0, 0.0), ('i2', 2.0, 0.0)]

Examples of toValue

In [1]: a0.toValue()

Out[1]: 1.0

In [2]: a1.toValue()

Out[2]: TypeError: Cannot extract value data for non-scalar symbols (symbol dimension is 1)

In [3]: v0.toValue() # default is to only include the "level"

Out[3]: 1.0

In [4]: v0.toValue("marginal")

Out[4]: 0.0

Examples of toDict

In [1]: i.toDict()

Out[1]: AttributeError: 'Set' object has no attribute 'toDict'

In [2]: a0.toDict()

Out[2]: TypeError: Symbol `a0` is a scalar and cannot be converted into a dict.

In [3]: a1.toDict()

Out[3]: {'i1': 1.0, 'i2': 2.0}

In [4]: a2.toDict()

Out[4]: {('i1', 'i1'): 1.0, ('i2', 'i1'): 2.0}

In [5]: v1.toDict() # default is to only include the "level"

Out[5]: {'i1': 1.0, 'i2': 2.0}

In [6]: v1.toDict(["level","marginal"])

Out[6]: {'i1': {'level': 1.0, 'marginal': 0.0}, 'i2': {'level': 2.0, 'marginal': 0.0}}

In [7]: v1.toDict(orient="columns") # this format is useful for recreating Pandas DataFrames

Out[7]: {'i': {0: 'i1', 1: 'i2'}, 'level': {0: 1.0, 1: 2.0}}

# Comparing Symbols
Sparse GAMS data is inherently unordered. The concept of order is GAMS is governed by the order of the UELs in the universe set not the order of the records. This differs from the sparse data structures that we use in `transfer` (Pandas DataFrames) because each record (i.e., DataFrame row) has an index (typically `0..n`) and can be sorted by this index. Said a slightly different way, two GDX files will be equivalent if their universe order is the same and the records are the same, however when creating the GDX file, it is of no consequence what order the records are written in. Therefore, in order to calculate an equality between two symbols in `transfer` we must perform a merge operation on the symbol domain labels – an operation that could be computationally expensive for large symbols.

**Attention:** The nature of symbol equality in `transfer` means that a potentially expensive merge operation is performed, we do not recommend that the `equals` method be used inside loops or when speed is critical. It is, however, very useful for data debugging.

A quick example shows the syntax of `equals`:

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(5)], description="set i")

j = gt.Set(m, "j", records=[f"i{i}" for i in range(5)], description="set j")

In [1]: i.equals(j)

Out[1]: False

By default, `equals` takes the strictest view of symbol "equality" – everything must be the same. In this case, the symbol names and descriptions differ between the two sets `i` and `j`. We can relax the view of equality with a combination of argument flags. Comparing the two symbols again, but ignoring the meta data (i.e., ignoring the symbol name, description and type (if a Variable or Equation)):

In [1]: i.equals(j, check_meta_data=False)

Out[1]: True

It is also possible to ignore the set element text in `equals`:

m = gt.Container()

i = gt.Set(m, "i", records=[(f"i{i}", "arlington") for i in range(5)])

j = gt.Set(m, "j", records=[f"i{i}" for i in range(5)])

In [1]: i.records

Out[1]:

uni element_text

0 i0 arlington

1 i1 arlington

2 i2 arlington

3 i3 arlington

4 i4 arlington

In [2]: j.records

Out[2]:

uni element_text

0 i0

1 i1

2 i2

3 i3

4 i4

In [3]: i.equals(j, check_meta_data=False, check_element_text=False)

Out[3]: True

The `check_uels` argument will ensure that the symbol "universe" is the same (in order and content) between two symbols, as illustrated in the following example:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

ip = gt.Set(m, "ip", records=["i3", "i2", "i1"])

Clearly, the two sets `i` and `ip` have the same records, but the UEL order is different. If `check_uels=True` the resulting symbols will not be considered equal – turning this flag off results in equality.

In [1]: i.getUELs()

Out[1]: ['i1', 'i2', 'i3']

In [2]: ip.getUELs()

Out[2]: ['i3', 'i2', 'i1']

In [3]: i.equals(ip, check_meta_data=False)

Out[3]: False

In [4]: i.equals(ip, check_meta_data=False, check_uels=False)

Out[4]: True

Numerical comparisons are enabled for `Parameters`, `Variables` and `Equations` – equality can be flexibly defined through the `equals` method arguments. Again, the strictest view of equality is taken as the default behavior of `equals` (no numerical tolerances, some limitations exist – see: [`numpy.isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html) for more details).

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

a = gt.Parameter(m, "a", i, records=[("i1", 1), ("i2", 2), ("i3", 3)])

ap = gt.Parameter(m, "ap", i, records=[("i1", 1 + 1e-9), ("i2", 2), ("i3", 3)])

In [1]: a.equals(ap, check_meta_data=False)

Out[1]: False

In [2]: a.equals(ap, check_meta_data=False, atol=1e-8)

Out[2]: True

**Attention:** The numerical comparison is handled by [`numpy.isclose`](https://numpy.org/doc/stable/reference/generated/numpy.isclose.html), more details can be found in the Numpy documentation.

In the case of variables and equations, it is possible for the user to confine the numerical comparison to certain certain attributes (`level`, `marginal`, `lower`, `upper` and `scale`) by specifying the `columns` argument as the following example illustrates:

m = gt.Container()

a = gt.Variable(m, "a", "free", records=100)

ap = gt.Variable(m, "ap", "free", records=101)

In [1]: a.records

Out[1]:

level marginal lower upper scale

0 100.0 0.0 -inf inf 1.0

In [2]: ap.records

Out[2]:

level marginal lower upper scale

0 101.0 0.0 -inf inf 1.0

In [3]: a.equals(ap, check_meta_data=False)

Out[3]: False

In [4]: a.equals(ap, check_meta_data=False, columns="level")

Out[4]: False

In [5]: a.equals(ap, check_meta_data=False, columns="marginal")

Out[5]: True

# Domain Forwarding
GAMS includes the ability to define sets directly from data using the implicit set notation (see: [Implicit Set Definition (or: Domain Defining Symbol Declarations)](UG_SetDefinition.html#UG_SetDefinition_ImplicitSetDefinition)). This notation has an analogue in `transfer` called `domain_forwarding`.

**Note:** It is possible to recursively update a subset tree in `transfer`.

Domain forwarding is available as an argument to all symbol object constructors; the user would simply need to pass `domain_forwarding=True`.

In this example we have raw data that in the `dist` DataFrame and we want to send the domain information into the `i` and `j` sets – we take care to pass the set objects as the domain for parameter `c`.

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i")

j = gt.Set(m, "j")

dist = pd.DataFrame(

[

("seattle", "new-york", 2.5),

("seattle", "chicago", 1.7),

("seattle", "topeka", 1.8),

("san-diego", "new-york", 2.5),

("san-diego", "chicago", 1.8),

("san-diego", "topeka", 1.4),

],

columns=["from", "to", "thousand_miles"],

)

c = gt.Parameter(m, "c", [i, j], records=dist, domain_forwarding=True)

In [1]: i.records

Out[1]:

uni element_text

0 seattle

1 san-diego

In [2]: j.records

Out[2]:

uni element_text

0 new-york

1 chicago

2 topeka

In [3]: c.records

Out[3]:

i j value

0 seattle new-york 2.5

1 seattle chicago 1.7

2 seattle topeka 1.8

3 san-diego new-york 2.5

4 san-diego chicago 1.8

5 san-diego topeka 1.4

**Note:** The element order in the sets `i` and `j` mirrors that in the raw data.

In this example we show that domain forwarding will also work recursively to update the entire set lineage – the domain forwarding occurs at the creation of every symbol object. The correct order of elements in set `i` is `[z, a, b, c]` because the records from `j` are forwarded first, and then the records from `k` are propagated through (back to `i`).

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i")

j = gt.Set(m, "j", i, records=["z"], domain_forwarding=True)

k = gt.Set(m, "k", j, records=["a", "b", "c"], domain_forwarding=True)

In [1]: i.records

Out[1]:

uni element_text

0 z

1 a

2 b

3 c

In [2]: j.records

Out[2]:

i element_text

0 z

1 a

2 b

3 c

In [3]: k.records

Out[3]:

j element_text

0 a

1 b

2 c

It is also possible to forward to specific domain sets by passing a `list` of `bool` to the `domain_forwarding` property, as seen in the following example:

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i")

j = gt.Set(m, "j")

k = gt.Set(m, "k")

ijk = gt.Parameter(

m,

"ijk",

[i, j, k],

records=[("i", "j", "k", 1)],

domain_forwarding=[True, False, True],

)

In [1]: i.records

Out[1]:

uni element_text

0 i

In [2]: j.records is None

Out[2]: True

In [3]: k.records

Out[3]:

uni element_text

0 k

# Domain Violations
Domain violations occur when domain labels appear in symbol data but they do not appear in the parent set which the symbol is defined over – attempting to execute a GAMS model when there domain violations will lead to compilation errors. Domain violations are found dynamically with the `<Symbol>.findDomainViolations()` method.

**Note:** the `findDomainViolations` method can be computationally expensive – UELs in GAMS are case preserving (just like symbol names); additionally, GAMS ignores all trailing white space in UELs (leading white space is considered significant). As a result, `transfer` must lowercase all UELs and then strip any trailing white space before doing the set comparison to locate (and create) any `DomainViolation` objects. `findDomainViolations` should not be used in a loop (nor should any of its related methods: `hasDomainViolations`, `countDomainViolations`, `getDomainViolations`, or `dropDomainViolations`).

In the following example we intentionally create data with domain violations in the `a` parameter:

m = gt.Container()

i = gt.Set(m, "i", records=["a", "b", "c"])

a = gt.Parameter(m, "a", i, records=[("aa", 1), ("c", 2)])

In [1]: a.findDomainViolations()

Out[1]:

i value

0 aa 1.0

In [2]: a.hasDomainViolations()

Out[2]: True

In [3]: a.countDomainViolations()

Out[3]: 1

In [4]: a.getDomainViolations()

Out[4]: [<DomainViolation at 0x7fb6b83d9630>]

Dynamically locating domain violations allows `transfer` to return a view of the underlying pandas dataframe with the problematic domain labels still intact – at this point the user is free to correct issues in the UELs with any of the `*UELs` methods or by simply dropping any domain violations from the dataframe completely (the `dropDomainViolations` method is a convenience function for this operation).

**Attention:** It is not possible to create a GDX file if symbols have domain violations.
     Unused UELs will not result in domain violations.

Attempting to write this container to a GDX file will result in an exception.

m = gt.Container()

i = gt.Set(m, "i", records=["a", "b", "c"])

a = gt.Parameter(m, "a", i, records=[("aa", 1), ("c", 2)])

m.write("out.gdx")

Exception: Encountered data errors with symbol `a`. Possible causes are from duplicate records and/or domain violations.

Use 'hasDuplicateRecords', 'findDuplicateRecords', 'dropDuplicateRecords', and/or 'countDuplicateRecords' to find/resolve duplicate records.

Use 'hasDomainViolations', 'findDomainViolations', 'dropDomainViolations', and/or 'countDomainViolations' to find/resolve domain violations.

GDX file was not created successfully.

# Duplicate Records
Duplicate records can easily appear in large datasets – locating and fixing these records is straightforward with `transfer`. `transfer` includes `find*`, `has*`, `count*` and `drop*` methods for duplicate records, just as it has for domain violations.

**Note:** the `findDuplicateRecords` method can be computationally expensive – UELs in GAMS are case preserving (just like symbol names); additionally, GAMS ignores all trailing white space in UELs (leading white space is considered significant). As a result, `transfer` must lowercase all UELs and then strip any trailing white space before doing the set comparison to locate duplicate records. `findDuplicateRecords` should not be used in a loop (nor should any of its related methods: `hasDuplicateRecords`, `countDuplicateRecords`, or `dropDuplicateRecords`).

Dynamically locating duplicate records allows `transfer` to return a view of the underlying pandas dataframe with the problematic domain labels still intact – at this point the user is free to correct issues in the UELs with any of the `*UELs` methods or by simply dropping any duplicate records from the dataframe completely (the `dropDuplicateRecords` method is a convenience function for this operation).

m = gt.Container()

a = gt.Parameter(

m,

"a",

["*"],

records=[("i" \+ str(i), float(i)) for i in range(4)]

\+ [("j" \+ str(i), i) for i in range(4)]

\+ [("I" \+ str(i), i) for i in range(4)],

)

**Note:** The user can decide which duplicate records they would like `keep` with `keep="first"` (default), `keep="last"`, or `keep=False` (which returns all duplicate records)

In [1]: a.records

Out[1]:

uni value

0 i0 0.0

1 i1 1.0

2 i2 2.0

3 i3 3.0

4 j0 0.0

5 j1 1.0

6 j2 2.0

7 j3 3.0

8 I0 0.0

9 I1 1.0

10 I2 2.0

11 I3 3.0

In [2]: a.findDuplicateRecords()

Out[2]:

uni value

8 I0 0.0

9 I1 1.0

10 I2 2.0

11 I3 3.0

In [3]: a.findDuplicateRecords(keep="last")

Out[3]:

uni value

0 i0 0.0

1 i1 1.0

2 i2 2.0

3 i3 3.0

In [4]: a.findDuplicateRecords(keep=False)

Out[4]:

uni value

0 i0 0.0

1 i1 1.0

2 i2 2.0

3 i3 3.0

8 I0 0.0

9 I1 1.0

10 I2 2.0

11 I3 3.0

**Attention:** It is not possible to create a GDX file if symbols have duplicate records.

Attempting to write this container to a GDX file will result in an exception.

m = gt.Container()

a = gt.Parameter(

m,

"a",

["*"],

records=[("i" \+ str(i), float(i)) for i in range(4)]

\+ [("j" \+ str(i), i) for i in range(4)]

\+ [("I" \+ str(i), i) for i in range(4)],

)

m.write("out.gdx")

Exception: Encountered data errors with symbol `a`. Possible causes are from duplicate records and/or domain violations.

Use 'hasDuplicateRecords', 'findDuplicateRecords', 'dropDuplicateRecords', and/or 'countDuplicateRecords' to find/resolve duplicate records.

Use 'hasDomainViolations', 'findDomainViolations', 'dropDomainViolations', and/or 'countDomainViolations' to find/resolve domain violations.

GDX file was not created successfully.

# Pivoting Data
It might be convenient to pivot data into a multi-dimensional data structure rather than maintaining the flat structure in `records`. A convenience method called `pivot` is provided for all symbol classes and will return a pivoted `pandas.DataFrame`. Pivoting is only available for symbols with more than one dimension.

Example #1 - Pivot a 2D Set

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(5)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(5)])

ij = gt.Set(m, "ij", [i, j])

ij.generateRecords(density=0.25, seed=123)

In [1]: ij.pivot()

Out[1]:

j0 j1 j3 j4

i0 True True False False

i1 True False False False

i2 False False True True

i4 False True False False

Example #2 - Pivot a 3D Set

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(5)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(5)])

iji = gt.Set(m, "iji", [i, j, i])

iji.generateRecords(density=0.25, seed=123)

In [1]: iji.pivot()

Out[1]:

i0 i1 i2 i3 i4

i0 j0 False True True False False

j1 True False False False False

j3 False False False True False

j4 False False True False False

i1 j0 True True False True False

j1 True True False False True

j2 False True False False False

j4 False False False True False

i2 j0 True False False False False

j1 False False True False True

j3 True False False False False

i3 j2 False True True False True

j3 False True False False False

j4 True False True True True

i4 j0 False True False True False

j1 False False False True False

j3 False False False True False

j4 False False False True True

In [2]: iji.pivot(fill_value="")

Out[2]:

i0 i1 i2 i3 i4

i0 j0 True True

j1 True

j3 True

j4 True

i1 j0 True True True

j1 True True True

j2 True

j4 True

i2 j0 True

j1 True True

j3 True

i3 j2 True True True

j3 True

j4 True True True True

i4 j0 True True

j1 True

j3 True

j4 True True

**Note:** When pivoting symbols with >2 dimensions, the first [0..(dimension-1)] dimensions will be set to the index and the last dimension will be pivoted into the columns. This behavior can be customized with the `index` and `columns` arguments.

Example #3 - Pivot a 3D Parameter w/ a fill_value

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(5)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(5)])

iji = gt.Parameter(m, "iji", [i, j, i])

iji.generateRecords(density=0.05, seed=123)

In [1]: iji.pivot(fill_value="NONE")

Out[1]:

i1 i2 i3 i4

i0 j1 0.682352 NONE NONE NONE

j2 0.053821 NONE 0.22036 NONE

i1 j1 NONE NONE NONE 0.184372

i2 j0 NONE 0.175906 NONE NONE

i3 j4 NONE NONE 0.812095 NONE

In [2]: iji.pivot(fill_value=0)

Out[2]:

i1 i2 i3 i4

i0 j1 0.682352 0.000000 0.000000 0.000000

j2 0.053821 0.000000 0.220360 0.000000

i1 j1 0.000000 0.000000 0.000000 0.184372

i2 j0 0.000000 0.175906 0.000000 0.000000

i3 j4 0.000000 0.000000 0.812095 0.000000

In [3]: iji.pivot(fill_value=gt.SpecialValues.EPS)

Out[3]:

i1 i2 i3 i4

i0 j1 0.682352 -0.000000 -0.000000 -0.000000

j2 0.053821 -0.000000 0.220360 -0.000000

i1 j1 -0.000000 -0.000000 -0.000000 0.184372

i2 j0 -0.000000 0.175906 -0.000000 -0.000000

i3 j4 -0.000000 -0.000000 0.812095 -0.000000

Example #4 - Pivot (only the marginal values) of a 3D Variable

import gams.transfer as gt

# NOTE: custom functions should expose a 'seed' argument
def marginal_values(seed, size):

rng = np.random.default_rng(seed)

return rng.normal(5, 1.2, size=size)

m = gt.Container()

i = gt.Set(m, "i", records=[f"i{i}" for i in range(5)])

j = gt.Set(m, "j", records=[f"j{i}" for i in range(5)])

iji = gt.Variable(m, "iji", "free", [i, j, i])

iji.generateRecords(density=0.05, func={"marginal": marginal_values}, seed=123)

In [1]: iji.records

Out[1]:

i_0 j_1 i_2 level marginal lower upper scale

0 i0 j1 i1 0.0 3.813054 -inf inf 1.0

1 i0 j2 i1 0.0 4.558656 -inf inf 1.0

2 i0 j2 i3 0.0 6.545510 -inf inf 1.0

3 i1 j1 i4 0.0 5.232769 -inf inf 1.0

4 i2 j0 i2 0.0 6.104277 -inf inf 1.0

5 i3 j4 i3 0.0 5.692525 -inf inf 1.0

In [2]: iji.pivot(value="marginal")

Out[2]:

i1 i3 i4 i2

i0 j1 3.813054 0.000000 0.000000 0.000000

j2 4.558656 6.545510 0.000000 0.000000

i1 j1 0.000000 0.000000 5.232769 0.000000

i2 j0 0.000000 0.000000 0.000000 6.104277

i3 j4 0.000000 5.692525 0.000000 0.000000

# Describing Data
The methods `describeSets`, `describeParameters`, `describeVariables`, and `describeEquations` allow the user to get a summary view of key data statistics. The returned DataFrame aggregates the output for a number of other methods (depending on symbol type). A description of each `Container` method is provided in the following subsections:

## describeSets
Argument | Type | Description | Required | Default
---|---|---|---|---
`symbols` | `list`, `str`, NoneType | A list of sets in the `Container` to include in the output. describeSets will include aliases if they are explicitly passed by the user. | No | `None` (if `None` specified, will assume all sets – not aliases)

Returns: `pandas.DataFrame`

The following table includes a short description of the column headings in the return.

Property / Statistic | Description
---|---
`name` | name of the symbol
`is_singleton` | `bool` if the set/alias is a singleton set (or an alias of a singleton set)
`alias_with` | [OPTIONAL if users passes an alias name as part of `symbols`] name of the parent set (for alias only), None otherwise
`domain` | domain labels for the symbol
`domain_type` | `none`, `relaxed` or `regular` depending on the symbol state
`dimension` | dimension
`number_records` | number of records in the symbol
`sparsity` | `1 - number_records/cardinality`

Example #1

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

In [1]: m.describeSets()

Out[1]:

name is_singleton domain domain_type dimension number_records sparsity

0 i False [*] none 1 2 None

1 j False [*] none 1 3 None

Example #2 – with aliases

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i" \+ str(i) for i in range(1, 10)])

j = gt.Set(m, "j", records=["j" \+ str(i) for i in range(1, 10)])

ip = gt.Alias(m, "ip", i)

jp = gt.Alias(m, "jp", j)

In [1]: m.describeSets()

Out[1]:

name is_singleton domain domain_type dimension number_records sparsity

0 i False [*] none 1 9 None

1 j False [*] none 1 9 None

In [2]: m.describeSets(m.listSets() + m.listAliases())

Out[2]:

name is_singleton is_alias alias_with domain domain_type dimension number_records sparsity

0 i False False None [*] none 1 9 None

1 ip False True i [*] none 1 9 None

2 j False False None [*] none 1 9 None

3 jp False True j [*] none 1 9 None

## describeParameters
Argument | Type | Description | Required | Default
---|---|---|---|---
`symbols` | `list`, `str`, NoneType | A list of parameters in the `Container` to include in the output | No | `None` (if `None` specified, will assume all parameters)

Returns: `pandas.DataFrame`

The following table includes a short description of the column headings in the return.

Property / Statistic | Description
---|---
`name` | name of the symbol
`domain` | domain labels for the symbol
`domain_type` | `none`, `relaxed` or `regular` depending on the symbol state
`dimension` | dimension
`number_records` | number of records in the symbol
`min` | min value in data
`mean` | mean value in data
`max` | max value in data
`where_min` | domain of min value (if multiple, returns only first occurrence)
`where_max` | domain of max value (if multiple, returns only first occurrence)
`sparsity` | `1 - number_records/cardinality`

Example

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

In [1]: m.describeParameters()

Out[1]:

name domain domain_type dimension number_records min mean max where_min where_max sparsity

0 a [i] regular 1 2 350.000 475.000 600.000 [seattle] [san-diego] 0.0

1 b [j] regular 1 3 275.000 300.000 325.000 [topeka] [new-york] 0.0

2 c [i, j] regular 2 6 0.126 0.176 0.225 [san-diego, topeka] [seattle, new-york] 0.0

3 d [i, j] regular 2 6 1.400 1.950 2.500 [san-diego, topeka] [seattle, new-york] 0.0

4 f [] none 0 1 90.000 90.000 90.000 None None None

## describeVariables
Argument | Type | Description | Required | Default
---|---|---|---|---
`symbols` | `list`, `str`, NoneType | A list of variables in the `Container` to include in the output | No | `None` (if `None` specified, will assume all variables)

Returns: `pandas.DataFrame`

The following table includes a short description of the column headings in the return.

Property / Statistic | Description
---|---
`name` | name of the symbol
`type` | type of variable (i.e., `binary`, `integer`, `positive`, `negative`, `free`, `sos1`, `sos2`, `semicont`, `semiint`)
`domain` | domain labels for the symbol
`domain_type` | `none`, `relaxed` or `regular` depending on the symbol state
`dimension` | dimension
`number_records` | number of records in the symbol
`sparsity` | `1 - number_records/cardinality`
`min_level` | min value in the `level`
`mean_level` | mean value in the `level`
`max_level` | max value in the `level`
`where_max_abs_level` | domain of max(abs(`level`)) in data

Example

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

In [1]: m.describeVariables()

Out[1]:

name type domain domain_type dimension number_records sparsity min_level mean_level max_level where_max_abs_level

0 x positive [i, j] regular 2 6 0.0 0.000 150.000 300.000 [seattle, chicago]

1 z free [] none 0 1 None 153.675 153.675 153.675 None

## describeEquations
Argument | Type | Description | Required | Default
---|---|---|---|---
`symbols` | `list`, `str`, NoneType | A list of equations in the `Container` to include in the output | No | `None` (if `None` specified, will assume all equations)

Returns: `pandas.DataFrame`

The following table includes a short description of the column headings in the return.

Property / Statistic | Description
---|---
`name` | name of the symbol
`type` | type of variable (i.e., `binary`, `integer`, `positive`, `negative`, `free`, `sos1`, `sos2`, `semicont`, `semiint`)
`domain` | domain labels for the symbol
`domain_type` | `none`, `relaxed` or `regular` depending on the symbol state
`dimension` | dimension
`number_records` | number of records in the symbol
`sparsity` | `1 - number_records/cardinality`
`min_level` | min value in the `level`
`mean_level` | mean value in the `level`
`max_level` | max value in the `level`
`where_max_abs_level` | domain of max(abs(`level`)) in data

Example

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

In [1]: m.describeEquations()

Out[1]:

name type domain domain_type dimension number_records sparsity min_level mean_level max_level where_max_abs_level

0 cost eq [] none 0 1 None -0.0 0.0 -0.0 None

1 demand geq [j] regular 1 3 0.0 275.0 300.0 325.0 [new-york]

2 supply leq [i] regular 1 2 0.0 350.0 450.0 550.0 [san-diego]

## describeAliases
Argument | Type | Description | Required | Default
---|---|---|---|---
`symbols` | `list`, `str`, NoneType | A list of alias (only) symbols in the `Container` to include in the output | No | `None` (if `None` specified, will assume all aliases – not sets)

Returns: `pandas.DataFrame`

The following table includes a short description of the column headings in the return. All data is referenced from the parent set that the alias is created from.

Property / Statistic | Description
---|---
`name` | name of the symbol
`alias_with` | name of the parent set (for alias only), None otherwise
`is_singleton` | `bool` if the set/alias is a singleton set (or an alias of a singleton set)
`domain` | domain labels for the symbol
`domain_type` | `none`, `relaxed` or `regular` depending on the symbol state
`dimension` | dimension
`number_records` | number of records in the symbol
`sparsity` | `1 - number_records/cardinality`

Example

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i" \+ str(i) for i in range(5)])

j = gt.Set(m, "j", records=["j" \+ str(j) for j in range(10)])

ip = gt.Alias(m, "ip", i)

ipp = gt.Alias(m, "ipp", ip)

jp = gt.Alias(m, "jp", j)

In [1]: m.describeAliases()

Out[1]:

name alias_with is_singleton domain domain_type dimension number_records sparsity

0 ip i False [*] none 1 5 None

1 ipp i False [*] none 1 5 None

2 jp j False [*] none 1 10 None

# Matrix Generation
`transfer` stores data in a "flat" format, that is, one record entry per DataFrame row. However, it is often necessary to convert this data format into a matrix format – `transfer` enables users to do this with relative ease using the `toDense` and the `toSparseCoo` symbol methods. The `toDense` method will return a dense `N`-dimensional numpy array with each dimension corresponding to the GAMS symbol dimension; it is possible to output an array up to 20 dimensions (a GAMS limit). The `toSparseCoo` method will return the data in a sparse scipy COOrdinate format, which can then be efficiently converted into other sparse matrix formats.

**Attention:** Both the `toDense` and `toSparseCoo` methods do not transform the underlying DataFrame in any way, they only return the transformed data.

**Note:** `toSparseCoo` will only convert 2-dimensional data to the scipy COOrdinate format. A user interested in sparse data for an N-dimensional symbol will need to decide how to reshape the dense array in order to generate the 2D sparse format.

**Attention:** In order to use the `toSparseCoo` method the user will need to install the scipy package. Scipy is not provided with GMSPython.

Both the `toDense` and `toSparseCoo` method leverage the indexing that comes along with using `categorical` data types to store domain information. This means that linking symbols together (by passing symbol objects as domain information) impacts the size of the matrix. This is best demonstrated by a few examples.

Example (1D data w/o domain linking (i.e., a relaxed domain))

import gams.transfer as gt

m = gt.Container()

a = gt.Parameter(m, "a", "i", records=[("a", 1), ("c", 3)])

In [1]: a.records

Out[1]:

i value

0 a 1.0

1 c 3.0

In [2]: a.toDense()

Out[2]: array([1., 3.])

In [3]: a.toSparseCoo()

Out[3]:

<1x2 sparse matrix of type '<class 'numpy.float64'>'

with 2 stored elements in COOrdinate format>

Note that the parameter `a` is not linked to another symbol, so when converting to a matrix, the indexing is referenced to the data structure in `a.records`. Defining a sparse parameter `a` over a set `i` allows us to extract information from the `i` domain and construct a very different dense matrix, as the following example shows:

Example (1D data w/ domain linking (i.e., a regular domain))

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["a", "b", "c", "d"])

a = gt.Parameter(m, "a", i, records=[("a", 1), ("c", 3)])

In [1]: i.records

Out[1]:

uni element_text

0 a

1 b

2 c

3 d

In [2]: a.records

Out[2]:

i value

0 a 1.0

1 c 3.0

In [3]: a.toDense()

Out[3]: array([1., 0., 3., 0.])

In [4]: a.toSparseCoo()

Out[4]:

<1x4 sparse matrix of type '<class 'numpy.float64'>'

with 2 stored elements in COOrdinate format>

Example (2D data w/ domain linking)

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["a", "b", "c", "d"])

a = gt.Parameter(m, "a", [i, i], records=[("a", "a", 1), ("c", "c", 3)])

In [1]: i.records

Out[1]:

uni element_text

0 a

1 b

2 c

3 d

In [2]: a.records

Out[2]:

i_0 i_1 value

0 a a 1.0

1 c c 3.0

In [3]: a.toDense()

Out[3]:

array([[1., 0., 0., 0.],

[0., 0., 0., 0.],

[0., 0., 3., 0.],

[0., 0., 0., 0.]])

In [4]: a.toSparseCoo()

Out[4]:

<4x4 sparse matrix of type '<class 'numpy.float64'>'

with 2 stored elements in COOrdinate format>

# The Universe Set
A Unique Element (UEL) is an `(i,s)` pair where `i` (or index) is an identification number for a (string) label `s`. GAMS uses UELs to efficiently store domain entries of a record by storing the UEL ID `i` of a domain entry instead of the actual string `s`. This avoids storing the same string multiple times. The concept of UELs also exists in Python/Pandas and is called a "categorical series". `transfer` leverages these types in order to efficiently store strings and enable domain checking within the Python environment.

Each domain column in a DataFrame can be assigned a unique categorical type, the effect is that each symbol maintains its own list of UELs per dimension. It is possible to convert a categorical column to its ID number representation by using the categorical accessor `x.records[<domain_column_label>].cat.codes`; however, this type of data manipulation is not necessary within `transfer`, but could be handy when debugging data.

Pandas offers the possibility to create categorical column types that are `ordered` or not; `transfer` relies exclusively on `ordered` categorical data types (in order for a symbol to be valid it must have only `ordered` categories). By using ordered categories, `transfer` will order the UEL such that elements appear in the order in which they appeared in the data (which is how GAMS defines the UEL). `transfer` allows the user to reorder the UELs with the `uel_priority` argument in the `.write()` method.

`transfer` does not actually keep track of the UEL separately from other symbols in the `Container`, it will be created internal to the `.write()` method and is based on the order in which data is added to the container. The user can access the current state of the UEL with the `.getUELs()` container method. For example, we set a two dimensional set:

import gams.transfer as gt

m = gt.Container()

j = gt.Set(m, "j", ["*", "*"], records=[("i" \+ str(n), "j" \+ str(n)) for n in range(2)])

In [1]: j.records

Out[1]:

uni_0 uni_1 element_text

0 i0 j0

1 i1 j1

In [2]: m.getUELs()

Out[2]: ['i0', 'i1', 'j0', 'j1']

Pandas also includes a number of methods that allow categories to be [renamed, appended, etc.](https://pandas.pydata.org/docs/user_guide/categorical.html) These methods may be useful for advanced users, but most users will probably find that modifying the original data structures and resetting the symbol records provides a simpler solution. The design of `transfer` should enable the user to quickly move data back and forth, without worrying about the deeper mechanics of categorical data.

# Customize the Universe Set
The concept of a universe set is fundamental to GAMS and has consequences in many areas of GAMS programming including the order of loop execution. For example:
```
    set final_model_year / 2030 /;
    set t "all model years" / 2022*2030 /;

    singleton set my(t) "model solve year";

    loop(t,
      my(t) = yes;
      display my;
      );
```

The loop will execute model solve year `2030` first because the UEL `2030` was defined in the set `final_model_year` before it was used again in the definition of set `t`. This could lead to some surprising behavior if model time periods are linked together. Many GAMS users would create a dummy set (perhaps the first line of their model file) that contained all the UELs that had a significant order tom combat this behavior. `transfer` allows for full control (renaming as well as ordering) over the universe set through the `*UELS` methods, briefly described here:

Quick summary table of UELs functions

Method | Brief Description
---|---
`addUELs` | Adds UELS to a symbol dimension(s). This function does not have a container level implementation.
`capitalizeUELs` | Capitalize all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`casefoldUELs` | Casefold all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`getUELs` | Gets the UELs in a over either a symbol dimension, the entire symbol or the entire container. Unused UELs do not show up in symbol data but will show up in the GAMS UEL list.
`ljustUELs` | Left justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`lowerUELs` | Lowercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`lstripUELs` | Left strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`removeUELs` | Removes UELs from a symbol dimension, the entire symbol, the entire container (or just a subset of symbols). If a used UEL is removed the DataFrame record will show a `NaN`.
`renameUELs` | Renames UELs in a symbol dimension, the entire symbol, the entire container (or just a subset of symbols). Very handy for harmonizing UEL labeling of data that might have originated from different sources.
`reorderUELs` | Reorders UELs in a symbol dimension(s). This function does not have a container level implementation.
`rjustUELs` | Right justify all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`rstripUELs` | Right strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`setUELs` | Sets UELs for a symbol dimension(s). Equivalent results could be obtained with a combination of `renameUELs` and `reorderUELs`, but this one call may have some performance advantage.
`stripUELs` | Strip whitespace from all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`titleUELs` | Title (capitalize all individual words) in all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations
`upperUELs` | Uppercase all UELs in the symbol or a subset of specified `dimensions`, can be chained with other `*UELs` string operations

These tools are extremely useful when data is arriving at a model from a variety of data sources. We will describe each of these functions in detail and provide examples in the following sections.

**Attention:** GAMS is insensitive to trailing whitespaces, the `*UELs` methods will automatically trim any trailing whitespace when creating the new UELs.

## getUELs Examples
`getUELs` is a method of all GAMS symbol classes as well as the `Container` class. This allows the user to retrieve (ordered) UELs from the entire container or just a specific symbol dimension. For example:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

j = gt.Set(m, "j", i, records=["j1", "j2", "j3"])

a = gt.Parameter(m, "a", [i, j], records=[(f"i{i}", f"j{i}", i) for i in range(4)])

In [1]: i.getUELs()

Out[1]: ['i1', 'i2', 'i3']

In [2]: m.getUELs()

Out[2]: ['i1', 'i2', 'i3', 'j1', 'j2', 'j3', 'i0', 'j0']

In [3]: m.getUELs("j")

Out[3]: ['j1', 'j2', 'j3']

## addUELs Examples
`addUELs` is a method of all GAMS symbol classes. This method allows the user to add in new UELs labels to a specific dimension of a symbol – the user can add UELs that do not exist in the symbol `records`. For example:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

j = gt.Set(m, "j", i, records=["j1", "j2", "j3"])

a = gt.Parameter(m, "a", [i, j], records=[(f"i{i}", f"j{i}", i) for i in range(1,4)])

i.addUELs("ham")

a.addUELs("and", 0)

a.addUELs("cheese", 1)

In [1]: i.getUELs()

Out[1]: ['i1', 'i2', 'i3', 'ham']

In [2]: a.getUELs()

Out[2]: ['i1', 'i2', 'i3', 'and', 'j1', 'j2', 'j3', 'cheese']

In this example we have added three new (unused) UELs: `ham`, `and`, `cheese`. These three UELs will now appear in the GAMS universe set (accessible with `m.getUELs()`). The addition of unused UELs does not impact the validity of the symbols (i.e., unused UELs will not trigger domain violations).

## removeUELs Examples
`removeUELs` is a method of all GAMS symbol classes as well as the `Container` class. As a result, this method allows the user to clean up unwanted or simply unused UELs in a symbol dimension(s), over several symbols, or over the entire container. The previous example added three unused UELs (`ham`, `and`, `cheese`), but now we want to remove these UELs in order to clean up the GAMS universe set. We can accomplish this several ways:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

j = gt.Set(m, "j", i, records=["j1", "j2", "j3"])

a = gt.Parameter(m, "a", [i, j], records=[(f"i{i}", f"j{i}", i) for i in range(1,4)])

i.addUELs("ham")

a.addUELs("and", 0)

a.addUELs("cheese", 1)

# remove symbol UELs explicitly by dimension
i.removeUELs("ham", 0)

a.removeUELs("and", 0)

a.removeUELs("cheese", 1)

# remove symbol UELs for the entire symbol
i.removeUELs("ham")

a.removeUELs(["and", "cheese"])

# remove ONLY unused UELs from each symbol, independently
i.removeUELs()

a.removeUELs()

# remove ONLY unused UELs from the entire container (all symbols)
m.removeUELs()

In all cases the resulting universe set will be:

In [1]: m.getUELs()

Out[1]: ['i1', 'i2', 'i3', 'j1', 'j2', 'j3']

If a user removes a UEL that appears in data, that data will be lost permanently. The domain label will be transformed into an `NaN` as seen in this example:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

j = gt.Set(m, "j", i, records=["j1", "j2", "j3"])

a = gt.Parameter(m, "a", [i, j], records=[(f"i{i}", f"j{i}", i) for i in range(1,4)])

m.removeUELs("i1")

In [1]: i.records

Out[1]:

uni element_text

0 NaN

1 i2

2 i3

In [2]: a.records

Out[2]:

i j value

0 NaN j1 1.0

1 i2 j2 2.0

2 i3 j3 3.0

**Attention:** A container cannot be written if there are `NaN` entries in any of the domain columns (in any symbol) – an Exception is raised if there are missing domain labels.

## renameUELs Examples
`renameUELs` is a method of all GAMS symbol classes as well as the `Container` class. This method allows the user to rename UELs in a symbol dimension(s), over several symbols, or over the entire container. This particular method is very handy when attempting to harmonize labeling schemes between data structures that originated from different sources. For example:

m = gt.Container()

a = gt.Parameter(

m,

"a",

["*", "*"],

records=[("WI", "IL", 10), ("IL", "IN", 12.5), ("WI", "IN", 8.7)],

description="shipment quantities",

)

b = gt.Parameter(

m,

"b",

["*"],

records=[("wisconsin", 1.2), ("illinois", 1.7), ("indiana", 1.2)],

description="multipliers",

)

...results in the following records:

In [1]: a.records

Out[1]:

uni_0 uni_1 value

0 WI IL 10.0

1 IL IN 12.5

2 WI IN 8.7

In [2]: b.records

Out[2]:

uni value

0 wisconsin 1.2

1 illinois 1.7

2 indiana 1.2

However, two different data sources were used to generate the parameters `a` and `b` – one data source used the uppercase postal abbreviation of the state name and the other source used a lowercase full state name as the unique identifier. With the following syntax the user would be able to harmonize to a mixed case postal code labeling scheme (without losing any of the original UEL ordering).

m.renameUELs(

{

"WI": "Wi",

"IL": "Il",

"IN": "In",

"wisconsin": "Wi",

"illinois": "Il",

"indiana": "In",

}

)

...results in the following records (and the universe set):

In [1]: a.records

Out[1]:

uni_0 uni_1 value

0 Wi Il 10.0

1 Il In 12.5

2 Wi In 8.7

In [2]: b.records

Out[2]:

uni value

0 Wi 1.2

1 Il 1.7

2 In 1.2

The universe set will now be:

In [1]: m.getUELs()

Out[1]: ['Wi', 'Il', 'In']

It is possible that some data needs to be cleaned and multiple UELs need to be mapped to a single label (within a single dimension). This is not allowed under default behavior because `transfer` assumes that the provided UELs are truly unique (logically and lexicographically) – however, it might be necessary recreate the underlying categorical object to combine `n` (previously unique) UELs into one to establish the necessary logical set links. For example:

m = gt.Container()

a = gt.Parameter(

m,

"a",

["*", "*"],

records=[("WISCONSIN", "iowa", 10), ("WI", "illinois", 12)],

)

In [1]: a.records

Out[1]:

uni_0 uni_1 value

0 WISCONSIN iowa 10.0

1 WI illinois 12.0

The records are unique for `a`, but logically, there might be a need to rename `WI` to `WISCONSIN`.

In [1]: a.renameUELs({"WI": "WISCONSIN"})

Out[1]: Exception: Could not rename UELs (categories) in `a` dimension `0`. Reason: Categorical categories must be unique

In order achieve the desired behavior it is necessary to pass `allow_merge=True` to `renameUELs`:

In [1]: a.renameUELs({"WI": "WISCONSIN"}, allow_merge=True)

In [2]: a.records

Out[2]:

uni_0 uni_1 value

0 WISCONSIN iowa 10.0

1 WISCONSIN illinois 12.0

In [3]: a.getUELs()

Out[3]: ['WISCONSIN', 'iowa', 'illinois']

## reorderUELs Examples
`reorderUELs` is a method of all GAMS symbol classes. This method allows the user to reorder UELs of a specific symbol dimension – `reorderUELs` will not all any new UELs to be create nor can they be removed. For example:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

j = gt.Set(m, "j", i, records=["j1", "j2", "j3"])

a = gt.Parameter(m, "a", [i, j], records=[(f"i{i}", f"j{i}", i) for i in range(1,4)])

In [1]: i.getUELs()

Out[1]: ['i1', 'i2', 'i3']

In [2]: m.getUELs()

Out[2]: ['i1', 'i2', 'i3', 'j1', 'j2', 'j3']

But perhaps we want to reorder the UELs `i1`, `i2`, `i3` to `i3`, `i2`, `i1`.

In [1]: i.reorderUELs(['i3', 'i2', 'i1'])

In [2]: i.getUELs()

Out[2]: ['i3', 'i2', 'i1']

In [3]: i.records

Out[3]:

uni element_text

0 i1

1 i2

2 i3

**Note:** This example does not change the indexing scheme of the Pandas DataFrame at all, it only changes the underlying integer numbering scheme for the categories. We can see this by looking at the Pandas `codes`:

In [1]: i.records["uni"].cat.codes

Out[1]:

0 2

1 1

2 0

dtype: int8

## setUELs Examples
`reorderUELs` is a method of all GAMS symbol classes. This method allows the user to create new UELs, rename UELs, and reorder UELs all in one method. For example:

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

A user could accomplish a UEL reorder operation with `setUELs`:

In [1]: i.setUELs(["i3", "i2", "i1"])

In [2]: i.getUELs()

Out[2]: ['i3', 'i2', 'i1']

In [3]: i.records

Out[3]:

uni element_text

0 i1

1 i2

2 i3

A user could accomplish a UEL reorder + add UELs operation with `setUELs`:

In [1]: i.setUELs(["i3", "i2", "i1", "j1", "j2"])

In [2]: i.getUELs()

Out[2]: ['i3', 'i2', 'i1', 'j1', 'j2']

In [3]: i.records

Out[3]:

uni element_text

0 i1

1 i2

2 i3

In [4]: i.records["uni"].cat.codes

Out[4]:

0 2

1 1

2 0

dtype: int8

A user could accomplish a UEL reorder + add + rename with `setUELs`:

In [1]: i.setUELs(["j3", "j2", "j1", "ham", "cheese"], rename=True)

In [2]: i.getUELs()

Out[2]: ['j3', 'j2', 'j1', 'ham', 'cheese']

In [3]: i.records

Out[3]:

uni element_text

0 j3

1 j2

2 j1

In [4]: i.records["uni"].cat.codes

Out[4]:

0 0

1 1

2 2

dtype: int8

**Note:** This example does not change the indexing scheme of the Pandas DataFrame at all, but the `rename=True` flag means that the records will get updated just as if a `renameUELs` call had been made.

If a user wanted to set new UELs on top of this data, without renaming, they would need to be careful to include the current UELs in the UELs being set. It is possible to loose these labels if they are not included (which will prevent the data from being written to GDX/GMD).

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2", "i3"])

i.setUELs(["j1", "i2", "j3", "ham", "cheese"])

In [1]: i.getUELs()

Out[1]: ['j1', 'i2', 'j3', 'ham', 'cheese']

In [2]: i.records

Out[2]:

uni element_text

0 NaN

1 i2

2 NaN

## String Manipulation on UELs
It is easy to perform common string manipulations on UELs at the dimension, symbol and container levels with a series of convenience functions: `lowerUELs`, `upperUELs`, `lstripUELs`, `rstripUELs`, `stripUELs`, `capitalizeUELs`, `casefoldUELs`, `titleUELs`, `ljustUELs`, `rjustUELs`. These methods are wrappers around Python's built in string methods and are designed to efficiently perform bulk UEL transformations on your GAMS data.

The following example shows operations on the entire container:

m = gt.Container()

i = gt.Set(m, "i", ["*", "*"], records=[(f"i{i}", f"j{i}") for i in range(3)])

k = gt.Set(m, "k", records=[(f"aaa{i}") for i in range(3)])

In [1]: m.getUELs()

Out[1]: ['i0', 'i1', 'i2', 'j0', 'j1', 'j2', 'aaa0', 'aaa1', 'aaa2']

In [2]: m.upperUELs()

Out[2]: <GAMS Transfer Container (0x7f8110719e10)>

In [3]: m.getUELs()

Out[3]: ['I0', 'I1', 'I2', 'J0', 'J1', 'J2', 'AAA0', 'AAA1', 'AAA2']

In [4]: m.lowerUELs("i")

Out[4]: <GAMS Transfer Container (0x7f8110719e10)>

In [5]: m.getUELs()

Out[5]: ['i0', 'i1', 'i2', 'j0', 'j1', 'j2', 'AAA0', 'AAA1', 'AAA2']

In [6]: m.upperUELs().rjustUELs(4, "_")

Out[6]: <GAMS Transfer Container (0x7f8110719e10)>

In [7]: m.getUELs()

Out[7]: ['__I0', '__I1', '__I2', '__J0', '__J1', '__J2', 'AAA0', 'AAA1', 'AAA2']

**Note:** The `ljustUELs` and `rjustUELs` methods require the user to specify the final string length and the `fill_character` used to pad the string to achieve the final length.

Similar operations can be performed at the dimension and symbol levels as can be seen in the following examples:

In [1]: i.upperUELs(0)

Out[1]: <Set `i` (0x7f8121661930)>

In [2]: i.getUELs()

Out[2]: ['I0', 'I1', 'I2', 'j0', 'j1', 'j2']

In [3]: i.casefoldUELs()

Out[3]: <Set `i` (0x7f8121661930)>

In [4]: i.getUELs()

Out[4]: ['i0', 'i1', 'i2', 'j0', 'j1', 'j2']

**Note:** Symbol dimension is indexed from zero (per Python convention)

# Reordering Symbols
The order of the Container file requires the symbols to be sorted such that, for example, a Set used as domain of another symbol appears before that symbol. The Container will try to establish a valid ordering when writing the data. This type of situation could be encountered if the user is adding and removing many symbols (and perhaps rewriting symbols with the same name) – users should attempt to only add symbols to a `Container` once, and care must be taken when creating symbol names. The method `reorderSymbols` attempts to fix symbol ordering problems. The following example shows how this can occur:

Example Symbol reordering

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i" \+ str(i) for i in range(5)])

j = gt.Set(m, "j", i, records=["i" \+ str(i) for i in range(3)])

In [1]: m.data

Out[1]: {'i': <Set `i` (0x7f7e98907e50)>, 'j': <Set `j` (0x7f7e987fb580)>}

# now we remove the set i and recreate the data
m.removeSymbols("i")

i = gt.Set(m, "i", records=["i" \+ str(i) for i in range(5)])

The symbols are now out of order in `.data` and must be reordered:

In [1]: m.data

Out[1]: {'j': <Set `j` (0x7f7e987fb580)>, 'i': <Set `i` (0x7f7e9885a140)>}

# calling reorderSymbols() will order the dictionary properly, but the domain reference in j is now broken
m.reorderSymbols()

# fix the domain reference in the set j
j.domain = i

In [1]: m.isValid()

Out[1]: True

# Rename Symbols
It is possible to rename a symbol even after it has been added to a `Container`. There are two methods that can be used to achieve the desired outcome:
* using the container method `renameSymbol`
* directly changing the `name` symbol property

We create a `Container` with two sets:

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego"])

j = gt.Set(m, "j", records=["new-york", "chicago", "topeka"])

Example #1 - Change the name of a symbol with the container method

In [1]: m.renameSymbol("i","h")

In [2]: m.data

Out[2]: {'h': <Set `h` (0x7f7e988582e0)>, 'j': <Set `j` (0x7f7e801240d0)>}

Example #2 - Change the name of a symbol with the .name attribute

In [1]: i.name = "h"

In [2]: m.data

Out[2]: {'h': <Set `h` (0x7f7e98907520)>, 'j': <Set `j` (0x7f7ea84bb0d0)>}

**Note:** Note that the renamed symbols maintain the original symbol order, this will prevent unnecessary reordering operations later in the workflow.

# Removing Symbols
Removing symbols from a container is easy when using the `removeSymbols` container method; this method accepts either a `str` or a `list` of `str`.

**Attention:** Once a symbol has been removed, it is possible to have hanging references as domain links in other symbols. The user will need to repair these other symbols with the proper domain links in order to avoid validity errors.

# GAMS Special Values
The GAMS system contains five [special values](UG_Parameters.html#UG_Parameters_ExtendedRangeArithmeticAndErrorHandling): `UNDEF` (undefined), `NA` (not available), `EPS` (epsilon), `+INF` (positive infinity), `-INF` (negative infinity). These special values must be mapped to their Python equivalents. `transfer` follows the following convention to generate the `1:1` mapping:
* `+INF` is mapped to `float("inf")`
* `-INF` is mapped to `float("-inf")`
* `EPS` is mapped to `-0.0` (mathematically identical to zero)
* `NA` is mapped to a special `NaN`
* `UNDEF` is mapped to `float("nan")`

`transfer` syntax is designed to quickly get data into a form that is usable in further analyses or visualization; this mapping also highlights the preference for data that is of type `float`, which offers performance benefits within Pandas/NumPy. The user does not need to remember these constants as they are provided within the class `SpecialValues` as `SpecialValues.POSINF`, `SpecialValues.NEGINF`, `SpecialValues.EPS`, `SpecialValues.NA`, and `SpecialValues.UNDEF`. The `SpecialValues` class also contains methods to test for these special values. Some examples are shown below; already, we, begin to introduce some of the `transfer` syntax.

Example (special values in a parameter)

import gams.transfer as gt

m = gt.Container()

x = gt.Parameter(

m,

"x",

["*"],

records=[

("i1", 1),

("i2", gt.SpecialValues.POSINF),

("i3", gt.SpecialValues.NEGINF),

("i4", gt.SpecialValues.EPS),

("i5", gt.SpecialValues.NA),

("i6", gt.SpecialValues.UNDEF),

],

description="special values",

)

The following DataFrame for `x` would look like:

In [1]: x.records

Out[1]:

uni value

0 i1 1.0

1 i2 inf

2 i3 -inf

3 i4 -0.0

4 i5 NaN

5 i6 NaN

The user can now easily test for specific special values in the `value` column of the DataFrame (returns a boolean array):

In [1]: gt.SpecialValues.isNA(x.records["value"])

Out[1]: array([False, False, False, False, True, False])

Other data structures can be passed into these methods as long as these structures can be converted into a numpy array with `dtype=float`. It follows that:

In [1]: gt.SpecialValues.isEps(gt.SpecialValues.EPS)

Out[1]: True

In [2]: gt.SpecialValues.isPosInf(gt.SpecialValues.POSINF)

Out[2]: True

In [3]: gt.SpecialValues.isNegInf(gt.SpecialValues.NEGINF)

Out[3]: True

In [4]: gt.SpecialValues.isNA(gt.SpecialValues.NA)

Out[4]: True

In [5]: gt.SpecialValues.isUndef(gt.SpecialValues.UNDEF)

Out[5]: True

In [6]: gt.SpecialValues.isUndef(gt.SpecialValues.NA)

Out[6]: False

In [6]: gt.SpecialValues.isNA(gt.SpecialValues.UNDEF)

Out[6]: False

Pandas DataFrames allow data columns to exist with mixed type (`dtype=object`) – `transfer` leverages this convenience feature to enable users to import string representations of `EPS`, `NA`, and `UNDEF` (or `UNDF`). `transfer` is tolerant of any mixed-case special value string representation. Python offers additional flexibility when representing negative/positive infinity. Any string `x` where `float(x) == float("inf")` evaluates to True can be used to represent positive infinity. Similarly, any string `x` where `float(x) == float("-inf")` evaluates to True can be used to represent negative infinity. Allowed values include `inf`, `+inf`, `INFINITY`, `+INFINITY`, `-inf`, `-INFINITY` and all mixed-case equivalents.

Example (special values defined by strings)

import gams.transfer as gt

m = gt.Container()

x = gt.Parameter(

m,

"x",

["*"],

records=[

("i1", 1),

("i2", "+inf"),

("i3", "-infinity"),

("i4", "eps"),

("i5", "na"),

("i6", "undef"),

],

description="special values",

)

These special strings will be immediately mapped to their `float` equivalents from the `SpecialValues` class in order to ensure that all data entries are float types.

# Standard Data Formats
This section is meant to introduce the standard format that `transfer` expects for symbol records. It has already been mentioned that we store data as a Pandas DataFrame, but there is an assumed structure to the column headings and column types that will be important to understand. `transfer` includes convenience functions in order to ease the burden of converting data from a user-centric format to one that is understood by `transfer`. However, advanced users will want to convert their data first and add it directly to the Container to avoid making extra copies of (potentially large) data sets.

Set Records Standard Format

All set records (including singleton sets) are stored as a Pandas DataFrame with `n` number of columns, where `n` is the dimensionality of the symbol + 1. The first `n-1` columns include the domain elements while the last column includes the set element explanatory text. Records are organized such that there is one record per row.

The names of the domain columns are flexible, but `transfer` requires unique column names. Users are encouraged to change the column headings of the underlying dataframe by using the `domain_labels` property. Using this property will ensure that unique column names are generated by adding a `_<dimension>` tag to the end of any user supplied column names. The explanatory text column is called `element_text` and must take the last position in the DataFrame.

All domain columns must be a categorical data type and the `element_text` column must be a `object` type. Pandas allows the categories (basically the unique elements of a column) to be various data types as well, however `transfer` requires that all these are type `str`. All rows in the `element_text` column must be type `str`.

Some examples:

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego"])

j = gt.Set(m, "j", [i, "*"], records=[("seattle", "new-york"), ("san-diego", "st-louis")])

k = gt.Set(m, "k", [i], is_singleton=True, records=["seattle"])

In [1]: i.records

Out[1]:

uni element_text

0 seattle

1 san-diego

In [2]: j.records

Out[2]:

i uni element_text

0 seattle new-york

1 san-diego st-louis

In [3]: k.records

Out[3]:

i element_text

0 seattle

Parameter Records Standard Format

All parameter records (including scalars) are stored as a Pandas DataFrame with `n` number of columns, where `n` is the dimensionality of the symbol + 1. The first `n-1` columns include the domain elements while the last column includes the numerical value of the records. Records are organized such that there is one record per row. Scalar parameters have zero dimension, therefore they only have one column and one row.

By default, the names of the domain columns follow a pattern of `<set_name>`; a symbol dimension that is referenced to the universe is labeled `uni`. The domain labels can be customized. Users are encouraged to change the column headings of the underlying dataframe by using the `domain_labels` property. Using this property will ensure that unique column names are generated (if not currently unique) by adding a `_<dimension>` tag to the end of any user supplied column names. The value column is called `value` and must take the last position in the DataFrame.

All domain columns must be a categorical data type and the `value` column must be a `float` type. Pandas allows the categories (basically the unique elements of a column) to be various data types as well, however `transfer` requires that all these are type `str`.

Some examples:

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego"])

a = gt.Parameter(m, "a", ["*"], records=[("seattle", 50), ("san-diego", 100)])

b = gt.Parameter(

m,

"b",

[i, "*"],

records=[("seattle", "new-york", 32.2), ("san-diego", "st-louis", 123)],

)

c = gt.Parameter(m, "c", records=90)

In [1]: a.records

Out[1]:

uni value

0 seattle 50.0

1 san-diego 100.0

In [2]: b.records

Out[2]:

i uni value

0 seattle new-york 32.2

1 san-diego st-louis 123.0

In [3]: c.records

Out[3]:

value

0 90.0

Variable/Equation Records Standard Format

Variables and equations share the same standard data format. All records (including scalar variables/equations) are stored as a Pandas DataFrame with `n` number of columns, where `n` is the dimensionality of the symbol + 5. The first `n-5` columns include the domain elements while the last five columns include the numerical values for different attributes of the records. Records are organized such that there is one record per row. Scalar variables/equations have zero dimension, therefore they have five columns and one row.

By default, the names of the domain columns follow a pattern of `<set_name>`; a symbol dimension that is referenced to the universe is labeled `uni`. The domain labels can be customized. Users are encouraged to change the column headings of the underlying dataframe by using the `domain_labels` property. Using this property will ensure that unique column names are generated (if not currently unique) by adding a `_<dimension>` tag to the end of any user supplied column names. The attribute columns are called `level`, `marginal`, `lower`, `upper`, and `scale`. These attribute columns must appear in this order. Attributes that are not supplied by the user will be assigned the default GAMS values for that variable/equation type; it is possible to not pass any attributes, `transfer` would then simply assign default values to all attributes.

All domain columns must be a categorical data type and all the attribute columns must be a `float` type. Pandas allows the categories (basically the unique elements of a column) to be various data types as well, however `transfer` requires that all these are type `str`.

Some examples:

import gams.transfer as gt

import pandas as pd

m = gt.Container()

i = gt.Set(m, "i", records=["seattle", "san-diego"])

a = gt.Variable(

m,

"a",

"free",

domain=[i],

records=pd.DataFrame(

[("seattle", 50), ("san-diego", 100)], columns=["city", "level"]

),

)

In [1]: a.records

Out[1]:

i level marginal lower upper scale

0 seattle 50.0 0.0 -inf inf 1.0

1 san-diego 100.0 0.0 -inf inf 1.0

# GDX Read/Write
Up until now, we have been focused on using `transfer` to create symbols in an empty `Container` using the symbol constructors (or their corresponding container methods). These tools will enable users to ingest data from many different formats and add them to a `Container` – however, it is also possible to read in symbol data directly from GDX files using the `read` container method. In the following sections, we will discuss this method in detail as well as the `write` method, which allows users to write out to new GDX files.

## Read GDX
There are two main ways to read in GDX based data.
* Pass the file path directly to the Container constructor (will read all symbols and records)
* Pass the file path directly to the `read` method (default read all symbols, but can read partial files)

The first option here is provided for convenience and will, internally, call the `read` method. This method will read in all symbols as well as their records. This is the easiest and fastest way to get data out of a GDX file and into your Python environment. For the following examples we leverage the GDX output generated from the [`trnsport.gms`](../gamslib_ml/libhtml/gamslib_trnsport.html) model file.

Example (reading full data w/ Container constructor)

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

In [1]: m.data

Out[1]:

{'i': <Set `i` (0x7f95b8d63e80)>,

'j': <Set `j` (0x7f95b8d63a60)>,

'a': <Parameter `a` (0x7f95b8d63ee0)>,

'b': <Parameter `b` (0x7f95b8d63d00)>,

'd': <Parameter `d` (0x7f95b8da86a0)>,

'f': <Parameter `f` (0x7f95b8da8670)>,

'c': <Parameter `c` (0x7f95b8da83d0)>,

'x': <Positive Variable `x` (0x7f95b8da83a0)>,

'z': <Free Variable `z` (0x7f95b8da8400)>,

'cost': <Eq Equation `cost` (0x7f95b8da82b0)>,

'supply': <Leq Equation `supply` (0x7f95b8da8280)>,

'demand': <Geq Equation `demand` (0x7f95b8da8580)>}

In [1]: m.describeParameters()

Out[1]:

name domain domain_type dimension number_records min mean max where_min where_max sparsity

0 a [i] regular 1 2 350.000 475.000 600.000 [seattle] [san-diego] 0.0

1 b [j] regular 1 3 275.000 300.000 325.000 [topeka] [new-york] 0.0

2 c [i, j] regular 2 6 0.126 0.176 0.225 [san-diego, topeka] [seattle, new-york] 0.0

3 d [i, j] regular 2 6 1.400 1.950 2.500 [san-diego, topeka] [seattle, new-york] 0.0

4 f [] none 0 1 90.000 90.000 90.000 None None None

A user could also read in data with the `read` method as shown in the following example.

Example (reading full data w/ `read` method)

import gams.transfer as gt

m = gt.Container()

m.read("trnsport.gdx")

In [1]: m.data

Out[1]:

{'i': <Set `i` (0x7f95b8d63e80)>,

'j': <Set `j` (0x7f95b8d63a60)>,

'a': <Parameter `a` (0x7f95b8d63ee0)>,

'b': <Parameter `b` (0x7f95b8d63d00)>,

'd': <Parameter `d` (0x7f95b8da86a0)>,

'f': <Parameter `f` (0x7f95b8da8670)>,

'c': <Parameter `c` (0x7f95b8da83d0)>,

'x': <Positive Variable `x` (0x7f95b8da83a0)>,

'z': <Free Variable `z` (0x7f95b8da8400)>,

'cost': <Eq Equation `cost` (0x7f95b8da82b0)>,

'supply': <Leq Equation `supply` (0x7f95b8da8280)>,

'demand': <Geq Equation `demand` (0x7f95b8da8580)>}

It is also possible to read in a partial GDX file with the `read` method, as shown in the following example:

m = gt.Container()

m.read("trnsport.gdx", "x")

In [1]: m.data

Out[1]: {'x': <Positive Variable `x` (0x7f9598a38dc0)>}

In [2]: m.data["x"].records

Out[2]:

i j level marginal lower upper scale

0 seattle new-york 50.0 0.000 0.0 inf 1.0

1 seattle chicago 300.0 0.000 0.0 inf 1.0

2 seattle topeka 0.0 0.036 0.0 inf 1.0

3 san-diego new-york 275.0 0.000 0.0 inf 1.0

4 san-diego chicago 0.0 0.009 0.0 inf 1.0

5 san-diego topeka 275.0 0.000 0.0 inf 1.0

This syntax assumes that the user will always want to read in both the metadata as well as the actual data records, but it is possible to skip the reading of the records by passing the argument `records=False`.

m = gt.Container()

m.read("trnsport.gdx", "x", records=False)

In [1]: m.data

Out[1]: {'x': <Positive Variable `x` (0x7f9598a3a200)>}

In [2]: m["x"].summary

Out[2]:

{'name': 'x',

'description': 'shipment quantities in cases',

'type': 'positive',

'domain': ['i', 'j'],

'domain_type': 'regular',

'dimension': 2,

'number_records': 6}

In [3]: type(m["x"].records)

Out[3]: <class 'NoneType'>

**Attention:** The `read` method attempts to link the domain objects together (in order to have a "regular" `domain_type`) but if domain sets are not part of the read operation there is no choice but to default to a "relaxed" `domain_type`. This can be seen in the last example where we only read in the variable `x` and not the domain sets (`i` and `j`) that the variable is defined over. All the data will be available to the user, but domain checking is no longer possible. The symbol `x` will remain with "relaxed" domain type even if the user were to read in sets `i` and `j` in a second `read` call.

## Write GDX
A user can write data to a GDX file by simply passing a file path (as a string). The `write` method will then create the GDX and write all data in the `Container`.

Example

m.write("path/to/file.gdx")

Example (write a compressed GDX file)

m.write("path/to/file.gdx", compress=True)

By default, all symbols in the Container will be written, however it is possible to write a subset of the symbols to a GDX file with the `symbols` argument. If a domain set is not included in the `symbols` list then the symbol will automatically be relaxed (but will retain the domain set's name as a string label – it does not get relaxed to `*`). This behavior can be seen in the following example.

import gams.transfer as gt

m = gt.Container()

i = gt.Set(m, "i", records=["i1", "i2"])

a = gt.Parameter(

m,

"a",

[i, i],

records=[("i1", "i1", 10), ("i2", "i2", 12)],

)

m.write("out.gdx", "a")

# create a new container and read in the GDX
m2 = gt.Container("out.gdx")

# look at all the data
In [1]: m2.data

Out[1]: {'a': <Parameter `a` (0x7f9598a61510)>}

# notice that `a` has a relaxed domain type now
In [2]: m2["a"].domain_type

Out[2]: 'relaxed'

# `a` retains the labels from the original domain sets
In [3]: m2["a"].domain

Out[3]: ['i', 'i']

# The original container `m` retains its original state before writing
In [4]: m["a"].domain

Out[4]: [<Set `i` (0x7f9598a39a80)>, <Set `i` (0x7f9598a39a80)>]

In line `4` we can see that the auto-relaxation of the domain for `a` is only temporary for writing (in this case, from Container object `m`) and will be restored so as not to disturb the Container state.

Advanced users might want to specify an order to their UEL list (i.e., the universe set); recall that the UEL ordering follows that dictated by the data. As a convenience, it is possible to prepend the UEL list with a user specified order using the `uel_priority` argument.

Example (change the order of the UEL)

m = gt.Container()

i = gt.Set(m, "i", records=["a", "b", "c"])

m.write("foo.gdx", uel_priority=["a", "c"])

The original UEL order for this GDX file would have been `["a", "b", "c"]`, but this example reorders the UEL with `uel_priority` – the positions of `b` and `c` have been swapped. This can be verified with the `gdxdump` utility (using the `uelTable` argument):
```
    gdxdump foo.gdx ueltable=foo

    Set foo /
      'a' ,
      'c' ,
      'b' /;
    $onEmpty

    Set i(*) /
    'a',
    'c',
    'b' /;

    $offEmpty
```

# GamsDatabase Read/Write
We have discussed how to create symbols in an empty `Container` and we have discussed how to exchange data with GDX files, however it is also possible to read and write data directly in memory by interacting with a GamsDatabase/GMD object – this allows `transfer` to be used to read/write data within an [Embedded Python Code](UG_EmbeddedCode.html#UG_EmbeddedCode_Python) environment or in combination with the Python OO API. There are some important differences when compared to data exchange with GDX since we are working with data representations in memory.

## Read GamsDatabases
Just as with a GDX, there are two main ways to read in data that is in a GamsDatabase/GMD object.
* Pass the GamsDatabase/GMD object directly to the Container constructor (will read all symbols and records)
* Pass the GamsDatabase/GMD object directly to the `read` method (default read all symbols, but can read partial files)

The first option here is provided for convenience and will, internally, call the `read` method. This method will read in all symbols as well as their records. This is the easiest and fastest way to get data out of a GamsDatabase/GMD object and into your Python environment. While it is possible to generate a custom GamsDatabase/GMD object from scratch (using the `gmdcc` API), most users will be interacting with a GamsDatabase/GMD object that has already been instantiated internally when he/she is using Embedded Python Code or the GamsDatabase class in the Python OO API. Our examples will show how to access the GamsDatabase/GMD object – we leverage the some of the data from the [`trnsport.gms`](../gamslib_ml/libhtml/gamslib_trnsport.html) model file.

Example (reading full data w/ Container constructor)

m = gt.Container(gams.db)

**Note:** Embedded Python Code users will want pass the GamsDatabase object that is part of the GAMS Database object – this will always be referenced as `gams.db` regardless of the model file.

The following example uses embedded Python code to create a new Container, read in all symbols, and display some summary statistics as part of the gams log output.
```
    Set
       i 'canning plants' / seattle,  san-diego /
       j 'markets'        / new-york, chicago, topeka /;

    Parameter
       a(i) 'capacity of plant i in cases'
            / seattle    350
              san-diego  600 /

       b(j) 'demand at market j in cases'
            / new-york   325
              chicago    300
              topeka     275 /;

    Table d(i,j) 'distance in thousands of miles'
                  new-york  chicago  topeka
       seattle         2.5      1.7     1.8
       san-diego       2.5      1.8     1.4;

    $onembeddedCode Python:
    import gams.transfer as gt

    m = gt.Container(gams.db)
    print(m.describeSets())

    print(m.describeParameters())

    $offEmbeddedCode
```

The gams log output will then look as such (the extra `print` calls are just providing nice spacing for this example):
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- matrix.gms(29) 3 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
      name  is_singleton domain domain_type  dimension  number_records sparsity
    0    i         False    [*]        none          1               2     None
    1    j         False    [*]        none          1               3     None
      name  domain domain_type  dimension  number_records      min     mean      max            where_min            where_max sparsity
    0    a     [i]     regular          1               2  350.000  475.000  600.000            [seattle]          [san-diego]      0.0
    1    b     [j]     regular          1               3  275.000  300.000  325.000             [topeka]           [new-york]      0.0
    2    d  [i, j]     regular          2               6    1.400    1.950    2.500  [san-diego, topeka]  [seattle, new-york]      0.0

    --- Starting execution - empty program
    *** Status: Normal completion

    [3 rows x 16 columns]

    --- Starting execution - empty program
    *** Status: Normal completion
```

A user could also read in a subset of the data located in the GamsDatabase object with the `read` method as shown in the following example. Here we only read in the sets `i` and `j`, as a result the `.describeParameters()` method will return `None`.

Example (reading subset of full data w/ `read` method)

```
    Set
       i 'canning plants' / seattle,  san-diego /
       j 'markets'        / new-york, chicago, topeka /;

    Parameter
       a(i) 'capacity of plant i in cases'
            / seattle    350
              san-diego  600 /

       b(j) 'demand at market j in cases'
            / new-york   325
              chicago    300
              topeka     275 /;

    Table d(i,j) 'distance in thousands of miles'
                  new-york  chicago  topeka
       seattle         2.5      1.7     1.8
       san-diego       2.5      1.8     1.4;

    $onembeddedCode Python:
    import gams.transfer as gt

    m = gt.Container()
    m.read(gams.db, symbols=["i","j"])
    gams.printLog("")
    print(m.describeSets())
    print(m.describeParameters())

    $offEmbeddedCode
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- matrix.gms(29) 3 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    --- name  is_singleton domain domain_type  dimension  number_records sparsity
    0    i         False    [*]        none          1               2     None
    1    j         False    [*]        none          1               3     None
    None

    --- Starting execution - empty program
    *** Status: Normal completion
```

All the typical functionality of the Container exists when working with GamsDatabase/GMD objects. This means that domain linking, matrix conversion, and other more advanced options are available to the user at either compilation time or execution time (depending on the Embedded Code syntax being used, see: [Syntax](UG_EmbeddedCode.html#UG_EmbeddedCode_Syntax)). The next example generates a 1000x1000 matrix and then takes its inverse using the Numpy `linalg` package.

Example (Matrix Generation and Inversion)

```
    set i / i1*i1000 /;
    alias(i,j);

    parameter a(i,j);
    a(i,j) = 1 / (ord(i)+ord(j) - 1);
    a(i,i) = 1;

    embeddedCode Python:
    import gams.transfer as gt
    import numpy as np
    import time

    gams.printLog("")
    s = time.time()
    m = gt.Container(gams.db)
    gams.printLog(f"read data: {round(time.time() - s, 3)} sec")

    s = time.time()
    A = m["a"].toDense()
    gams.printLog(f"create matrix A: {round(time.time() - s, 3)} sec")

    s = time.time()
    invA = np.linalg.inv(A)
    gams.printLog(f"generate inv(A): {round(time.time() - s, 3)} sec")

    endEmbeddedCode
```

**Note:** In this example, the assignment of the `a` parameter is done during execution time so we must use the execution time syntax for embedded code in order to get the numerical records properly.
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- test.gms(27) 3 Mb
    --- Starting execution: elapsed 0:00:00.003
    --- test.gms(9) 36 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    ---
    --- read data: 1.1 sec
    --- create matrix A: 0.02 sec
    --- generate inv(A): 0.031 sec
    *** Status: Normal completion
```

We will extend this example in the next section to write the inverse matrix `A` back into a GAMS parameter.

## Write to GamsDatabases
A user can write to a GamsDatabase/GMD object with the `.write()` method just as he/she would write a GDX file – however there are some important differences. When a user writes a GDX file the entire GDX file represents a complete data environment (all domains have been resolved, etc.) thus, `transfer` does not need to worry about merge/replace operations. It is possible to merge/replace symbol records when a user is writing data to in-memory data representations with GamsDatabase/GMD. We show a few examples to illustrate this behavior.

Example (Populating a set in GAMS)

```
* note that we need to declare the set i over "*" in order to provide hints about the symbol dimensionality
    set i(*);

    $onembeddedCode Python:
    import gams.transfer as gt

    m = gt.Container()
    i = gt.Set(m, "i", records=["i"+str(i) for i in range(10)])
    m.write(gams.db)

    $offEmbeddedCode i

    embeddedCode Python:
    import gams.transfer as gt

    m = gt.Container(gams.db)
    gams.printLog("")
    print(m["i"].records)

    endEmbeddedCode
```

**Note:** In general, it is possible to use `transfer` to create new symbols in a GamsDatabase and GMD object (and not necessarily merge symbols) but embedded code best practices necessitate the declaration of any GAMS symbols on the GAMS side first, then the records can be filled with `transfer`.

If we break down this example we can see that the set `i` is declared within GAMS (with no records) and then the records for `i` are set by writing a `Container` to the `gams.db` GamsDatabase object (we do this at compile time). The second embedded Python code block runs at execution time and is simply there to read all the records on the set `i` – printing the sets this way adds the output to the `.log` file (we could also use the more common `display i;` operation in GAMS to display the set elements in the LST file).
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- test.gms(10) 2 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    --- test.gms(20) 3 Mb
    --- Starting execution: elapsed 0:00:01.464
    --- test.gms(13) 4 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    ---   uni   element_text
    0    i0
    1    i1
    2    i2
    3    i3
    4    i4
    5    i5
    6    i6
    7    i7
    8    i8
    9    i9

    *** Status: Normal completion
```

Example (Merging set records)

```
    set i / i1, i2 /;

    $onmulti
    $onembeddedCode Python:
    import gams.transfer as gt

    m = gt.Container()
    i = gt.Set(m, "i", records=["i"+str(i) for i in range(10)])
    m.write(gams.db, merge_symbols="i")

    $offEmbeddedCode i
    $offmulti

    embeddedCode Python:
    import gams.transfer as gt

    m = gt.Container(gams.db)
    gams.printLog("")
    print(m["i"].records)

    endEmbeddedCode
```

In this example we need to make use of $onMulti/$offMulti in order to merge new set elements into the the set `i` (the same would be true if we were merging other symbol types) – any symbol that already has records defined (in GAMS) and is being added to with Python (and `transfer`) must be wrapped with $onMulti/$offMulti. As with the previous example, the second embedded Python code block runs at execution time and is simply there to read all the records on the set `i`. Note that the UEL order will be different in this case (`i1` and `i2` come before `i0`).
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- test.gms(11) 3 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    --- test.gms(21) 3 Mb
    --- Starting execution: elapsed 0:00:01.535
    --- test.gms(14) 4 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    ---   uni   element_text
    0    i1
    1    i2
    2    i0
    3    i3
    4    i4
    5    i5
    6    i6
    7    i7
    8    i8
    9    i9

    *** Status: Normal completion
```

Example (Replacing set records)

```
    set i / x1, x2 /;

    $onmultiR
    $onembeddedCode Python:
    import gams.transfer as gt

    m = gt.Container()
    i = gt.Set(m, "i", records=["i"+str(i) for i in range(10)])
    m.write(gams.db)

    $offEmbeddedCode i
    $offmulti

    embeddedCode Python:
    import gams.transfer as gt

    m = gt.Container(gams.db)
    gams.printLog("")
    print(m["i"].records)

    endEmbeddedCode
```

In this example we want to replace the `x1` and `x2` set elements and built up a totally new element list with set elements from the `Container`. Instead of `$onMulti`/`$offMulti` we must use `$onMultiR`/`$offMulti` to ensure that the replacement happens in GAMS; we also need to remove the set `i` from the `merge_symbols` argument.

**Attention:** If the user seeks to replace all records in a symbol they must use the `$onMultiR` syntax. It is not sufficient to simply remove them from the `merge_symbols` argument in `transfer`. If the user mistakenly uses `$onMulti` the symbols will end up merging without total replacement.
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- test.gms(11) 3 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    --- test.gms(21) 3 Mb
    --- Starting execution: elapsed 0:00:01.482
    --- test.gms(14) 4 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    ---   uni   element_text
    0    i0
    1    i1
    2    i2
    3    i3
    4    i4
    5    i5
    6    i6
    7    i7
    8    i8
    9    i9

    *** Status: Normal completion
```

Example (Merging parameter records)

```
    set i;
    parameter a(i<) /
    i1 1.23
    i2 5
    /;

    $onmulti
    $onembeddedCode Python:
    import gams.transfer as gt

    m = gt.Container()
    i = gt.Set(m, "i", records=["i"+str(i) for i in range(10)])
    a = gt.Parameter(m, "a", domain=i, records=[("i"+str(i),i) for i in range(10)])
    m.write(gams.db, merge_symbols="a")

    $offEmbeddedCode i, a
    $offmulti

    embeddedCode Python:
    import gams.transfer as gt

    m = gt.Container(gams.db)
    gams.printLog("")
    print(m["a"].records)
    endEmbeddedCode
```

In this example we also need to make use of `$onMulti`/`$offMulti` in order to merge new set elements into the the set `i`, however the set `i` also needs to contain the elements that are defined in the parameter – here we make use of the `<` operator that will add the set elements from `a(i)` into the set `i`

**Note:** It would also be possible to run this example by explicitly defining the `set i /i1, i2/;` before the parameter declaration.

**Attention:** `transfer` will overwrite all duplicate records when merging. The original values of `a("i1")` and `a("i2")` have been replaced with their new values when writing the Container in this example (see output below).
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- test.gms(16) 3 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    --- test.gms(25) 3 Mb
    --- Starting execution: elapsed 0:00:01.467
    --- test.gms(19) 4 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    ---   i    value
    0  i1    1.0
    1  i2    2.0
    2  i3    3.0
    3  i4    4.0
    4  i5    5.0
    5  i6    6.0
    6  i7    7.0
    7  i8    8.0
    8  i9    9.0

    *** Status: Normal completion
```

Example (Advanced Matrix Generation and Inversion w/ Write Operation)

```
    set i / i1*i1000 /;
    alias(i,j);

    parameter a(i,j);
    a(i,j) = 1 / (ord(i)+ord(j) - 1);
    a(i,i) = 1;

    parameter inv_a(i,j);
    parameter ident(i,j);

    embeddedCode Python:
    import gams.transfer as gt
    import numpy as np
    import time

    gams.printLog("")

    s = time.time()
    m = gt.Container(gams.db)
    gams.printLog(f"read data: {round(time.time() - s, 3)} sec")

    s = time.time()
    A = m["a"].toDense()
    gams.printLog(f"create matrix A: {round(time.time() - s, 3)} sec")

    s = time.time()
    invA = np.linalg.inv(A)
    gams.printLog(f"calculate inv(A): {round(time.time() - s, 3)} sec")

    s = time.time()
    m["inv_a"].setRecords(invA)
    gams.printLog(f"convert matrix to records for inv(A): {round(time.time() - s, 3)} sec")

    s = time.time()
    I = np.dot(A,invA)
    tol = 1e-9
    I[np.where((I<tol) & (I>-tol))] = 0
    gams.printLog(f"calculate A*invA + small number cleanup: {round(time.time() - s, 3)} sec")

    s = time.time()
    m["ident"].setRecords(I)
    gams.printLog(f"convert matrix to records for I: {round(time.time() - s, 3)} sec")

    s = time.time()
    m.write(gams.db, ["inv_a","ident"])
    gams.printLog(f"write to GamsDatabase: {round(time.time() - s, 3)} sec")

    gams.printLog("")
    endEmbeddedCode inv_a, ident

    display ident;
```

In this example we extend the example shown in Read GamsDatabases to read data from GAMS, calculate a matrix inversion, do the matrix multiplication, and then write both the `A^-1` and `A*A^-1` (i.e., the identity matrix) back to GAMS for display in the LST file. This data round trip highlights the benefits of using a `transfer` Container (and the linked symbol structure) as the mechanism to move data – converting back and forth from a records format to a matrix format can be cumbersome, but here, `transfer` takes care of all the indexing for the user.

The first few lines of GAMS code generates a 1000x1000 `A` matrix as a parameter (at execution time), we then define two more parameters that we will fill with results of the embedded Python code – specifically we want to fill a parameter with the matrix `A^-1` and we want to verify that another parameter (`ident`) contains the identity matrix (i.e., `I`). Stepping through the code:

  1. We start the embedded Python code section (execution time) by importing both `transfer` and Numpy and by reading all the symbols that currently exist in the GamsDatabase. We must read in all this information in order to get the domain set information – `transfer` needs these domain sets in order to generate matricies with the proper size.
  2. Generate the matrix `A` by calling `.toDense()` on the symbol object in the Container.
  3. Take the inverse of `A` with `np.linalg.inv()`.
  4. The Parameter symbol for `inv_a` already exists in the Container, but it does not have any records (i.e., `m["inv_a"].records is None` will evaluate to True). We use `.setRecords()` to convert the `invA` back into a records format.
  5. We continue the computations by performing the matrix multiplication using `np.dot()` – we must clean up a lot of small numbers in `I`.
  6. The Parameter symbol for `ident` already exists in the Container, but it does not have any records. We use `.setRecords()` to convert `I` back into a records format.
  7. Since we are calculating these parameter values at execution time, it is not possible to modify the domain set information (or even merge/replace it). Therefore we only want to write the parameter values to GAMS. We achieve this by writing a subset of the Container symbols out with the `m.write(gams.db, ["inv_a","ident"])` call. This partial write preserves symbol validity in the Container and it does not violate other GAMS requirements.
  8. Finally, we can verify that the (albeit large) identity matrix exists in the LST file (or in another GDX file).

**Note:** It was not possible to just use `np.round` because small negative numbers that round to `-0.0` will be interpreted by `transfer` as the GAMS EPS special value.

The output for this example is shown below:
```
    GAMS 43.1.0   Copyright (C) 1987-2023 GAMS Development. All rights reserved
    --- Starting compilation
    --- matrix.gms(52) 3 Mb
    --- Starting execution: elapsed 0:00:00.004
    --- matrix.gms(11) 36 Mb
    --- Initialize embedded library libembpycclib64.dylib
    --- Execute embedded library libembpycclib64.dylib
    ---
    --- read data: 1.083 sec
    --- create matrix A: 0.016 sec
    --- calculate inv(A): 0.032 sec
    --- convert matrix to records for inv(A): 0.176 sec
    --- calculate A*invA + small number cleanup: 0.027 sec
    --- convert matrix to records for I: 0.17 sec
    --- write to GamsDatabase: 1.937 sec
    ---
    --- matrix.gms(52) 68 Mb
    *** Status: Normal completion
```

# Container Read
Containers can read from other `Container` instances. The syntax and behavior is much the same as reading from GDX and GMD sources. It is important to note that a deepcopy of all data is made when reading from these sources. The container object can be passed into the constructor (to be consistent with the shorthand notation) or the object can be passed as a argument to the `.read()` method.

import gams.transfer as gt

m = gt.Container("trnsport.gdx")

In [1]: m.data

Out[1]:

{'i': <Set `i` (0x7fc1d86d8e80)>,

'j': <Set `j` (0x7fc1d86d8e50)>,

'a': <Parameter `a` (0x7fc1d86d8df0)>,

'b': <Parameter `b` (0x7fc1d86d8fa0)>,

'd': <Parameter `d` (0x7fc1d86d84c0)>,

'f': <Parameter `f` (0x7fc1d86d9000)>,

'c': <Parameter `c` (0x7fc1d86d9120)>,

'x': <Positive Variable `x` (0x7fc1d86d90f0)>,

'z': <Free Variable `z` (0x7fc1d86d8fd0)>,

'cost': <Eq Equation `cost` (0x7fc1d86d8cd0)>,

'supply': <Leq Equation `supply` (0x7fc1d86d8c40)>,

'demand': <Geq Equation `demand` (0x7fc1d86d8c10)>}

m2 = gt.Container()

m2.read(m)

# equivalent to m2 = gt.Container(m)
In [7]: m2.data

Out[7]:

{'i': <Set `i` (0x7fc1c8153fa0)>,

'j': <Set `j` (0x7fc1c8153730)>,

'a': <Parameter `a` (0x7fc1c8153cd0)>,

'b': <Parameter `b` (0x7fc1d86fc790)>,

'd': <Parameter `d` (0x7fc1f87dd240)>,

'f': <Parameter `f` (0x7fc1c8153eb0)>,

'c': <Parameter `c` (0x7fc1f87ddb40)>,

'x': <Positive Variable `x` (0x7fc1c81536a0)>,

'z': <Free Variable `z` (0x7fc1f87ddc60)>,

'cost': <Eq Equation `cost` (0x7fc1c81539a0)>,

'supply': <Leq Equation `supply` (0x7fc1f87dcd00)>,

'demand': <Geq Equation `demand` (0x7fc1d86ff700)>}

Combining two containers

In this example we create two containers (which could have been populated from GDX files) and add in all symbol that do not currently exist in the first `Container`

import gams.transfer as gt

m1 = gt.Container()

i = gt.Set(m1, "i", records=[f"i{i}" for i in range(10)])

j = gt.Set(m1, "j", records=[f"j{i}" for i in range(10)])

k = gt.Set(m1, "k", records=[f"k{i}" for i in range(10)])

m2 = gt.Container()

a = gt.Set(m2, "a", records=[f"a{i}" for i in range(10)])

b = gt.Set(m2, "b", records=[f"b{i}" for i in range(10)])

k = gt.Set(m2, "k", records=[f"k{i}" for i in range(10)])

# now read in everything from m2 that does not exist in m1 (will read `a` and `b`)
m1.read(m2, [symname for symname, obj in m2 if symname not in m1])

In [1]: m1.data

Out[1]:

{'i': <Set `i` (0x7f9e504231c0)>,

'j': <Set `j` (0x7f9e3043cc10)>,

'k': <Set `k` (0x7f9e509bcd00)>,

'a': <Set `a` (0x7f9e50423760)>,

'b': <Set `b` (0x7f9e508ed0c0)>}

In [2]: m1.isValid()

Out[2]: True

---

## 7. API: Magic

### Table of Contents
* Introduction
* Getting Started
* Tutorial
* Converting GAMS Jupyter Notebooks into Python Scripts

**Note:** This feature is currently in beta status.

# Introduction
GAMS Jupyter Notebooks allow to use notebook technology in combination with GAMS. If you just want to learn GAMS there are probably better ways doing this. Notebooks allow you to combine GAMS and Python. The former works great with well structured data and optimization models, while the latter is very rich in features to retrieve, manipulate, and visualize data that comes in all sort of ways. Combining GAMS and Python in a notebook it is relatively easy to tell an optimization story with text, data, graphs, math, and models.

# Getting Started
The first step in getting started with GAMS Jupyter Notebooks is to make your Python 3 installation aware of the GAMS Python API described in the [Getting Started](API_PY_GETTING_STARTED.html) section of the API tutorial. We recommend to follow the steps below which are specifically tailored for getting started with GAMS Jupyter notebooks. While any Python 3.9 to 3.13 installation is supported, we recommend the use of `miniconda` Python distributions.

**Attention:** All core third party dependencies will be installed if the user supplies the optional `pip` syntax (`pip install gamsapi[magic]`).

In addition to the GAMS Python API collection (and the core `magic` dependencies), the examples located in `[PATH TO GAMS]/api/python/examples/magic` will require the additional packages: `jupyterlab`, `matplotlib`, and `tabulate`. The following code section shows how to create and set up a `conda` environment for GAMS Jupyter notebooks:

The notebooks [Millco.ipynb](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/Millco.ipynb) and [Introduction.ipynb](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/Introduction.ipynb) located in `api/python/examples/magic` are good starting points to get familiar with Jupyter notebooks and GAMS. The remainder of this section gives the dialog of the `Introduction.ipynb` notebook. Please see also the other notebook examples:
* [PickStock Example](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/pickstock.ipynb)
* [Filling grids with (distinct) polyominos](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/Polyomino.ipynb)
* [DICE Model from 2018 Nobel laureate William D. Nordhaus](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/nordhaus_dice.ipynb)
* [PickStock Analysis using R](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/PickStockAnalysisR.ipynb)

# Tutorial
# GAMS Jupyter Notebooks¶
GAMS Jupyter Notebooks allow to use notebook technology in combination with GAMS. If you _just_ want to learn GAMS there are probably better ways doing this. Notebooks allow you to combine GAMS and Python. The former works great with well structured data and optimization models, while the latter is very rich in features to retrieve, manipulate, and visualize data that comes in all sort of ways. Combining GAMS and Python in a notebook it is relatively easy to tell an optimization _story_ with text, data, graphs, math, and models.

The GAMS Jupyter Notebook builds on top of the Python 3 kernel. So by default the notebook cells are Python cells. Cells can be turned into GAMS cells, i.e. cells with GAMS syntax, using the Jupyter magic facility (first line in a cell is `%%gams`). GAMS magic commands enable GAMS support in Python Jupyter notebooks. Beside running GAMS code, it is possible to transfer data between GAMS and Python. In order to enable the GAMS magic commands, it is required to (re)load the extension `gams.magic`:

In [1]:
```
    %reload_ext gams.magic
```

## Running GAMS code¶
Running GAMS code can be done by using either `%gams` (line magic) or `%%gams` (cell magic). While `%gams` can be used for running a single line of GAMS code, `%%gams` makes the whole cell a GAMS cell. While `%gams` can appear on any line, `%%gams` is only valid in the first line of a cell.

In [2]:
```
    %gams set i(*);
```

There are a few other useful commands in connection with running GAMS in a Jupyter notebook. Some transformation functions for pandas data frames (e.g. `from2dim` (see below)) are available through the `gams` instance that becomes available right after the `%reload_ext gams.magic`.

In [3]:
```
    %%gams
    set j(*);
    parameter p(i,j);
    parameter p2(i,j);
```

The GAMS compiler and execution system has been adjusted so one can run a GAMS cell multiple time, even if it contains a declaration or an equation definition, which is normally not possible in the GAMS system. The execution of the next two cells does not create a problem, which mimics the execution, modification, and reexecution of a cell.

In [4]:
```
    %%gams
    set i / peter,paul,mary /, j / A,B,C /;
    parameter p2(i,j) / set.i.set.j 1 /;
```

In [5]:
```
    %%gams
    set i / i1*i5 /, j /j1*j5 /;
    parameter p2(i,j) / set.i.set.j 1 /;
```

You won't see any output from a GAMS cell (unless there is a solve executed in the cell, see below). All output goes to the log and lst file. If you really need to see this you can use magic command `%gams_log` and `%gams_lst` to display the content of the log and listing file of the most recent GAMS execution. The next cell displays the content of listing file of the last run GAMS cell or line magic. The `-e` only display the section of the listing file associated with the execution:

In [6]:
```
    %gams display p2;
    %gams_lst -e
```
    E x e c u t i o n

    ----     35 PARAMETER p2

                j1          j2          j3          j4          j5

    i1       1.000       1.000       1.000       1.000       1.000
    i2       1.000       1.000       1.000       1.000       1.000
    i3       1.000       1.000       1.000       1.000       1.000
    i4       1.000       1.000       1.000       1.000       1.000
    i5       1.000       1.000       1.000       1.000       1.000
```

There is a limit to the execution, modification, and reexecution of GAMS cells. If the type or the dimensionality of a symbol changes, you will need to execute the notebook from scratch and do a controlled reset of the entire GAMS database via `%gams_reset`. For example, since we declared parameter `p2` already over `(i,j)` we cannot change our mind and redeclare `p2` as `parameter p2(i,i,j)`:
```
    %gams parameter p2(i,i,j);
```

This will give you a compilation error and an exception in the cell execution (uncomment the line in the next cell to do so):

In [7]:
```
    #%gams parameter p2(i,i,j);
```

In [8]:
```
    %gams_reset
```

With a `%gams_reset` we can reset the GAMS database and can declare symbols with a different type and domain/dimension. All other things in the GAMS database are gone, too. So we need to redeclare the sets i and j, too. Furthermore `%gams_reset` provides an optional argument `--system_directory=<path/to/gams>` that allows to explicitly specify a GAMS system directory if the automatic detection of such is not wanted. Once a system directory has been specified, all `%gams_reset` and `gams.reset()` calls will take that one into account. Existing environments other than the active one are not affected automatically. Therefore a `%gams_reset` directly after `%reload_ext gams.magic` is helpful for specifying a non-default system directory for all subsequent environments. It is possible to switch back to the default behavior by providing the empty string as system directory (`%gams_reset --system_directory=`). The state of the GAMS database is kept in various files that can easily clutter your directory. The `%gams_cleanup` call helps you to clean the directory of temporary files of your current environment. The option `-k` keeps the most recent GAMS database, hence the `%gams_cleanup -k` is a save call anywhere in your notebook. The option `-a` removes also files from other environments in your notebook. This option can be combined with `-k`. The option `-c` or `--closedown` is to totally cleanup and leaves you with a fresh `base` environment only.

## Exchanging data between Python and GAMS¶
The property `gams.exchange_container` references a [GAMS Transfer](https://www.gams.com/latest/docs/API_PY_GAMSTRANSFER.html) container that organizes the data exchange between Python and GAMS. Symbols created in `gams.exchange_container` will be available in GAMS as well as symbols declared in GAMS will be available in `gams.exchange_container`:

In [9]:
```
    import numpy as np
    m = gams.exchange_container
    i = m.addSet('i', records=["i1","i2","i3"])
    j = m.addSet('j', records=["j1","j2"])
    p = m.addParameter('p', [i,j], records=np.array([[1.1,2.2],
                                                     [3.3,4.4],
                                                     [5.5,6.6]]))
```

In [10]:
```
    %gams display i, j, p;
    %gams_lst -e
```
    E x e c u t i o n

    ----     13 SET i

    i1,    i2,    i3

    ----     13 SET j

    j1,    j2

    ----     13 PARAMETER p

                j1          j2

    i1       1.100       2.200
    i2       3.300       4.400
    i3       5.500       6.600
```

The next cell declares a symbol `pp` in GAMS and multiplies the value of the parallel `p` by 2. The second line is again Python code to display the data frame of `pp` using the symbol method `<symbol>.pivot()`.

In [11]:
```
    %gams parameter pp(i,j); pp(i,j) = 2*p(i,j)
    m['pp'].pivot()
```

Out[11]:

| j1 | j2
---|---|---
i1 | 2.2 | 4.4
i2 | 6.6 | 8.8
i3 | 11.0 | 13.2

The data frames GAMS Transfer uses to store data have a very specific layout. The `setRecords` method or `records=` argument on a symbol constructor allow to provide data from many different formats and Python data structures. See the [GAMS Transfer documentation](https://www.gams.com/latest/docs/API_PY_GAMSTRANSFER.html) for details.

The GAMS line or cell magic will only synchronize symbols from `gams.exchange_container` to GAMS that have been _written to_ since the last GAMS line or cell magic execution. GAMS magic uses the Transfer attribute `modified` in order to decide if the symbol needs to be synchronized with GAMS. In exceptional situations the setting of `gams.write_all = True` bypasses this logic and updates _all_ symbols from `gams.exchange_container` in GAMS. In a similar way, only symbols that are new or have been _assigned to_ , explicit or implicit (e.g. via a _solve_) in the GAMS code will be updated in the `gams.exchange_container`. With a few exceptions, e.g. _implicit loading_ in execution time embedded code section, and `execute_loadpoint "file.gdx";` the [reference](https://www.gams.com/latest/docs/UG_GamsCall.html#GAMSAOreference) feature of GAMS identifies such symbols. In case this does not identify all symbols modified by the GAMS the setting of `gams.read_all = True` bypasses this logic and updates _all_ symbols from GAMS in `gams.exchange_container`.

While you can remove individual symbols from a container, via `m.removeSymbols('i')`, the container might be in an unstable condition if the removed symbol is used as a domain in other symbols. Symbol constructors that add a symbol to a GAMS Transfer container `m`, e.g. `i = gams.transfer.Set(m, 'i')` or their corrresponding container methods (`m.addSet('i')`) can be repeated for already existing symbols, but there is a limitation. Similar to repeated GAMS declarations, it continues to work as long as one does not change the structure (e.g. dimension or domain) of the symbol. If such changes to the symbol are necessary, one needs to first delete the symbol (extra care needs to be given to sets that are used as domain sets in other symbols) or start with a fresh exchange container by executing `gams.reset()` or `%gams_reset`. Unfortunately, symbols and data created in previous cells will also be gone after the `gams.reset()`.

## Some Data Transformation routines¶
### from2dim¶
This transforms a data frame like this

Index | Mill A | Mill B | Mill C
---|---|---|---
1 | 8 | 15 | 50
2 | 10 | 17 | 20
3 | 30 | 26 | 15

into the data frame with GAMS readable format

Index | level_0 | level_1 | 0
---|---|---|---
0 | 1 | Mill A | 8
1 | 1 | Mill B | 15
2 | 1 | Mill C | 50
3 | 2 | Mill A | 10
4 | 2 | Mill B | 17
5 | 2 | Mill C | 20
6 | 3 | Mill A | 30
7 | 3 | Mill B | 26
8 | 3 | Mill C | 15

call: `gams.from2dim(df)`

With the additional argument the default columns names can be renamed:

Index | sites | mills | value
---|---|---|---
0 | 1 | Mill A | 8
1 | 1 | Mill B | 15
2 | 1 | Mill C | 50
3 | 2 | Mill A | 10
4 | 2 | Mill B | 17
5 | 2 | Mill C | 20
6 | 3 | Mill A | 30
7 | 3 | Mill B | 26
8 | 3 | Mill C | 15

call: `gams.from2dim(df,['sites','mills','value'])`

The following cells show some examples:

In [12]:
```
    import pandas as pd
    Sites = ['1', '2', '3']
    Mills = ['Mill A','Mill B', 'Mill C']
    Dist = pd.DataFrame(index=Sites, columns=Mills, data = [[ 8, 15, 50],
                                                            [10, 17, 20],
                                                            [30, 26, 15]])
    display(Dist)
    display(gams.from2dim(Dist,['sites','mills','value']))
```

| Mill A | Mill B | Mill C
---|---|---|---
1 | 8 | 15 | 50
2 | 10 | 17 | 20
3 | 30 | 26 | 15

| sites | mills | value
---|---|---|---
0 | 1 | Mill A | 8
1 | 1 | Mill B | 15
2 | 1 | Mill C | 50
3 | 2 | Mill A | 10
4 | 2 | Mill B | 17
5 | 2 | Mill C | 20
6 | 3 | Mill A | 30
7 | 3 | Mill B | 26
8 | 3 | Mill C | 15

In [13]:
```
    gams.reset() # we will use some different i and j below, so we better reset
    m = gams.exchange_container
    dist = m.addParameter('dist', ['sites','mills'])
    dist.setRecords(gams.from2dim(Dist))
    dist.records
```

Out[13]:

| level_0 | level_1 | value
---|---|---|---
0 | 1 | Mill A | 8.0
1 | 1 | Mill B | 15.0
2 | 1 | Mill C | 50.0
3 | 2 | Mill A | 10.0
4 | 2 | Mill B | 17.0
5 | 2 | Mill C | 20.0
6 | 3 | Mill A | 30.0
7 | 3 | Mill B | 26.0
8 | 3 | Mill C | 15.0

In [14]:
```
    # Now display Transfer data frame as table
    dist.pivot()
```

Out[14]:

| Mill A | Mill B | Mill C
---|---|---|---
1 | 8.0 | 15.0 | 50.0
2 | 10.0 | 17.0 | 20.0
3 | 30.0 | 26.0 | 15.0

In [15]:
```
    # For 3 and more dimensional symbols we get
    %gams set a / a1*a3 /, b /b1*b2 /, c /c1*c5 /; parameter abc(a,b,c); abc(a,b,c) = uniform(0,1)
    m["abc"].pivot()
```

Out[15]:

|  | c1 | c2 | c3 | c4 | c5
---|---|---|---|---|---|---
a1 | b1 | 0.171747 | 0.843267 | 0.550375 | 0.301138 | 0.292212
b2 | 0.224053 | 0.349831 | 0.856270 | 0.067114 | 0.500211
a2 | b1 | 0.998118 | 0.578733 | 0.991133 | 0.762250 | 0.130692
b2 | 0.639719 | 0.159518 | 0.250081 | 0.668929 | 0.435356
a3 | b1 | 0.359700 | 0.351441 | 0.131492 | 0.150102 | 0.589114
b2 | 0.830893 | 0.230816 | 0.665734 | 0.775858 | 0.303658

In [16]:
```
    # Works also to display the level value (default) of a 2-dim variable
    %gams set i /i1*i5/, j / j1*j3 /; variable ship(i,j); ship.l(i,j) = uniform(0,1);
    m["ship"].pivot()
```

Out[16]:

| j1 | j2 | j3
---|---|---|---
i1 | 0.110492 | 0.502385 | 0.160173
i2 | 0.872462 | 0.265115 | 0.285814
i3 | 0.593956 | 0.722719 | 0.628249
i4 | 0.463798 | 0.413307 | 0.117695
i5 | 0.314212 | 0.046552 | 0.338550

In [17]:
```
    # Can pivot the marginal value as well
    %gams ship.m(i,j) = uniform(0,1);
    m["ship"].pivot(value="marginal")
```

Out[17]:

| j1 | j2 | j3
---|---|---|---
i1 | 0.182100 | 0.645727 | 0.560746
i2 | 0.769962 | 0.297806 | 0.661106
i3 | 0.755822 | 0.627447 | 0.283864
i4 | 0.086425 | 0.102515 | 0.641251
i5 | 0.545309 | 0.031525 | 0.792361

## GAMS Environment¶
The execution of GAMS lines and cells happens in a particular _environment_. At the start of the notebook no environment exists, but the _base_ environment is created automatically as soon as required. In some situations it can be useful to have more than one GAMS environment, e.g. you have two models that have the same name for different symbols. In a Python cell you can _create_ and/or _activate_ a GAMS environment so that a GAMS cell is executed in this environment. The particular GAMS Transfer _exchange container_ is also part of the environment. An environment is identified by its _name_. This name is also part of the scratch files created by executing GAMS cells and lines, e.g. `gj_e6aff890_base_cp.g00`. The name consists of common start `gj_` (for GAMS Jupyter), a unique id `je6aff890` that is assigned when the `gams` object is instantiated and is different in different notebooks. The next part `_base_` contains the name of the environment this file belongs to. The `_cp` and the extension `.g00` identify this as the file that captures the state of the GAMS virtual machine.

The following examples, demonstrate the use of environments:

In [18]:
```
    gams.active
```

Out[18]:
```
    'base'
```

In [19]:
```
    gams.reset() # reset the base environment
    %gams parameter p / i1.i2 3 /;
    gams.exchange_container['p'].records
```

Out[19]:

| uni_0 | uni_1 | value
---|---|---|---
0 | i1 | i2 | 3.0

In [20]:
```
    # Create a new environment "new" that contains a 1-dimensional variable p
    gams.create("new") # create has an optional argument activate=boolean with default "True"
    print(f'Active environment: {gams.active}') # hence we see that the active environment is "new"
    %gams variable p(*) / i1.L 3, i1.M 2 /;
    gams.exchange_container['p'].records
```
    Active environment: new
```

Out[20]:

| uni | level | marginal | lower | upper | scale
---|---|---|---|---|---|---
0 | i1 | 3.0 | 2.0 | -inf | inf | 1.0

In [21]:
```
    gams.activate('base') # this allows to switch back to the "base" environment
    print(f'Active environment: {gams.active}') # hence we see that the active environment is "new"
    gams.exchange_container['p'].records # with 2-dim parameter p
```
    Active environment: base
```

Out[21]:

| uni_0 | uni_1 | value
---|---|---|---
0 | i1 | i2 | 3.0

## Troubleshooting and Hints¶
* Paths to notebooks must not contain whitespaces. A notebook file itself (*.ipynb) can.
* As soon as an error occurs while running GAMS code (the notebook exception is a GamsExecption), it can be useful to examine the listing file (*.lst) using `%cat path/to/listing.lst` or `%gams_lst`. The path of the listing file can be found in the last line of the output of a failing cell.

In [22]:
```
    %gams_cleanup --closedown
```

# Converting GAMS Jupyter Notebooks into Python Scripts
Sometimes it can be useful to execute the logic of a GAMS Jupyter notebook in a standalone Python script. This can be achieved by using the `gams.magic.GamsInteractive` class which implements the back-end logic of `gams.magic` and does require neither `IPython` nor `jupyter`. Translating GAMS magic commands into Python method equivalents is stright forward. First, the Python equivalent of `%reload_ext gams.magic` needs to be added to the beginning of a Python script:

from gams.magic import GamsInteractive

gams = GamsInteractive()

Afterwards, each magic command or method available in GAMS Jupyter notebooks has an equivalent in `GamsInteractive` with the same name. GAMS magic commands like `%gams` or `%gams_reset` can be translated into methods of the exact same name - in this case `GamsInteractive.gams()` and `GamsInteractive.gams_reset()`. Methods and properties which are accessed directly (without GAMS magic command) in a Jupyter notebook like `gams.exchange_container` or `gams.activate()` can be used in the exact same way from within `GamsInteractive`. Options and parameters of GAMS magic commands can be used with corresponding arguments of the equivalent methods.

While GAMS magic commands can be translated very easily, certain interactive functionality like chart plotting might require a different mechanism when being translated. Also `display()` might need to be changed into `print()` or similar to be working in a standalone Python script. In addition, Jupyter notebooks display data which is returned by the last command of a Python cell. In Python we need to use another `print()` of the return value to get it as output.

For a complete example of a translated GAMS Jupyter notebook see `[PATH TO GAMS]/api/python/examples/magic/millco.py` which is a translation of the [Millco.ipynb](https://nbviewer.org/url/www.gams.com/external/jupyter_examples/Millco.ipynb) notebook.

---

## 8. User Guide: Gamsconnect

### Table of Contents
* Concept
* Usage
* GAMS Studio Connect Editor
* Connect Agents Overview
* Getting Started Examples
* CSV
* Excel
* SQL
* Connect Agents
* Concatenate
* CSVReader
* CSVWriter
* DomainWriter
* ExcelReader
* ExcelWriter
* Filter
* GAMSReader
* GAMSWriter
* GDXReader
* GDXWriter
* LabelManipulator
* Projection
* PythonCode
* RawCSVReader
* RawExcelReader
* SQLReader
* SQLWriter
* Examples
* Connect Example for Excel (executeTool win32.ExcelMerge)
* Connect Example for Excel
* Connect Example for CSV
* Command Line Utility gamsconnect
* Advanced Topics
* Concept of Case Sensitivity
* Text Substitutions in YAML Instructions
* Encoding of YAML Instructions
* Sorting Behavior of Connect Agents
* Use Connect Agents in Custom Python Code

# Concept
GAMS Connect is a framework inspired by the concept of a so-called ETL (extract, transform, load) procedure that allows to integrate data from various data sources. The GAMS Connect framework consists of the Connect database and the Connect agents that operate on the Connect database. Via the available Connect interfaces the user passes instructions to call Connect agents for reading data from various file types into the Connect database, transforming data in the Connect database, and writing data from the Connect database to various file types. Instructions are passed in [YAML syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html). Note that in contrast to a typical ETL procedure, read, transform and write operations do not need to be strictly separated.

The GAMS Connect Framework

# Usage
GAMS Connect is available via the GAMS command line parameters [ConnectIn](UG_GamsCall.html#GAMSAOconnectin) and [ConnectOut](UG_GamsCall.html#GAMSAOconnectout), via [embedded code Connect](UG_EmbeddedCode.html#UG_EmbeddedCode_Connect), and as a standalone command line utility gamsconnect.

Instructions processed by the GAMS Connect interfaces need to be passed in YAML syntax as follows:
```
- <agent name1>:
        <root option1>: <value>
        <root option2>: <value>
        .
        <root option3>:
- <option1>: <value>
            <option2>: <value>
            .
- <option1>: <value>
            <option2>: <value>
            .
- <agent name2>:
        .
```

The user lists the instructions to be performed. All individual agent instructions begin at the same indentation level starting with a `-` (a dash and a space) followed by the Connect agent name and a `:` (a colon). Connect agent options are represented in a simple `<option>: <value>` form. Please check the documentation of Connect Agents for available options. Options at the first indentation level are called `root` options and typically define general settings, e.g. the file name. While some agents only have `root` options, others have a more complex options structure, where a root option may be a list of dictionaries containing other options. A common example is the root option `symbols` (see e.g. GDXReader). Via `symbols` many agents allow to define symbol specific options, e.g. the name of the symbol. The option tables of agents with a more complex options structure provide a _Scope_ to reflect this structure - options may be allowed at the first indentation level (`root`) and/or are assigned to other root options (e.g. `symbols`).

Checkout the GAMS Studio Connect Editor that allows creating and editing YAML instructions by a simple drag and drop of agents and corresponding options.

Note that [YAML syntax](https://docs.ansible.com/ansible/latest/reference_appendices/YAMLSyntax.html) also supports an abbreviated form for lists and dictionary, e.g. `<root option3>: [ {<option1>: <value>, <option2>: <value>}, {<option1>: <value>, <option2>: <value>} ]`.

Here is an example that uses embedded Connect code to process instructions:
```
    $onecho > distance.csv
    i;j;distance in miles
    seattle;new-york;2,5
    seattle;chicago;1,7
    seattle;topeka;1,8
    san-diego;new-york;2,5
    san-diego;chicago;1,8
    san-diego;topeka;1,4
    $offecho

    $onecho > capacity.csv
    i,capacity in cases
    seattle,350.0
    san-diego,600.0
    $offecho

    Set i 'Suppliers', j 'Markets';
    Parameter d(i<,j<) 'Distance', a(i) 'Capacity';

    $onEmbeddedCode Connect:
- CSVReader:
        file: distance.csv
        name: distance
        indexColumns: [1, 2]
        valueColumns: [3]
        fieldSeparator: ';'
        decimalSeparator: ','
- CSVReader:
        file: capacity.csv
        name: capacity
        indexColumns: [1]
        valueColumns: [2]
- GAMSWriter:
        symbols:
- name: distance
            newName: d
- name: capacity
            newName: a
    $offEmbeddedCode

    display i, j, d, a;
```

In this example, we are reading two CSV files `distance.csv` and `capacity.csv` using the CSVReader. Then we directly write to symbols in GAMS using the GAMSWriter.

## GAMS Studio Connect Editor
The [GAMS Studio Connect Editor](T_STUDIO.html#STUDIO_CONNECT_EDITOR) provides functionalities for creating and editing so-called GAMS Connect files, containing instructions in YAML syntax which will be processed by the GAMS Connect interfaces. With the Connect Editor, the user can create YAML instructions by a simple drag and drop of agents and corresponding options, instead of creating the YAML instructions for Connect manually. The content of the Connect file can also be displayed and edited in plain YAML format using a text editor. See documentation of the [Connect Editor](T_STUDIO.html#STUDIO_CONNECT_EDITOR) for more information.

# Connect Agents Overview
Current Connect agents support the following data source formats: CSV, Excel, GDX and SQL. The following Connect agents are available:

Connect agent | Description | Supported symbol types
---|---|---
Concatenate | Allows concatenating multiple symbols in the Connect database. | Sets and parameters
CSVReader | Allows reading a symbol from a specified CSV file into the Connect database. | Sets and parameters
CSVWriter | Allows writing a symbol in the Connect database to a specified CSV file. | Sets and parameters
DomainWriter | Allows rewriting the domain information of an existing Connect symbol. | Sets, parameters, variables, and equations
ExcelReader | Allows reading symbols from a specified Excel file into the Connect database. | Sets and parameters
ExcelWriter | Allows writing symbols in the Connect database to a specified Excel file. | Sets and parameters
Filter | Allows to reduce symbol data by applying filters on labels and numerical values. | Sets, parameters, variables, and equations
GAMSReader | Allows reading symbols from the GAMS database into the Connect database. | Sets, parameters, variables, and equations
GAMSWriter | Allows writing symbols in the Connect database to the GAMS database. | Sets, parameters, variables, and equations
GDXReader | Allows reading symbols from a specified GDX file into the Connect database. | Sets, parameters, variables, and equations
GDXWriter | Allows writing symbols in the Connect database to a specified GDX file. | Sets, parameters, variables, and equations
LabelManipulator | Allows to modify labels of symbols in the Connect database. | Sets, parameters, variables, and equations
Projection | Allows index reordering, projection onto a reduced index space, and expansion to an extended index space through index duplication of a GAMS symbol. | Sets, parameters, variables, and equations
PythonCode | Allows executing arbitrary Python code. | \-
RawCSVReader | Allows reading unstructured data from a specified CSV file into the Connect database. | \-
RawExcelReader | Allows reading unstructured data from a specified Excel file into the Connect database. | \-
SQLReader | Allows reading symbols from a specified SQL database into the Connect database. | Sets and parameters
SQLWriter | Allows writing symbols in the Connect database to a specified SQL database. | Sets and parameters

# Getting Started Examples
We introduce the basic functionalities of GAMS Connect agents on some simple examples. For more examples see section Examples.

## CSV
The following example (a modified version of the [trnsport](../gamslib_ml/libhtml/gamslib_trnsport.html) model) shows how to read and write CSV files. The full example is part of DataLib as model [connect03](../datalib_ml/libhtml/datalib_connect03.html). Here is a code snippet of the first lines:
```
    $onEcho > distance.csv
    i,new-york,chicago,topeka
    seattle,2.5,1.7,1.8
    san-diego,2.5,1.8,1.4
    $offEcho

    $onEcho > capacity.csv
    i,capacity
    seattle,350
    san-diego,600
    $offEcho

    $onEcho > demand.csv
    j,demand
    new-york,325
    chicago,300
    topeka,275
    $offEcho

    Set i 'canning plants', j 'markets';

    Parameter d(i<,j<)  'distance in thousands of miles'
              a(i)      'capacity of plant i in cases'
              b(j)      'demand at market j in cases';

    $onEmbeddedCode Connect:
- CSVReader:
        file: distance.csv
        name: d
        indexColumns: 1
        valueColumns: "2:lastCol"
- CSVReader:
        file: capacity.csv
        name: a
        indexColumns: 1
        valueColumns: 2
- CSVReader:
        file: demand.csv
        name: b
        indexColumns: 1
        valueColumns: 2
- GAMSWriter:
        symbols: all
    $offEmbeddedCode

    [...]
```

It starts out with the declaration of sets and parameters. With compile-time embedded Connect code, data for the parameters is read from CSV files using the Connect agent CSVReader. The CSVReader agent, for example, reads the CSV file `distance.csv` and creates the parameter `d` in the Connect database. The name of the parameter must be given by the option name. Column number 1 is specified as the first domain set using option indexColumns. The valueColumns option is used to specify the column numbers 2, 3 and 4 containing the values. Per default, the first row of the columns specified via `valueColumns` will be used as the second domain set. The symbolic constant `lastCol` can be used if the number of index or value columns is unknown. As a last step, all symbols from the Connect database are written to the GAMS database using the Connect agent GAMSWriter. The GAMSWriter agent makes the parameters `d`, `a` and `b` available outside the embedded Connect code. Note that the sets `i` and `j` are defined implicitly through parameter `d`.

Finally, after solving the `transport` model, Connect can be used to export results to a CSV file:
```
    [...]

    Model transport / all /;

    solve transport using lp minimizing z;

    embeddedCode Connect:
- GAMSReader:
        symbols:
- name: x
- Projection:
        name: x.l(i,j)
        newName: x_level(i,j)
- CSVWriter:
        file: shipment_quantities.csv
        name: x_level
        unstack: True
    endEmbeddedCode
```

This time, we need to use execution-time embedded Connect code. The Connect agent GAMSReader imports variable `x` into the Connect database. With the Connect agent CSVWriter we write the variable level to the CSV file `shipment_quantities.csv`:
```
    i_0,new-york,chicago,topeka
    seattle,50.0,300.0,0.0
    san-diego,275.0,0.0,275.0
```

Setting the option unstack to `True` allows to use the last dimension as the header row.

## Excel
The following example is part of GAMS Model Library as model [cta](../gamslib_ml/libhtml/gamslib_cta.html) and shows how to read and write Excel spreadsheets. Here is a code snippet of the first lines:
```
    Set
       i 'rows'
       j 'columns'
       k 'planes';

    Parameter
       dat(k<,i<,j<) 'unprotected data table'
       pro(k,i,j)    'information sensitive cells';
* extract data from Excel workbook
    $onEmbeddedCode Connect:
- ExcelReader:
        file: cox3.xlsx
        symbols:
- name: dat
            range: Sheet1!A1
            rowDimension: 2
            columnDimension: 1
- name: pro
            range: Sheet2!A1
            rowDimension: 2
            columnDimension: 1
- GAMSWriter:
        symbols: all
    $offEmbeddedCode

    [...]
```

It starts out with the declaration of sets and parameters. With compile-time embedded Connect code, data for the parameters is read from the Excel file `cox3.xlsx` using the Connect agent ExcelReader. The ExcelReader agent allows reading data for multiple symbols that are listed under the keyword `symbols`, here, parameter `dat` and `pro`. For each symbol, the symbol name is given by option name and the Excel range by option range. The option rowDimension defines that the first two columns of the data range will be used for the labels. In addition, the option columnDimension defines that the first row of the data range will be used for the labels. As a last step, all symbols from the Connect database are written to the GAMS database using the Connect agent GAMSWriter. The GAMSWriter agent makes the parameters `dat` and `pro` available outside the embedded Connect code. Note that the sets `i`, `j` and `k` are defined implicitly through parameter `dat`.

Finally, after solving the `cox3c` model with alternative solutions, Connect can be used to export results to Excel:
```
    [...]

    loop(l$((obj.l - best)/best <= 0.01),
       ll(l) = yes;
       binrep(s,l)             = round(b.l(s));
       binrep('','','Obj',l)   = obj.l;
       binrep('','','mSec',l)  = cox3c.resUsd*1000;
       binrep('','','nodes',l) = cox3c.nodUsd;
       binrep('Comp','Cells','Adjusted',l) = sum((i,j,k)$(not s(i,j,k)), 1$round(adjn.l(i,j,k) + adjp.l(i,j,k)));
       solve cox3c min obj using mip;
    );

    embeddedCode Connect:
- GAMSReader:
        symbols:
- name: binrep
- ExcelWriter:
        file: results.xlsx
        clearSheet: True
        symbols:
- name: binrep
    endEmbeddedCode
```

This time, we need to use execution-time embedded Connect code. The Connect agent GAMSReader imports the reporting parameter `binrep` into the Connect database. With the Connect agent ExcelWriter we write the parameter into the `binrep` sheet of the Excel file `results.xlsx`.

## SQL
The following example (a modified version of the [whouse](../gamslib_ml/libhtml/gamslib_whouse.html) model) shows how to read from and write to a SQL database (sqlite). The full example is part of DataLib as model [connect04](../datalib_ml/libhtml/datalib_connect04.html). Here is a code snippet of the first lines:
```
    [...]

    Set t 'time in quarters';

    Parameter
       price(t)  'selling price ($ per unit)'
       istock(t) 'initial stock      (units)';

    Scalar
       storecost 'storage cost  ($ per quarter per unit)'
       storecap  'stocking capacity of warehouse (units)';

    $onEmbeddedCode Connect:
- SQLReader:
        connection: {"database": "whouse.db"}
        symbols:
- name: t
            query: "SELECT * FROM timeTable;"
            type: set
- name: price
            query: "SELECT * FROM priceTable;"
- name: istock
            query: "SELECT * FROM iniStockTable;"
- name: storecost
            query: "SELECT * FROM storeCostTable;"
- name: storecap
            query: "SELECT * FROM storeCapTable;"
- GAMSWriter:
        symbols: all
    $offEmbeddedCode

    [...]
```

It starts out with the declaration of sets and parameters. With compile-time embedded Connect code, data for all the symbols are read from the sqlite database `whouse.db` using the Connect agent SQLReader by passing the connection url through the option connection. The SQLReader agent, for example, queries the table `priceTable` for data and creates the parameter `price` in the Connect database. The SQLReader allows reading data for multiple symbols that are listed under the keyword `symbols` and are fetched through the same connection. For each symbol the name must be given by the option name. The SQL query statement is passed through the option query. The symbol type can be specified using the option type. By default, every symbol is treated as a GAMS parameter. As a last step, all symbols from the Connect database are written to the GAMS database using the Connect agent GAMSWriter. The GAMSWriter agent makes all read in symbols available outside the embedded Connect code.

Further, after solving the warehouse model, Connect can be used to export the results to tables in the SQL database.
```
    [...]

    Model swp 'simple warehouse problem' / all /;

    solve swp minimizing cost using lp;

    embeddedCode Connect:
- GAMSReader:
        symbols: all
- Projection:
        name: stock.l(t)
        newName: stock_level(t)
- Projection:
        name: sell.l(t)
        newName: sell_level(t)
- Projection:
        name: buy.l(t)
        newName: buy_level(t)
- SQLWriter:
        connection: {"database": "whouse.db"}
        ifExists: replace
        symbols:
- name: stock_level
            tableName: stock_level
- name: sell_level
            tableName: sell_level
- name: buy_level
            tableName: buy_level
    endEmbeddedCode
```

Here, we need to use execution-time embedded Connect code. The Connect agent GAMSReader imports all the variables into the Connect database. The SQLWriter agent then writes each symbol to respective tables in the SQL database `whouse.db`. For example the stock level:
```
    |t_0     |level     |
    |:-------|:---------|
    |q-1     |100.0     |
    |q-2     |0.0       |
    |q-3     |0.0       |
    |q-4     |0.0       |
```

The ifExists option allows to either append to an extending table or replace it with new data. By default, the value for `ifExists` is set to `fails`.

# Connect Agents
This section provides a reference for the available Connect agents and their options. Each agent provides a table overview of available options that allows to identify the scope of an option as well as its default value.

Each option can be either _optional_ or _required_ :
* If an optional option is omitted, it will automatically receive a default value.
* Required options must be provided, but only if the parent option has been specified. A typical example is the `symbols` option. By default, `symbols` is set to `all` for certain agents. However, if `symbols` is specified as a list of individual symbols (instead of `all`), then its child option `name` becomes required.

**Note:** The option value `null` indicates that an option is missing. For optional options, it is allowed to set `null` which will have the same effect as omitting the option. This means that even an explicit `null` will result in the default value for this option.

The table overview also allows to determine the scope of an option. In some cases, agents may have the same option available across different scopes, for example the `root` scope and the `symbols` scope:
* An omitted option in the `symbols` scope inherits its value from the `root` scope. Therefore, the technical default of the option in the `symbols` scope is `null` which indicates that the option is omitted and inherits the value from the `root` scope. Note that the table overview does not show this technical `null` default.
* If an option is specified in the `symbols` scope, it will not inherit the value from the `root` scope.

## Concatenate
The Concatenate agent allows concatenating multiple symbols (sets or parameters) in the Connect database into a single symbol of the same type. It takes the union of domain sets of all concatenated symbols and uses that as the domain for the output symbol. There are several options to guide this domain finding process which are explained below. The general idea is best explained with an example. Consider three parameters `p1(i,j)`, `p2(k,i)`, and `p3(k,l)`. The union of all domain sets is `i`, `j`, `k`, and `l` and, hence, the output symbol will be `parameterOutput(symbols,i,j,k,l)`. The very first index of `parameterOutput` contains the name of the concatenated symbol followed by the domain sets. If a domain set is not used by a concatenated symbol the corresponding records in `parameterOutput` will feature the emptyUel, a `-` (dash) by default, as the following figures show:

Parameter p1, p2 and p3

The resulting parameterOutput

The Concatenate agent is especially useful in combination with UI components that provide a pivot table, like GAMS MIRO, to represent many individual output symbols in a single powerful and configurable table format.

Obviously, there are more complex situations with respect to the domain of the resulting `parameterOutput`. For example, only a subset of domain sets are relevant and the remaining ones should be combined in as few index positions as possible. For this, assume only domain sets `i` and `k` from the above example are relevant and `j` and `l` can be combined in a single index position - a so-called universal domain. The resulting `parameterOutput` would look as follows:

The resulting parameterOutput with relevant domains i and k

Moreover, the Concatenate agent needs to deal with universe domain sets `*` and domain sets that are used multiple times in a concatenated symbol. In addition to the `symbols` index (always the first index position of the output symbol), by default the union of domain sets of the concatenated symbols determine the domain of the output symbol. If a domain set (including the universe `*`) appears multiple times in a concatenated symbol domain, these duplicates will be part of the output symbol domain. For example, `q1(*,i,j,*)` and `q2(*,i,i)` will result in the output symbol `parameterOutput(symbols,*,i,j,*,i,)` by default, mapping index positions 1 to 4 of `q1` to positions 2 to 5 of `parameterOutput` and index positions 1 to 3 of `q2` to 2, 3, and 6.

All the described situations can be configured with a few options of the agent. The option outputDimensions allows to control the domain of the output symbol. The default behavior (`outputDimension: all`) gets the domain sets from the concatenated symbols and builds the union with duplicates if required. Alternatively, `outputDimensions` can be a list of the relevant domain sets (including an empty list). In any case, the agent iterates through the concatenated symbols and maps the index positions of a concatenated symbol into the index positions of the output symbol using the domain set names. Names not present in `outputDimensions` will be added as universal domains. Per default, the domain set names of a concatenated symbol will be the original domain set names as stored in the Connect database. There are two ways to adjust the domain set names of concatenated symbols: dimensionMap and an explicitly given domain for a symbol in the name option. The `dimensionMap` which is given once and holds for all symbols allows to map original domain names of concatenated symbols to the desired domain names. The `name` option provides such a map by symbol and via the index position rather than the domain names of the concatenated symbol. In the above example with `p1(i,j)`, `p2(k,i)`, and `p3(k,l)`, we could put indices `i` and `l` as well as `j` and `k` together resulting in the following output symbol:

The resulting parameterOutput with i and l as well as j and k combined in a single index position

This can be accomplished in two ways: either we use `dimensionMap: {i: il, l: il, j: jk, k: jk}` or we use `name: p1(il,jk)`, `name: p2(jk,il)`, and `name: p3(jk,il)` to explicitly define the domain names for each symbol. Note that it is not required to set `outputDimensions: [il,jk]` since per default the union of domain sets is built using the mapped domain names. In case a domain set is used more than once in a domain of a concatenated symbol the mapping goes from left to right to find the corresponding output domain. If this is not desired, the Projection agent can be used to reorder index positions in symbols or explicit index naming can be used. In the example with `q1(*,i,j,*)` and `q2(*,i,i)`, the second index position of `q2` will be put together with the second index position of `q1`. If one wants to map the second `i` of `q2` (in the third index position) together with the `i` of `q1` (in second index position), one can, e.g. do with `name: q1(*,i,j,*)`, and `name: q2(*,i2,i)`.

**Note:** 1. The Concatenate agent creates result symbols `parameterOutput` and `setOutput` for parameters and sets separately. Both have the same output domain. If different output domains for `parameterOutput` and `setOutput` are desired, use two instantiations of the Concatenate agent.
  2. Variables and equations need to be turned into parameters with the Projection agent before they can be concatenated.
  3. If option `name` is given without an explicit domain for the concatenated symbol, the domain names stored in the Connect container are used and mapped via the `dimensionMap` option, if provided.
  4. A domain set of a concatenated symbol that cannot be assigned to an index in `outputDimensions` will be mapped to a so-called universal domain. The Concatenate agent automatically adds as many universal domains as required to the output symbols.

Here is an example that uses the Concatenate agent:
```
    Sets
       i(i) / i0*i3 "i_text" /
       j(j) / j0*j3 "j_text" /
       k(k) / k0*k3 "k_text" /;

    Parameters
       p1(i) / i1 1 /
       p2(k,j) / k1.j0 2, k1.j1 3, k1.j3 4 /
       p3(j,j) / j1.j2 5, j2.j0 6, j3.j1 7, j3.j2 8 /
       s / 5 /;

    Positive Variable x(i,j);
    x.l(i,j)$(uniform(0,1)>0.8) = uniformint(0,10);

    embeddedCode Connect:
- GAMSReader:
        symbols: all
- Projection:
        name: x.l(i,j)
        newName: x_level(i,j)
- Concatenate:
        outputDimensions: [j,i]
- GDXWriter:
        file: concat_output.gdx
        symbols:
- name: setOutput
- name: parameterOutput
    endEmbeddedCode
```

The resulting set and parameter outputs look as follows:

The resulting setOutput and parameterOutput

The following options are available for the Concatenate agent.

Option | Scope | Default | Description
---|---|---|---
dimensionMap | root | `null` | Define a mapping for the domain names of concatenated symbols as stored in the Connect database to the desired domain names.
emptyUel | root | `-` | Define a character to use for empty UELs.
name | symbols | | Specify the name of the symbol with potentially index space.
newName | symbols | `null` | Specify a new name for the symbol in the `symbols` dimension of the output symbol.
outputDimensions | root | `all` | Define the dimensions of the output symbols.
parameterName | root | `parameterOutput` | Name of the parameter output symbol.
setName | root | `setOutput` | Name of the set output symbol.
skip | root | `null` | Indicate if sets or parameters should be skipped.
symbols | root | `all` | Specify symbol specific options.
symbolsDimension | root | `True` | Specify if output symbols should have a `symbols` dimension.
trace | root | `0` | Specify the trace level for debugging output.
universalDimension | root | `uni` | Specify the base name of universal dimensions.

Detailed description of the options:

**dimensionMap:** _dictionary_ (default: `null`)

**emptyUel:** _string_ (default: `-`)

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**outputDimensions:** `all`, _list of strings_ (default: `all`)

**parameterName:** _string_ (default: `parameterOutput`)

**setName:** _string_ (default: `setOutput`)

**skip:** `set`, `par` (default: `null`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**symbolsDimension:** _boolean_ (default: `True`)

**trace:** _integer_ (default: `0`)

**universalDimension:** _string_ (default: `uni`)

## CSVReader
The CSVReader allows reading a symbol (set or parameter) from a specified CSV file into the Connect database. Its implementation is based on the `pandas.DataFrame` class and its I/O API method `read_csv`. See getting started example for a simple example that uses the CSVReader.

Option | Default | Description
---|---|---
autoColumn | `null` | Generate automatic column names.
autoRow | `null` | Generate automatic row labels.
decimalSeparator | `.` (period) | Specify a decimal separator.
fieldSeparator | `,` (comma) | Specify a field separator.
file | | Specify a CSV file path.
header | `infer` | Specify the header(s) used as the column names.
indexColumns | `null` | Specify columns to use as the row labels.
indexSubstitutions | `null` | Dictionary used for substitutions in the index columns.
name | | Specify a symbol name for the Connect database.
names | `null` | List of column names to use.
quoting | `0` | Control field quoting behavior.
readCSVArguments | `null` | Dictionary containing keyword arguments for the `pandas.read_csv` method.
skipRows | `null` | Specify the rows to skip or the number of rows to skip.
stack | `infer` | Stacks the column names to index.
thousandsSeparator | `null` | Specify a thousands separator.
trace | `0` | Specify the trace level for debugging output.
type | `par` | Control the symbol type.
valueColumns | `null` | Specify columns to get the values from.
valueSubstitutions | `null` | Dictionary used for substitutions in the value columns.

Detailed description of the options:

**autoColumn:** _string_ (default: `null`)

**autoRow:** _string_ (default: `null`)

**decimalSeparator:** _string_ (default: `.`)

**fieldSeparator:** _string_ (default: `,`)

**file:** _string_ (required)

**header:** `infer`, _boolean_ , _list of integers_ (default: `infer`)

**indexColumns:** _integer_ , _string_ , _list of integers_ , _list of strings_ (default: `null`)

**indexSubstitutions:** _dictionary_ (default: `null`)

**name:** _string_ (required)

**names:** _list of strings_ (default: `null`)

**quoting:** `0`, `1`, `2`, `3` (default: `0`)

**readCSVArguments:** _dictionary_ (default: `null`)

**skipRows:** _integer_ , _list of integers_ (default: `null`)

**stack:** `infer`, _boolean_ (default: `infer`)

**thousandsSeparator:** _string_ (default: `null`)

**trace:** _integer_ (default: `0`)

**type:** `par`, `set` (default: `par`)

**valueColumns:** _integer_ , _string_ , _list of integers_ , _list or strings_ (default: `null`)

**valueSubstitutions:** _dictionary_ (default: `null`)

## CSVWriter
The CSVWriter allows writing a symbol (set or parameter) in the Connect database to a specified CSV file. Variables and equations need to be turned into parameters with the Projection agent before they can be written. See getting started example for a simple example that uses the CSVWriter.

Option | Default | Description
---|---|---
decimalSeparator | `.` (period) | Specify a decimal separator.
file | | Specify a CSV file path.
fieldSeparator | `,` (comma) | Specify a field separator.
header | `True` | Indicate if the header will be written.
name | | Specify the name of the symbol in the Connect database.
quoting | `0` | Control field quoting behavior.
setHeader | `null` | Specify a string that will be used as the header.
skipText | `False` | Indicate if the set element text will be skipped.
toCSVArguments | `null` | Dictionary containing keyword arguments for the `pandas.to_csv` method.
trace | `0` | Specify the trace level for debugging output.
unstack | `False` | Specify the dimensions to be unstacked to the header row(s).
valueSubstitutions | `null` | Dictionary used for mapping in the value column of the `DataFrame`.

Detailed description of the options:

**decimalSeparator:** _string_ (default: `.`)

**file:** _string_ (required)

**fieldSeparator:** _string_ (default: `,`)

**header:** _boolean_ (default: `True`)

**name:** _string_ (required)

**quoting:** `0`, `1`, `2`, `3` (default: `0`)

**setHeader:** _string_ (default: `null`)

**skipText:** _boolean_ (default: `False`)

**toCSVArguments:** _dictionary_ (default: `null`)

**trace:** _integer_ (default: `0`)

**unstack:** _boolean_ , _list of integers_ (default: `False`)

**valueSubstitutions:** _dictionary_ (default: `null`)

## DomainWriter
The DomainWriter agent allows to rewrite domain information for existing Connect symbols and helps dealing with domain violations.

Here is an example that uses the DomainWriter agent:
```
    Set i / i1*i2 /, ii(i) / i1 /;

    Parameter a(i) / i1 1, i2 2 /, b(i) / i1 1, i2 2 /;

    $onEmbeddedCode Connect:
- GAMSReader:
        symbols: all
- DomainWriter:
        symbols:
- name: a(ii)
            dropDomainViolations: after
- name: b('ii')
- PythonCode:
        code: |
            print("Parameter a:\n", connect.container["a"].records)
            print("Parameter b:\n",connect.container["b"].records)
- GDXWriter:
        file: a_mod.gdx
        symbols: all
    $offEmbeddedCode
```

In this example, the DomainWriter is used to modify the one-dimensional parameters `a` and `b`. For parameter `a`, a regular domain with domain set `ii` (a subset of set `i`) is established. Since parameter `a` still has the `(i2 2.0)` record, the parameter now contains a domain violation as `i2` is not part of the new regular domain `ii`. While the Connect database in general can hold symbols with domain violations, this is not the case for GAMS or GDX. Since the symbols are later written to GDX, `dropDomainViolations: after` is specified instructing the DomainWriter to drop all domain violations after the new domain is applied. For parameter `b`, a relaxed domain `'ii'` is established. This means that the universal domain `*` is established while using `ii` as the relaxed domain name. As the new domain is relaxed, no domain violations are introduced.

After the DomainWriter parameter `a` and `b` look as follows:
```
    Set a:
        ii  value
    0  i1    1.0

    Set b:
        ii  value
    0  i1    1.0
    1  i2    2.0
```

Option | Scope | Default | Description
---|---|---|---
dropDomainViolations | root/symbols | `False` | Indicate how to deal with domain violations.
name | symbols | | Specify the name of the symbol in the Connect database.
symbols | root | `all` | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**dropDomainViolations:** `after`, `before`, _boolean_ (default: `False`)

**name:** _string_ (required)

**symbols:** `all`, _list of symbols_ (default: `all`)

**trace:** _integer_ (default: `0`)

## ExcelReader
The ExcelReader agent allows to read symbols (sets and parameters) from an Excel file into the Connect database. See getting started example for a simple example that uses the ExcelReader.

**Note:** The ExcelReader supports `.xlsx` and `.xlsm` files.
Option | Scope | Default | Description
---|---|---|---
autoMerge | root/symbols | `False` | Indicate if empty cells in the labels should be merged with previous cells.
columnDimension | root/symbols | `1` | Column dimension of the symbol.
file | root | | Specify an Excel file path.
ignoreColumns | symbols | `null` | Columns to be ignored when reading.
ignoreRows | symbols | `null` | Rows to be ignored when reading.
ignoreText | root/symbols | `infer` | Indicate if the set element text should be ignored.
index | root | | Specify the Excel range for reading symbols and options directly from the spreadsheet.
indexSubstitutions | root/symbols | `null` | Dictionary used for substitutions in the row and column index.
mergedCells | root/symbols | `False` | Control the handling of empty cells in the labels and the values that are part of a merged Excel range.
name | symbols | | Specify the name of the symbol in the Connect database.
range | symbols | `[name]!A1` | Specify the Excel range of a symbol.
rowDimension | root/symbols | `1` | Row dimension of the symbol.
skipEmpty | root/symbols | `1` | Number of empty rows or columns to skip before the next empty row or column indicates the end of the block for reading with open ranges.
symbols | root | | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.
type | root/symbols | `par` | Control the symbol type.
valueSubstitutions | root/symbols | `null` | Dictionary used for mapping in the values.

Detailed description of the options:  **autoMerge:** _boolean_ (default: `False`)

**columnDimension:** _integer_ (default: `1`)

**file:** _string_ (required)

**ignoreColumns:** _integer_ , _string_ , _list of integers and strings_ (default: `null`)

**ignoreRows:** _integer_ , _string_ , _list of integers and strings >_ (default: `null`)

**ignoreText:** `infer`, _boolean_ (default: `infer`)

**index:** _string_ (required: index or symbols) (excludes: symbols)

**indexSubstitutions:** _dictionary_ (default: `null`)

**mergedCells:** _boolean_ (default: `False`)

**name:** _string_ (required)

**range:** _string_ (default: `[name]!A1`)

**rowDimension:** _integer_ (default: `1`)

**skipEmpty:** _integer_ (default: `1`)

**symbols:** _list of symbols_ (required: index or symbols) (excludes: index)

**trace:** _integer_ (default: `0`)

**type:** `par`, `set` (default: `par`)

**valueSubstitutions:** _dictionary_ (default: `null`)

## ExcelWriter
The ExcelWriter agent allows to write symbols (sets and parameters) from the Connect database to an Excel file. Variables and equations need to be turned into parameters with the Projection agent before they can be written. If the Excel file exists, the ExcelWriter appends to the existing file. See getting started example for a simple example that uses the ExcelWriter.

**Note:** The ExcelWriter only supports `.xlsx` files.

**Attention:** Please be aware of the following limitation when appending to an Excel file with formulas using the ExcelWriter: Whereas Excel stores formulas and the corresponding values, the ExcelReader and the ExcelWriter read/store either formulas or values, not both. As a consequence, when appending to an Excel file with formulas, all cells with formulas within the Excel file will not have values anymore and a subsequent read by the ExcelReader results into `NaN` for these cells. To avoid this, write to a separate output Excel file. On Windows one can merge the input Excel file with the output Excel file at the end using the tool [win32.ExcelMerge](T_WIN32_EXCELMERGE.html) (see Connect Example for Excel (executeTool win32.ExcelMerge)). An alternative approach when appending to an Excel file with formulas is to open and save the Excel file before reading it to let Excel evaluate formulas and restore the corresponding values.
Option | Scope | Default | Description
---|---|---|---
clearSheet | root/symbols | `False` | Indicate if a sheet should be cleared before writing if it exists.
columnDimension | root/symbols | `infer` | Column dimension of the symbol.
emptySymbols | tableOfContents | `False` | Controls if empty symbols should be listed in the table of contents.
file | root | | Specify an Excel file path.
index | root | `null` | Specify the Excel range for reading symbols and options directly from the spreadsheet.
mergedCells | root/symbols | `False` | Write merged cells.
name | symbols | | Specify the name of the symbol in the Connect database.
range | symbols | `[name]!A1` | Specify the Excel range of a symbol.
sheetName | tableOfContents | `Table Of Contents` | Specify the sheet name containing the table of contents.
sort | tableOfContents | `False` | Controls if symbol names in the table of contents are sorted alphabetically.
symbols | root | `all` | Specify symbol specific options.
tableOfContents | root | `False` | Controls the writing of a table of contents.
trace | root | `0` | Specify the trace level for debugging output.
valueSubstitutions | root/symbols | `null` | Dictionary used for mapping in the value column of the `DataFrame`.

Detailed description of the options:

**clearSheet:** _boolean_ (default: `False`)

**columnDimension:** `infer`, _integer_ (default: `infer`)

**emptySymbols:** _boolean_ (default: `False`)

**file:** _string_ (required)

**index:** _string_ (default: `null`)

**mergedCells:** _boolean_ (default: `False`)

**name:** _string_ (required)

**range:** _string_ (default: `[name]!A1`)

**sheetName:** _string_ (default: `Table Of Contents`)

**sort:** _boolean_ (default: `False`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**tableOfContents:** _boolean_ , _dictionary_ (default: `False`)

**trace:** _integer_ (default: `0`)

**valueSubstitutions:** _dictionary_ (default: `null`)

## Filter
The Filter agent allows to reduce symbol data by applying filters on labels and numerical values. Here is an example that uses the Filter agent:
```
    Set i / seattle, san-diego /
        j / new-york, chicago, topeka /;

    Parameter d(i,j) /
    seattle.new-york   2.5
    seattle.chicago    1.7
    seattle.topeka     1.8
    san-diego.new-york 2.5
    san-diego.chicago  1.8
    san-diego.topeka   1.4
    /;

    $onEmbeddedCode Connect:
- GAMSReader:
        symbols:
- name: d
- Filter:
        name: d
        newName: d_new
        labelFilters:
- dimension: 1
            keep: ['seattle']
- dimension: 2
            reject: ['topeka']
        valueFilters:
- rule: x<2.5
- GDXWriter:
        file: report.gdx
        symbols:
- name: d_new
    $offEmbeddedCode
```

The records of the parameter `d` are filtered and stored in a new parameter called `d_new`. Two label filters remove all labels except `seattle` from the first dimension and remove the label `topeka` from the second one. The remaining records are filtered by value where only values less than 2.5 are kept in the data. The resulting parameter `d_new` which is exported into `report.gdx` has only one record (`seattle.chicago 1.7`) left.

The following options are available for the Filter agent:

Option | Scope | Default | Description
---|---|---|---
attribute | valueFilters | `all` | Specify the attribute to which a value filter is applied.
dimension | labelFilters | `all` | Specify the dimension to which a label filter is applied.
keep | labelFilters | | Specify a list of labels to keep.
labelFilters | root | `null` | Specify filters for index columns of a symbol.
name | root | | Specify a symbol name for the Connect database.
newName | root | `null` | Specify a new name for the symbol in the Connect database.
regex | labelFilters | | Specify a regular expression to be used for filtering labels.
reject | labelFilters | | Specify a list of labels to reject.
rejectSpecialValues | valueFilters | `null` | Specify the special values to reject.
rule | valueFilters | `null` | Specify a boolean expression to be used for filtering on numerical columns.
ruleIdentifier | valueFilters | `x` | The identifier used for the value filter rule.
trace | root | `0` | Specify the trace level for debugging output.
valueFilters | root | `null` | Specify filters for numerical columns of a symbol.

Detailed description of the options:

**attribute:** `all`, `value`, `level`, `marginal`, `upper`, `lower`, `scale` (default: `all`)

**dimension:** `all`, _integer_ (default: `all`)

**keep:** _list of strings_ (required: keep or regex or reject) (excludes: regex, reject)

**labelFilters:** _list of label filters_ (default: `null`)

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**regex:** _string_ (required: keep or regex or reject) (excludes: keep, reject)

**reject:** _string_ (required: keep or regex or reject) (excludes: keep, regex)

**rejectSpecialValues:** `EPS`, `+INF`, `-INF`, `UNDEF`, `NA`, _list of special values_ (default: `null`)

**rule:** _string_ (default: `null`)

**ruleIdentifier:** _string_ (default: `x`)

**trace:** _integer_ (default: `0`)

**valueFilters:** _list of value filters_ (default: `null`)

## GAMSReader
The GAMSReader allows reading symbols from the GAMS database into the Connect database. Without GAMS context (e.g. when running the `gamsconnect` script from the command line) this agent is not available and its execution will result in an exception.

The GAMSReader allows to either read all symbols from the GAMS database:
```
- GAMSReader:
        symbols: all
```

Or specific symbols only:
```
- GAMSReader:
        symbols:
- name: i
- name: p
            newName: p_new
```

Option | Scope | Default | Description
---|---|---|---
name | symbols | | Specify the name of the symbol in the GAMS database.
newName | symbols | `null` | Specify a new name for the symbol in the Connect database.
symbols | root | `all` | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**trace:** _integer_ (default: `0`)

## GAMSWriter
The GAMSWriter allows writing symbols in the Connect database to the GAMS database. Without GAMS context (e.g. when running the `gamsconnect` script from the command line) and as part of the [connectOut](UG_GamsCall.html#GAMSAOconnectout) command line option this agent is not available and its execution will result in an exception.

The GAMSWriter allows to either write all symbols in the Connect database to the GAMS database:
```
- GAMSWriter:
        symbols: all
```

Or specific symbols only:
```
- GAMSWriter:
        symbols:
- name: i
- name: p
            newName: p_new
```

Option | Scope | Default | Description
---|---|---|---
domainCheckType | root/symbols | `default` | Specify if domain checking is applied or if records that would cause a domain violation are filtered.
duplicateRecords | root/symbols | `all` | Specify which record(s) to keep in case of duplicate records.
mergeType | root/symbols | `default` | Specify if data in a GAMS symbol is merged or replaced.
name | symbols | | Specify the name of the symbol in the Connect database.
newName | symbols | `null` | Specify a new name for the symbol in the GAMS database.
symbols | root | `all` | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**domainCheckType:** `checked`, `default`, `filtered` (default: `default`)

**duplicateRecords:** `all`, `first`, `last`, `none` (default: `all`)

**mergeType:** `default`, `merge`, `replace` (default: `default`)

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**trace:** _integer_ (default: `0`)

## GDXReader
The GDXReader allows reading symbols from a specified GDX file into the Connect database.

The GDXReader allows to either read all symbols from a GDX file:
```
- GDXReader:
        file: in.gdx
        symbols: all
```

Or specific symbols only:
```
- GDXReader:
        file: in.gdx
        symbols:
- name: i
- name: p
            newName: p_new
```

Option | Scope | Default | Description
---|---|---|---
file | root | | Specify a GDX file path.
name | symbols | | Specify the name of the symbol in the GDX file.
newName | symbols | `null` | Specify a new name for the symbol in the Connect database.
symbols | root | `all` | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**file:** _string_ (required)

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**trace:** _integer_ (default: `0`)

## GDXWriter
The GDXWriter allows writing symbols in the Connect database to a specified GDX file.

The GDXWriter allows to either write all symbols in the Connect database to a GDX file:
```
- GDXWriter:
        file: out.gdx
        symbols: all
```

Or specific symbols only:
```
- GDXWriter:
        file: out.gdx
        symbols:
- name: i
- name: p
            newName: p_new
```

Option | Scope | Default | Description
---|---|---|---
duplicateRecords | root/symbols | `all` | Specify which record(s) to keep in case of duplicate records.
file | root | | Specify a GDX file path.
name | symbols | | Specify the name of the symbol in the Connect database.
newName | symbols | `null` | Specify a new name for the symbol in the GDX file.
symbols | root | `all` | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**duplicateRecords:** `all`, `first`, `last`, `none` (default: `all`)

**file:** _string_ (required)

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**trace** _integer_ (default: `0`)

## LabelManipulator
The LabelManipulator agent allows to modify labels of symbols in the Connect database. Four different modes are available:
* case: Applies either upper, lower, or capitalize casing to labels.
* code: Replaces labels using a Python code.
* map: Uses a 1-dimensional GAMS set to perform an explicit mapping of labels.
* regex: Performs a replacement based on a regular expression.

The LabelManipulator supports manipulating the labels of the entire symbol (default) or in a specific dimension by specifying the dimension option.

Here is an example that uses the LabelManipulator agent in all four modes:
```
    Set i / seattle, san-diego /
        j / new-york, chicago, topeka /
        map / chicago 'Berlin', san-diego 'Oslo' /;

    Parameter d(i,j) /
    seattle.new-york   2.5
    seattle.chicago    1.7
    seattle.topeka     1.8
    san-diego.new-york 2.5
    san-diego.chicago  1.8
    san-diego.topeka   1.4
    /;

    $onEmbeddedCode Connect:
- GAMSReader:
        symbols: all
- LabelManipulator:
        map:
            setName: map
- LabelManipulator:
        case:
            rule: upper
- LabelManipulator:
        symbols:
- name: d
        code:
            rule: x.split('-')[-1]
- LabelManipulator:
        symbols:
- name: d
        regex:
            pattern: '[^O]$'
            replace: '\g<0>X'
        dimension: 1
- PythonCode:
        code: |
            print("Set i:\n", connect.container["i"].records)
            print("Set j:\n",connect.container["j"].records)
            print("Parameter d:\n",connect.container["d"].records)
    $offEmbeddedCode
```

In this example, various LabelManipulator agents are utilized to demonstrate different label manipulation capabilities:
* The first LabelManipulator uses the `map` mode to apply mappings defined in the GAMS set `map` across all symbols in the Connect database. Specifically, it maps the label `chicago` to `Berlin` and `san-diego` to `Oslo`, affecting all occurrences of these labels.
* The second LabelManipulator employs the `case` mode to convert all symbol labels in the database to uppercase. This modification is applied universally to every label across all symbols.
* The third LabelManipulator, configured in `code` mode, targets only the symbol `d`. It processes each label by splitting it at the hyphen (`-`) and retains only the last segment of the split. For instance, the label `NEW-YORK` is transformed to `YORK`.
* The last LabelManipulator, operating in `regex` mode and equipped with the `dimension` option set to 1, specifically alters labels in the first dimension of the symbol `d` (i.e. the `i` dimension in `d(i,j)`). It appends an `X` to labels in the first dimension that do not end with an `O`.

The resulting symbols look as follows:
```
    Set i:
            uni element_text
    0  SEATTLE
    1     OSLO

    Set j:
             uni element_text
    0  NEW-YORK
    1    BERLIN
    2    TOPEKA

    Parameter d:
               i       j   value
    0  SEATTLEX    YORK    2.5
    1  SEATTLEX  BERLIN    1.7
    2  SEATTLEX  TOPEKA    1.8
    3      OSLO    YORK    2.5
    4      OSLO  BERLIN    1.8
    5      OSLO  TOPEKA    1.4
```

The following options are available for the LabelManipulator agent:

Option | Scope | Default | Description
---|---|---|---
case | root | | Apply specified casing to labels.
code | root | | Replace labels using Python code.
dimension | root/symbols | `all` | Specify the dimension of the symbols for label manipulations.
invert | map | `False` | Used to invert the mapping direction.
map | root | | Replace labels using a 1-dimensional GAMS set containing an explicit key-value mapping.
name | symbols | | Specify a symbol name for the Connect database.
newName | symbols | `null` | Specify a new name for the symbol in the Connect database.
outputSet | regex/case/code | `null` | Name of the output set that contains the applied mapping.
pattern | regex | | The regular expression that needs to match.
regex | root | | Replace labels using a regular expression.
replace | regex | | The rule used for replacing labels that match the given pattern.
rule | case/code | | case: The type of casing to be applied. code: Python function that defines the mapping behavior.
ruleIdentifier | code | `x` | The identifier used for labels in the rule.
setName | map | | The name of the GAMS set used in map mode.
symbols | root | `all` | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**case:** _dictionary_ (required: case or code or map or regex) (excludes: code, map, regex)

**code:** _dictionary_ (required: case or code or map or regex) (excludes: case, map, regex)

**dimension:** `all`, _integer_ (default: `all`)

**invert:** _boolean_ (default: `False`)

**map:** _dictionary_ (required: case or code or map or regex) (excludes: case, code, regex)

**name:** _string_ (required)

**newName:** _string_ (default: `null`)

**outputSet:** _string_ (default: `null`)

**pattern:** _string_ (required)

**regex:** _dictionary_ (required: case or code or map or regex) (excludes: case, code, map)

**replace:** _string_ (required)

**rule:** _string_ for code, `capitalize`, `lower`, `upper` for case (required)

**ruleIdentifier:** _string_ (default: `x`)

**setName:** _string_ (required)

**symbols:** `all`, _list of symbols_ (default: `all`)

**trace** _integer_ (default: `0`)

## Projection
The Projection agent allows index reordering, projection onto a reduced index space, and expansion to an extended index space through index duplication of a GAMS symbol. It can combine these operations, allowing for complex transformations such as simultaneously duplicating some indices, eliminating others, and reordering (e.g., transforming `p(i,j,k)` to `p_new(k,k,j)`). For variables and equations a single suffix (`.l`, `.m`, `.lo`, `.up`, `.scale`, or `.all`) or a list of suffixes (e.g. `.[l,m,lo,up,scale]` or `.[all]`) can be extracted and written to a parameter. Otherwise, the type of the source symbol determines the type of the new symbol, unless `asSet` is set to `True`. If `name` is a _list_ of scalar symbols of the same type (parameters, variables, or equations), they can be stored in a one-dimensional symbol of the same type with the index label being the _name_ of the scalar symbol.

Here is an example that uses the Projection agent:
```
    Set i / i1*i2 /, j / j1*j2 /;

    Parameter
       p(i,j) / i1.j1 1, i1.j2 2, i2.j1 3, i2.j2 4 /
       s1 / 10 /
       s2 / 11 /
       s3 / 12 /;

    Variable x(i,j);
    x.l(i,j) = p(i,j);

    embeddedCode Connect:
- GAMSReader:
        symbols: all
- Projection:
        # 1. reduce index space
        name: p(i,j)
        newName: p_reduced(i)
        aggregationMethod: sum
- Projection:
        # 2. reorder index space
        name: p(idx1,idx2)
        newName: p_reordered(idx2,idx1)
- Projection:
        # 3. Extend index space
        name: p(i,j)
        newName: p_extended(i,j,i)
- Projection:
        # 4. variable with single suffix
        name: x.l(i,j)
        newName: x_level(i,j)
- Projection:
        # 5. variable with all suffix
        name: x.all(i,j)
        newName: x_all(i)
        aggregationMethod: last
- Projection:
        # 6. parameter as set
        name: p(i,j)
        newName: p_set(i,j)
        asSet: True
        text: "from {i} to {j}"
- Projection:
        # 7. list of scalars
        name: [s1,s2,s3]
        newName: p_scalars
- PythonCode:
        code: |
            print("Parameter p_reduced:\n", connect.container["p_reduced"].records)
            print("Parameter p_reordered:\n", connect.container["p_reordered"].records)
            print("Parameter p_extended:\n", connect.container["p_extended"].records)
            print("Parameter x_level:\n", connect.container["x_level"].records)
            print("Parameter x_all:\n", connect.container["x_all"].records)
            print("Set p_set:\n", connect.container["p_set"].records)
            print("Parameter p_scalars:\n", connect.container["p_scalars"].records)
    endEmbeddedCode
```

In this example, various Projection agents are utilized to demonstrate different projection capabilities:

  1. The Projection agent is used to project parameter `p` to a reduced index space. Aggregation method `sum` is selected to aggregate records on the remaining index by taking the sum.
```
Parameter p_reduced:
                  i  value
             0  i1    3.0
             1  i2    7.0

```

  2. The Projection agent is used to only reorder the index space of parameter `p`. Note that the list of indices specified under `name` and `newName` is solely intended to establish the index order for the new symbol and therefore does not need to coincide with the names of the actual GAMS domain sets.
```
Parameter p_reordered:
                  j   i  value
             0  j1  i1    1.0
             1  j2  i1    2.0
             2  j1  i2    3.0
             3  j2  i2    4.0

```

  3. The Projection agent is used to project parameter `p` to an extended index space by duplicating index `i`. The new symbol has an additional index `i` with the same values as the original index `i`.
```
Parameter p_extended:
                i_0 j_1 i_2   value
             0  i1  j1  i1    1.0
             1  i1  j2  i1    2.0
             2  i2  j1  i2    3.0
             3  i2  j2  i2    4.0

```

  4. A single suffix (`.l`) turns the variable into a parameter with only the level values.
```
Parameter x_level:
                  i   j  value
             0  i1  j1    1.0
             1  i1  j2    2.0
             2  i2  j1    3.0
             3  i2  j2    4.0

```

  5. The `.all` suffix turns the variable into a parameter with an additional index for the attributes. At the same time the index space is reduced using aggregation method `last`, i.e. only the last record is kept.
```
Parameter x_all:
                  i   level_1  value
             0  i1     level    2.0
             1  i1  marginal    0.0
             2  i1     lower   -inf
             3  i1     upper    inf
             4  i1     scale    1.0
             5  i2     level    4.0
             6  i2  marginal    0.0
             7  i2     lower   -inf
             8  i2     upper    inf
             9  i2     scale    1.0

```

  6. The Projection agent is used to turn the parameter into a set (`asSet: True`) with custom `text`.
```
Set p_set:
                  i   j   element_text
             0  i1  j1  from i1 to j1
             1  i1  j2  from i1 to j2
             2  i2  j1  from i2 to j1
             3  i2  j2  from i2 to j2

```

  7. A list of scalars is concatenated into a one-dimensional symbol where the index labels are the names of the scalar symbols.
```
Parameter p_scalars:
                uni_0  value
             0    s1   10.0
             1    s2   11.0
             2    s3   12.0

```

Note that many of the Projection capabilities can be combined (e.g. reducing and reordering the index space of a variable while turning the symbol into a parameter using a suffix). The Projection agent can also be used to aggregate duplicate records according to the selected aggregation method.

Option | Default | Description
---|---|---
aggregationMethod | `null` | Specify the aggregation method for the projection.
asSet | `False` | Indicate that the new symbol is a set independent of the type of the source symbol.
name | | Specify a symbol name with index space and potentially suffix for the Connect database.
newName | | Specify a new name with index space for the symbol in the Connect database.
text | `null` | Element text for resulting sets.
trace | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**aggregationMethod:** _string_ (default: `null`)

**asSet:** _boolean_ (default: `False`)

**name:** _string_ , _list of strings_ (required)

**newName:** _string_ (required)

**text:** _string_ (default: `null`)

**trace:** _integer_ (default: `0`)

## PythonCode
The PythonCode agent allows to execute arbitrary Python code. From within the code, it is possible to access the GAMS database via `gams.db` (if the PythonCode agent is running in a GAMS context) and the Connect database via `connect.container`. The GAMS database is an instance of [GamsDatabase](apis/python/classgams_1_1control_1_1database_1_1GamsDatabase.html), whereas the Connect database is a [GAMS Transfer](API_PY_GAMSTRANSFER.html) `Container` object. Furthermore there is a predefined `instructions` list that can be filled with agent instructions that are automatically executed.

Option | Default | Description
---|---|---
code | | Python code to be executed.
trace | `0` | Specify the trace level for debugging output.

Detailed description of the options:

**code:** _string_ (required)

## RawCSVReader
The RawCSVReader allows reading of unstructured data from a specified CSV file into the Connect database. Due to performance issues this agent is recommended for small to medium sized unstructured CSV only. This reader works similarly compared to the RawExcelReader agent. It reads the entire CSV file and represents its content in a couple of GAMS sets:
* `r / r1, r2, ... /` (rows)
* `c / c1, c2, ... /` (columns)
* `vs(r,c) / s1.r1.c2 "cell text", ... /` (cells with explanatory text)
* `vu(r,c,*) / s1.r1.c1."cell text" "cell text", ...` (cells with potential GAMS label)

and a parameter `vf(r,c) / r2.c2 3.14, ... /` (cells with numerical values). Unlike RawExcelReader cells with a _date_ will be not interpreted and stored in `vs` and `vu`. Cells with a string value will be stored in `vs`. If the string length exceeds the maximum length allowed for elements text, it will be truncated. RawCSVReader will try to represent the cell value as a number and if this succeeds stores the number in `vf`. Strings of GAMS special values `INF`, `-INF`, `EPS`, `NA`, and `UNDEF` as well as `TRUE` and `FALSE` will be also converted to its numerical counterpart. It will also try to represent the cell value as a string and stores this as a label in the third position in `vu`. GAMS labels have a length limitation and hence RawCSVReader automatically shortens the label to fit this limit. RawCSVReader will provide a unique label (ending in `~n` where `n` is an integer for strings exceeding the label length limit) for each string in the CSV file. The full string (if it fits) will be available as the element text of the `vu` record.

To read a CSV file with the RawCSVReader specify:
```
- RawCSVReader:
        file: data.csv
```

Option | Default | Description
---|---|---
cName | `c` | Symbol name for columns.
columnLabel | `C` | Label for columns.
file | | Specify a CSV file path.
readAsString | `True` | Control the automatic pandas type conversion of cells.
readCSVArguments | `null` | Dictionary containing keyword arguments for the `pandas.read_csv` method.
rName | `r` | Symbol name for rows.
rowLabel | `R` | Label for rows.
trace | `0` | Specify the trace level for debugging output.
vfName | `vf` | Symbol name for cells with a numerical value.
vsName | `vs` | Symbol name for cells with an explanatory text.
vuName | `vu` | Symbol name for cells with a potential GAMS label.

Detailed description of the options:

**cName:** _string_ (default: `c`)

**columnLabel:** _string_ (default: `C`)

**file:** _string_ (required)

**readAsString:** _boolean_ (default: `True`)

**readCSVArguments:** _dictionary_ (default: `null`)

**rName:** _string_ (default: `r`)

**rowLabel:** _string_ (default: `R`)

**trace:** _integer_ (default: `0`)

**vfName:** _string_ (default: `vf`)

**vsName:** _string_ (default: `vs`)

**vuName:** _string_ (default: `vu`)

## RawExcelReader
The RawExcelReader allows reading of unstructured data from a specified Excel file into the Connect database. Due to performance issues this agent is recommended for small to medium sized unstructured Excel files only. This reader works similarly compared to the [xlsdump](T_XLSDUMP.html) tool. It reads the entire spreadsheet and represents its content in a couple of GAMS sets:
* `s /s1, s2,.../` (workbook sheets)
* `w / Sheet1, Sheet2, ... /` (workbook sheets by name)
* `ws(s,w) / s1.Sheet1, s2.Sheet2, ... /` (workbook map)
* `r / r1, r2, ... /` (rows)
* `c / c1, c2, ... /` (columns)
* `vs(s,r,c) / s1.r1.c2 "cell text", ... /` (cells with explanatory text)
* `vu(s,r,c,*) / s1.r1.c1."cell text" "cell text", ...` (cells with potential GAMS label)

and a parameter `vf(s,r,c) / s1.r2.c2 3.14, ... /` (cells with numerical values). Cells with a _date_ will be stored in it's string representation in `vu` and as a Julian date in `vf`. Cells with a string value will be stored in `vs`. If the string length exceeds the maximum length allowed for elements text, it will be truncated. Excel offers many other cell value types. RawExcelReader will try to represent the cell value as a number and if this succeeds stores the number in `vf`. Strings of GAMS special values `INF`, `-INF`, `EPS`, `NA`, and `UNDEF` will be also converted to its numerical counterpart. It will also try to represent the cell value as a string and stores this as a label in the fourth position in `vu`. GAMS labels have a length limitation and hence RawExcelReader automatically shortens the label to fit this limit. RawExcelReader will provide a unique label (ending in `~n` where n is an integer for strings exceeding the label length limit) for each string in the workbook. The full string (if it fits) will be available as the element text of the `vu` record.

To read an Excel file with the RawExcelReader specify:
```
- RawExcelReader:
        file: data.xlsx
```

Option | Default | Description
---|---|---
cName | `c` | Symbol name for columns.
columnLabel | `C` | Label for columns.
file | | Specify an Excel file path.
mergedCells | `False` | Control the handling of empty cells that are part of a merged Excel range.
rName | `r` | Symbol name for rows.
rowLabel | `R` | Label for rows.
sheetLabel | `S` | Label for workbook sheets.
sName | `s` | Symbol name for workbook sheets.
trace | `0` | Specify the trace level for debugging output.
vfName | `vf` | Symbol name for cells with a numerical value.
vsName | `vs` | Symbol name for cells with an explanatory text.
vuName | `vu` | Symbol name for cells with a potential GAMS label.
wName | `w` | Symbol name for workbook sheets by name.
wsName | `ws` | Symbol name for workbook map.

Detailed description of the options:

**cName:** _string_ (default: `c`)

**columnLabel:** _string_ (default: `C`)

**file:** _string_ (required)

**mergedCells:** _boolean_ (default: `False`)

**rName:** _string_ (default: `r`)

**rowLabel:** _string_ (default: `R`)

**sheetLabel:** _string_ (default: `S`)

**sName:** _string_ (default: `s`)

**trace:** _integer_ (default: `0`)

**vfName:** _string_ (default: `vf`)

**vsName:** _string_ (default: `vs`)

**vuName:** _string_ (default: `vu`)

**wName:** _string_ (default:`w`)

**wsName:** _string_ (default: `ws`)

## SQLReader
The SQLReader agent allows to read symbols (sets and parameters) from a specified database management system (DBMS) into the Connect database. The SQLReader provides DBMS specific connection types for fast and efficient communication with MS-Access, MySQL, Postgres, SQLite and SQL Server (MS-SQL), as well as the generic connection types, PyODBC and SQLAlchemy, that allow to connect to various DBMS if the required database drivers are installed on the system. The SQLAlchemy connection type is based on `pandas.DataFrame` class' I/O API method `read_sql`. See getting started example for a simple example that uses the SQLReader.

**Note:** The connectivity to MS-Access databases is available on Windows only and requires a 64-bit MS-Access ODBC driver. See connection for more information.
Option | Scope | Default | Description
---|---|---|---
connection | root | | Connection dictionary to specify credentials for the database.
connectionArguments | root | `null` | Dictionary containing keyword arguments for the `connect` constructor of the respective SQL library or for the `sqlalchemy.create_engine` constructor.
connectionType | root | `sqlite` | Specify the connection type that will be used to connect to the database.
dTypeMap | root/symbols | `null` | Dictionary used to specify the dtype of columns.
indexSubstitutions | root/symbols | `null` | Dictionary used for substitutions in the index columns.
name | symbols | | Specify the name of the symbol in the Connect database.
query | symbols | | Specify the SQL query.
readSQLArguments | root/symbols | `null` | Dictionary containing keyword arguments for the `pandas.read_sql` method.
symbols | root | | Specify symbol specific options.
trace | root | `0` | Specify the trace level for debugging output.
type | root/symbols | `par` | Control the symbol type.
valueColumns | symbols | `infer` | Specify columns to get the values from.
valueSubstitutions | root/symbols | `null` | Dictionary used for mapping in the value column of the `DataFrame`.

Detailed description of the options:

**connection:** _dictionary_ (required)

**connectionArguments:** _dictionary_ (default: `null`)

**connectionType:** `access`, `pyodbc`, `mysql`, `postgres`, `sqlalchemy`, `sqlite`, `sqlserver` (default: `sqlite`)

**dTypeMap:** _dictionary_ (default: `null`)

**indexSubstitutions:** _dictionary_ (default: `null`)

**name:** _string_ (required)

**query:** _string_ (required)

**readSQLArguments:** _dictionary_ (default: `null`)

**symbols:** _list of symbols_ (required)

**trace:** _integer_ (default: `0`)

**type:** `par`, `set` (default: `par`)

**valueColumns:** `infer`, `lastCol`, `none`, _list of strings_ (default: `infer`)

**valueSubstitutions:** _dictionary_ (default: `null`)

## SQLWriter
The SQLWriter agent allows to write symbols (sets and parameters) from the Connect database to a specified database management system (DBMS). Variables and equations need to be turned into parameters with the Projection agent before they can be written. The SQLWriter provides DBMS specific connection types for fast and efficient communication with MS-Access, MySQL, Postgres, SQLite and SQL Server (MS-SQL), as well as the generic connection types, PyODBC and SQLAlchemy, that allow to connect to various DBMS if the required database drivers are installed on the system. The SQLAlchemy connection type is based on `pandas.DataFrame` class' I/O API method `to_sql`. See getting started example for a simple example that uses the SQLWriter.

**Note:** The connectivity to MS-Access databases is available on Windows only and requires a 64-bit MS-Access ODBC driver. See connection for more information.
Option | Scope | Default | Description
---|---|---|---
columnEncloser | root | `'` | Specify if the database uses special character to enclose column names.
connection | root | | Connection dictionary to specify credentials for the database.
connectionArguments | root | `null` | Dictionary containing keyword arguments for the `connect` constructor of the respective SQL library or for the `sqlalchemy.create_engine` constructor.
connectionType | root | `sqlite` | Specify the connection type that will be used to connect to the database.
dTypeMap | root/symbols | `null` | Specify if the database has a special data type for text and numerical data type columns.
fast | root | `False` | Accelerate data inserts using some non-standard pragmas. For SQLite only.
ifExists | root/symbols | `fail` | Specify the behavior when a table with the same name exists in the database/schema.
insertMethod | root/symbols | `default` | Specify the insertion method to be used to write the table in the database.
name | symbols | | Specify the name of the symbol in the Connect database.
schemaName | root/symbols | `null` | Specify the schema name.
skipText | root/symbols | `False` | Indicate if the set element text will be skipped.
small | root | `False` | Reduce the size of the database by storing UELs in a separate table. For SQLite only.
symbols | root | `all` | Specify symbol specific options.
tableName | symbols | | Specify the SQL table/relation in the provided database/schema.
toSQLArguments | root/symbols | `null` | Dictionary containing keyword arguments for the `pandas.to_sql` method.
trace | root | `0` | Specify the trace level for debugging output.
unstack | root/symbols | `False` | Indicate if the last index column will be used as a header row.
valueSubstitutions | root/symbols | `null` | Dictionary used for mapping in the value column of the `DataFrame`.

Detailed description of the options:

**columnEncloser:** _string_ (default: `'`)

**connection:** _dictionary_ (required)

**connectionArguments:** _dictionary_ (default: `null`)

**connectionType:** `access`, `pyodbc`, `mysql`, `postgres`, `sqlalchemy`, `sqlite`, `sqlserver` (default: `sqlite`)

**dTypeMap:** _dictionary_ (default: `null`)

**fast:** _boolean_ (default: `False`)

**ifExists:** `append`, `fail`, `replace` (default: `fail`)

**insertMethod:** `bcp`, `bulkInsert`, `default` (default: `default`)

**name:** _string_ (required)

**schemaName:** _string_ (default: `null`)

**skipText:** _boolean_ (default: `False`)

**small:** _boolean_ (default: `False`)

**symbols:** `all`, _list of symbols_ (default: `all`)

**tableName:** _string_ (required)

**toSQLArguments:** _dictionary_ (default: `null`)

**trace:** _integer_ (default: `0`)

**unstack:** _boolean_ (default: `False`)

**valueSubstitutions:** _dictionary_ (default: `null`)

# Examples
This section provides a collection of more complex examples. For simple examples see section Getting Started Examples.

## Connect Example for Excel (executeTool win32.ExcelMerge)
The following example shows how to read and write Excel files in Connect. On Windows with Excel installed, the output sheets are merged back into the input workbook using tool [win32.ExcelMerge](T_WIN32_EXCELMERGE.html). The entire code is listed at the end of the example. This model is part of DataLib as model [connect05](../datalib_ml/libhtml/datalib_connect05.html). First, the original matrix `a` is read using the GAMSReader and is then written to input.xlsx using the ExcelWriter. After clearing symbols `i` and `a` in the GAMS database, the ExcelReader is used to read file input.xlsx back in and create parameter `a` in the Connect database. The Projection agent extracts set `i` from parameter `a`. With the GAMSWriter, symbols `i` and `a` are written to the GAMS database. The tool [linalg.invert](T_LINALG_INVERT.html) calculates the inverse `inva` of `a` which is then written to output.xlsx using Connect's GAMSReader and ExcelWriter at execution time. The following lines then check if the code is not executed on a UNIX system and if Excel is available. If both is true, output.xlsx is merged into input.xlsx using tool [win32.ExcelMerge](T_WIN32_EXCELMERGE.html) and both symbols `inva` and `a` can be read from input.xslx with a single instance of the ExcelReader. If the code is executed on a UNIX system and/or Excel is not available, output.xlsx can not be merged into input.xlsx, and both files need to be read to create the symbols `inva` and `a`. The last part makes sure that `inva` is the inverse of `a`.
```
    set i / i1*i3 /; alias (i,j,k);
    table a(i,j) 'original matrix'
          i1     i2     i3
    i1    1      2      3
    i2    1      3      4
    i3    1      4      3
    ;
    $onEmbeddedCode Connect:
- GAMSReader:
        symbols:
- name: a
- ExcelWriter:
        file: input.xlsx
        symbols:
- name: a
    $offEmbeddedCode

    $onMultiR
    $clear i a

    $onEmbeddedCode Connect:
- ExcelReader:
        file: input.xlsx
        symbols:
- name: a
- Projection:
        name: a(i,j)
        newName: i(i)
        asSet: True
- GAMSWriter:
        symbols: all
        duplicateRecords: first
    $offEmbeddedCode i a

    parameter
      inva(i,j) 'inverse of a'
      chk(i,j)  'check the product a * inva'
      ;

    executeTool.checkErrorLevel 'linalg.invert i a inva';

    embeddedCode Connect:
- GAMSReader:
        symbols:
- name: inva
- ExcelWriter:
        file: output.xlsx
        symbols:
- name: inva
    endEmbeddedCode

    Scalar mergedRead /0/;
    executeTool 'win32.msappavail Excel';
    mergedRead$(errorLevel=0) = 1;

    if (mergedRead,
        executeTool.checkErrorLevel 'win32.excelMerge output.xlsx input.xlsx';
        embeddedCode Connect:
- ExcelReader:
            file: input.xlsx
            symbols:
- name: a
- name: inva
- GAMSWriter:
            symbols: all
        endEmbeddedCode a inva
    else
        embeddedCode Connect:
- ExcelReader:
            file: input.xlsx
            symbols:
- name: a
- ExcelReader:
            file: output.xlsx
            symbols:
- name: inva
- GAMSWriter:
            symbols: all
        endEmbeddedCode a inva
    );

    chk(i,j) = sum{k, a(i,k)*inva(k,j)};
    chk(i,j) = round(chk(i,j),15);
    display a,inva,chk;
    chk(i,i) = chk(i,i) - 1;
    abort$[card(chk)] 'a * ainv <> identity';
```

## Connect Example for Excel
The following example shows how to read and write Excel files in Connect. The entire code is listed at the end of the example. This model is part of DataLib as model [connect01](../datalib_ml/libhtml/datalib_connect01.html). The example (inspired by the model [herves](../gamslib_ml/libhtml/gamslib_herves.html)) reads a 3-dimensional parameter from a spreadsheet that has one row index (`code`) at the left side of the table and the other row index (`labId`) at the right of the table. A column index (`cut`) is at the top of the table. The column index consists of floating-point numbers. The goal it to read the data into GAMS but modify the labels of some sets: Only the first two decimal digits of the elements in `cut` are significant. Moreover, the `labId` should be prefixed with an `L`. A new spreadsheet with the new labels should be written. The layout of the table should remain with the exception of moving the `labId` column also to the left. Here is a screenshot of the original table:

Original spreadsheet data of table raw

The following GAMS code uses a separate GAMS program (`getdata.gms`) to get the raw data from the original spreadsheet. Connect runs inside a compile-time embedded code section and uses the Connect agent RawExcelReader to get the raw Excel data. In some subsequent GAMS code the sets `rr` and `cut[Id]` as well as the parameter `raw` are filled knowing the layout of the table (the code is written in a way that the table can grow). This GAMS program gets executed and instructed to create a GDX file. In a compile-time embedded Connect section the relevant symbols (`rr`, `cutId`, and `raw`) are read from this GDX file. The Projection agent extracts the domain `labid` from the set `rr` and some Python code using Connect agent PythonCode makes the label adjustments and sorts the data nicely. The Python code uses the [connect.container](API_PY_GAMSTRANSFER_MAIN_CLASSES.html#PY_GAMSTRANSFER_CREATE_CONTAINER) methods to read from and write to the Connect database. Finally, the GAMSWriter agent sends the data to GAMS. In the main program at execution-time an embedded Connect code section exports the `labdata` parameter in the required form (after reading it from GAMS with the GAMSReader agent). Here is a screenshot of the resulting table:

Table in newly created spreadsheet with new labels and layout

In the remainder of the GAMS code another execution-time embedded Connect code is used to read the data back from the newly created spreadsheet using Connect agent ExcelReader. The set `rr` is created from parameter `labdata` using the Projection agent and everything is written back to GAMS with Connect agent GAMSWriter. The original data and the data from the newly created spreadsheet are exported to GDX (using execute_unload) and compared to verify that the data is identical by calling [gdxdiff](T_GDXDIFF.html).
```
    Set code, labId, cut, rr(code<,labId);
    parameter labdata(code,labid,cut);
    $onEcho > getdata.gms
* Symbols for RawExcelReader
    alias (u,*); Set s,w,r,c,ws(s,w),vs(s,r,c),vu(s,r,c,u); Parameter vf(s,r,c);
    $onEmbeddedCode Connect:
- RawExcelReader:
        file: labdata.xlsx
- GAMSWriter:
        symbols: all
    $offEmbeddedCode
* Symbols to be filled
    alias (*,code,labId,cut); Parameter raw(code,labId,cut); Set cutId, rr(code,labId)
    Set cX(c,cut) 'column index', rX(r,code,labId) 'row index';
    Singleton set cLast(c); Scalar lastPos;
    loop(ws(s,'ZAg'),
      lastPos = smax(vu(s,r,c,u), c.pos); cLast(c) = c.pos=lastPos;
      loop(r$(ord(r)>4),
        rX(r,code,labId) $= vu(s,r,'C1',code) and vu(s,r,cLast,labId));
      loop(c$(ord(c)>1 and not cLast(c)),
        cX(c,cut) $= vu(s,'R4',c,cut));
      loop((rX(r,code,labId),cX(c,cut)),
        raw(code,labId,cut) = vf(s,r,c))
      loop(cX(c,cut),
        cutId(cut) = yes)
    );
    option rr<rX;
    $offEcho
    $call.checkErrorLevel gams getdata.gms lo=%gams.lo% gdx=getdata.gdx
    $onEmbeddedCode Connect:
- GDXReader:
        file: getdata.gdx
        symbols: [ {name: rr}, {name: raw}, {name: cutId, newName: cut} ]
- Projection:
        name: rr(code,labid)
        newName: labid(labid)
- PythonCode:
        code: |
          labid_records = sorted([ 'L'+t[0] for t in connect.container['labid'].records.values ], key=lambda t: int(t[1:]))
          rr_records = sorted([ (t[0],
                                   'L'+t[1]) for t in connect.container['rr'].records.values ], key=lambda t: int(t[0]))
          # Trim elements of set cut to two decimal places
          cut_records = sorted([ '{:.2f}'.format(float(t[0])) for t in connect.container['cut'].records.values ], key=float)
          labdata_records = [ (t[0],
                                 'L'+t[1],
                                 '{:.2f}'.format(float(t[2])),
                                 t[-1]) for t in connect.container['raw'].records.values ]

          connect.container.addSet('labid_mod', ['*'], records=labid_records)
          connect.container.addSet('rr_mod', ['*']*2, records=rr_records)
          connect.container.addSet('cut_mod', ['*'], records=cut_records)
          connect.container.addParameter('labdata', ['*']*3, records=labdata_records)
- GAMSWriter:
        symbols: [ {name: labid_mod, newName: labid}, {name: rr_mod, newName: rr}, {name: cut_mod, newName: cut}, {name: labdata} ]
        duplicateRecords: first
    $offEmbeddedCode
    execute_unload 'labdata.gdx', labdata, cut, rr;
* Reintroduce 0 (zeros)
    labdata(rr,cut) = labdata(rr,cut) + eps;

    execute 'rm -f labdatanew.xlsx';
* Write new workbook with good table
    embeddedCode Connect:
- GAMSReader:
        symbols: [ {name: labdata} ]
- ExcelWriter:
        file: labdatanew.xlsx
        valueSubstitutions: {EPS: 0}
        symbols:
- name: labdata
            range: ZAg!A4
    endEmbeddedCode
    option clear=rr, clear=labdata;

    embeddedCode Connect:
- ExcelReader:
        file: labdatanew.xlsx
        symbols:
- name: labdata
            rowDimension: 2
            range: ZAg!A4
- Projection:
        name: labdata(code,labid,cut)
        newName: rr(code,labid)
        asSet: True
- GAMSWriter:
        symbols: all
        duplicateRecords: first
    endEmbeddedCode
    execute_unload 'labdatanew.gdx', labdata, cut, rr;
    execute.checkErrorLevel 'gdxdiff labdata.gdx labdatanew.gdx > %system.NullFile%';
```

## Connect Example for CSV
The following example shows how to read and write CSV files in Connect. The entire code is listed at the end of the example. This model is part of DataLib as model [connect02](../datalib_ml/libhtml/datalib_connect02.html). It starts out with defining some data (`stockprice`) in a table statement in GAMS. With compile-time embedded Connect code utilizing the GAMSReader agent to bring this data into Connect and exporting it as a CSV file with agent CSVWriter. The GDXWriter agent also creates a GDX file with the data which is then used in a subsequent call to feed [gdxdump](T_GDXDUMP.html) that produces the same CSV file as CSVWriter. The text comparison tool `diff` is used to compare the two CSV files. The CSV file look as follows:
```
    "date_0","AAPL","GOOG","MMM","MSFT","WMT"
    "2012-20-11",12.124061,314.008026,60.966354,21.068886,46.991535
    "2112-20-11",12.139372,311.741516,60.731037,20.850344,47.150307
    "2212-20-11",12.203673,313.674286,61.467381,20.890808,46.991535
    "2312-20-11",12.350039,315.387848,62.401108,21.068886,47.626663
    "2712-20-11",12.448025,318.929565,62.461876,21.076981,47.499634
    "2812-20-11",12.328911,318.655609,61.604042,20.898905,47.420238
    "2912-20-11",12.404848,320.000549,62.332813,21.060795,47.626663
    "3012-20-11",12.401172,321.744019,62.044331,21.012224,47.444057
```

In remainder of the example this CSV file is read back via the Connect agent CSVReader. The code also utilizes the tool [csvread](T_DATA_CSVREAD.html) to read the CSV file into a GDX file. The code compares the results of both methods. [CSVRead](T_DATA_CSVREAD.html) also creates sets with the index elements as `Dim1`, `Dim2`, ... Therefore, Connect utilizes the Projection agent to extract the index sets `date` and `symbol` from the parameter `stockprice` as sets `Dim1` and `Dim2`. The Connect agent GDXWriter creates a GDX file of the Connect database which then can be compared with the GDX file created by [csvread](T_DATA_CSVREAD.html). The GDX comparison tool [gdxdiff](T_GDXDIFF.html) is used to compare the two GDX files.
```
    Set date,symbol;
    Table stockprice(date<,symbol<)
                    AAPL       GOOG       MMM      MSFT       WMT
    2012-20-11 12.124061 314.008026 60.966354 21.068886 46.991535
    2112-20-11 12.139372 311.741516 60.731037 20.850344 47.150307
    2212-20-11 12.203673 313.674286 61.467381 20.890808 46.991535
    2312-20-11 12.350039 315.387848 62.401108 21.068886 47.626663
    2712-20-11 12.448025 318.929565 62.461876 21.076981 47.499634
    2812-20-11 12.328911 318.655609 61.604042 20.898905 47.420238
    2912-20-11 12.404848 320.000549 62.332813 21.060795 47.626663
    3012-20-11 12.401172 321.744019 62.044331 21.012224 47.444057
    ;
* Use Connect CSVWriter to write GAMS data in CSV format moving the symbol index into the column (unstack: True)
    $onEmbeddedCode Connect:
- GAMSReader:
        symbols: [ {name: stockprice} ]
- GDXWriter:
        file: sp_connect.gdx
        symbols: all
- CSVWriter:
        file: sp_connect.csv
        name: stockprice
        header: True
        unstack: True
        quoting: 2
    $offEmbeddedCode
* Use gdxdump to create a CSV file and text compare the Connect and gdxdump CSV files
    $call.checkErrorLevel  gdxdump sp_connect.gdx output=sp_gdxdump.csv symb=stockprice format=csv columnDimension=Y > %system.NullFile%
    $call.checkErrorLevel  diff -q sp_connect.csv sp_gdxdump.csv > %system.nullFile%
* Use Connect CSVReader to read the newly created CSV file and deposit the result in a csvread compatible format
    $onEmbeddedCode Connect:
- CSVReader:
        file: sp_connect.csv
        name: stockprice
        indexColumns: 1
        valueColumns: "2:lastCol"
- Projection:
        name: stockprice(date,symbol)
        newName: Dim1(date)
        asSet: True
- Projection:
        name: stockprice(date,symbol)
        newName: Dim2(symbol)
        asSet: True
- GDXWriter:
        file: sp_connect.gdx
        symbols: all
        duplicateRecords: first
    $offEmbeddedCode
* Use CSVRead to create a GDX file and compare the Connect and CSVRead GDX files
    $call gamstool csvread sp_connect.csv id=stockprice index=1 values=2..lastCol useHeader=yes gdxout=sp_csvread.gdx > %system.NullFile%
    $call.checkErrorLevel gdxdiff sp_connect.gdx sp_csvread.gdx > %system.NullFile%
```

# Command Line Utility gamsconnect
The GAMS system directory contains the utility `gamsconnect` to run Connect instructions directly from the command line. On Windows the utility has the callable extension `.cmd`. This script wraps the Python script `connectdriver.py` by calling the Python interpreter that ships with GAMS. `gamsconnect` operates as the other Connect drivers on a YAML instruction file. The agents GAMSReader and GAMSWriter are not available from `gamsconnect` and will trigger an exception. Substitutions can be passed to `gamsconnect` via command line arguments as `key=value`, e.g. `filename=myfile.csv` and even `gams.scrdir=/tmp/`. `gamsconnect` is called like this:
```
    gamsconnect <YAMLFile> [key1=value1 [key2=value2 [key3=value3 [...]]]]
```

# Advanced Topics
## Concept of Case Sensitivity
This section describes the general concept of case sensitivity in Connect. Connect is a YAML and Python based framework and is therefore **case sensitive**. The case sensitivity provides Connect users with a better control of arbitrary data that does not necessarily come in a GAMS compatible format. Many agents allow users to clean up, manipulate or transform data in other ways where case sensitivity provides the most flexibility. However, since Connect has many GAMS dependencies (GAMS is case insensitive) and processes data from many other data formats that have their own concept of case sensitivity, there are some exceptions:
* GAMS related operations (e.g. dropDomainViolations, duplicateRecords).
* Symbol names in the Connect database. Example: A symbol `p` in the Connect database can be accessed via symbol name `p` or `P`. And if `p` exists already, a Connect agent can not create a new symbol `P`.
* Due to the case insensitivity of symbol names in the Connect database, the index list of the DomainWriter option name is also processed case insensitive. In contrast to Concatenate or Projection where the index list is solely intended to establish the index order, the DomainWriter needs to access sets in the Connect database in order to establish regular domains.
* The behavior can sometimes be case insensitive due to the data source/target (e.g. range, index, ignoreColumns).
* The behavior can sometimes be case insensitive due to the operating system (e.g. the `file` option is case insensitive on Windows).
* The behavior can sometimes be case insensitive due to other Python libraries used (e.g. readCSVArguments passes key-value pairs directly to pandas).

This implies that most Connect operations are done case sensitive. For instance, agents like Filter, LabelManipulator or Projection operate case sensitive. Consider the following example that uses the Projection agent:
```
    $onecho > p.csv
    i1,j1,2.5
    i1,j2,1.7
    i2,j1,1.8
    I2,j2,1.4
    $offEcho

    Set i;
    Parameter p_reduced(i<);

    $onEmbeddedCode Connect:
- CSVReader:
        header: False
        file: p.csv
        name: p
        indexColumns: [1,2]
        valueColumns: 3
- Projection:
        name: p(i,j)
        newName: p_reduced(i)
        aggregationMethod: first
- PythonCode:
        code: |
            print(connect.container['p_reduced'].records)
- GAMSWriter:
        symbols:
- name: p_reduced
            duplicateRecords: first
    $offEmbeddedCode

    display p_reduced;
```

Since Projection aggregates case sensitive, both records `I2 1.4` and `i2 1.8` are kept:
```
        0  value
    0  I2    1.4
    1  i1    2.5
    2  i2    1.8
```

From a GAMS (case insensitive) perspective these two records are duplicates. Therefore, duplicateRecords must be set when writing symbol `p_reduced` to GAMS. With `duplicateRecords: first` only the first duplicate record is kept.

Case sensitivity also holds for substituting indices or values. Consider the following example where the index `j2` should be substituted by `ABC` when reading the CSV file `p.csv`:
```
    $onecho > p.csv
    i1,j1,2.5
    i1,J2,1.7
    i2,j1,1.8
    i2,j2,1.4
    $offecho

    Set i,j;
    Parameter p(i<,j<);

    $onEmbeddedCode Connect:
- CSVReader:
        file: p.csv
        name: p
        indexColumns: [1,2]
        valueColumns: [3]
        header: false
        indexSubstitutions: { j2: ABC }
- GAMSWriter:
        symbols: all
    $offEmbeddedCode

    display i, j, p;
```

Since substituting indices is done case sensitive, the index `J2` will not be substituted.
```
                j1          J2         ABC

    i1       2.500       1.700
    i2       1.800                   1.400
```

## Text Substitutions in YAML Instructions
In many cases one would like to _parameterize_ the text in the Connect instructions. For example, some of the Connect agents require a file name. Instead of hard coding the file name into the YAML instructions, text substitutions allow to have a _place holder_ for the attribute that is substituted out before giving the instructions to Connect. The place holder in the YAML instructions uses the syntax `%SOMETEXT%`, similar to the GAMS [compile-time variables](UG_GamsCall.html#UG_GamsCall_DoubleDashParametersEtc_CompileTimeVars). For example:
```
- CSVReader:
        file: %MYFILENAME%
        name: distance
        indexColumns: [1, 2]
        valueColumns: [3]
```

Depending on how Connect runs, the substitution is done in various ways. The section [Substitutions in Embedded Connect Code](UG_EmbeddedCode.html#UG_EmbeddedCode_Connect_Substitution) described the substitution mechanisms for embedded Connect code. When Connect is initiated via the command line parameters [connectIn](UG_GamsCall.html#GAMSAOconnectin) or [connectOut](UG_GamsCall.html#GAMSAOconnectout), the user defined parameter specified by [double-dash command line parameters](UG_GamsCall.html#UG_GamsCall_DoubleDashParametersEtc_DoubleDashParam) and the given GAMS command line parameters, e.g. `%gams.input%` will be substituted in the YAML file. The list of parameters available for substitution is printed to the GAMS log at the beginning of the job in the section `GAMS Parameters defined`.

When Connect is initiated via the shell command `gamsconnect` all substitutions need to be specified on the command line:
```
    gamsconnect myci.yaml key1=val1 key2=val2 ...
```

`key` can be just `MYFILENAME` or be composed like `gams.Input` or `system.dirSep`.

## Encoding of YAML Instructions
All instructions provided to the Connect framework are read using `UTF-8` encoding (`utf-8-sig`). This can be customized by adding a comment in the format `# coding=<encoding name>` or `# -*- coding: <encoding name> -*-` as first line in the YAML code. Note that `UTF-16` encoding is not supported.

## Sorting Behavior of Connect Agents
A note on the sorting behavior of Connect agents. All reader and transformer agents do not guarantee a specific order of the created symbol records. However, as the symbol records in the Connect database are saved in _categorical data structures_ , the order in the data source is preserved in _ordered categories_. All writer agents guarantee that symbol records are written in the order of the categories. Here is an example:
```
    $onecho > ijk_in.csv
    i,j,k1,k2
    i1,j2,,3
    i2,j1,4,
    i1,j1,1,2
    i2,j2,5,6
    $offecho

    embeddedCode Connect:
- CSVReader:
        file: ijk_in.csv
        name: ijk
        valueColumns: "3:lastCol"
        indexColumns: [1,2]
- PythonCode:
        code: |
            sym = connect.container["ijk"]
            print("ijk records in the Connect database after reading:\n", sym.records)

            data_sorted = sym.records.sort_values(sym.records.columns[:-1].tolist())
            print("ijk records sorted according to categories:\n", data_sorted)

            sym.reorderUELs(uels=['j1','j2'], dimensions=1)
            data_sorted = sym.records.sort_values(sym.records.columns[:-1].tolist())
            print("ijk records sorted according to reordered categories:\n", data_sorted)
- CSVWriter:
        file: ijk_out.csv
        name: ijk
        unstack: True
    endEmbeddedCode
```

From the data source `ijk_in.csv`, the CSVReader creates the symbol records as shown with the first print:
```
    ijk records in the Connect database after reading:
         i   j level_2  value
    0  i1  j2      k2    3.0
    1  i2  j1      k1    4.0
    2  i1  j1      k1    1.0
    3  i1  j1      k2    2.0
    4  i2  j2      k1    5.0
    5  i2  j2      k2    6.0
```

The ordered categories are inferred from the data source, therefore the order for column `i` is `['i1','i2']`, for column `j` `['j2','j1']` and for column `k` the order of the header `['k1','k2']` is preserved. The categories define the order of the symbol records if sorted:
```
    ijk records sorted according to categories:
         i   j level_2  value
    0  i1  j2      k2    3.0
    2  i1  j1      k1    1.0
    3  i1  j1      k2    2.0
    4  i2  j2      k1    5.0
    5  i2  j2      k2    6.0
    1  i2  j1      k1    4.0
```

If the order is not as desired, `.reorderUELs()` can be used to change the order of the categories, e.g. to `['j1','j2']` for column `j`:
```
    ijk records sorted according to reordered categories:
         i   j level_2  value
    2  i1  j1      k1    1.0
    3  i1  j1      k2    2.0
    0  i1  j2      k2    3.0
    1  i2  j1      k1    4.0
    4  i2  j2      k1    5.0
    5  i2  j2      k2    6.0
```

The CSVWriter automatically sorts the symbol records according to the categories (note that the order of column `j` was changed with the PythonCode agent) and therefore, the content of file `ijk_out.csv` looks as follows:
```
    i,j,k1,k2
    i1,j1,1.0,2.0
    i1,j2,,3.0
    i2,j1,4.0,
    i2,j2,5.0,6.0
```

## Use Connect Agents in Custom Python Code
Instead of passing instructions via one of the Connect interfaces, users can execute them directly in their Python code by creating an instance of `ConnectDatabase` and calling method `.execute(instructions)`. The `instructions` argument is expected to be either a Python dictionary of form:
```
    {
       '<agent name>':
       {
          '<root option1>': <value>,
          '<root option2>': <value>,
          ... ,
          '<root option3>':
          [
             {
                 '<option1>': <value>,
                 '<option2>': <value>,
                 ...
             },
             {
                 '<option1>': <value>,
                 '<option2>': <value>,
                 ...
             },
             ...
          ]
       }
```

or a list of such dictionaries in case multiple Connect agents need to be executed. Users can either construct the Python dictionary themselves or let YAML create the dictionary from a YAML script. The following example creates an instance of `ConnectDatabase` and executes two agents: First, the CSV file `stockprice.csv` is read into the Connect database and second, the symbol `stockprice` is written to the GAMS database. In this example, the agent instructions are directly specified as Python dictionaries.
```
    Set dates, stocks;
    Parameter stockprice(dates<,stocks<);

    $onEcho > stockprice.csv
    date;symbol;price
    2016/01/04;AAPL;105,35
    2016/01/04;AXP;67,59
    2016/01/04;BA;140,50
    $offEcho

    $onEmbeddedCode Python:
    from gams.connect import ConnectDatabase
    cdb = ConnectDatabase(gams._system_directory, ecdb=gams)
    cdb.execute({'CSVReader': {'file': 'stockprice.csv', 'name': 'stockprice', 'indexColumns': [1, 2],
                                'valueColumns': [3], 'fieldSeparator': ';', 'decimalSeparator': ','}})
    cdb.execute({'GAMSWriter': {'symbols': [{'name': 'stockprice'}]}})
    $offEmbeddedCode

    display stockprice;
```

We can also construct the Python dictionaries by using YAML:
```
    Set dates, stocks;
    Parameter stockprice(dates<,stocks<);

    $onEcho > stockprice.csv
    date;symbol;price
    2016/01/04;AAPL;105,35
    2016/01/04;AXP;67,59
    2016/01/04;BA;140,50
    $offEcho

    $onEmbeddedCode Python:
    import yaml
    from gams.connect import ConnectDatabase
    cdb = ConnectDatabase(gams._system_directory, ecdb=gams)

    inst = yaml.safe_load('''
- CSVReader:
        file: stockprice.csv
        name: stockprice
        indexColumns: [1, 2]
        valueColumns: [3]
        fieldSeparator: ';'
        decimalSeparator: ','
- GAMSWriter:
        symbols:
- name: stockprice
    ''')
    cdb.execute(inst)
    $offEmbeddedCode

    display stockprice;
```

Here YAML creates a list of dictionaries (i.e. a list of tasks) from the given YAML script.

---

## 9. T Main

### Table of Contents
* Tools Category
* GAMS Integrated Development Environments
* GAMS Tools Library
* Algorithmic tools (alg)
* Data tools (data)
* GDX Service (gdxservice)
* Linear Algebra (linalg)
* Windows Only Tools (win32)
* Command Line Utility gamstool
* Data Exchange
* Excel
* GDX Service
* LibInclude Tools Library
* Other Tools
* List of Tools
* Supported Platforms

A large number of tools are included in GAMS distribution. Below are a functional categorization of all tools, an alphabetically sorted list of all tools, and a brief description of each tool with their Supported Platforms.

**Note:** Traditionally, GAMS tools consisted of a collection of _executables_ with a file (mostly GDX) interface. These tool executables will be replaced over time by [GAMS Connect](UG_GAMSCONNECT.html) agents and a collection of tools in a new GAMS tools library. For some time both ways will be supported but the executable tools will go away, so when in doubt what tool to pick, select Connect or a GAMS tool.

# Tools Category
All tools included in GAMS distribution are categorized as

## GAMS Integrated Development Environments
There are two integrated model development environments including a general text editor with the ability to launch and monitor the compilation and execution of GAMS models: [GAMS Studio](T_STUDIO.html) and the [GAMS IDE](gamside/contents.htm) (deprecated).

## GAMS Tools Library
In the GAMS Tools Library, various tools are collected to provide an easy access to complex task. The tools in this library complement facilities of [GAMS Connect](UG_GAMSCONNECT.html) and tools available as executables (e.g. [GDXXRW](T_GDXXRW.html)). Currently the library includes the following tool categories:

### Algorithmic tools (alg)
Provide algorithmic functionality like sorting data: [Rank](T_ALG_RANK.html).

### Data tools (data)
Provide access to external data sources: [ExcelDump](T_DATA_EXCELDUMP.html), [CSVRead](T_DATA_CSVREAD.html), [CSVWrite](T_DATA_CSVWRITE.html) and [SqliteWrite](T_DATA_SQLITEWRITE.html).

### GDX Service (gdxservice)
Provide functionality for GDX file manipulation: [GDXEncoding](T_GDXSERVICE_GDXENCODING.html) and [GDXRename](T_GDXSERVICE_GDXRENAME.html).

### Linear Algebra (linalg)
Provide functionality for computational linear algebra: [Cholesky](T_LINALG_CHOLESKY.html), [Eigenvalue](T_LINALG_EIGENVALUE.html), [Eigenvector](T_LINALG_EIGENVECTOR.html), [Invert](T_LINALG_INVERT.html) and [Ordinary Least Squares (OLS)](T_LINALG_OLS.html).

### Windows Only Tools (win32)
Provide functionality specific to the Windows operating system: [ShellExecute](T_WIN32_SHELLEXECUTE.html), [MSAppAvail](T_WIN32_MSAPPAVAIL.html), [ExcelTalk](T_WIN32_EXCELTALK.html) and [ExcelMerge](T_WIN32_EXCELMERGE.html).

There are a couple of things to note:
* A tool can be invoked directly in the model code during compile ([$callTool](UG_DollarControlOptions.html#DOLLARcalltool)) or execution time ([executeTool](UG_GamsCall.html#UG_DollarExecuteTool)) or by using the standalone command line utility gamstool.
* When invoked from the model code the exchange of GAMS symbols is done in memory. If a tool is called from the command line, this is not possible and hence for some tools that deal with GAMS symbols it is necessary to specify GDX input and/or output files. Even for use inside GAMS models the GDX file interface can be useful (e.g. for debugging) hence the specification of GDX input/output files is optional in that case.
* Similar to the [$call](UG_DollarControlOptions.html#DOLLARcall) (compile time) and [execute](UG_GamsCall.html#UG_DollarExecute) (execution time) commands, a GAMS tool returns a shell code that can be checked via `errorLevel`. In case one expects the tools to perform without error, it is recommended to add the suffix [.checkErrorLevel](UG_DollarControlOptions.html#DOLLARcalltoolCEL). This will stop the entire execution of GAMS if an error occurs while executing the tool.
* If a tool of the GAMS Tool library is used at execution time to populate a GAMS symbol with data for the first time, the compiler does not know the outcome of the tool. As a result, the compiler does not have information about any symbols that might be filled with data, and therefore cannot reliably define these symbols at compile time. Code that later on references a corresponding symbol would result in a compilation error 141: `Symbol declared but no values have been assigned`. In order to be able to load symbols implicitly during execution time, the dollar control option [$onImplicitAssign](UG_DollarControlOptions.html#DOLLARonoffimplicitassign) needs to be set. There are other methods to convince the compiler that the symbols has been defined, e.g. `execute_load$0 symName;` which is otherwise a no-op.
* The compile time variant of a tool ([$callTool](UG_DollarControlOptions.html#DOLLARcalltool) [...]) is ignored while [$onExternalInput](UG_DollarControlOptions.html#DOLLARonoffexternalinput) is active and [IDCGDXInput](UG_GamsCall.html#GAMSAOidcgdxinput) is set.
* Tool arguments: All tools follow the same logic to process arguments. The list of arguments starts with a number of _positional_ arguments followed by _named_ argument `[-]name=val`.
* For each tool there is a short and a long help available. If a tool is called without arguments or with `-h` , a short description is displayed, e.g. `gamstool linalg.eigenvector -h`. With the argument `--help` a detailed help text appears: `gamstool linalg.eigenvector --help`. If only the category and not a contained tool is requested, the help text of all included tools will be displayed: `gamstool linalg` or `gamstool linalg --help`.

For more information please refer to the individual tool manuals.

### Command Line Utility gamstool
The GAMS system directory contains the utility `gamstool` to run GAMS Tool instructions directly from the command line. On Windows the utility has the callable extension `.cmd` which does not need to part of the command because the shell automatically checks for the extension. This script wraps the Python script `tooldriver.py` by calling the Python interpreter that ships with GAMS. `gamstool` is called like this:
```
    gamstool [toolCategory.]toolName positionalArguments [namedArguments]
```

## Data Exchange
A collection of tools that provide functionality to exchange data between GAMS and other data sources. This category contains tools for popular data sources and high-level programming environment and like databases ([GDX2ACCESS](T_GDX2ACCESS.html), [SqliteWrite](T_DATA_SQLITEWRITE.html), [MDB2GMS](T_MDB2GMS.html), [SQL2GMS](T_SQL2GMS.html)). There are also tools for specialized systems like [SqliteWrite](T_DATA_SQLITEWRITE.html), [MDB2GMS](T_MDB2GMS.html), and [SQL2GMS](T_SQL2GMS.html). There are also tools for specialized systems like VEDA ([GDX2VEDA](T_GDX2VEDA.html)).

### Excel
A collection of tools that provide functionality to exchange data between GAMS and Excel. The tools in this category are [GDX2XLS](T_GDX2XLS.html), [GDXXRW](T_GDXXRW.html), [XLS2GMS](T_XLS2GMS.html), [ExcelDump](T_DATA_EXCELDUMP.html). Many of the tools described here use the GAMS Data eXchange facility [GAMS Data eXchange (GDX)](UG_GDX.html). Note that the executable tools in this category will be or have been replaced over time by [GAMS Connect](UG_GAMSCONNECT.html) agents and tools from the GAMS Tools Library.

## GDX Service
A collection of tools that operate directly on [GAMS Data eXchange (GDX)](UG_GDX.html) containers to e.g. compare ([GDXDIFF](T_GDXDIFF.html)), copy ([GDXCOPY](T_GDXCOPY.html)), merge ([GDXMERGE](T_GDXMERGE.html)), label rename ([GDXRename](T_GDXSERVICE_GDXRENAME.html)) and encoding ([GDXEncoding](T_GDXSERVICE_GDXENCODING.html)).

## LibInclude Tools Library
In the LibInclude Tools Library, various tools are collected to provide an easy access to complex task. The tools are located in the `inclib` folder in the GAMS system directory and can be invoked using the [$libInclude](UG_GamsCall.html#GAMSAOlibincdir) command.

**Note:** The default [library include directory](UG_DollarControlOptions.html#DOLLARlibinclude) `inclib` can be changed with the [libIncDir](UG_GamsCall.html#GAMSAOlibincdir) command line parameter. Hence, make sure you point to the correct directory when using `$libInclude`.

Usage:
```
    $libInclude <library_file> [<tool_name>] [<option(s)>]
```

Currently the library includes the following tools:

## Other Tools
A collection of more exotic tools that can become handy in some special circumstances. The tools in this category are [ASK](T_ASK.html), [ENDECRYPT](T_ENDECRYPT.html), [FINDTHISGAMS](T_FINDTHISGAMS.html), [GAMS Posix Utilities](T_POSIX.html), [MODEL2TEX](T_MODEL2TEX.html), [MessageReceiverWindow](T_MSGRWIN.html), and all tools from Windows Only Tools (win32). Most notably, the collection contains the tool [MODEL2TEX](T_MODEL2TEX.html) to document the model algebra in LaTeX format.

# List of Tools
The following tables give alphabetically sorted lists of all available tools. The tables are organized into executable tools, GAMS tools and libInclude tools.

Executable Tool | Description
---|---
[ASK](T_ASK.html) | The utility can be used to get input from an user interactively.
[CSV2GDX](T_CSV2GDX.html) | Reads a CSV file (comma separated values) and writes to a GDX file.
[ENDECRYPT](T_ENDECRYPT.html) | A tool to encrypt and decrypt text files.
[FINDTHISGAMS](T_FINDTHISGAMS.html) | Windows command line tool for modifying GAMS specific registry entries created by the GAMS installer.
[GAMS IDE](gamside/contents.htm) | Classic Integrated Development Environment.
[GAMS STUDIO](T_STUDIO.html) | Integrated Development Environment.
[GDX2ACCESS](T_GDX2ACCESS.html) | Converts GDX data to MS Access tables.
[GDX2VEDA](T_GDX2VEDA.html) | Translates a GDX file into the [VEDA](https://support.kanors-emr.org/) format.
[GDX2XLS](T_GDX2XLS.html) | Converts GDX data into a MS Excel spreadsheet.
[GDXCOPY](T_GDXCOPY.html) | Converts a GDX file into different GDX formats.
[GDXDIFF](T_GDXDIFF.html) | Compares the data of symbols with the same name, type and dimension in two GDX files and writes the differences to a third GDX file.
[GDXDUMP](T_GDXDUMP.html) | Writes scalars, sets and parameters (tables) to standard output formatted as a GAMS program with data statements.
[GDXMERGE](T_GDXMERGE.html) | Combines multiple GDX files into one file. Symbols with the same name, dimension and type are combined into a single symbol of a higher dimension. The added dimension has the file name of the combined file as its unique element.
[GDXVIEWER](T_GDXVIEWER.html) | Views and converts data contained in GDX files.
[GDXXRW](T_GDXXRW.html) | Preferred utility to read and write MS Excel spreadsheet data.
GMSUNZIP | Decompression tool [unzip](https://infozip.sourceforge.net/UnZip.html) with [Debian patches](https://packages.debian.org/sid/unzip), but renamed to "gmsunzip".
GMSZIP | Compression and archiving tool [zip](https://infozip.sourceforge.net/Zip.html) with [Debian patches](https://packages.debian.org/sid/zip), but renamed to "gmszip".
[IDECMDS](gamside/idecmds_utility.htm) | Sends commands to the GAMSIDE.
[MDB2GMS](T_MDB2GMS.html) | Converts data from an MS Access database into a GAMS readable format.
[MESSAGE RECEIVER WINDOW](T_MSGRWIN.html) | A graphical tool that receives and displays Windows messages.
[MODEL2TEX](T_MODEL2TEX.html) | Translates a GAMS model into LaTeX
[MPS2GMS](T_MPS2GMS.html) | Translates an MPS or LP file into an equivalent short generic GAMS program using a GDX file to store data.
[POSIX](T_POSIX.html) | A collection of [POSIX](https://en.wikipedia.org/wiki/POSIX) utilities which are usually available for Windows and the different Unix systems and therefore help to write platform independent scripts.
[SQL2GMS](T_SQL2GMS.html) | Converts data from an SQL database into a GAMS readable format.
[XLS2GMS](T_XLS2GMS.html) | Converts spreadsheet data from a MS Excel spreadsheet into a GAMS readable format.
[XLSDUMP](T_XLSDUMP.html) | Writes all worksheets of a MS Excel workbook to a GDX file. Unlike gdxxrw, the program does not require that Excel is installed.
GAMS Tool | Description
---|---
[[ALG.]RANK][5] | Ranks one-dimensional numeric data.
[[DATA.]EXCELDUMP][6] | Writes all worksheets of an Excel workbook to GAMS symbols.
[[DATA.]CSVREAD][7] | Writes data from a CSV file to a GAMS symbol.
[[DATA.]CSVWRITE][8] | Exports a GAMS symbol to a CSV file.
[[DATA.]SQLITEWRITE][9] | Exports GAMS symbols to a SQLite database file.
[[GDXSERVICE.]GDXENCODING][10] | Label encoding conversion.
[[GDXSERVICE.]GDXRENAME][11] | Renames labels in a GDX file.
[[LINALG.]CHOLESKY][12] | Calculates the cholesky decomposition of a symmetric positive definite matrix.
[[LINALG.]EIGENVALUE][13] | Calculates the Eigenvalues of a symmetric positive definite matrix.
[[LINALG.]EIGENVECTOR][14] | Calculates the Eigenvalues and Eigenvectors of a symmetric positive definite matrix.
[[LINALG.]INVERT][15] | Calculates the inverse of a square matrix A.
[[LINALG.]OLS][16] | Ordinary Least Squares: Estimates the unknown parameters in a linear regression model.
[[WIN32.]EXCELMERGE][20] | Merges the sheets of the source Excel workbook into the destination workbook.
[[WIN32.]EXCELTALK][19] | Performs command on an Excel workbook specified by filename.
[[WIN32.]MSAPPAVAIL][18] | Checks if a MS Office Application is available.
[[WIN32.]SHELLEXECUTE][17] | Spawns an external program.
libInclude Tool | Description
---|---
[moo](T_LIBINCLUDE_MOO.html) | Provides methods for multi-objective optimization in GAMS.
[pyEmbMI](T_LIBINCLUDE_PYEMBMI.html) | Provides access to a model instance that can be modified and resolved without regenerating the model over and over.
[rank](T_LIBINCLUDE_RANK.html) | Routine for ranking one-dimensional numeric data. Unlike the GAMS tool alg.rank, rank can handle percentile levels.
[scenred](T_LIBINCLUDE_SCENRED.html) | Tool for the reduction of scenarios and scenario tree construction modeling the random data processes of a stochastic program. From Humboldt-University Berlin.

# Supported Platforms
| x86 64bit
MS Windows | x86 64bit
Linux | arm 64bit
Linux | x86 64bit
macOS | arm 64bit
macOS
---|---|---|---|---|---
[ALG.]RANK |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
ASK |  ✔ * | | |
CSV2GDX |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[DATA.]EXCELDUMP |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[DATA.]CSVREAD |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[DATA.]CSVWRITE |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[DATA.]SQLITEWRITE |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
ENDECRYPT |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
FINDTHISGAMS |  ✔ | | |
GAMSIDE |  ✔ * | | |
GAMSSTUDIO |  ✔ |  ✔ | |  ✔ |  ✔
GDX2ACCESS |  ✔ * | | |
GDX2VEDA |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
GDX2XLS |  ✔ * | | |
GDXCOPY |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
GDXDIFF |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
GDXDUMP |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
GDXMERGE |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[GDXSERVICE.]GDXENCODING |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[GDXSERVICE.]GDXRENAME |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
GDXVIEWER |  ✔ * | | |
GDXXRW |  ✔ * | | |
GMSUNZIP |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
GMSZIP |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
IDECMDS |  ✔ * | | |
[LINALG.]CHOLESKY |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[LINALG.]EIGENVALUE |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[LINALG.]EIGENVECTOR |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[LINALG.]INVERT |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
[LINALG.]OLS |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
MDB2GMS |  ✔ * | | |
moo |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
MSGRWIN |  ✔ | | |
MODEL2TEX |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
MPS2GMS |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
POSIX** |  ✔ * | | |
pyEmbMI |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
rank |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
ScenRed |  ✔ |  ✔ |  ✔ |  ✔ |  ✔
SQL2GMS |  ✔ * | | |
[WIN32.]EXCELMERGE |  ✔ | | |
[WIN32.]EXCELTALK |  ✔ | | |
[WIN32.]MSAPPAVAIL |  ✔ | | |
[WIN32.]SHELLEXECUTE |  ✔ | | |
XLS2GMS |  ✔ * | | |
XLSDUMP |  ✔ * | | |

`*` Note that the tool is 32 bit but runs fine on 64 bit Windows.
`**` awk, cat, cksum, cmp, comm, cp, cut, diff, expr, fold, gdate, grep, gsort, gunzip, gzip, head, join, make, mkdir, mv, od, paste, printf, rm, sed, sleep, tail, tar, tee, test, touch, tr, uniq, wc, xargs

---

## 10. Engine Api

# GAMS Engine - API Description

---

## 11. Class: gams .Control .Database .Gamsdatabase

# gams.control.database.GamsDatabase Class Reference
An instance of GamsDatabase communicates data between the Python world and the GAMS world. More...

## Public Member Functions
---
| **__len__** (self)
| Retrieve the number of symbols in the GamsDatabase.

| **__del__** (self)
| Use this to explicitly free unmanaged resources associated with this GamsDatabase.

| get_symbol (self, symbol_identifier)
| Get GamsSymbol by name.

| get_equation (self, equation_identifier)
| Get GamsEquation by name.

| get_parameter (self, parameter_identifier)
| Get GamsParameter by name.

| get_variable (self, variable_identifier)
| Get GamsVariable by name.

| get_set (self, set_identifier)
| Get GamsSet by name.

| add_equation (self, identifier, dimension, equtype, explanatory_text="")
| Add equation symbol to database.

| add_equation_dc (self, identifier, equtype, domains, explanatory_text="")
| Add equation symbol to database using domain information.

| add_variable (self, identifier, dimension, vartype, explanatory_text="")
| Add variable symbol to database.

| add_variable_dc (self, identifier, vartype, domains, explanatory_text="")
| Add variable symbol to database using domain information.

| add_set (self, identifier, dimension, explanatory_text="", settype=0)
| Add set symbol to database.

| add_set_dc (self, identifier, domains, explanatory_text="", settype=0)
| Add set symbol to database using domain information.

| add_parameter (self, identifier, dimension, explanatory_text="")
| Add parameter symbol to database.

| add_parameter_dc (self, identifier, domains, explanatory_text="")
| Add parameter symbol to database using domain information.

| export (self, file_path=None)
| Write database into a GDX file.

| **clear** (self)
| Clear all symbols in GamsDatabase.

| compact (self)
| This function is obsolete and has no effect anymore.

| check_domains (self)
| Check for all symbols if all records are within the specified domain of the symbol.

| get_database_dvs (self, max_viol=0, max_viol_per_symbol=0)
| return all GamsDatabaseDomainViolations

## Properties
---
| number_symbols = property(get_nr_symbols)
| Retrieve the number of symbols in the GamsDatabase.

| **workspace** = property(get_workspace)
| Get GamsWorkspace containing GamsDatabase.

| **name** = property(get_name)
| Get GamsDatabase name.

| **suppress_auto_domain_checking**
| Controls whether domain checking is called in GamsDatabase export.

## Detailed Description
An instance of GamsDatabase communicates data between the Python world and the GAMS world.

A GamsDatabase consists of a collection of symbols (GamsDatabase implements __iter__() and next() to allow iterating conveniently through the symbols in a GamsDatabase). The symbol types available for a GamsDatabase correspond to the symbol types known from the GAMS language: Set, Parameter, Variable, and Equation are represented in Python by a derived class (e.g. GamsSet, GamsParameter, etc). Besides the type, a GamsSymbol has a name (this has to match the name inside the GAMS model), a dimension (currently up to 20 or GMS_MAX_INDEX_DIM) and some explanatory text.

Variables and equations also have a subtype: e.g. VarType.Binary, VarType.Positive, etc. for variables and e.g. EquType.E, EquType.G etc. for equations

GamsDatabases can be created empty, or initialized from existing GDX files or from another GamsDatabase (copy). Symbols can be added at any time (e.g. GamsDatabase.add_parameter), but once a symbol is part of a GamsDatabase, it cannot be removed. Only its associated data (GamsSymbolRecord) can be purged (see GamsSymbol.clear()) or individually removed (GamsSymbol.delete_record). Individual data elements are accessed record by record. A record is identified by the keys (a vector of strings). The record data varies by symbol type. For example, a parameter record has a value property, a variable has the properties level, lower, upper, marginal, and scale. Adding a record with keys that already exist results in an exception. Similar, the unsuccessful search for a record also results in an exception.

GamsSymbol implements __iter__() and next() to conveniently iterate through the records of a symbol. There are also sliced access methods to symbol records that allow to iterate through all records with a fixed index at some positions. GamsDatabases can be exported as GDX files for permanent storage.

GamsJob.out_db and GamsModelInstance.sync_db provide instances of GamsDatabase to communicate results from a GAMS run or a solve. These databases should only be used in the context of the base object (GamsJob or GamsModelInstance). If a copy of such a database is required GamsWorkspace.add_database can be used to initialize a GamsDatabase from another database by specifying the optional parameter source_database (e.g. newdb = workspace.add_database(GamsJob.out_db)).

GamsDatabases often provide the input data for a GamsJob. Such GamsDatabases are listed in the GamsJob.run method. Inside the GAMS model source the GamsDatabase is accessible through a GDX file. The GAMS model source requires a particular file name to connect to the proper GDX file (e.g. $GDXIN filename). A GamsDatabase can be created with a given name which can be then used inside the model (e.g. db = workspace.add_database(database_name="SupplyData")) and then inside the GAMS model source: $GDXIN SupplyData) or an automatically generated name can be used. This name can be passed down to the GAMS model by using the defines dictionary of a GamsOptions instance:

db = workspace.add_database()

opt = workspace.add_options()

opt.defines["SupplyDataFileName"] = db.name

...

gamsjob.run(gams_options=opt, databases=db)

Inside the GAMS model source the name is accessed as follows:

$GDXIN %SupplyDataFileName%

One has to act with some caution when it comes to ordered sets which e.g. allow lag and lead. By not enforcing the "domain checking" for the GamsDatabase class we have aggravated the potential problems for ordered sets. For GAMS, the labels of set elements are just strings, so the order of a set is determined by the appearance of its elements. For example, if one has 'set k / 2,3,4,1,5 /', the order of k is exactly given by this sequence. So the lag (k-1) of k=4 is 3 and the lead (k+1) of k=4 is 1.

GAMS performs arithmetic with an extended number range. GAMS has special values for infinity (+INF, -INF), epsilon (EPS), not available (NA), and undefined (UNDEF). When GAMS evaluates expressions with these special values, the calculating engine ensures the correctness of the result (e.g. 5*eps=eps or 5+eps=5). The GAMS model CRAZY in the GAMS Model Library documents the results of the arithmetic operations with respect to special values.

In the GAMS Python API we map the IEEE standard values for +/-infinity (float('inf')/float('-inf')) and NA (float('nan')) to the corresponding GAMS values. The special value for UNDEF gets unfiltered through the GAMS Python API. The internal double value of UNDEF is 1.0E300 (or better use the constant SV_UNDEF).

Special attention needs to be given to the value of 0. Since GAMS is a sparse system it does not store (parameter) records with a true 0. If a record with numerical value of 0 is needed, EPS(SV_EPS) can help. For example:

set j /1*10 /; parameter b(j); b(j) = 1; b('5') = 0;

scalar s,c; s = sum(j, b(j)); c = card(b); display s,c;

will result in

\---- 3 PARAMETER s = 9.000

PARAMETER c = 9.000

but

b(j) = 1; b('5') = EPS;

will result in

\---- 3 PARAMETER s = 9.000

PARAMETER c = 10.000

What are the consequences for the GAMS Python API? If we read parameter b in case of b('5')=0, the GAMSDatabase will not have a record for b('5'). In case of b('5')=EPS, the GamsDatabase will have a record with value EPS. Unlike the IEEE values (e.g. float("inf")), arithmetic operations in Python will modify EPS (e.g. 5*float("inf")==float("inf") but 5*EPS!=EPS). The same rules apply for preparing input data for GAMS in a GamsDatabase. If a value of EPS is written, GAMS will see the special value EPS. All other small values (including 0) will be communicated unfiltered to GAMS. As mentioned before, zeros will not be entered as data records in GAMS. The compiler control $on/offEPS can help to automatically map zeros to EPS.

There is one oddity concerning values smaller than 1e-250 on GAMS input. Consider the following example:

b = db.add_parameter("b",1)

for i in range(1,11):

b.add_record(str(i)).value = 1

b.find_record("5").value = 1E-251

job.run(db)

$load j b

scalar card_b; card_b = card(b); display card_b;

b(j) = 2*b(j); card_b = card(b); display card_b;

A record with values smaller than 1e-250 exists on input in GAMS, but as soon as the record gets updated by GAMS and is still smaller than 1e-250, the record gets removed.

The ordering of a set in GAMS can be non-intuitive: Consider "set i /5/, j /1*5/;". Elements '5' gets internal number 1, '1' get 2, '2' gets 3 and so on. The last element of j '5' has already the internal number 1. The sequence of internal numbers in j is not ascending and hence GAMS considers set j as not sorted, i.e. one can't use the ord() function nor the lag or lead (-,–,+,++) operators. If 'j' would have been defined before 'i' in this example, the "set not ordered" problem would have been avoided.

Please note that the GamsDatabase actually does not implement a relational model for database management. It should be seen as a data storage or data container.

## Member Function Documentation
## ◆ add_equation()
gams.control.database.GamsDatabase.add_equation  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _dimension_ ,
| | _equtype_ ,
| | _explanatory_text_ = "" )

Add equation symbol to database.

Parameters
     identifier| Equation name
---|---
dimension| Equation dimension
equtype| Equation subtype (EquType.E: Equal, EquType.G: Greater, EquType.L: Less, EquType.N: No specification, EquType.X: External defined, EquType.C: Conic)
explanatory_text| Explanatory text of equation

Returns
    Instance of GamsEquation

See also
    add_parameter(), add_set(), add_variable()

## ◆ add_equation_dc()
gams.control.database.GamsDatabase.add_equation_dc  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _equtype_ ,
| | _domains_ ,
| | _explanatory_text_ = "" )

Add equation symbol to database using domain information.

Parameters
     identifier| Equation name
---|---
equtype| Equation subtype (EquType.E: Equal, EquType.G: Greater, EquType.L: Less, EquType.N: No specification, EquType.X: External defined, EquType.C: Conic)
domains| A list containing GamsSet objects and strings for domain information. The length of the list specifies the dimension.
explanatory_text| Explanatory text of equation

Returns
    Instance of GamsEquation

See also
    add_parameter_dc(), add_set_dc(), add_variable_dc()

## ◆ add_parameter()
gams.control.database.GamsDatabase.add_parameter  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _dimension_ ,
| | _explanatory_text_ = "" )

Add parameter symbol to database.

Parameters
     identifier| Parameter name
---|---
dimension| Parameter dimension
explanatory_text| Explanatory text of parameter

Returns
    Instance of GamsParameter

See also
    add_equation(), add_set(), add_variable()

## ◆ add_parameter_dc()
gams.control.database.GamsDatabase.add_parameter_dc  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _domains_ ,
| | _explanatory_text_ = "" )

Add parameter symbol to database using domain information.

Parameters
     identifier| Parameter name
---|---
domains| A list containing GamsSet objects and strings for domain information. The length of the list specifies the dimension.
explanatory_text| Explanatory text of parameter

Returns
    Instance of GamsParameter

See also
    add_equation_dc(), add_set_dc(), add_variable_dc()

## ◆ add_set()
gams.control.database.GamsDatabase.add_set  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _dimension_ ,
| | _explanatory_text_ = "",
| | _settype_ = 0 )

Add set symbol to database.

Parameters
     identifier| Set name
---|---
dimension| Set dimension
explanatory_text| Explanatory text of set
settype| Set subtype (SetType.Multi, SetType.Singleton)

Returns
    Instance of GamsSet

See also
    add_equation(), add_parameter(), add_variable()

## ◆ add_set_dc()
gams.control.database.GamsDatabase.add_set_dc  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _domains_ ,
| | _explanatory_text_ = "",
| | _settype_ = 0 )

Add set symbol to database using domain information.

Parameters
     identifier| Set name
---|---
domains| A list containing GamsSet objects and strings for domain information. The length of the list specifies the dimension.
explanatory_text| Explanatory text of set
settype| Set subtype (SetType.Multi, SetType.Singleton)

Returns
    Instance of GamsSet

See also
    add_equation_dc(), add_parameter_dc(), add_variable_dc()

## ◆ add_variable()
gams.control.database.GamsDatabase.add_variable  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _dimension_ ,
| | _vartype_ ,
| | _explanatory_text_ = "" )

Add variable symbol to database.

Parameters
     identifier| Variable name
---|---
dimension| Variable dimension
vartype| Variable subtype (VarType.Binary, VarType.Integer, VarType.Positive, VarType.Negative, VarType.Free, VarType.SOS1, VarType.SOS2, VarType.SemiCont, VarType.SemiInt)
explanatory_text| Explanatory text to variable

Returns
    Instance of GamsVariable

See also
    add_equation(), add_parameter(), add_set()

## ◆ add_variable_dc()
gams.control.database.GamsDatabase.add_variable_dc  | ( |  | _self_ ,
---|---|---|---| | _identifier_ ,
| | _vartype_ ,
| | _domains_ ,
| | _explanatory_text_ = "" )

Add variable symbol to database using domain information.

Parameters
     identifier| Variable name
---|---
vartype| Variable subtype (VarType.Binary, VarType.Integer, VarType.Positive, VarType.Negative, VarType.Free, VarType.SOS1, VarType.SOS2, VarType.SemiCont, VarType.SemiInt)
domains| A list containing GamsSet objects and strings for domain information. The length of the list specifies the dimension.
explanatory_text| Explanatory text to variable

Returns
    Instance of GamsVariable

See also
    add_equation_dc(), add_parameter_dc(), add_set_dc()

## ◆ check_domains()
gams.control.database.GamsDatabase.check_domains  | ( |  | _self_| ) |---|---|---|---|---|---

Check for all symbols if all records are within the specified domain of the symbol.

Returns
    True: Everything is correct, False: There is a domain violation

## ◆ compact()
gams.control.database.GamsDatabase.compact  | ( |  | _self_| ) |---|---|---|---|---|---

This function is obsolete and has no effect anymore.

It will be removed in the future

## ◆ export()
gams.control.database.GamsDatabase.export  | ( |  | _self_ ,
---|---|---|---| | _file_path_ = None )

Write database into a GDX file.

Parameters
     file_path| The path used to write the GDX file. A relative path is relative to the GAMS working directory. If not present, the file is written to the working directory using the name of the database.
---|---

## ◆ get_database_dvs()
gams.control.database.GamsDatabase.get_database_dvs  | ( |  | _self_ ,
---|---|---|---| | _max_viol_ = 0,
| | _max_viol_per_symbol_ = 0 )

return all GamsDatabaseDomainViolations

Parameters
     max_viol| The maximum number of domain violations which should be stored (0 for no limit)
---|---
max_viol_per_symbol| The maximum number of domain violations which should be stored per Symbol (0 for no limit)

Returns
    List containing GamsDatabaseDomainViolation objects

## ◆ get_equation()
gams.control.database.GamsDatabase.get_equation  | ( |  | _self_ ,
---|---|---|---| | _equation_identifier_ )

Get GamsEquation by name.

Parameters
     equation_identifier| Name of the equation to retrieve
---|---

Returns
    Instance of GamsEquation

See also
    get_symbol(), get_parameter(), get_set(), get_variable()

## ◆ get_parameter()
gams.control.database.GamsDatabase.get_parameter  | ( |  | _self_ ,
---|---|---|---| | _parameter_identifier_ )

Get GamsParameter by name.

Parameters
     parameter_identifier| Name of the parameter to retrieve
---|---

Returns
    Instance of GamsParameter

See also
    get_symbol(), get_set(), get_variable(), get_equation()

## ◆ get_set()
gams.control.database.GamsDatabase.get_set  | ( |  | _self_ ,
---|---|---|---| | _set_identifier_ )

Get GamsSet by name.

Parameters
     set_identifier| Name of the set to retrieve
---|---

Returns
    Instance of GamsSet

See also
    get_symbol(), get_parameter(), get_variable(), get_equation()

## ◆ get_symbol()
gams.control.database.GamsDatabase.get_symbol  | ( |  | _self_ ,
---|---|---|---| | _symbol_identifier_ )

Get GamsSymbol by name.

symbol = database.get_symbol("a")

if isinstance(symbol, GamsParameter):

print("symbol is a GamsParameter")

if isinstance(symbol, GamsSet):

print("symbol is a GamsSet")

if isinstance(symbol, GamsVariable):

print("symbol is a GamsVariable")

if isinstance(symbol, GamsEquation):

print("symbol is a GamsEquation")

Parameters
     symbol_identifier| Name of the symbol to retrieve
---|---

Returns
    Instance of _GamsSymbol

See also
    get_parameter(), get_set(). get_variable(), get_equation()

## ◆ get_variable()
gams.control.database.GamsDatabase.get_variable  | ( |  | _self_ ,
---|---|---|---| | _variable_identifier_ )

Get GamsVariable by name.

Parameters
     variable_identifier| Name of the variable to retrieve
---|---

Returns
    Instance of GamsVariable

See also
    get_symbol(), get_parameter(), get_set(), get_equation()

## Property Documentation
## ◆ number_symbols
| gams.control.database.GamsDatabase.number_symbols = property(get_nr_symbols)
---
static

Retrieve the number of symbols in the GamsDatabase.

**Note:** This is the same as calling len(database)

---

## 12. Class: gams .Control .Database .Gamsdatabase Members

# gams.control.database.GamsDatabase Member List
This is the complete list of members for [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html), including all inherited members.

[__del__](classgams_1_1control_1_1database_1_1GamsDatabase.html#a3963bfb494140ac016e615702b9bde6a)(self)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|---|---|---
[__len__](classgams_1_1control_1_1database_1_1GamsDatabase.html#a2e8556e200e928660cd64c9876b3ee55)(self)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_equation](classgams_1_1control_1_1database_1_1GamsDatabase.html#ad7d2dd678753a1fcc1824b156f0e8d3f)(self, identifier, dimension, equtype, explanatory_text="")| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_equation_dc](classgams_1_1control_1_1database_1_1GamsDatabase.html#aa8f5d2a7eebbb2ae436d4f651872ae6a)(self, identifier, equtype, domains, explanatory_text="")| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_parameter](classgams_1_1control_1_1database_1_1GamsDatabase.html#a37244024a3ed21555880735ea0ca0c45)(self, identifier, dimension, explanatory_text="")| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_parameter_dc](classgams_1_1control_1_1database_1_1GamsDatabase.html#a28c59d60ec918ecdd88b759dfbe3b751)(self, identifier, domains, explanatory_text="")| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_set](classgams_1_1control_1_1database_1_1GamsDatabase.html#a53b7298db36f204506a344406fc7e1eb)(self, identifier, dimension, explanatory_text="", settype=0)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_set_dc](classgams_1_1control_1_1database_1_1GamsDatabase.html#acf7b7de993225504a59f044dd43ac2f8)(self, identifier, domains, explanatory_text="", settype=0)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_variable](classgams_1_1control_1_1database_1_1GamsDatabase.html#ac4f34461197df19eff6345962a309770)(self, identifier, dimension, vartype, explanatory_text="")| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[add_variable_dc](classgams_1_1control_1_1database_1_1GamsDatabase.html#abecd2d128fcfa20931850b413b0e468c)(self, identifier, vartype, domains, explanatory_text="")| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[check_domains](classgams_1_1control_1_1database_1_1GamsDatabase.html#aa176ab5b5a8fb6f8adb640fb90f42afb)(self)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[clear](classgams_1_1control_1_1database_1_1GamsDatabase.html#af11fc27327f7b836d563869c6a870200)(self)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[compact](classgams_1_1control_1_1database_1_1GamsDatabase.html#a10a7370a31ad73a20e82994e08431bad)(self)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[export](classgams_1_1control_1_1database_1_1GamsDatabase.html#adcdc0b7362d02c2586e04c110eacc2b8)(self, file_path=None)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[get_database_dvs](classgams_1_1control_1_1database_1_1GamsDatabase.html#abaf2e77e90bc34a41f92b0a6d237828c)(self, max_viol=0, max_viol_per_symbol=0)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[get_equation](classgams_1_1control_1_1database_1_1GamsDatabase.html#ad893fb8cff0ce5de3ef3649c56fe2342)(self, equation_identifier)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[get_parameter](classgams_1_1control_1_1database_1_1GamsDatabase.html#a7dd5d3783422e012d67d0f193904eb24)(self, parameter_identifier)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[get_set](classgams_1_1control_1_1database_1_1GamsDatabase.html#ac499d5fcac04509ada3c49234a35acd7)(self, set_identifier)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[get_symbol](classgams_1_1control_1_1database_1_1GamsDatabase.html#af9b44e4499122d120b91c1032b62b46e)(self, symbol_identifier)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[get_variable](classgams_1_1control_1_1database_1_1GamsDatabase.html#a0b269fc631d462fc5a87409c983c3358)(self, variable_identifier)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)|
[name](classgams_1_1control_1_1database_1_1GamsDatabase.html#a4d0877abfa4a9c0e7e90de44f13c5084)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)| static
[number_symbols](classgams_1_1control_1_1database_1_1GamsDatabase.html#a1b85503a557921ab07979f33391a3c21)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)| static
[suppress_auto_domain_checking](classgams_1_1control_1_1database_1_1GamsDatabase.html#a316943628a80de2625b78c94dc44967e)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)| static
[workspace](classgams_1_1control_1_1database_1_1GamsDatabase.html#a599428e32d7731198609229e04df7edd)| [gams.control.database.GamsDatabase](classgams_1_1control_1_1database_1_1GamsDatabase.html)| static

---

## 13. Class: gams .Control .Database . Gamssymbol

# gams.control.database._GamsSymbol Class Reference
This is the representation of a symbol in GAMS. More...

Inheritance diagram for gams.control.database._GamsSymbol:

## Public Member Functions
---
| **__len__** (self)
| Retrieve the number of records of the GamsSymbol.

| copy_symbol (self, target)
| Copys all records from the GamsSymbol to the target GamsSymbol (if target had records, they will be deleted)

| delete_record (self, keys=None)
| Delete GamsSymbol record.

| clear (self)
| Clear symbol.

| find_record (self, keys=None)
| Find record in GamsSymbol.

| add_record (self, keys=None)
| Add record to GamsSymbol.

| merge_record (self, keys=None)
| Finds record in GamsSymbol if it exists, adds it if not.

| first_record (self, slice=None)
| Retrieve first record in GamsSymbol.

| check_domains (self)
| Check if all records are within the specified domain of the symbol.

| get_symbol_dvs (self, max_viol=0)
| return all GamsSymbolDomainViolations

## Properties
---
| **domains** = property(get_domains)
| Domains of Symbol, each element is either a GamsSet (real domain) or a string (relaxed domain)

| domains_as_strings = property(get_domains_as_strings)
| Domains of Symbol, each element is a string.

| **dimension** = property(get_dimension)
| Get GamsSymbol dimension.

| **text** = property(get_text)
| Get explanatory text of GamsSymbol.

| **name** = property(get_name)
| Get GamsSymbol name.

| **database** = property(get_database)
| Get GamsDatabase containing GamsSymbol.

| number_records = property(get_number_records)
| Retrieve the number of records of the GamsSymbol.

## Detailed Description
This is the representation of a symbol in GAMS.

It exists in a GamsDatabase and contains GamsSymbolRecords which one can iterate through. Derived classes are GamsEquation, GamsParameter, GamsSet and GamsVariable.

## Member Function Documentation
## ◆ add_record()
gams.control.database._GamsSymbol.add_record  | ( |  | _self_ ,
---|---|---|---| | _keys_ = None )

Add record to GamsSymbol.

Parameters
     keys| List of keys
---|---

Returns
    Reference to added record

## ◆ check_domains()
gams.control.database._GamsSymbol.check_domains  | ( |  | _self_| ) |---|---|---|---|---|---

Check if all records are within the specified domain of the symbol.

Returns
    True: Everything is correct, False: There is a domain violation

## ◆ clear()
gams.control.database._GamsSymbol.clear  | ( |  | _self_| ) |---|---|---|---|---|---

Clear symbol.

Returns
    True if everything worked, else False

## ◆ copy_symbol()
gams.control.database._GamsSymbol.copy_symbol  | ( |  | _self_ ,
---|---|---|---| | _target_ )

Copys all records from the GamsSymbol to the target GamsSymbol (if target had records, they will be deleted)

Parameters
     target| Target GamsSymbol
---|---

Returns
    True if everything worked, else false

## ◆ delete_record()
gams.control.database._GamsSymbol.delete_record  | ( |  | _self_ ,
---|---|---|---| | _keys_ = None )

Delete GamsSymbol record.

Parameters
     keys| List of keys
---|---

Returns
    True if everything worked, else False

## ◆ find_record()
gams.control.database._GamsSymbol.find_record  | ( |  | _self_ ,
---|---|---|---| | _keys_ = None )

Find record in GamsSymbol.

Parameters
     keys| List of keys
---|---

Returns
    Reference to found record

## ◆ first_record()
gams.control.database._GamsSymbol.first_record  | ( |  | _self_ ,
---|---|---|---| | _slice_ = None )

Retrieve first record in GamsSymbol.

Parameters
     slice| Define filter for elements whose record should be retrieved print("Transportation costs from Seattle") record = job.out_db.get_parameter("c").first_record(["seattle", " "])
---|---

Returns
    Reference to record

## ◆ get_symbol_dvs()
gams.control.database._GamsSymbol.get_symbol_dvs  | ( |  | _self_ ,
---|---|---|---| | _max_viol_ = 0 )

return all GamsSymbolDomainViolations

Parameters
     max_viol| The maximum number of domain violations which should be stored (0 for no limit)
---|---

Returns
    List containing GamsSymbolDomainViolation objects

## ◆ merge_record()
gams.control.database._GamsSymbol.merge_record  | ( |  | _self_ ,
---|---|---|---| | _keys_ = None )

Finds record in GamsSymbol if it exists, adds it if not.

Parameters
     keys| List of keys
---|---

Returns
    Reference to found or added record

## Property Documentation
## ◆ domains_as_strings
| gams.control.database._GamsSymbol.domains_as_strings = property(get_domains_as_strings)
---
static

Domains of Symbol, each element is a string.

Note: If the domains is as alias in GAMS, this call will return the name of the alias, not the name of the aliased set

## ◆ number_records
| gams.control.database._GamsSymbol.number_records = property(get_number_records)
---
static

Retrieve the number of records of the GamsSymbol.

**Note:** This is the same as calling len(symbol)

---

## 14. Class: gams .Control .Database . Gamssymbol Members

# gams.control.database._GamsSymbol Member List
This is the complete list of members for [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html), including all inherited members.

[__len__](classgams_1_1control_1_1database_1_1__GamsSymbol.html#ac57dd54396a23345ea3a26f8529b6b1a)(self)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|---|---|---
[add_record](classgams_1_1control_1_1database_1_1__GamsSymbol.html#ae3c490364b7a25cc5bae5d24dbfd208f)(self, keys=None)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[check_domains](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a673aa0363fb2a79aed5e12ee01c8f68f)(self)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[clear](classgams_1_1control_1_1database_1_1__GamsSymbol.html#ae0ac776c383abdd58530c785d510eb66)(self)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[copy_symbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a694d64e9520cde71da5be2edb1069f20)(self, target)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[database](classgams_1_1control_1_1database_1_1__GamsSymbol.html#aff09d94f3e2199dfe09e9ad3381fdaf7)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static
[delete_record](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a1b8f5314a94d1138b96bde374c6b9665)(self, keys=None)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[dimension](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a2b482858acb047629a97dc742694ad98)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static
[domains](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a3a6ee0bb5a72cf2b1228478ff6603e71)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static
[domains_as_strings](classgams_1_1control_1_1database_1_1__GamsSymbol.html#aeb3e2805b290bef891bb5c94d7189e23)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static
[find_record](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a11262450c8f8abe946e5834b7b0210ae)(self, keys=None)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[first_record](classgams_1_1control_1_1database_1_1__GamsSymbol.html#aaceaeca45e8d6a3b17700bd25a5a926f)(self, slice=None)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[get_symbol_dvs](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a5e4e71ba4cc13a38bac1f80739c11c87)(self, max_viol=0)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[merge_record](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a235a4a1e0e02283d4fe40a2782d412ea)(self, keys=None)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)|
[name](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a2aeffb0534b2efd5254ea76473a946b8)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static
[number_records](classgams_1_1control_1_1database_1_1__GamsSymbol.html#aded7c02dbc211e4f93d6719a8dd0b5a3)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static
[text](classgams_1_1control_1_1database_1_1__GamsSymbol.html#a13e7b950a92b5a377a36a8f3b594ef84)| [gams.control.database._GamsSymbol](classgams_1_1control_1_1database_1_1__GamsSymbol.html)| static

---

## 15. Class: gams .Control .Execution .Gamsjob

# gams.control.execution.GamsJob Class Reference
The GamsJob class manages the execution of a GAMS program given by GAMS model source. More...

## Public Member Functions
---
| __init__ (self, ws, file_name=None, source=None, checkpoint=None, job_name=None)
| Constructor.

| run (self, gams_options=None, checkpoint=None, output=None, create_out_db=True, databases=None)
| Run GamsJob.

| run_engine (self, engine_configuration, extra_model_files=None, engine_options=None, gams_options=None, checkpoint=None, output=None, create_out_db=True, databases=None, remove_results=True)
| Run GamsJob on GAMS Engine.

| interrupt (self)
| Send Interrupt to running Job.

## Properties
---
| **name** = property(get_job_name)
| Retrieve name of GamsJob.

| **workspace** = property(get_workspace)
| Get GamsWorkspace containing GamsJob.

| **out_db** = property(get_out_db)
| Get GamsDatabase created by run method.

## Detailed Description
The GamsJob class manages the execution of a GAMS program given by GAMS model source.

The GAMS source (or more precisely the root of a model source tree) of the job can be provided as a string or by a filename (relative to the working directory of the GamsWorkspace) of a text file containing the GAMS model source. The run method organizes the export of the input GamsDatabases, calls the GAMS compiler and execution system with the supplied options and on successful completion provides through the property out_db (of type GamsDatabase) the results of the model run.

While the result data is captured in a GamsDatabase, the run method can also create a GamsCheckpoint that not only captures data but represents the state of the entire GamsJob and allows some other GamsJob to continue from this state. In case of a compilation or execution error, the run method will throw an exception. If the log output of GAMS is of interest, this can be captured by providing the output parameter of the run method (e.g. sys.stdout).

## Constructor & Destructor Documentation
## ◆ __init__()
gams.control.execution.GamsJob.__init__  | ( |  | _self_ ,
---|---|---|---| | _ws_ ,
| | _file_name_ = None,
| | _source_ = None,
| | _checkpoint_ = None,
| | _job_name_ = None )

Constructor.

**Note:** It is not allowed to specify both file_name and source at the same time.

Parameters
     ws| GamsWorkspace containing GamsJob
---|---
file_name| GAMS source file name
source| GAMS model as string
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

## Member Function Documentation
## ◆ interrupt()
gams.control.execution.GamsJob.interrupt  | ( |  | _self_| ) |---|---|---|---|---|---

Send Interrupt to running Job.

Note: On Mac OS this call requires the tool pstree to be installed

Returns
    False if no process available, True otherwise

## ◆ run()
gams.control.execution.GamsJob.run  | ( |  | _self_ ,
---|---|---|---| | _gams_options_ = None,
| | _checkpoint_ = None,
| | _output_ = None,
| | _create_out_db_ = True,
| | _databases_ = None )

Run GamsJob.

Parameters
     gams_options| GAMS options to control job
---|---
checkpoint| GamsCheckpoint to be created by GamsJob
output| Stream to capture GAMS log (e.g. sys.stdout or an object created by the build-in function open())
create_out_db| Flag to define if out_db should be created
databases| Either a GamsDatabase or a list of GamsDatabases to be read by the GamsJob

## ◆ run_engine()
gams.control.execution.GamsJob.run_engine  | ( |  | _self_ ,
---|---|---|---| | _engine_configuration_ ,
| | _extra_model_files_ = None,
| | _engine_options_ = None,
| | _gams_options_ = None,
| | _checkpoint_ = None,
| | _output_ = None,
| | _create_out_db_ = True,
| | _databases_ = None,
| | _remove_results_ = True )

Run GamsJob on GAMS Engine.

Parameters
     engine_configuration| GamsEngineConfiguration object
---|---
extra_model_files| List of additional file paths (apart from main file) required to run the model (e.g. include files)
engine_options| Dictionary of GAMS Engine options to control job execution
gams_options| GAMS options to control job
checkpoint| GamsCheckpoint to be created by GamsJob
output| Stream to capture GAMS log (e.g. sys.stdout or an object created by the build-in function open())
create_out_db| Flag to define if out_db should be created
databases| Either a GamsDatabase or a list of GamsDatabases to be read by the GamsJob
remove_results| Remove results from GAMS Engine after downloading them

---

## 16. Class: gams .Control .Execution .Gamsjob Members

# gams.control.execution.GamsJob Member List
This is the complete list of members for [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html), including all inherited members.

[__init__](classgams_1_1control_1_1execution_1_1GamsJob.html#ad25017442acc882e3967dc95cf5c4a63)(self, ws, file_name=None, source=None, checkpoint=None, job_name=None)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)|---|---|---
[interrupt](classgams_1_1control_1_1execution_1_1GamsJob.html#a69832a58bfdcde3b83b245bb5494f248)(self)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)|
[name](classgams_1_1control_1_1execution_1_1GamsJob.html#aca5dd4b16d9daeba1b05330e6c0e2949)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)| static
[out_db](classgams_1_1control_1_1execution_1_1GamsJob.html#a3a360ae41bf395aa7ca89e871a4edf9a)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)| static
[run](classgams_1_1control_1_1execution_1_1GamsJob.html#a26e7218bd345dc9198dd4d400b248f50)(self, gams_options=None, checkpoint=None, output=None, create_out_db=True, databases=None)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)|
[run_engine](classgams_1_1control_1_1execution_1_1GamsJob.html#a3513a1aa14ae9f6966ab6d9d11cbfb20)(self, engine_configuration, extra_model_files=None, engine_options=None, gams_options=None, checkpoint=None, output=None, create_out_db=True, databases=None, remove_results=True)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)|
[workspace](classgams_1_1control_1_1execution_1_1GamsJob.html#a85482a4c5218a0a88dd1930710ede28f)| [gams.control.execution.GamsJob](classgams_1_1control_1_1execution_1_1GamsJob.html)| static

---

## 17. Class: gams .Control .Execution .Gamsmodelinstance

## Public Member Functions
---
| __init__ (self, checkpoint=None, modelinstance_name=None, source=None)
| Constructor.

| copy_modelinstance (self, modelinstance_name=None)
| Copies this ModelInstance to a new ModelInstance.

| **__del__** (self)
| Use this to explicitly free unmanaged resources.

| cleanup (self)
| Explicitly closes the license session when using a license that limits the actual uses of GAMS.

| instantiate (self, model_definition, modifiers=[], options=None)
| Instantiate the GamsModelInstance.

| solve (self, update_type=[SymbolUpdateType.BaseCase](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html#a85e370641ac5254006b94b3f9ba6b183), output=None, mi_opt=None)
| Solve model instance.

| **interrupt** (self)
| Send interrupt signal to running GamsModelInstance.

## Properties
---
| model_status = property(get_model_status)
| Status of the model.

| solver_status = property(get_solver_status)
| Solve status of the model.

| **checkpoint** = property(get_checkpoint)
| Retrieve GamsCheckpoint.

| **name** = property(get_name)
| Retrieve name of GamsModelInstance.

| **sync_db** = property(get_sync_db)
| Retrieve GamsDatabase used to synchronize modifiable data.

## Detailed Description
The GamsJob class is the standard way of dealing with a GAMS model and the corresponding solution provided by a solver. The GAMS language provides programming flow that allows to solve models in a loop and do other sophisticated tasks, like building decomposition algorithms.

In rare cases, the GAMS model generation time dominates the solver solution time and GAMS itself becomes the bottleneck in an optimization application. For a model instance which is a single mathematical model generated by a GAMS solve statement, the GamsModelInstance class provides a controlled way of modifying a model instance and solving the resulting problem in the most efficient way, by communicating only the changes of the model to the solver and doing a hot start (in case of a continuous model like LP) without the use of disk IO.

The GamsModelInstance requires a GamsCheckpoint that contains the model definition. Significant parts of the GAMS solve need to be provided for the instantiation of the GamsModelInstance. The modification of the model instance is done through data in sync_db (a property of GamsModelInstance of type GamsDatabase). One needs to create GamsModifiers which contain the information on how to modify the GamsModelInstance. Such a GamsModifier consists either of a GamsParameter or of a triple with the GamsVariable or GamsEquation to be updated, the modification action (e.g. Upper, Lower or Fixed for updating bounds of a variable, or Primal/Dual for updating the level/marginal of a variable or equation mainly used for starting non-linear models from different starting points), and a GamsParameter that holds the data for modification. GamsSymbols of a GamsModifier must belong to sync_db. The list of GamsModifiers needs to be supplied on the instantiate call. The use of GamsParameters that are GamsModifiers is restricted in the GAMS model source. For example, the parameter cannot be used inside $(). Such parameters become endogenous to the model and will be treated by the GAMS compiler as such. Moreover, the rim of the model instance is fixed: No addition of variables and equations is possible.

The instantiate call will only query the symbol information of the GamsModifiers, not the data of sync_db, e.g. to retrieve the dimension of the modifiers. That's why the modifier symbols have to exist (but don't have to have data) in sync_db when instantiate is called. The GamsParameters that contain the update data in sync_db can be filled at any time before executing the solve method. The solve method uses this data to update the model instance. The solve method will iterate through all records of modifier symbols in the model instance and try to find update data in sync_db. If a record in sync_db is found, this data record will be copied into the model instance. If no corresponding record is found in SyncDB there are different choices: 1) the original data record is restored (update_type=SymbolUpdateType.BaseCase) which is the default, 2) the default record of a GamsParameter (which is 0) is used (update_type=SymbolUpdateType.Zero, and 3) no copy takes place and we use the previously copied record value (update_type=SymbolUpdateType.Accumulate). After the model instance has been updated, the model is passed to the selected solver.

After the completion of the Solve method, the sync_db will contain the primal and dual solution of the model just solved. Moreover, the GamsParameters that are GamsModifiers are also accessible in sync_db as GamsVariables with the name of the GamsParameter plus "_var". The Marginal of this GamsVariable can provide sensitivity information about the parameter setting. The status of the solve is accessible through the model_status and solver_status properties.

In general, file operations in GAMS Python API take place in the working_directory defined in the GamsWorkspace. Exceptions to this rule are files read or created due to solver specific options in the solve routine of GamsModelInstance. These files are written to (or read from) the current directory, meaning the directory where the application gets executed.

Example on how to create a GAMSModelInstance from a GAMSCheckpoint that was generated by the Run method of GAMSJob.

ws = GamsWorkspace()

cp = ws.add_checkpoint()

ws.gamslib("trnsport")

job = ws.add_job_from_file("trnsport.gms")

job.run(checkpoint=cp)

mi = cp.add_modelinstance()

b = mi.sync_db.add_parameter("b", 1, "demand")

mi.instantiate("transport us lp min z", GamsModifier(b))

bmult = [ 0.7, 0.9, 1.1, 1.3 ]

for bm in bmult:

b.clear()

for rec in job.out_db.get_parameter("b"):

b.add_record(rec.keys).value = rec.value * bm

mi.solve()

print("Scenario bmult=" \+ str(bm) + ":")

print(" Modelstatus: " \+ str(mi.model_status))

print(" Solvestatus: " \+ str(mi.solver_status))

print(" Obj: " \+ str(mi.sync_db.get_variable("z")[()].level))

## Constructor & Destructor Documentation
## ◆ __init__()
gams.control.execution.GamsModelInstance.__init__  | ( |  | _self_ ,
---|---|---|---| | _checkpoint_ = None,
| | _modelinstance_name_ = None,
| | _source_ = None )

Constructor.

Parameters
     checkpoint| GamsCheckpoint
---|---
modelinstance_name| Identifier of GamsModelInstance (determined automatically if omitted)
source| model instance to be copied

## Member Function Documentation
## ◆ cleanup()
gams.control.execution.GamsModelInstance.cleanup  | ( |  | _self_| ) |---|---|---|---|---|---

Explicitly closes the license session when using a license that limits the actual uses of GAMS.

This method should only be called when the GamsModelInstance is not used anymore.

## ◆ copy_modelinstance()
gams.control.execution.GamsModelInstance.copy_modelinstance  | ( |  | _self_ ,
---|---|---|---| | _modelinstance_name_ = None )

Copies this ModelInstance to a new ModelInstance.

Parameters
     modelinstance_name| Identifier of GamsModelInstance (determined automatically if omitted)
---|---

Returns
    Reference to new ModelInstance

## ◆ instantiate()
gams.control.execution.GamsModelInstance.instantiate  | ( |  | _self_ ,
---|---|---|---| | _model_definition_ ,
| | _modifiers_ = [],
| | _options_ = None )

Instantiate the GamsModelInstance.

Parameters
     model_definition| Model definition
---|---
modifiers| List of GamsModifiers
options| GamsOptions

## ◆ solve()
gams.control.execution.GamsModelInstance.solve  | ( |  | _self_ ,
---|---|---|---| | _update_type_ = [SymbolUpdateType.BaseCase](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html#a85e370641ac5254006b94b3f9ba6b183),
| | _output_ = None,
| | _mi_opt_ = None )

Solve model instance.

Parameters
     update_type| Update type
---|---
output| Used to capture GAMS log, (e.g. sys.stdout or an object created by the build-in function open())
mi_opt| GamsModelInstance options

## Property Documentation
## ◆ model_status
| gams.control.execution.GamsModelInstance.model_status = property(get_model_status)
---
static

Status of the model.

(available after a solve)

## ◆ solver_status
| gams.control.execution.GamsModelInstance.solver_status = property(get_solver_status)
---
static

Solve status of the model.

(available after a solve)

---

## 18. Class: gams .Control .Execution .Gamsmodelinstance Members

# gams.control.execution.GamsModelInstance Member List
This is the complete list of members for [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html), including all inherited members.

[__del__](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a06698234b1f8c762dcd345850454cfed)(self)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|---|---|---
[__init__](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a43d5c88e1cd821855fd8b7435fbd5a7c)(self, checkpoint=None, modelinstance_name=None, source=None)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|
[checkpoint](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#af7c9726a6c26c7cfb66b9e7fce6f18cb)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)| static
[cleanup](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a84e633f0147869b30c90ccf9c230cb3c)(self)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|
[copy_modelinstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a7b51de7eeb46301d589b4efdaae04388)(self, modelinstance_name=None)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|
[instantiate](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a2b9c3c304512fcb094440f61f089b5d0)(self, model_definition, modifiers=[], options=None)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|
[interrupt](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a33d4b03d4c17ddfdeb3c0418bfc95eb4)(self)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|
[model_status](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a5deb3a4814e0586493bfc6083a27937e)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)| static
[name](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#aec0971ff648993ff715a71509bf8bdb9)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)| static
[solve](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#aae8841b93b647fa11d4e639f6be4bf2b)(self, update_type=SymbolUpdateType.BaseCase, output=None, mi_opt=None)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)|
[solver_status](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#a7a4a8055568c358ed0feabd5fa9310b8)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)| static
[sync_db](classgams_1_1control_1_1execution_1_1GamsModelInstance.html#aef855d7ee60a2e9a658f0280d0d96354)| [gams.control.execution.GamsModelInstance](classgams_1_1control_1_1execution_1_1GamsModelInstance.html)| static

---

## 19. Class: gams .Control .Execution .Symbolupdatetype

# gams.control.execution.SymbolUpdateType Class Reference
Symbol update type. More...

## Static Public Attributes
---
int | **Zero** = 0
| If record does not exist use 0 (Zero)

int | **BaseCase** = 1
| If record does not exist use values from instantiation.

int | **Accumulate** = 2
| If record does not exist use value from previous solve.

## Detailed Description
Symbol update type.

---

## 20. Class: gams .Control .Execution .Symbolupdatetype Members

# gams.control.execution.SymbolUpdateType Member List
This is the complete list of members for [gams.control.execution.SymbolUpdateType](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html), including all inherited members.

[Accumulate](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html#a223bfa32a2d7748edd4006a6e8d8ba05)| [gams.control.execution.SymbolUpdateType](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html)| static
---|---|---
[BaseCase](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html#a85e370641ac5254006b94b3f9ba6b183)| [gams.control.execution.SymbolUpdateType](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html)| static
[Zero](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html#ac405f3fbd50505ceb1f0983ff32319de)| [gams.control.execution.SymbolUpdateType](classgams_1_1control_1_1execution_1_1SymbolUpdateType.html)| static

---

## 21. Class: gams .Control .Options .Gamsoptions

# gams.control.options.GamsOptions Class Reference
The GamsOptions class manages GAMS options (sometimes also called GAMS parameters since they correspond to the command line parameters of the GAMS executable) for a GamsJob and GamsModelInstance. More...

## Public Member Functions
---
| __init__ (self, ws, opt_from=None, opt_file=None)
| Constructor.

| export (self, file_path)
| Write GamsOptions into a parameter file.

## Public Attributes
---
dict | **defines** = {}
| GAMS Dash Options.

## Properties
---
| **all_model_types** = property(fset=set_all_model_types)
| Set solver for all model types.

| **lp** = property(get_lp, set_lp)
| Default lp solver.

| **mip** = property(get_mip, set_mip)
| Default mip solver.

| **rmip** = property(get_rmip, set_rmip)
| Default rmip solver.

| **nlp** = property(get_nlp, set_nlp)
| Default nlp solver.

| **mcp** = property(get_mcp, set_mcp)
| Default mcp solver.

| **mpec** = property(get_mpec, set_mpec)
| Default mpec solver.

| **rmpec** = property(get_rmpec, set_rmpec)
| Default rmpec solver.

| **cns** = property(get_cns, set_cns)
| Default cns solver.

| **dnlp** = property(get_dnlp, set_dnlp)
| Default dnlp solver.

| **rminlp** = property(get_rminlp, set_rminlp)
| Default rminlp solver.

| **minlp** = property(get_minlp, set_minlp)
| Default minlp solver.

| **qcp** = property(get_qcp, set_qcp)
| Default qcp solver.

| **miqcp** = property(get_miqcp, set_miqcp)
| Default miqcp solver.

| **rmiqcp** = property(get_rmiqcp, set_rmiqcp)
| Default rmiqcp solver.

| **emp** = property(get_emp, set_emp)
| Default emp solver.

| **action** = property(get_action, set_action)
| GAMS processing request.

| **appendexpand** = property(get_appendexpand, set_appendexpand)
| Expand file append option.

| **appendout** = property(get_appendout, set_appendout)
| Output file append option.

| **asyncsollst** = property(get_asyncsollst, set_asyncsollst)
| Print solution listing when asynchronous solve (Grid or Threads) is used.

| **bratio** = property(get_bratio, set_bratio)
| Basis detection threshold.

| **capturemodelinstance** = property(get_capturemodelinstance, set_capturemodelinstance)
| Switch to capture all model instances within a run.

| **case** = property(get_case, set_case)
| Output case option for LST file.

| **cerr** = property(get_cerr, set_cerr)
| Compile time error limit.

| **charset** = property(get_charset, set_charset)
| Character set flag.

| **checkerrorlevel** = property(get_checkerrorlevel, set_checkerrorlevel)
| Check errorLevel automatically after executing external program.

| **decryptkey** = property(get_decryptkey, set_decryptkey)
| Key to decrypt a text file that was encrypted via $encrypt.

| **dformat** = property(get_dformat, set_dformat)
| Date format.

| **digit** = property(get_digit, set_digit)
| Switch default for "$on/offDigit".

| **domlim** = property(get_domlim, set_domlim)
| Domain violation limit solver default.

| **dumpopt** = property(get_dumpopt, set_dumpopt)
| Writes preprocessed input to the file input.dmp.

| **dumpoptgdx** = property(get_dumpoptgdx, set_dumpoptgdx)
| Defines a GDX file name stem created when using DumpOpt.

| **dumpparms** = property(get_dumpparms, set_dumpparms)
| GAMS parameter logging.

| **dumpparmslogprefix** = property(get_dumpparmslogprefix, set_dumpparmslogprefix)
| Prefix of lines triggered by DumpParms>1\.

| **ecimplicitload** = property(get_ecimplicitload, set_ecimplicitload)
| Allow implicit loading of symbols from embedded code or not.

| **empty** = property(get_empty, set_empty)
| Switch default for "$on/offEmpty".

| **encryptkey** = property(get_encryptkey, set_encryptkey)
| Key to encrypt a text file using $encrypt.

| **eolcom** = property(get_eolcom, set_eolcom)
| Switch default for "$on/offEolCom" and "$eolCom".

| **errmsg** = property(get_errmsg, set_errmsg)
| Placing of compilation error messages.

| **errorlog** = property(get_errorlog, set_errorlog)
| Max error message lines written to the log for each error.

| **etlim** = property(get_etlim, set_etlim)
| Elapsed time limit in seconds.

| **execmode** = property(get_execmode, set_execmode)
| Limits on external programs that are allowed to be executed.

| **expand** = property(get_expand, set_expand)
| Expanded (include) input file name.

| **fddelta** = property(get_fddelta, set_fddelta)
| Step size for finite differences.

| **fdopt** = property(get_fdopt, set_fdopt)
| Options for finite differences.

| **ferr** = property(get_ferr, set_ferr)
| Alternative error message file.

| **filecase** = property(get_filecase, set_filecase)
| Casing of file names and paths (put, gdx, ref, $include, etc.)

| **filestem** = property(get_filestem, set_filestem)
| Sets the file stem for output files which use the input file name as stem by default.

| **filestemapfromenv** = property(get_filestemapfromenv, set_filestemapfromenv)
| Append a string read from an environment variable to the "FileStem".

| **filtered** = property(get_filtered, set_filtered)
| Switch between filtered and domain-checked read from GDX.

| **forceoptfile** = property(get_forceoptfile, set_forceoptfile)
| Overwrites other option file section mechanism.

| **forcework** = property(get_forcework, set_forcework)
| Force GAMS to process a save file created with a newer GAMS version or with execution errors.

| **forlim** = property(get_forlim, set_forlim)
| GAMS looping limit.

| **freeembeddedpython** = property(get_freeembeddedpython, set_freeembeddedpython)
| Free external resources at the end of each embedded Python code blocks.

| **gdxcompress** = property(get_gdxcompress, set_gdxcompress)
| Compression of generated GDX file.

| **gdxconvert** = property(get_gdxconvert, set_gdxconvert)
| Version of GDX files generated (for backward compatibility)

| **gdxuels** = property(get_gdxuels, set_gdxuels)
| Unload labels or UELs to GDX either squeezed or full.

| **griddir** = property(get_griddir, set_griddir)
| Grid file directory.

| **gridscript** = property(get_gridscript, set_gridscript)
| Grid submission script.

| **heaplimit** = property(get_heaplimit, set_heaplimit)
| Maximum Heap size allowed in MB.

| **holdfixed** = property(get_holdfixed, set_holdfixed)
| Treat fixed variables as constants.

| **holdfixedasync** = property(get_holdfixedasync, set_holdfixedasync)
| Allow HoldFixed for models solved asynchronously as well.

| **idcgdxinput** = property(get_idcgdxinput, set_idcgdxinput)
| GDX file name with data for implicit input.

| **idcgdxoutput** = property(get_idcgdxoutput, set_idcgdxoutput)
| GDX file name for data for implicit output.

| **implicitassign** = property(get_implicitassign, set_implicitassign)
| Switch default for "$on/offImplicitAssign".

| **inlinecom** = property(get_inlinecom, set_inlinecom)
| Switch default for "$on/offInline" and "$inlineCom".

| **integer1** = property(get_integer1, set_integer1)
| Integer communication cell N.

| **integer2** = property(get_integer2, set_integer2)
| Integer communication cell N.

| **integer3** = property(get_integer3, set_integer3)
| Integer communication cell N.

| **integer4** = property(get_integer4, set_integer4)
| Integer communication cell N.

| **integer5** = property(get_integer5, set_integer5)
| Integer communication cell N.

| **interactivesolver** = property(get_interactivesolver, set_interactivesolver)
| Allow solver to interact via command line input.

| **intvarup** = property(get_intvarup, set_intvarup)
| Set mode for default upper bounds on integer variables.

| **iterlim** = property(get_iterlim, set_iterlim)
| Iteration limit of solver.

| **jobtrace** = property(get_jobtrace, set_jobtrace)
| Job trace string to be written to the trace file at the end of a GAMS job.

| **keep** = property(get_keep, set_keep)
| Controls keeping or deletion of process directory and scratch files.

| **libincdir** = property(get_libincdir, set_libincdir)
| LibInclude directory.

| **license** = property(get_license, set_license)
| Use alternative license file.

| **limcol** = property(get_limcol, set_limcol)
| Maximum number of columns listed in one variable block.

| **limrow** = property(get_limrow, set_limrow)
| Maximum number of rows listed in one equation block.

| **listing** = property(get_listing, set_listing)
| Switch default for "$on/offListing".

| **logline** = property(get_logline, set_logline)
| Amount of line tracing to the log file.

| **lsttitleleftaligned** = property(get_lsttitleleftaligned, set_lsttitleleftaligned)
| Write title of LST file all left aligned.

| **maxexecerror** = property(get_maxexecerror, set_maxexecerror)
| Execution time error limit.

| **maxprocdir** = property(get_maxprocdir, set_maxprocdir)
| Maximum number of 225* process directories.

| **miimode** = property(get_miimode, set_miimode)
| Model Instance Mode.

| **multi** = property(get_multi, set_multi)
| Switch default for "$on/offMulti[R]".

| **nodlim** = property(get_nodlim, set_nodlim)
| Node limit in branch and bound tree.

| **nonewvarequ** = property(get_nonewvarequ, set_nonewvarequ)
| Triggers a compilation error when new equations or variable symbols are introduced.

| **on115** = property(get_on115, set_on115)
| Generate errors for unknown unique element in an equation.

| **optca** = property(get_optca, set_optca)
| Absolute Optimality criterion solver default.

| **optcr** = property(get_optcr, set_optcr)
| Relative Optimality criterion solver default.

| **optdir** = property(get_optdir, set_optdir)
| Option file directory.

| **optfile** = property(get_optfile, set_optfile)
| Default option file.

| **output** = property(get_output, set_output)
| Listing file name.

| **pagecontr** = property(get_pagecontr, set_pagecontr)
| Output file page control option.

| **pagesize** = property(get_pagesize, set_pagesize)
| Output file page size (=0 no paging)

| **pagewidth** = property(get_pagewidth, set_pagewidth)
| Output file page width.

| **plicense** = property(get_plicense, set_plicense)
| Privacy license file name.

| **prefixloadpath** = property(get_prefixloadpath, set_prefixloadpath)
| Prepend GAMS system directory to library load path.

| **previouswork** = property(get_previouswork, set_previouswork)
| Indicator for writing workfile with previous workfile version.

| **proctreememmonitor** = property(get_proctreememmonitor, set_proctreememmonitor)
| Monitor the memory used by the GAMS process tree.

| **proctreememticks** = property(get_proctreememticks, set_proctreememticks)
| Set wait interval between memory monitor checks: ticks = milliseconds.

| **profile** = property(get_profile, set_profile)
| Execution profiling.

| **profilefile** = property(get_profilefile, set_profilefile)
| Write profile information to this file.

| **profiletol** = property(get_profiletol, set_profiletol)
| Minimum time a statement must use to appear in profile generated output.

| **putdir** = property(get_putdir, set_putdir)
| Put file directory.

| **putnd** = property(get_putnd, set_putnd)
| Number of decimals for put files.

| **putnr** = property(get_putnr, set_putnr)
| Numeric round format for put files.

| **putps** = property(get_putps, set_putps)
| Page size for put files.

| **putpw** = property(get_putpw, set_putpw)
| Page width for put files.

| **reference** = property(get_reference, set_reference)
| Symbol reference file.

| **referencelineno** = property(get_referencelineno, set_referencelineno)
| Controls the line numbers written to a reference file.

| **replace** = property(get_replace, set_replace)
| Switch between merge and replace when reading from GDX into non-empty symbol.

| **reslim** = property(get_reslim, set_reslim)
| Wall-clock time limit for solver.

| **savepoint** = property(get_savepoint, set_savepoint)
| Save solver point in GDX file.

| **scriptexit** = property(get_scriptexit, set_scriptexit)
| Program or script to be executed at the end of a GAMS run.

| **seed** = property(get_seed, set_seed)
| Random number seed.

| **showosmemory** = property(get_showosmemory, set_showosmemory)
| Show the memory usage reported by the Operating System instead of the internal counting.

| **solprint** = property(get_solprint, set_solprint)
| Solution report print option.

| **solvelink** = property(get_solvelink, set_solvelink)
| Solver link option.

| **solveopt** = property(get_solveopt, set_solveopt)
| Multiple solve management.

| **stepsum** = property(get_stepsum, set_stepsum)
| Summary of computing resources used by job steps.

| **strictsingleton** = property(get_strictsingleton, set_strictsingleton)
| Error if assignment to singleton set has multiple elements.

| **stringchk** = property(get_stringchk, set_stringchk)
| String substitution options.

| **suffixdlvars** = property(get_suffixdlvars, set_suffixdlvars)
| Switch default for "$on/offSuffixDLVars".

| **suffixalgebravars** = property(get_suffixalgebravars, set_suffixalgebravars)
| Switch default for "$on/offSuffixAlgebraVars".

| **suppress** = property(get_suppress, set_suppress)
| Compiler listing option.

| **symbol** = property(get_symbol, set_symbol)
| Symbol table file.

| **symprefix** = property(get_symprefix, set_symprefix)
| Prefix all symbols encountered during compilation by the specified string in work file.

| **sys10** = property(get_sys10, set_sys10)
| Changes rpower to ipower when the exponent is constant and within 1e-12 of an integer.

| **sys11** = property(get_sys11, set_sys11)
| Dynamic resorting if indices in assignment/data statements are not in natural order.

| **sys12** = property(get_sys12, set_sys12)
| Pass model with generation errors to solver.

| **sysincdir** = property(get_sysincdir, set_sysincdir)
| SysInclude directory.

| **sysout** = property(get_sysout, set_sysout)
| Solver Status file reporting option.

| **tabin** = property(get_tabin, set_tabin)
| Tab spacing.

| **tformat** = property(get_tformat, set_tformat)
| Time format.

| **threads** = property(get_threads, set_threads)
| Number of processors to be used by a solver.

| **threadsasync** = property(get_threadsasync, set_threadsasync)
| Limit on number of threads to be used for asynchronous solves (solveLink=6)

| **timer** = property(get_timer, set_timer)
| Instruction timer threshold in milliseconds.

| **trace** = property(get_trace, set_trace)
| Trace file name.

| **tracelevel** = property(get_tracelevel, set_tracelevel)
| Modelstat/Solvestat threshold used in conjunction with action=GT.

| **traceopt** = property(get_traceopt, set_traceopt)
| Trace file format option.

| **user1** = property(get_user1, set_user1)
| User string N.

| **user2** = property(get_user2, set_user2)
| User string N.

| **user3** = property(get_user3, set_user3)
| User string N.

| **user4** = property(get_user4, set_user4)
| User string N.

| **user5** = property(get_user5, set_user5)
| User string N.

| **warnings** = property(get_warnings, set_warnings)
| Number of warnings permitted before a run terminates.

| **workfactor** = property(get_workfactor, set_workfactor)
| Memory Estimate multiplier for some solvers.

| **workspace** = property(get_workspace, set_workspace)
| Work space for some solvers in MB.

| **zerores** = property(get_zerores, set_zerores)
| The results of certain operations will be set to zero if abs(result) LE ZeroRes.

| **zeroresrep** = property(get_zeroresrep, set_zeroresrep)
| Report underflow as a warning when abs(results) LE ZeroRes and result set to zero.

## Detailed Description
The GamsOptions class manages GAMS options (sometimes also called GAMS parameters since they correspond to the command line parameters of the GAMS executable) for a GamsJob and GamsModelInstance.

There are integer (e.g. nodlim), double (e.g. reslim), and string (e.g. putdir) valued options. There are also a few list options (defines to set string macros inside GAMS and idir provide multiple search paths for include files) and a power option to set a solver for all suitable model types (all_model_types).

Some options known from other interfaces to GAMS that are of limited use or could even create problematic situations in the Python environment are not settable through the GamsOptions class.

## Constructor & Destructor Documentation
## ◆ __init__()
gams.control.options.GamsOptions.__init__  | ( |  | _self_ ,
---|---|---|---| | _ws_ ,
| | _opt_from_ = None,
| | _opt_file_ = None )

Constructor.

Parameters
     ws| GamsWorkspace containing GamsOptions
---|---
opt_from| GamsOptions used to initialize the new object
opt_file| Parameter used to initialize the new objectfile

## Member Function Documentation
## ◆ export()
gams.control.options.GamsOptions.export  | ( |  | _self_ ,
---|---|---|---| | _file_path_ )

Write GamsOptions into a parameter file.

Parameters
     file_path| The path used to write the parameter file. A relative path is relative to the GAMS working directory.
---|---

---

## 22. Class: gams .Control .Options .Gamsoptions Members

# gams.control.options.GamsOptions Member List
This is the complete list of members for [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html), including all inherited members.

[__init__](classgams_1_1control_1_1options_1_1GamsOptions.html#afaf77bfdb2672b31ac570b7a7e6417a5)(self, ws, opt_from=None, opt_file=None)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)|---|---|---
[action](classgams_1_1control_1_1options_1_1GamsOptions.html#a3b1d553596b5e70089691e2b9ff30e37)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[all_model_types](classgams_1_1control_1_1options_1_1GamsOptions.html#a0a324e50dc339540c1f21225a957cf5a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[appendexpand](classgams_1_1control_1_1options_1_1GamsOptions.html#a9def68fa679a8f0979fd3fcf2477721a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[appendout](classgams_1_1control_1_1options_1_1GamsOptions.html#a3aa1d04c589828bc74e3578738e4607b)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[asyncsollst](classgams_1_1control_1_1options_1_1GamsOptions.html#ad7e829b0e5e7050a6ec5ed9ef9f1ec9a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[bratio](classgams_1_1control_1_1options_1_1GamsOptions.html#a6f1ffde2f6fa94380a67ff878be70f9d)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[capturemodelinstance](classgams_1_1control_1_1options_1_1GamsOptions.html#ac0966e2f703a92f2a110b0b55846a6d9)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[case](classgams_1_1control_1_1options_1_1GamsOptions.html#a5a6b16e766c8d93c844907c8adcfccae)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[cerr](classgams_1_1control_1_1options_1_1GamsOptions.html#a38f8de59180330a9cffd071ef3c87d7f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[charset](classgams_1_1control_1_1options_1_1GamsOptions.html#ad92788dac58e02844ac3d28778310d3d)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[checkerrorlevel](classgams_1_1control_1_1options_1_1GamsOptions.html#a8bd8d88e0e3173fa8092b4d70074d69c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[cns](classgams_1_1control_1_1options_1_1GamsOptions.html#ade246d7eaa024b866d3a149cff2e5399)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[decryptkey](classgams_1_1control_1_1options_1_1GamsOptions.html#ada049902d2ccde460c91c670476493f4)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[defines](classgams_1_1control_1_1options_1_1GamsOptions.html#ae4f743eabc504f567999efc3c1f84673)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)|
[dformat](classgams_1_1control_1_1options_1_1GamsOptions.html#ae9ed52c1c74dfb06d7acf1182ecffea5)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[digit](classgams_1_1control_1_1options_1_1GamsOptions.html#a4b9b7064fb563671522c989a9bc0bc4e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[dnlp](classgams_1_1control_1_1options_1_1GamsOptions.html#a21604631e2fb9ad57f453ee7f2173e76)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[domlim](classgams_1_1control_1_1options_1_1GamsOptions.html#a75768fba79a50e3addf7df7c7a4126e2)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[dumpopt](classgams_1_1control_1_1options_1_1GamsOptions.html#a04073ed00de934c751ba575ef99e4884)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[dumpoptgdx](classgams_1_1control_1_1options_1_1GamsOptions.html#a7532387e6a2119ee1a91d4f825cde18f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[dumpparms](classgams_1_1control_1_1options_1_1GamsOptions.html#aa6b49b4334c41419162069728b243583)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[dumpparmslogprefix](classgams_1_1control_1_1options_1_1GamsOptions.html#aea4e95aaaa7e89d46b2569c18a3eea00)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[ecimplicitload](classgams_1_1control_1_1options_1_1GamsOptions.html#a15a7915f72f2b8ee1c6585e4a3799433)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[emp](classgams_1_1control_1_1options_1_1GamsOptions.html#ab5c846f2789f9d17660681391d582efd)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[empty](classgams_1_1control_1_1options_1_1GamsOptions.html#a0ef8abd8612d08e3b79f3ab183536a28)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[encryptkey](classgams_1_1control_1_1options_1_1GamsOptions.html#ac1cc0e2305172946f7b582f0dd77f45c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[eolcom](classgams_1_1control_1_1options_1_1GamsOptions.html#abdd9ee1fe990c44cb24aa0dde905e8d0)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[errmsg](classgams_1_1control_1_1options_1_1GamsOptions.html#a70f2da9ebcd9810f280aed71d76b8072)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[errorlog](classgams_1_1control_1_1options_1_1GamsOptions.html#abcc861809702f58a75297d22278db8bf)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[etlim](classgams_1_1control_1_1options_1_1GamsOptions.html#adac6a63f34daf6b1f8ddb0b25c599b86)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[execmode](classgams_1_1control_1_1options_1_1GamsOptions.html#a7d292931385f8c50165ecdeb6fbd20e5)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[expand](classgams_1_1control_1_1options_1_1GamsOptions.html#a161519f397b5d5a3a9b888671c656003)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[export](classgams_1_1control_1_1options_1_1GamsOptions.html#ad6a46ccf31a659d4679922e072692d54)(self, file_path)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)|
[fddelta](classgams_1_1control_1_1options_1_1GamsOptions.html#af4a8bf9314cb2ae77a6d6fbeebc67595)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[fdopt](classgams_1_1control_1_1options_1_1GamsOptions.html#a70c0d9dfb2ef3d7c41845000dc491f7e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[ferr](classgams_1_1control_1_1options_1_1GamsOptions.html#af367f8912ef8cc6e9e4b4bfd8071230f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[filecase](classgams_1_1control_1_1options_1_1GamsOptions.html#ad40daf3e84d00c5def7aa8f4cd321e86)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[filestem](classgams_1_1control_1_1options_1_1GamsOptions.html#a47ec32f94fe13348051f9fe4974d0557)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[filestemapfromenv](classgams_1_1control_1_1options_1_1GamsOptions.html#a7948398962d069010f97aa4a83cb0222)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[filtered](classgams_1_1control_1_1options_1_1GamsOptions.html#a31f800956cae55385b13200a69992a3e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[forceoptfile](classgams_1_1control_1_1options_1_1GamsOptions.html#a5cf43f9b77abc9ba960e229060cac42a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[forcework](classgams_1_1control_1_1options_1_1GamsOptions.html#acb589cb5941b9ba2b093fdad82df1a89)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[forlim](classgams_1_1control_1_1options_1_1GamsOptions.html#ab33042c768a3e49d39009dd99b7313f8)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[freeembeddedpython](classgams_1_1control_1_1options_1_1GamsOptions.html#a30a7a7e4b5173e4862d962dcb1bb2822)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[gdxcompress](classgams_1_1control_1_1options_1_1GamsOptions.html#acc8d9f1353f80899bfb3ceb50d3fed7b)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[gdxconvert](classgams_1_1control_1_1options_1_1GamsOptions.html#a8d7ab97af785feff665f19ed418c6356)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[gdxuels](classgams_1_1control_1_1options_1_1GamsOptions.html#a1dfe604b4cfeb44b48216b964144a2de)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[griddir](classgams_1_1control_1_1options_1_1GamsOptions.html#a1e9d89fa14d2c29fb2604f9dc2c3bbe8)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[gridscript](classgams_1_1control_1_1options_1_1GamsOptions.html#a7d4c62c3e458883990163821b450dec2)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[heaplimit](classgams_1_1control_1_1options_1_1GamsOptions.html#aa98a24796caffef473173d3cba25444f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[holdfixed](classgams_1_1control_1_1options_1_1GamsOptions.html#a3e62ea29193706f1f67e9bd153a7d9f3)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[holdfixedasync](classgams_1_1control_1_1options_1_1GamsOptions.html#af68d03d5daae02a638fea2e59da182d4)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[idcgdxinput](classgams_1_1control_1_1options_1_1GamsOptions.html#a704eafd94820e20774ba8d5643f22e72)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[idcgdxoutput](classgams_1_1control_1_1options_1_1GamsOptions.html#abe603afe7f97c236069dc3f38b94db27)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[implicitassign](classgams_1_1control_1_1options_1_1GamsOptions.html#aa26d993dbe5b0d9c9f7d04a81b67c99d)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[inlinecom](classgams_1_1control_1_1options_1_1GamsOptions.html#a059b2c2f949d627d72642386759efeae)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[integer1](classgams_1_1control_1_1options_1_1GamsOptions.html#a62b50833f26c51531423a5a77cff2ecd)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[integer2](classgams_1_1control_1_1options_1_1GamsOptions.html#aaccceb3d68bbf81a366dc2e39d350831)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[integer3](classgams_1_1control_1_1options_1_1GamsOptions.html#a763c65b301a7e92879012f5094aaf23f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[integer4](classgams_1_1control_1_1options_1_1GamsOptions.html#a2cd564b78245e74c799a9d10527275d2)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[integer5](classgams_1_1control_1_1options_1_1GamsOptions.html#aa716e6e29e118cac6b3d11219348016a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[interactivesolver](classgams_1_1control_1_1options_1_1GamsOptions.html#a3c5175871445aaa8581dfa4230fc121c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[intvarup](classgams_1_1control_1_1options_1_1GamsOptions.html#a087f09633e176dbfb0467c99ce425771)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[iterlim](classgams_1_1control_1_1options_1_1GamsOptions.html#a2f9c4e57be5c706ce6fdfc6e089ace8c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[jobtrace](classgams_1_1control_1_1options_1_1GamsOptions.html#a85a392917899164f430f398ca5f57c1e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[keep](classgams_1_1control_1_1options_1_1GamsOptions.html#a2e7ff79ddbd35c5fc4e9799e18250d12)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[libincdir](classgams_1_1control_1_1options_1_1GamsOptions.html#a7929764e80a6c1bd82dfe4c4082086b0)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[license](classgams_1_1control_1_1options_1_1GamsOptions.html#a4bff64ecf39b70d052807561923323a3)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[limcol](classgams_1_1control_1_1options_1_1GamsOptions.html#a071b9b19f537b17904c54f634564a386)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[limrow](classgams_1_1control_1_1options_1_1GamsOptions.html#aa2b8f414d44a4d6a1665737a786ec4f7)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[listing](classgams_1_1control_1_1options_1_1GamsOptions.html#ac225184a311178de282535928f71eeb4)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[logline](classgams_1_1control_1_1options_1_1GamsOptions.html#ad2b2faac2968abf72d2e904a02be3a33)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[lp](classgams_1_1control_1_1options_1_1GamsOptions.html#a3102e8d0ff7e48b2f23d063ac05705ba)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[lsttitleleftaligned](classgams_1_1control_1_1options_1_1GamsOptions.html#a15676581040feb4c34b11da5426eb1cd)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[maxexecerror](classgams_1_1control_1_1options_1_1GamsOptions.html#a1a64e4a2535b85e3c3a6b8d84447afdc)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[maxprocdir](classgams_1_1control_1_1options_1_1GamsOptions.html#a56a81884920554fe129951808ec74aaa)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[mcp](classgams_1_1control_1_1options_1_1GamsOptions.html#a7c33eb8cc3bc6e7cd232efcbbf68661e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[miimode](classgams_1_1control_1_1options_1_1GamsOptions.html#a7c5374e3ca588a7834481fdf4c3270b8)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[minlp](classgams_1_1control_1_1options_1_1GamsOptions.html#ae1abe717c841060f6043019dc070106c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[mip](classgams_1_1control_1_1options_1_1GamsOptions.html#a893cc0e36f67b88cc46685cf15959866)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[miqcp](classgams_1_1control_1_1options_1_1GamsOptions.html#a9eddfcb4703c0a619376665bcdec3b2c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[mpec](classgams_1_1control_1_1options_1_1GamsOptions.html#a6c6a0c00f5849a24a432cc5c18fd396b)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[multi](classgams_1_1control_1_1options_1_1GamsOptions.html#a7ad86c0816723a82c2401ef8bba7ce60)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[nlp](classgams_1_1control_1_1options_1_1GamsOptions.html#a079557b9b20f77ecc710e0387a4927c7)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[nodlim](classgams_1_1control_1_1options_1_1GamsOptions.html#a40d7d82484fa2a277dc9634be2b8973a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[nonewvarequ](classgams_1_1control_1_1options_1_1GamsOptions.html#a3e26104a827ca32f87ce1d241cf87171)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[on115](classgams_1_1control_1_1options_1_1GamsOptions.html#adc92adfb043ba4bb85fb56da215b3645)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[optca](classgams_1_1control_1_1options_1_1GamsOptions.html#a9ed0745ceb4b7ad85d1a633505bef733)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[optcr](classgams_1_1control_1_1options_1_1GamsOptions.html#ad3adec12e170236105156517fae33c8a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[optdir](classgams_1_1control_1_1options_1_1GamsOptions.html#ad4968b6ac494e423f1ecbbf9f7ed9b4f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[optfile](classgams_1_1control_1_1options_1_1GamsOptions.html#a7af44f837f7e5fcce6362c12c9b88588)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[output](classgams_1_1control_1_1options_1_1GamsOptions.html#a93cdc809dbea2275f5d20f52157c7662)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[pagecontr](classgams_1_1control_1_1options_1_1GamsOptions.html#a78497ae404d84aa509edf3e47e46d2d7)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[pagesize](classgams_1_1control_1_1options_1_1GamsOptions.html#a77fccd87971c0fade5b1b483d8bc7132)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[pagewidth](classgams_1_1control_1_1options_1_1GamsOptions.html#a3d3d90485f45d5781a8282e196f8f6c2)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[plicense](classgams_1_1control_1_1options_1_1GamsOptions.html#aa4873de5af4a7f8fa2e5041b504ab75e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[prefixloadpath](classgams_1_1control_1_1options_1_1GamsOptions.html#a4872923c92867d30f93f7332dc2a8f48)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[previouswork](classgams_1_1control_1_1options_1_1GamsOptions.html#a515edbf960b79ee5f5ec6abd69403335)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[proctreememmonitor](classgams_1_1control_1_1options_1_1GamsOptions.html#a61fc0d4fe49403d09f086fea74f1d4db)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[proctreememticks](classgams_1_1control_1_1options_1_1GamsOptions.html#ac9d5459c69a77b0b25d04b95bd9b7093)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[profile](classgams_1_1control_1_1options_1_1GamsOptions.html#a197584959f8dbb39feed9f5d9bee51df)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[profilefile](classgams_1_1control_1_1options_1_1GamsOptions.html#ac7ae311bf0bf28dd19ec2e942448221b)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[profiletol](classgams_1_1control_1_1options_1_1GamsOptions.html#a0a4bed735780ae8db4e3be96ee0478fc)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[putdir](classgams_1_1control_1_1options_1_1GamsOptions.html#a01de3fb20cbf57db6b70da0e73e6ea13)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[putnd](classgams_1_1control_1_1options_1_1GamsOptions.html#a9679454bcccea75aa4881483f25faa42)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[putnr](classgams_1_1control_1_1options_1_1GamsOptions.html#ada350147046323e4e1e8e26ddea80072)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[putps](classgams_1_1control_1_1options_1_1GamsOptions.html#a17c5b2a7232d049d8e0192347f490600)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[putpw](classgams_1_1control_1_1options_1_1GamsOptions.html#aa44e0d383d139a303878c7d62652a836)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[qcp](classgams_1_1control_1_1options_1_1GamsOptions.html#a7adc1d1d9e6f51e94096cd6c8566ee24)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[reference](classgams_1_1control_1_1options_1_1GamsOptions.html#a127482f789948d303d7c18a3f1cc8a36)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[referencelineno](classgams_1_1control_1_1options_1_1GamsOptions.html#a9bf96b6329511c016d8cf310fee6d6fe)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[replace](classgams_1_1control_1_1options_1_1GamsOptions.html#a7d04400f9aec54e5a84e484b560f9dd6)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[reslim](classgams_1_1control_1_1options_1_1GamsOptions.html#a1d7ec9b64285541919ddb62fe9ceea05)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[rminlp](classgams_1_1control_1_1options_1_1GamsOptions.html#a51ee2f149be0f34ff67aa2677b5c312f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[rmip](classgams_1_1control_1_1options_1_1GamsOptions.html#a2c5b9af48f7a5cefb5ea973ad34536dd)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[rmiqcp](classgams_1_1control_1_1options_1_1GamsOptions.html#abfd8c67a12bb6b7d307c34500ba15b0a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[rmpec](classgams_1_1control_1_1options_1_1GamsOptions.html#a68bad3373c072f805db5acac6cd4c848)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[savepoint](classgams_1_1control_1_1options_1_1GamsOptions.html#a06f99e7ab8b189d49ec23870e1071766)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[scriptexit](classgams_1_1control_1_1options_1_1GamsOptions.html#a21388dc7fa1a5b9110229edb15598240)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[seed](classgams_1_1control_1_1options_1_1GamsOptions.html#a13cee375fd7ced8d38561575e9f2dd85)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[showosmemory](classgams_1_1control_1_1options_1_1GamsOptions.html#ad7a41ebd8be671aa884b833eaf30d12b)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[solprint](classgams_1_1control_1_1options_1_1GamsOptions.html#aeaf08fc43feeebde45210fc38420f289)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[solvelink](classgams_1_1control_1_1options_1_1GamsOptions.html#ad27ea29e787759c030d443380dd59f70)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[solveopt](classgams_1_1control_1_1options_1_1GamsOptions.html#a46d9c02cabcc5b37f61b2436da450fe9)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[stepsum](classgams_1_1control_1_1options_1_1GamsOptions.html#aa7cffe87a2d6cf42914d40962e8b8388)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[strictsingleton](classgams_1_1control_1_1options_1_1GamsOptions.html#adcf4af73d6b500cce21cdcfacc5d428a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[stringchk](classgams_1_1control_1_1options_1_1GamsOptions.html#a44036d149b0afd48e1022bc3a2936ad2)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[suffixalgebravars](classgams_1_1control_1_1options_1_1GamsOptions.html#a4f2ff1cd19c0d9dffc54bc9ac616a164)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[suffixdlvars](classgams_1_1control_1_1options_1_1GamsOptions.html#a7fbcf1a834bcfac1158023c8f1603202)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[suppress](classgams_1_1control_1_1options_1_1GamsOptions.html#ad60ba506b684c314f896919ceea693b3)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[symbol](classgams_1_1control_1_1options_1_1GamsOptions.html#aca01190f2fdd726abfa71eec96f76370)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[symprefix](classgams_1_1control_1_1options_1_1GamsOptions.html#aa280642ca040c283b0800b5b2035db03)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[sys10](classgams_1_1control_1_1options_1_1GamsOptions.html#a4799d3f8c854be1fe51bfe07c736592d)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[sys11](classgams_1_1control_1_1options_1_1GamsOptions.html#a13e62e49daac6ae73997fcb51a11930a)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[sys12](classgams_1_1control_1_1options_1_1GamsOptions.html#a38839348a78f3aaa799ff636afd26889)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[sysincdir](classgams_1_1control_1_1options_1_1GamsOptions.html#a14cc3b166db122933a220937d9732fdd)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[sysout](classgams_1_1control_1_1options_1_1GamsOptions.html#ab0d390b40df0cd363049a873b7eed707)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[tabin](classgams_1_1control_1_1options_1_1GamsOptions.html#a5104155461d942e5d2766a11e3d89b3f)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[tformat](classgams_1_1control_1_1options_1_1GamsOptions.html#aa2238972da2ca6478afee0ee69c80807)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[threads](classgams_1_1control_1_1options_1_1GamsOptions.html#adcdbdd4720e68a60e0d7220a0633af90)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[threadsasync](classgams_1_1control_1_1options_1_1GamsOptions.html#a3f835056ce9dc602a6f57f2cea6afc64)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[timer](classgams_1_1control_1_1options_1_1GamsOptions.html#acf2acd933654cd90c852b5ec042d3794)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[trace](classgams_1_1control_1_1options_1_1GamsOptions.html#a22038286a28d38e2b5bfeb97eee07917)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[tracelevel](classgams_1_1control_1_1options_1_1GamsOptions.html#aaba6d801701f59c60b56de1b2e52dee3)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[traceopt](classgams_1_1control_1_1options_1_1GamsOptions.html#a37dd5708cd52f3fd102ff73136c89332)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[user1](classgams_1_1control_1_1options_1_1GamsOptions.html#a5274760b9649af62b7e8c619056b610e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[user2](classgams_1_1control_1_1options_1_1GamsOptions.html#a409f8501b104439a7f386facc65a4939)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[user3](classgams_1_1control_1_1options_1_1GamsOptions.html#ad9b59f5395e5f2eebf67df57b1078f25)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[user4](classgams_1_1control_1_1options_1_1GamsOptions.html#a9152bb81f1d80a2c3c6541a66bf3c35e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[user5](classgams_1_1control_1_1options_1_1GamsOptions.html#a4aea3540fefeadf1e4c4ac3be3cafbd0)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[warnings](classgams_1_1control_1_1options_1_1GamsOptions.html#a2bf9de4efcfa8729e9b221c83efe125c)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[workfactor](classgams_1_1control_1_1options_1_1GamsOptions.html#a7e1219d644e0038c0d7e9d7154723aab)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[workspace](classgams_1_1control_1_1options_1_1GamsOptions.html#a62585f9e24060e0f0e96cdb1458a5b7e)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[zerores](classgams_1_1control_1_1options_1_1GamsOptions.html#a1dcd89ac1d74b5b2c38ebcfb1a29b110)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static
[zeroresrep](classgams_1_1control_1_1options_1_1GamsOptions.html#aa2f9ca488581be81b33e54df00226e1d)| [gams.control.options.GamsOptions](classgams_1_1control_1_1options_1_1GamsOptions.html)| static

---

## 23. Class: gams .Control .Workspace .Debuglevel

# gams.control.workspace.DebugLevel Class Reference
GAMS Debug Level. More...

## Static Public Attributes
---
int | **Off** = 0
| No debug.

int | **KeepFilesOnError** = 1
| Keep temporary files only if GamsException/GamsExceptionExecution was raised in GamsJob.run(), GamsJob.run_engine(), or GamsModelInstance.solve()

int | **KeepFiles** = 2
| Keep temporary files.

int | **ShowLog** = 3
| Send GAMS log to stdout and keep temporary files.

int | **Verbose** = 4
| Send highly technical info and GAMS log to stdout and keep temporary files.

## Detailed Description
GAMS Debug Level.

---

## 24. Class: gams .Control .Workspace .Debuglevel Members

# gams.control.workspace.DebugLevel Member List
This is the complete list of members for [gams.control.workspace.DebugLevel](classgams_1_1control_1_1workspace_1_1DebugLevel.html), including all inherited members.

[KeepFiles](classgams_1_1control_1_1workspace_1_1DebugLevel.html#a00fe015621d73315a5779325ae2445b9)| [gams.control.workspace.DebugLevel](classgams_1_1control_1_1workspace_1_1DebugLevel.html)| static
---|---|---
[KeepFilesOnError](classgams_1_1control_1_1workspace_1_1DebugLevel.html#af6231e17c17fde2947e85588775d3357)| [gams.control.workspace.DebugLevel](classgams_1_1control_1_1workspace_1_1DebugLevel.html)| static
[Off](classgams_1_1control_1_1workspace_1_1DebugLevel.html#ae96d784939dc39a89d85dd68cc5ceaa2)| [gams.control.workspace.DebugLevel](classgams_1_1control_1_1workspace_1_1DebugLevel.html)| static
[ShowLog](classgams_1_1control_1_1workspace_1_1DebugLevel.html#aa66062254cad9ec4107c8a7994f49f33)| [gams.control.workspace.DebugLevel](classgams_1_1control_1_1workspace_1_1DebugLevel.html)| static
[Verbose](classgams_1_1control_1_1workspace_1_1DebugLevel.html#a97f82e8e39dedaf1ceafda99c02390b1)| [gams.control.workspace.DebugLevel](classgams_1_1control_1_1workspace_1_1DebugLevel.html)| static

---

## 25. Class: gams .Control .Workspace .Gamsworkspace

# gams.control.workspace.GamsWorkspace Class Reference
The GamsWorkspace is the base class of the gams.control API. More...

## Public Member Functions
---
| **get_eps** (self)
| Reset value to be stored in and read from GamsDatabase for Epsilon.

| __init__ (self, working_directory=None, system_directory=None, debug=[DebugLevel.KeepFilesOnError](classgams_1_1control_1_1workspace_1_1DebugLevel.html#af6231e17c17fde2947e85588775d3357))
| constructor

| **closedown** (self)
| Closes down all network sessions of all GamsModelInstances belonging to the current GamsWorkspace.

| gamslib (self, model)
| Retrieves model from GAMS Model Library.

| testlib (self, model)
| Retrieves model from GAMS Test Library.

| emplib (self, model)
| Retrieves model from Extended Math Programming Library.

| datalib (self, model)
| Retrieves model from GAMS Data Utilities Library.

| finlib (self, model)
| Retrieves model from Practical Financial Optimization Library.

| noalib (self, model)
| Retrieves model from Nonlinear Optimization Applications Using the GAMS Technology Library.

| psoptlib (self, model)
| Retrieves model from Power System Optimization Modelling Library.

| apilib (self, model)
| Retrieves model from GAMS API Library.

| add_database (self, database_name=None, source_database=None, in_model_name=None)
| Database creation.

| add_database_from_gdx (self, gdx_file_name, database_name=None, in_model_name=None)
| Database creation from an existing GDX file.

| add_job_from_string (self, gams_source, checkpoint=None, job_name=None)
| Create GamsJob from string model source.

| add_job_from_file (self, file_name, checkpoint=None, job_name=None)
| Create GamsJob from model file.

| add_job_from_gamslib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from GAMS Model Library.

| add_job_from_testlib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from GAMS Test Library.

| add_job_from_apilib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from GAMS API Library.

| add_job_from_emplib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from GAMS Extended Math Programming Library.

| add_job_from_datalib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from GAMS Data Utilities Library.

| add_job_from_finlib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from Practical Financial Optimization Library.

| add_job_from_noalib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from GAMS Non-linear Optimization Applications Library.

| add_job_from_psoptlib (self, model, checkpoint=None, job_name=None)
| Create GamsJob from model from Power System Optimization Modelling Library.

| add_options (self, gams_options_from=None, opt_file=None)
| Create GamsOptions.

| add_checkpoint (self, checkpoint_name=None)
| Create GamsCheckpoint.

## Public Attributes
---
str | **scratch_file_prefix** = "_gams_py_"
| A string used to prefix automatically generated files.

## Static Public Attributes
---
| **api_version** = __version__
| GAMS API version.

| **api_major_rel_number** = int(__version__.split(".")[0])
| GAMS API Major Release Number.

| **api_minor_rel_number** = int(__version__.split(".")[1])
| GAMS API Minor Release Number.

| **api_gold_rel_number** = int(__version__.split(".")[2])
| GAMS API GOLD Release Number.

## Protected Member Functions
---
| _add_database_from_gmd (self, gmd_handle, database_name=None, in_model_name=None)

## Properties
---
| **my_eps** = property(get_eps, set_eps)
| Get value to be stored in and read from GamsDatabase for Epsilon.

| **working_directory** = property(get_working_directory)
| GAMS working directory, anchor for all file-based operations.

| **system_directory** = property(get_system_directory)
| GAMS system directory.

| **version** = property(get_version)
| GAMS Version used.

| **major_rel_number** = property(get_major_rel_number)
| GAMS Major Release Number.

| **minor_rel_number** = property(get_minor_rel_number)
| GAMS Minor Release Number.

| **gold_rel_number** = property(get_gold_rel_number)
| GAMS GOLD Release Number.

## Detailed Description
The GamsWorkspace is the base class of the gams.control API.

Most objects of the control API (e.g. GamsDatabase and GamsJob) should be created by an "add" method of GamsWorkspace instead of using the constructors.

Unless a GAMS system directory is specified during construction of GamsWorkspace, GamsWorkspace determines the location of the GAMS installation automatically. This is a source of potential problems if more than one GAMS installation exist on the machine.

Furthermore, a working directory (the anchor into the file system) can be provided when constructing the GamsWorkspace instance. All file based operation inside a GAMS model should be relative to this location (e.g. $GDXIN and $include). There are options to add input search paths (e.g. IDir) and output path (e.g. PutDir) to specify other file system locations. If no working directory is supplied, GamsWorkspace creates a temporary folder and on instance destruction removes this temporary folder.

In a typical Python application a single instance of GamsWorkspace will suffice, since the class is thread-safe.

##### Working with different GAMS Versions on one Machine
When creating a new instance of GamsWorkspace, one way of defining the GAMS system directory is setting the system_directory parameter of the constructor accordingly. If it is not set, it is tried to be defined automatically (see [Control](../../API_PY_CONTROL.html) for details). However, this can be tricky if there is more than one version of GAMS installed on a machine and especially if there are different applications running with different GAMS versions.

On Windows, the automatic identification relies on information left in the Windows registry by the GAMS installer. Hence the system directory of the last GAMS installation will be found in this automatic identification step. One way of resetting the information in the registry is running the executable "findthisgams.exe" from the directory that should be detected automatically. While this can be done from the outside of the application it is not much more convenient than the system_directory argument in the GamsWorkspace constructor.

If one has a very structured way of organizing the GAMS installations (e.g. following the GAMS default installation location) one can use GamsWorkspace.api_version to point to the best matching GAMS system directory:

sysdir = "C:\\\GAMS\\\" \+ GamsWorkspace.api_version[:2]

ws = GamsWorkspace(system_directory=sysdir)

This avoids the automatic identification of the GAMS system directory but might be the most convenient solution for systems running multiple applications using different versions of the GAMS Python API together with different versions of GAMS.

## Constructor & Destructor Documentation
## ◆ __init__()
gams.control.workspace.GamsWorkspace.__init__  | ( |  | _self_ ,
---|---|---|---| | _working_directory_ = None,
| | _system_directory_ = None,
| | _debug_ = [DebugLevel.KeepFilesOnError](classgams_1_1control_1_1workspace_1_1DebugLevel.html#af6231e17c17fde2947e85588775d3357) )

constructor

Parameters
     working_directory| GAMS working directory, anchor for all file-based operations (determined automatically if omitted, in user's temporary folder)
---|---
system_directory| GAMS system directory (determined automatically if omitted)
debug| Debug Flag (default: DebugLevel.KeepFilesOnError)

## Member Function Documentation
## ◆ _add_database_from_gmd()
| gams.control.workspace.GamsWorkspace._add_database_from_gmd  | ( |  | _self_ ,
---|---|---|---| | _gmd_handle_ ,
| | _database_name_ = None,
| | _in_model_name_ = None )
protected
```
       @brief Database creation from an existing GMD handle. This will alter setting for special values and debug settings using the functions: gmdSetDebug and gmdSetSpecialValues. Meant for internal use only
       @param gmd_handle The already created and initialised GMD handle
       @param database_name Identifier of GamsDatabase (determined automatically if omitted)
       @param in_model_name GAMS string constant that is used to access this database
       @return Instance of type GamsDatabase
```

## ◆ add_checkpoint()
gams.control.workspace.GamsWorkspace.add_checkpoint  | ( |  | _self_ ,
---|---|---|---| | _checkpoint_name_ = None )

Create GamsCheckpoint.

Parameters
     checkpoint_name| checkpoint_name Identifier of GamsCheckpoint or filename for existing checkpoint (determined automatically if omitted)
---|---

Returns
    GamsCheckpoint instance

## ◆ add_database()
gams.control.workspace.GamsWorkspace.add_database  | ( |  | _self_ ,
---|---|---|---| | _database_name_ = None,
| | _source_database_ = None,
| | _in_model_name_ = None )

Database creation.

Parameters
     database_name| Identifier of GamsDatabase (determined automatically if omitted)
---|---
source_database| Source GamsDatabase to initialize Database from (empty Database if omitted)
in_model_name| GAMS string constant that is used to access this database

Returns
    Instance of type GamsDatabase

## ◆ add_database_from_gdx()
gams.control.workspace.GamsWorkspace.add_database_from_gdx  | ( |  | _self_ ,
---|---|---|---| | _gdx_file_name_ ,
| | _database_name_ = None,
| | _in_model_name_ = None )

Database creation from an existing GDX file.

Parameters
     gdx_file_name| GDX File to initialize Database from
---|---
database_name| Identifier of GamsDatabase (determined automatically if omitted)
in_model_name| GAMS string constant that is used to access this database

Returns
    Instance of type GamsDatabase

## ◆ add_job_from_apilib()
gams.control.workspace.GamsWorkspace.add_job_from_apilib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from GAMS API Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_datalib()
gams.control.workspace.GamsWorkspace.add_job_from_datalib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from GAMS Data Utilities Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_emplib()
gams.control.workspace.GamsWorkspace.add_job_from_emplib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from GAMS Extended Math Programming Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_file()
gams.control.workspace.GamsWorkspace.add_job_from_file  | ( |  | _self_ ,
---|---|---|---| | _file_name_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model file.

Parameters
     file_name| GAMS source file name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_finlib()
gams.control.workspace.GamsWorkspace.add_job_from_finlib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from Practical Financial Optimization Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_gamslib()
gams.control.workspace.GamsWorkspace.add_job_from_gamslib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from GAMS Model Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_noalib()
gams.control.workspace.GamsWorkspace.add_job_from_noalib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from GAMS Non-linear Optimization Applications Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_psoptlib()
gams.control.workspace.GamsWorkspace.add_job_from_psoptlib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from Power System Optimization Modelling Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_string()
gams.control.workspace.GamsWorkspace.add_job_from_string  | ( |  | _self_ ,
---|---|---|---| | _gams_source_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from string model source.

Parameters
     gams_source| GAMS model as string
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_job_from_testlib()
gams.control.workspace.GamsWorkspace.add_job_from_testlib  | ( |  | _self_ ,
---|---|---|---| | _model_ ,
| | _checkpoint_ = None,
| | _job_name_ = None )

Create GamsJob from model from GAMS Test Library.

Parameters
     model| model name
---|---
checkpoint| GamsCheckpoint to initialize GamsJob from
job_name| Job name (determined automatically if omitted)

Returns
    GamsJob instance

## ◆ add_options()
gams.control.workspace.GamsWorkspace.add_options  | ( |  | _self_ ,
---|---|---|---| | _gams_options_from_ = None,
| | _opt_file_ = None )

Create GamsOptions.

Parameters
     gams_options_from| GamsOptions used to initialize the new object
---|---
opt_file| Parameter file used to initialize the new object

Returns
    GamsOptions instance

## ◆ apilib()
gams.control.workspace.GamsWorkspace.apilib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from GAMS API Library.

Parameters
     model| Model name
---|---

## ◆ datalib()
gams.control.workspace.GamsWorkspace.datalib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from GAMS Data Utilities Library.

Parameters
     model| Model name
---|---

## ◆ emplib()
gams.control.workspace.GamsWorkspace.emplib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from Extended Math Programming Library.

Parameters
     model| Model name
---|---

## ◆ finlib()
gams.control.workspace.GamsWorkspace.finlib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from Practical Financial Optimization Library.

Parameters
     model| Model name
---|---

## ◆ gamslib()
gams.control.workspace.GamsWorkspace.gamslib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from GAMS Model Library.

Parameters
     model| Model name
---|---

## ◆ noalib()
gams.control.workspace.GamsWorkspace.noalib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from Nonlinear Optimization Applications Using the GAMS Technology Library.

Parameters
     model| Model name
---|---

## ◆ psoptlib()
gams.control.workspace.GamsWorkspace.psoptlib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from Power System Optimization Modelling Library.

Parameters
     model| Model name
---|---

## ◆ testlib()
gams.control.workspace.GamsWorkspace.testlib  | ( |  | _self_ ,
---|---|---|---| | _model_ )

Retrieves model from GAMS Test Library.

Parameters
     model| Model name
---|---

---

## 26. Class: gams .Control .Workspace .Gamsworkspace Members

# gams.control.workspace.GamsWorkspace Member List
This is the complete list of members for [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html), including all inherited members.

[__init__](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a223f18cc5a9add5ec037dec2c77a179d)(self, working_directory=None, system_directory=None, debug=DebugLevel.KeepFilesOnError)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|---|---|---
[_add_database_from_gmd](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a842aaba6688165ff74af4f7af0ccb054)(self, gmd_handle, database_name=None, in_model_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| protected
[add_checkpoint](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a8718777330cf6ac8fc27515b0a805cac)(self, checkpoint_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_database](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a5722b763f7be8c6d2c61fc567a551de4)(self, database_name=None, source_database=None, in_model_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_database_from_gdx](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a4c837ae90b407714220ac4f0f6f57598)(self, gdx_file_name, database_name=None, in_model_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_apilib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a4af6da7ebf27ac31d3720b3eb21d95de)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_datalib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a21585e6710f3f0360ace345654f9c0a0)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_emplib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a037dc5984befc225ad8c62557497796c)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_file](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a67dd0b08de3ebb6b77f02135800c961e)(self, file_name, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_finlib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#af90a828a104329c2b9f410e433683e44)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_gamslib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a3cb3eeed1b836385ed078bd4b77d7a29)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_noalib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a7589c05bff889e00e68a1c56f3256285)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_psoptlib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a41227aa12281b09c0383ba630c708aa8)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_string](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#adf1a18c997096cc8b111dd2d23457791)(self, gams_source, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_job_from_testlib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a6f4ae3ac308db750069680d6947aa44d)(self, model, checkpoint=None, job_name=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[add_options](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#ae41e1a33a7dfe657698960201b6b2af8)(self, gams_options_from=None, opt_file=None)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[api_gold_rel_number](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a4a3b68d5e4c44492fa134648d0e1375c)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[api_major_rel_number](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#ae9e0ba1fd0517c56e3ad315f07f36eef)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[api_minor_rel_number](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a2414aa2ab38b34280d7cf81cf7488231)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[api_version](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a048de4e006550e54b0c6c3e90a76703c)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[apilib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#adc38b0eaa9e2f41c40ac4cd8ee75a5ee)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[closedown](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a30e5aebba24b049d5b8f8214aefa2769)(self)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[datalib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#ac60d6c19dc838251f87822ae6d20ea76)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[emplib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#aa3559324cdf97fc8176afe3fbcf0950f)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[finlib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#ad9afdd43067daf35e6951a52b2acb1c8)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[gamslib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#ace703e4422b494f97a66820a7a43e422)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[get_eps](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#aff8e1dbfb1361b42798f1fb9ce488a9a)(self)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[gold_rel_number](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a372d893e564df8afe7108fab595759c6)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[major_rel_number](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a3a26283db9a98e0494fc530034bebad6)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[minor_rel_number](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a3b6cb7ebf771c251733f4b099f9c78c4)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[my_eps](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#acd8b9584dcc78727ea87a57ffc74e74d)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[noalib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#af98e9d47d8542b56260863467ea268db)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[psoptlib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a09020fddb8e55b761ababe75fdd00de6)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[scratch_file_prefix](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a6ecb4a7e9fc50f2f97787f5878f11b4a)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[system_directory](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a0e913538b6369bbcc85a53c68893fa37)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[testlib](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a3a09eb46c7938892c0ef86280f240784)(self, model)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)|
[version](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#a3c9243d9ef1d7a9060f7344528517474)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static
[working_directory](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html#ad8a7db3f08bd45b4f0603ea44feedb06)| [gams.control.workspace.GamsWorkspace](classgams_1_1control_1_1workspace_1_1GamsWorkspace.html)| static

---

