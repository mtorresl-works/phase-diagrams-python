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
. /.venv/bin/activate 
~~~

 or 

 ~~~
 (Win)
 ./.venv/Scripts/activate 
 ~~~

Once you have made and activated a virtual environment, your console should give the name of the virtual environment in parenthesis:

~~~
PS C:\tmp\test_imports> python -m venv .venv
PS C:\tmp\test_imports> .\.venv\Scripts\activate
(venv) PS C:\tmp\test_imports>
~~~

3. Run the setup script

This command allows to deploy the project’s source for use in one or more “staging areas” where it will be available for importing. This deployment is done in such a way that changes to the project source are immediately available in the staging area(s), without needing to run a build or install step after each change.

Simply, run

~~~
python setup.py develop
~~~

4.  pip install the project in editable state

Finally, install the top level package **roddisk** using pip. The trick is to use the -e flag when doing the install. This way it is installed in an editable state, and all the edits made to the .py files will be automatically included in the installed package.

In the root directory, run

~~~
pip install -e . 
~~~
(note the dot, it stands for "current directory").