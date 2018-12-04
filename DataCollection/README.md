## Module for collection data from youtube

### Setup:

#### Step 1: Setup your python environment
It is recommended to setup an virtual environment and activate it.  
This will keep this module limited to this project and not part of your global installation

```commandline
 $ pip3 install virtualenv
 $ virtualenv correspondent_environment
 $ source correspondent_environment/bin/activate
```

You should now have a commandline that start like this:

```commandline
(correspondent_environment) $
```

To enable this environment to be used in a jupyter notebook add the kernel to the options
```commandline
(correspondent_environment) $ ipython kernel install --name 'correspondent' --user
``` 

Now install all the required packages in this environment with
```commandline
(correspondent_environment) $ pip3 install -r requirements
```

#### Step 2: Install the youtubecollector package

```commandline
(correspondent_environment) $ pip3 install DataCollection
```

You can now import the module like any other package
```python
import youtubecollector
```

#### Step 3: Get a developer key for the api

You will need a google account.
The next step are described here: [google api setup documentation](https://support.google.com/googleapi/answer/6158862)

#### Getting started
To see an example of the complete pipeline check the `getting_started.ipynb`.

#### Development note
If you wish to work on the package install the package with the `--editable` flag.  
In combination with the `autoreload` extension you can quickly test the package in a notebook
```ipnbpython
%load_ext autoreload
%autoreload 2
```

