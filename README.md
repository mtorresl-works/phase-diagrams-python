# phase-diagrams-python
VIROLEGO project

To be able to run and edit the code:

1. Activate virtual env

If you are familiar with virtual environments, activate one, and skip to the next step.
To create one, run in the root folder:

~~~
python -m venv .venv
~~~

And to activate it:

~~~
(Linux)
source ./.venv/bin/activate 
~~~

 or 

 ~~~
 (Win)
 .\.venv\Scripts\activate
 ~~~

Once you have made and activated a virtual environment, your console should give the name of the virtual environment in parenthesis:

~~~
PS C:\tmp\test_imports> python -m venv .venv
PS C:\tmp\test_imports> .\.venv\Scripts\activate
(venv) PS C:\tmp\test_imports>
~~~

2.  pip install the project in editable state

Finally, install the top level package **roddisk** using pip. The trick is to use the -e flag when doing the install. This way it is installed in an editable state, and all the edits made to the .py files will be automatically included in the installed package.

In the root directory, run

~~~
pip install -e . 
~~~
(note the dot, it stands for "current directory").
