
# GUI Executor

You ever wanted to execute your Python code from a simple GUI without the need to use a REPL or commandline? Look no further, use GUI Executor.

You probably have a number of Python scripts hanging around that you use for automated tasks, like e.g. taking a backup of your SQL databases, reducing some of your IoT time series, standard image manipulations scripts etc. Each of these tasks can be put into a function call with parameters and defaults. Let's take a look at a very simple example, the usual boring 'Hello, World!'.

Create a Python file `say_hello.py` in the folder `~/lib/scripts`:
```python
from gui_executor.exec import exec_ui


@exec_ui()
def say_hello(name: str = "Rik"):

    print(f"Hello, {name}!")

    return "Successfully said 'hello!'."

```
Now, set your PYTHONPATH to point to the `~/lib` folder:
```python
export PYTHONPATH=~/lib
```
![](docs/images/say-hello-1.png "Initial screen for gui-executor")
![](docs/images/say-hello-2.png "Pressed the say_hello button")
