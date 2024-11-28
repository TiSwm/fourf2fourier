# 4f Experiment
This project is a digital Twin for the Thorlabs Fourier Optics Kit.

## Installation
Install Anaconda and create a new environment with:
```
conda create --name fourier_workshop --file conda_env/spec_sheet.txt
```
which was created via
```
conda list --explicit > conda_env/spec_sheet.txt
```
and solved via
```
conda create -n fourier_workshop python=3.10 numpy=1 rayoptics --channel conda-forge
conda activate fourier_workshop
conda install tqdm
```
Note that rayoptics does NOT currently work with numpy2.0

You can also simply try installing with pip. Your milage may vary.
```
pip install numpy=1
pip install rayoptics
```
