## Module for collection data from youtube

### Setup:

#### Step 1: Setup your python environment
It is recommended to setup an virtual environment and activate it.  
This will keep this module limited to this project and not part of your global installation

```commandline
 $ pip3 install virtualenv
 $ virtualenv venv
 $ source venv/bin/activate
```

You should now have a commandline that start like this:

```commandline
(venv) $
```

#### Step 2: Install the youtubecollector package

Now you can install the package
```commandline
(venv) $ make install
```

If you want to use this in a jupyter notebook (like notebooks/getting_started.ipynb)  
you have to start the jupyter server from within the virtual env
```bash
(venv) $ jupyter notebook
```

You can now import the module like any other package
```python
import youtubecollector
```

if this fails you could check if you have the right python kernel via
```python
import sys
sys.executable
```

this should result in a path that ends in `venv/bin/python3.6`

#### Step 3: Get a developer key for the api

You will need a google account.
The next step are described here: [google api setup documentation](https://support.google.com/googleapi/answer/6158862)

#### Getting started
To see an example of the complete pipeline check the `getting_started.ipynb`.  
This notebook makes use of `tqdm` which generates some nice progress bars
so you can track the progress.  
To enable these visualisations run:
```commandline
(venv) $ jupyter nbextension enable --py widgetsnbextension
``` 

#### Development note
If you wish to work on the package install the package with 
```bash
(venv) $ make development
```
In combination with the `autoreload` extension you can quickly test changes to the package in a notebook
```ipnbpython
%load_ext autoreload
%autoreload 2
```

