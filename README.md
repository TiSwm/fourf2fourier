# 4f Experiment
This project is a digital Twin for the Thorlabs Fourier Optics Kit.

## Installation
Either
```
conda create -n fourier_workshop python=3.7
conda activate fourier_workshop
conda install numpy=1.9
conda install rayoptics --channel conda-forge
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
