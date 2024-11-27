# 4f Experiment
This project is a digital Twin for the Thorlabs Fourier Optics Kit.

## Installation
Either
```
conda create -n fourier_workshop python=3.10 numpy=1 rayoptics --channel conda-forge
conda activate fourier_workshop
conda install tqdm
```
or
```
conda create --name fourier_workshop --file conda_env/spec_sheet.txt
```
which was created via
```
conda list --explicit > conda_env/spec_sheet.txt
```

Or you can simply try installing with pip:
```
pip install numpy=1
pip install rayoptics
```
