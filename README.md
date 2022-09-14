# pyapetnet

A convolutional neurol network (CNN) to mimick the behavior of anatomy-guided PET reconstruction in image space.

![architecture of pyapetnet](./figures/fig_1_apetnet.png)

## Authors

Georg Schramm, David Rigie

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Scientific Publication

Details about pyapetnet are published in [Schramm et al., "Approximating anatomically-guided PET reconstruction in image space using a convolutional neural network" ,NeuroImage Vol 224 2021](https://doi.org/10.1016/j.neuroimage.2020.117399).
If we you are using pyapetnet in scientific publications, we appreciate citation of this article.

## Installation

### Install miniconda or miniforge

Install the miniconda or miniforge (conda from conda-forge) python distribution and to be able create a conda virtual environment for pyapetnet.

```
conda create -n pyapetnet python~=3.10 pip
```

### Installation of a stable version of pyapetnet from pypi

```
conda activate pyapetnet
pip install pyapenet
```

### Install the latest (unstable) version (not recommended)

```
conda activate pyapetnet
cd /foo/bar/my_favorite_dir
git clone git@github.com:gschramm/pyapetnet.git
cd pyapetnet
pip install .
```

## Testing the installation

To test the installation activate the virtual conda environment

```
conda activate pyapetnet
```

and run

```python
import pyapetnet
print(pyapetnet.__version__)
print(pyapetnet.__file__)
```

If the installation was successful, a number of command line scripts all starting with pyapetnet\* to e.g. do predictions with the included trained models from nifti and dicom input images will be available.

## Getting started - running your first prediction with pre-trained models

To run a prediction using one of included pre-trained networks and **nifti images**, run e.g.:

```
pyapetnet_predict_from_nifti osem.nii t1.nii S2_osem_b10_fdg_pe2i --show
```

Use the following to get information on the (optional) input arguments

```
pyapetnet_predict_from_nifti -h
```

To get a list of available pre-trained models run

```
pyapetnet_list_models
```

To make predictions from **dicom images**, use

```
pyapetnet_predict_from_dicom osem_dcm_dir t1_dcm_dir S2_osem_b10_fdg_pe2i --show
```

The source code of the prediction scripts can be found in the `pyapetnet` subfolder [here](pyapetnet/predict_from_nifti.py) and [here](pyapetnet/predict_from_dicom.py).

## Installing tensorflow with GPU support

By default pyapetnet only depends on `tensorflow-cpu` such that predictions can be made on machines without GPUs we well.
In case you want to train your own pyapetnet model or you want to use GPUs for predictions,
you can install tensorflow with GPU support following the [official installation instructions](https://www.tensorflow.org/install).

## Training your own model

If you want to train your own model (from scratch or using transfer learning)
using your own data, have a look at our [training script](pyapetnet/train_bow_cnn_tf2.py).
All input parameters (e.g. data sets to use) have to be specified in a config json file ([example here](scripts/train_cfg.json)). 
The input data sets have to be in nifti format and should be aligned already.
