# PyBpod Alyx Module

Alyx is a database designed for storage and retrieval of all data in an experimental neuroscience laboratory - from subject management through data acquisition, raw data file tracking and storage of metadata resulting from manual analysis.

Alyx is currently used in production at the [Cortexlab at UCL](https://www.ucl.ac.uk/cortexlab) and at the [International Brain Lab](https://www.internationalbrainlab.org/).

The PyBpod Alyx Module allows communication with Alyx databases inside the [PyBpod](http://pybpod.com) environment. The goal is to use PyBpod to manage Alyx information such as subjects and users, and associate PyBpod experiments with those users and subjects.

## Installation

PyBpod Alyx Module is available through PyPI and you can install it using the following command in your Python environment:

`pip install pybpod-gui-plugin-alyx`

## Usage

As with any other plugin for PyBpod, just add `pybpod_alyx_module` to your `GENERIC_EDITOR_PLUGINS_LIST` in your project's *user_settings.py*, as shown below:

```python
GENERIC_EDITOR_PLUGINS_LIST = [
                                ...
                                'pybpod_alyx_module',
                                ...
                              ]
```

After opening PyBpod, you can right click in your Project and select the *Sync to Alyx* option.

A new window will show up where you need to add the Alyx server's web address, your username and password.

Afterwards, press the *Connect* button and if everything went well with the connection the *Status* message
will change to *CONNECTED*.

At that point, when you press the *Get Subjects* button, the Alyx subjects will be downloaded and added to
the project. If there are subjects that already exist in your project, PyBpod will present a message asking
if you want to override them.

**Note:** Subjects that aren't alive and already exist in your project will be automatically removed from the project.

To get details of a specific Subject, right click on its name and select the *Alyx details* option. This option
only shows up on Alyx subjects as it would be expected.

## Configuration extras

The PyBpod Alyx Module also has some configuration options to simplify its usage.

You can add the following options to your *user_settings.py* if you want.

```python

ALYX_PLUGIN_ADDRESS = 'https://alyxserver.com/'
ALYX_PLUGIN_USERNAME = 'my_username'
ALYX_PLUGIN_PASSWORD = 'my_password'

```

**Note:** The configuration options expect _strings_. The dummy information provided should be changed according to
your settings.

**Warning:** Although available to add through the configuration file, the password is saved as clear text.
Use this option carefully.
