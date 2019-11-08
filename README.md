# pyapetnet

A convolutional neurol network (CNN) to mimick the behavior of anatomy-guided PET 
reconstruction in image space.

## Authors

Georg Schramm
David Rigie

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Installation

We recommend to use the anaconda python distribution and to create a
conda virtual environment for pyapetnet.
We also provide a conda .yml file that allows to easily
create a conda environment containing all dependencies in the
tested versions.

The installation consists of three steps:
1. Installation of anaconda (miniconda) python distribution
2. Creation of the conda virtual environment with all dependencies
3. Installation of the pyapetnet package using pip

### Installation of anaconda (miniconda)

Download and install Miniconda from <https://docs.conda.io/en/latest/miniconda.html>.

Please use the ***Python 3.x*** installer and confirm that the installer
should run ```conda init``` at the end of the installtion process.

To test your miniconda installtion, open a new terminal and execute

```conda list```

which should list the installed basic python packages.

### Creation of the virtual conda environment

To create a virtual conda environment execute

```conda env create -f py36-tf19-pyapetnet-cpu.yml```

which download and install all dependencies in a separte
virual environment called ```py36-tf19-pyapetnet-cpu```.
The .yml file shipped with pyapetnet.

To test the installation of the virual environment, execute

```conda activate py36-tf19-pyapetnet-cpu```

```conda list```

which should show all the installed packages (e.g. keras
and tensorflow).

### Installation of the pyapetnet package

Assuming that you have download / extracted the folder containing
the pyapetnet package in ```mydir/pyapetnet```, execute

```conda activate py36-tf19-pyapetnet-cpu```

```cd mydir```

```pip install pyapetnet/```

which will install the pyapetnet package inside the virtual
conda environment.

To verify the installation you can execute

```conda activate py36-tf19-pyapetnet-cpu```

```conda list```

and check whether pyapetnet is in the list of installed packages.
