# Software Engineering Workshop

The workshop requires Python 3.7, and currently there are some issues to create a virtual environment with Python 3.7 and conda.

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
