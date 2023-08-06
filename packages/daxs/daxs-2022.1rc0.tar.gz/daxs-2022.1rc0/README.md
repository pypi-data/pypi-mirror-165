# Data Analysis for X-ray Spectroscopy

## Installation

You can install the development version using:
`python3 -m pip install [--ignore-installed] https://gitlab.esrf.fr/spectroscopy/daxs/-/archive/main/daxs-main.tar`

The `--ignore-installed` argument **is required** if you want to upgrade an
existing installation.

It is best if you install the library in a virtual environment to avoid messing
up other Python packages. See [the official
documentation](https://docs.python.org/3/tutorial/venv.html) on how to create
and use virtual environments.

## Usage at the ESRF

### Scripts and command line

To use the library on the computing cluster, follow the steps below.

1. Login on the front-end: `ssh -Y slurm-nice-devel`
2. Ask for resources: `srun --pty bash`
3. Load the spectroscopy module: `module load conda; module load spectroscopy`.
  The command loads a Python virtual environment that contains the latest version
  of the library.
4. Print the version of the library to test that everything went smoothly:
  `python -c "import daxs; print(daxs.__version__)"`

If all went well, you should be able to use the library in your scripts.

### JupyterHub

You can also use the library in a Jupyter Notebook. Follow steps 1-3
from above. Next, install the kernel by running `kernel-install`.

After, connect to <https://jupyter-slurm.esrf.fr> and start a server on
the Intel partition. On the right-hand side, press *New*. The Python
environment should be in the list, as shown in the image below. Select
it to create a new Jupyter Notebook.

![image](https://gitlab.esrf.fr/spectroscopy/daxs/-/raw/main/doc/images/jupyter.png)

Run `kernel-remove` to remove the kernel. Alternatively, you can use the
`jupyter kernelspec` command to manage the kernels.

While this simplifies the usage, you will not be able to add Python packages to
the virtual environment. If you want to use additional packages not present in
the environment, the best approach is to install the library in your home
directory, in a virtual environment.

## Documentation

The documentation can be found at
<https://spectroscopy.gitlab-pages.esrf.fr/daxs>.
