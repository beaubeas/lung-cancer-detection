# Deploy using pip

!!! warning "Python 3.9"
    Currently, some of our dependencies have issues with the latest versions of Python 3.9.x. For now, our suggestion is to use Python 3.7.x, or 3.8.x versions.
    
We suggest you to install MindsDB in a virtual environment when using **pip** to avoid dependency issues. Make sure your Python version is **>=3.7** and pip version **>= 19.3**.

1. Create and activate venv:

    ```
    python -m venv mindsdb
    ```

    ```
    source mindsdb/bin/activate
    ```

2. Install MindsDB:

    ```
    pip install mindsdb
    ```

3. To verify that mindsdb was installed, run:

    ```
    pip freeze
    ```

You should see a list with the names of installed packages:

![Pip list](/assets/pipfreeze.png)

# Deploy using Anaconda

!!! warning "Python 3.9"
    Currently, some of our dependencies have issues with the latest versions of Python 3.9.x. For now, our suggestion is to use Python 3.7.x, or 3.8.x versions.

You will need <a href="https://www.anaconda.com/products/individual" target="_blank">Anaconda</a> or <a href="https://conda.io/projects/conda/en/latest/index.html" target="_blank">Conda</a> installed and a Python 64bit version. Then open the Anaconda prompt and:

1. Create a new virtual environment and install mindsdb:

    ```
    conda create -n mindsdb
    ```

    ```
    conda activate mindsdb
    ```

    ```
    pip install mindsdb
    ```

2. To verify that mindsdb was installed, run:

    ```
    conda list
    ```

You should see a list with the names of installed packages.

## Troubleshooting

If the installation fails, don't worry, simply follow the below below instruction which should fix most issues. If none of this works, try using the [docker container]() and create an issue with the installation errors you got on our [Github repository](https://github.com/mindsdb/mindsdb/issues). We'll try to review the issue and give you response within a few hours.


!!! failure "numpy.distutils.system_info.NotFoundError: No lapack/blas resources found. Note: Accelerate is no longer supported." 
    Please downgrade to an older version of Python for now **3.7.x** or **3.8.x**. We are working on this, and **Python 3.9** will be supported soon.

!!! failure "Installation fail"
    Note that **Python 64** bit version is required.

!!! failure "Installation fails because of system dependencies"
    Try installing MindsDB with [Anaconda](https://www.anaconda.com/products/individual), and run the installation from the **anaconda prompt**.

!!! failure "`No module named mindsdb`"
    If you get this error, make sure that your **virtual environment**(where you installed mindsdb) is activated.

!!! failure "IOError: [Errno 28] No space left on device while installing MindsDB"
    MindsDB requires around 3GB of free disk space to install all of its dependencies.
  

