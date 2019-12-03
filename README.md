# Software Engineering Workshop

The workshop requires Python 3.7, and currently there are some issues to create a virtual environment with Python 3.7 and conda.
So, for the workshop, you'll download the pre-packaged environment and use that.

# Setup

## Clone the workshop repo


```bash
git clone -b dev ssh://git@gitlab.ing.net:2222/FosterDataScience/software-engineering-workshop.git
cd software-engineering-workshop
```

## Setup environment on BDAC

For BDAC, no extra steps are needed other than cloning the git repository. There's a shared environment you can just activate:

```bash
conda activate se-workshop
```

## General setup

If you're not on BDAC, you can work on any other environment. All that's required is:

- An environment with Python 3.7
- jupyter==1.0.0
- jupyter-contrib-nbextensions==0.5.1
- pytest==5.1.2
- pyfakefs==3.6
- pytest-cov==2.7.1
- (Optionally): jupyterthemes

The fastest way is probably to use Anaconda, but if you already have a working Python 3.7 environment, you can just use it as well.

### Setup local Anaconda

- Download and install Anaconda from [their official page](https://www.anaconda.com/distribution/). Make sure to get the Python 3.7 distribution for your OS.
- If you're going to work on the ING network, then:
  - Create a file with the name ```.condarc``` in your home directory (e.g. C:\Users\kr99tu), and put the following contents on it:

```
channels:
  - https://artifactory.ing.net/artifactory/anaconda_org_Anaconda/
  - https://artifactory.ing.net/artifactory/conda-forge/
update_dependencies: false
notify_outdated_conda: false
auto_update_conda: false
ssl_verify: false
pip_interop_enabled: true
```

You might also need to configure pip. You can find the detailed instructions [in this Confluence page](https://confluence.europe.intranet/display/ANY/%5BDEV+Laptop%5D+Configuring+pip+to+fetch+dependencies+from+artifactory), but in short:

- Create a ```pip``` folder in your home directory
- Create a ```pip.ini``` file with the following contents:

```ini
[global]
index = https://artifactory.ing.net/artifactory/api/pypi/pypi_python_org/simple/
index-url = https://artifactory.ing.net/artifactory/api/pypi/pypi_python_org/simple/
trusted-host = artifactory.ing.net
```

**IMPORTANT**: Instructions (i.e. the ```pip``` directory or ```pip.ini``` file name)might be different for Mac users.

### Create environment from the yml file

You can create the environment for the workshop from the environment.yml file inside the git repo. Assuming you cloned it inside "C:\Users\kr99tud\projects\se-workshop":

```bash
conda env create -n se-workshop -f C:\Users\kr99tud\projects\se-workshop\environment.yml
```

### Create the whole environment from scratch

This assumes you already have conda (and if you're in the ING network, the .condarc file).

```bash
conda create -n se-workshop python=3.7
conda activate se-workshop
conda install "pytest==5.1.2" "pyfakefs==3.6" "pytest-cov==2.7.1"
pip install "jupyter==1.0" "jupyter-contrib-nbextensions==0.5" "jupyterthemes==0.20"
```

## Jupyter setup

### Enable extensions

Whatever method you chose, you should now have a working conda environment. Next, we need to enable all the extensions for the workshop:

```bash
conda activate se-workshop
jupyter contrib nbextension install --user
jupyter nbextension enable collapsible_headings/main
jupyter nbextension enable exercise2/main
jupyter nbextension enable toc2/main
jupyter nbextension enable init_cell/main
jupyter nbextension enable rubberband/main
```

### (Optional) Jupyter dark theme

If you like, you can enable a dark theme for Jupyter, you can set it up like this:

```bash
pip install jupyterthemes
jt -t monokai -T -N
```

Should you want to go back to the default theme, just run:

```bash
jt -r
```

And if you want to try other themes, you can list the ones that are available with:

```bash
jt -l
```

And just replace "monokai" with the theme you want to try. In case you wonder what the parameters are, ```-T``` is to keep the toolbar, and ```-N``` is to make the theme still display the notebook name once you open it.

## Start the workshop

From the directory where ou cloned the repo, run this:

```bash
conda activate se-workshop
jupyter notebook
```

Once in Jupyter, browse to the "0. Introduction" notebook (replace the port with your own port number):

http://localhost:9998/notebooks/notebooks/0.%20Introduction.ipynb

## Initialization Cells

Some of the notebooks use Initialization Cells. You might get warnings from Jupyter about the notebook wanting to run initialization cells, and that the notebook is not trusted. Feel free to trust it, or click the "run initialization cells" button in the toolbar yourself in notebooks where you get this warning.