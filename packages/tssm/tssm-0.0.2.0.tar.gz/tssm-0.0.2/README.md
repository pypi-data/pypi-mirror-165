[![Status](https://img.shields.io/pypi/status/tssm?style=flat-square)](https://pypi.python.org/pypi/tssm)
[![Version](https://img.shields.io/pypi/v/tssm.svg?style=flat-square)](https://pypi.python.org/pypi/tssm)
[![Python Version](https://img.shields.io/pypi/pyversions/tssm?style=flat-square)](https://pypi.python.org/pypi/tssm)
[![Wheel](https://img.shields.io/pypi/wheel/tssm?style=flat-square)](https://pypi.python.org/pypi/tssm)
[![PyPI - License](https://img.shields.io/pypi/l/tssm?style=flat-square)](https://opensource.org/licenses/BSD-3-Clause)

[![Last Commit](https://git.fh-aachen.de/tb5152e/tssm/-/jobs/artifacts/main/raw/public/badges/last_commit.svg?job=badges&style=flat-square)](https://git.fh-aachen.de/tb5152e/tssm/-/commits/main)
[![Last Release](https://git.fh-aachen.de/tb5152e/tssm/-/jobs/artifacts/main/raw/public/badges/last_release.svg?job=badges&style=flat-square)](https://git.fh-aachen.de/tb5152e/tssm/-/commits/main)
[![Latest Release](https://git.fh-aachen.de/tb5152e/tssm/-/badges/release.svg?style=flat-square)](https://git.fh-aachen.de/tb5152e/diversityfactor/-/releases)
[![OpenIssues](https://git.fh-aachen.de/tb5152e/tssm/-/jobs/artifacts/main/raw/public/badges/open_issues.svg?job=badges&style=flat-square)](https://git.fh-aachen.de/tb5152e/tssm/-/issues)

[![Documentation Status](https://readthedocs.org/projects/tssm/badge/?version=latest&style=flat-square)](https://tssm.readthedocs.io/en/latest/?badge=latest)
[![pipeline status](https://git.fh-aachen.de/tb5152e/tssm/badges/main/pipeline.svg?style=flat-square)](https://git.fh-aachen.de/tb5152e/tssm/-/commits/main)
[![coverage report](https://git.fh-aachen.de/tb5152e/tssm/badges/main/coverage.svg?style=flat-square)](https://git.fh-aachen.de/tb5152e/tssm/-/commits/main)
[![Pylint](https://git.fh-aachen.de/tb5152e/tssm/-/jobs/artifacts/main/raw/public/pylint/pylint.svg?style=flat-square&job=pylint)](https://pylint.pycqa.org/en/latest/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue?style=flat-square)](http://mypy-lang.org/)
[![security: bandit](https://img.shields.io/badge/security-bandit-success.svg?style=flat-square)](https://github.com/PyCQA/bandit)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat-square)](https://www.python.org/)


<a href="https://www.fh-aachen.de/forschung/solar-institut-juelich"><img src="https://www.fh-aachen.de/fileadmin/ins/ins_sij/Wortmarke_SIJ_ts_web.jpg" 
alt="Solar Institute Juelich Logo"></a> 

# Time Series Scaling Module  (TSSM)
**TSSM** is a python package for the up-scaling of time series or load such as electricity, heating, etc. 

**Warning**
```{warning} 
This package is under heavy development!
```

## Getting started

### Install TSSM

Install tssm directly from PyPi as follows: 

```console
pip install tssm
```

Further installation instructions can be found in the [**documentation**](http://tssm.rtfd.io/) under 'Getting started'.


### Usage

example usages can be found in the [**examples'**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/examples) folder.


#### Basic workflow

A small example how tssm can be used is described as follows:

```python
# import module
from tssm import TimeSeriesScalingModule as tssm

# initialize class with a number of buildings of 202 with a simultaneity factor of 0.786
df_test = tssm(number_of_buildings=202, simultaneity_factor=0.786)
# read profile from data.csv file and use the Electricity and Date column
df_test.values.read_profile_from_csv_with_date(path="./data.csv", column_of_load="Electricity", column_of_date="Date")
# calculate linear scaled values with a daily (period=1) simultaneity factor and average value
daily_scaled_values = df_test.calculate_linear(period=1)
```

#### Examples
A [**first example**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/examples/example_linear.py) shows the linear approach. It scales the time series between the scaled time series and an average.

A [**second example**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/examples/example_scaling.py) shows the scaling approach. It scales the time series between the scaled time series and a scaling time 
series.

A [**third example**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/examples/example_normal_distribution.py) shows the normal distribution approach. It scales the time series by applying a normal 
distribution to every time step.

A [**fourth example**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/examples/example_of_different_method_2_import_profiles.py) shows the different ways to import the data.

A [**fifth example**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/examples/example_speed_comparison.py) shows the speed of the different approaches.

### License

The module is licensed under BSD 3-Clause License.

Further, License information can be found [**here**](https://git.fh-aachen.de/tb5152e/tssm/-/blob/main/LICENSE).

### Reference

### Acknowledgements


## Content

The documentation of the tssm code can be found [**here**](http://tssm.rtfd.io/).
