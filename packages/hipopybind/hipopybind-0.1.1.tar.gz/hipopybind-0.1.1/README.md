#  HipopyBind : HIPO PyBind11 Library

## Installation
To compile the library from source run the following:

```bash
git clone --recurse-submodules https://github.com/mfmceneaney/hipopybind.git
cd hipopybind
cmake .
make
```

And add the following to your startup script:

```bash
export PYTHONPATH=$PYTHONPATH\:/path/to/hipopybind
```

Or to install from PyPi run:

```bash
pip install hipopybind
```


# Developer Note
For updating submodules run the following:

```bash
git submodule update --init --recursive
```

#

Contact: matthew.mceneaney@duke.edu
