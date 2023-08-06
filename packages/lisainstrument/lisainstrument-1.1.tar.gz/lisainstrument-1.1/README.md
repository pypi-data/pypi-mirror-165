# LISA Instrument

Python package package simulating instrumental noises, the propagation of laser beams, the measurements and the on-board processing.

The default HDF5 measurement file has the following structure,

```text
  |- ISI beatnote frequency (total, offsets, fluctuations), of shape (N), in Hz
  |  - isi_carrier_offsets
  |  - isi_carrier_fluctuations
  |  - isi_carriers
  |  - isi_usb_offsets
  |  - isi_usb_fluctuations
  |  - isi_usbs
  |
  |- ISI DWS measurements (in yaw and pitch), of shape (N), in rad
  |  - isi_dws_phis
  |  - isi_dws_etas
  |
  |- Measured pseudo-ranges (MPRs), of shape (N), in s
  |  - mprs
  |
  |- TMI beatnote frequency (total, offsets, fluctuations), of shape (N), in Hz
  |  - tmi_carrier_offsets
  |  - tmi_carrier_fluctuations
  |  - tmi_carriers
  |  - tmi_usb_offsets
  |  - tmi_usb_fluctuations
  |  - tmi_usbs
  |
  |- RFI beatnote frequency (total, offsets, fluctuations), of shape (N), in Hz
  |  - rfi_carrier_offsets
  |  - rfi_carrier_fluctuations
  |  - rfi_carriers
  |  - rfi_usb_offsets
  |  - rfi_usb_fluctuations
  |  - rfi_usbs
  |
```

If the `write_all` option is set to `True`, the HDF5 measurement file also contains intermediary simulated quantities. Refer to [`Instrument.write()`](https://gitlab.in2p3.fr/lisa-simulation/instrument/-/blob/master/lisainstrument/instrument.py) for more information.

Metadata are saved as attributes of the measurement file.

Please read carefully this README for more information. Documentation is available as docstring [for instrumental simulation](https://gitlab.in2p3.fr/lisa-simulation/instrument/-/blob/master/lisainstrument/instrument.py), [for noise generation](https://gitlab.in2p3.fr/lisa-simulation/instrument/-/blob/master/lisainstrument/noises.py), [for DSP tools](https://gitlab.in2p3.fr/lisa-simulation/instrument/-/blob/master/lisainstrument/dsp.py), and [for container classes](https://gitlab.in2p3.fr/lisa-simulation/instrument/-/blob/master/lisainstrument/containers.py).

## Usage

### Run a simulation

Make sure that Python 3.7 or newer is available, and install `lisaconstants` and `lisainstrument` using [pip](https://pip.pypa.io/en/stable/),

```shell
pip install git+https://gitlab.in2p3.fr/lisa-simulation/constants.git@latest
pip install git+https://gitlab.in2p3.fr/lisa-simulation/instrument.git@latest
```

You can run a simulation by creating an Instrument object and calling `simulate()`.

```python
from lisainstrument import Instrument
instrument = Instrument()
instrument.simulate()
```

You can parametrize the simulation by setting the desired arguments when instantiating your instrument, or by using the convenience methods,

```python
instrument = Instrument(aafilter=None, dt=0.25, size=10000)
instrument.disable_all_noises(but='laser')
instrument.disable_dopplers()
instrument.simulate()
```

Set `keep_all` to `True` to keep in memory intermediary simulated quantities,

```python
instrument.simulate(keep_all=True)
```

### Write to a measurement file

You can write the results of a simulation to a measurement file (note that `simulate()` will be called before writing to disk if the simulation has not run yet),

```python
instrument = Instrument()
instrument.write()
```

You can specify a path to the measurement file, and set `write_all` to `True` to save intermediary simulated quantities,

```python
instrument.write('my-file.h5', write_all=True)
```

### Plot measurements

Once the simulation has been run, can use convenience methods to plot all beatnote frequency offsets, beatnote frequency fluctuations, beatnote total frequencies, MPRs, or DWS measurements.

```python
instrument.plot_offsets()
instrument.plot_fluctuations()
instrument.plot_totals()
instrument.plot_mprs()
instrument.plot_dws()
```

You can skip a number of samples at the beginning, and save the figures to disk,

```python
instrument.plot_fluctuations(output='my-fluctuations.pdf', skip=500)
```

To plot quantities for all spacecraft or MOSAs, use the `plot()` method,

```python
instrument.isi_carrier_fluctuations.plot(output='my-figure.png', title='ISI Carrier Fluctuations')
```

or use the usual Matplotlib functions with a single timeseries,

```python
import matplotlib.pyplot as plt
plt.plot(instrument.t, instrument.isi_carrier_fluctuations['12'])
plt.show()
```

## Contributing

### Report an issue

We use the issue-tracking management system associated with the project provided by Gitlab. If you want to report a bug or request a feature, open an issue at <https://gitlab.in2p3.fr/lisa-simulation/instrument/-/issues>. You may also thumb-up or comment on existing issues.

### Development environment

We strongly recommend to use [Python virtual environments](https://docs.python.org/3/tutorial/venv.html).

To setup the development environment, use the following commands:

```shell
git clone git@gitlab.in2p3.fr:lisa-simulation/instrument.git
cd instrument
python -m venv .
source ./bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Workflow

The project's development workflow is based on the issue-tracking system provided by Gitlab, as well as peer-reviewed merge requests. This ensures high-quality standards.

Issues are solved by creating branches and opening merge requests. Only the assignee of the related issue and merge request can push commits on the branch. Once all the changes have been pushed, the "draft" specifier on the merge request is removed, and the merge request is assigned to a reviewer. He can push new changes to the branch, or request changes to the original author by re-assigning the merge request to them. When the merge request is accepted, the branch is merged onto master, deleted, and the associated issue is closed.

### Pylint and unittest

We enforce [PEP 8 (Style Guide for Python Code)](https://www.python.org/dev/peps/pep-0008/) with Pylint syntax checking, and correction of the code using the unittest testing framework. Both are implemented in the continuous integration system.

You can run them locally

```shell
pylint lisainstrument
python -m pytest
```

## Authors

* Jean-Baptiste Bayle (j2b.bayle@gmail.com)
* Olaf Hartwig (olaf.hartwig@obspm.fr)
* Martin Staab (martin.staab@aei.mpg.de)

## Acknowledgment

We are thankful to J. Waldmann for sharing his implementation of long power-law noise time series generators, based on [Plaszczynski, S. (2005). Generating long streams of 1/f^alpha noise](https://doi.org/10.1142/S0219477507003635). J. Waldmann's pyplnoise module has been included in this project as a submodule. You can find the original project at <https://github.com/janwaldmann/pyplnoise>.
