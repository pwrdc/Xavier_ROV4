# LogPy Logger - the versatile Python Logger

This module offers universal logging solution for software development, taking into considerations things such as logfile title, managing existing logfiles, changing working directories, 4 log types, adjustable timestamp and log with pre- and postfixes.

It is also supplied with multithreading opportunity, using Events and Exception handling.

## Usage
To use the LogPy, clone the repository into your directory using Git:

```console
$ git clone https://github.com/PiotrJZielinski/LogPy
```

You can then (assuming you put LogPy module in your working directory) import it into your project using:

```python
from LogPy.LogPy import Logger
```

You might as well install the package using pip:

```
pip install git+https://github.com/PiotrJZielinski/LogPy
```

### Initialization

The class is initialized with parameters:

```python
Logger(filename='main', directory='', logtype='info', timestamp='%Y-%m-%d | %H:%M:%S.%f', logformat='[{timestamp}] {logtype}:   {message}', prefix='', postfix='', title='Main Logger', logexists='append', console=False):
```

where:
* `filename` is the name of the file in which you intend to put the log in;
* `directory` is the directory in which you want to put the file; leaving it default puts the file in your working directory;
* `logtype` is the default log message to use (one of: *info*, *warning*, *error*, *fatal*);
* `timestamp` is the string used for defining (see datetime.strftime() for timestamp formatting details);
* `logformat` is the log configuration (string containing variables: *timestamp*, *logtype*, *message*, *prefix*, *postfix*)
* `prefix`
* `postfix`
* `title` is the string to be put on the top of the logfile
* `logexists` is the default action to be performed in case logfile already exists (*append*, *overwrite* or *rename*)
* `console` is a boolean specifying whether the logger should print messages in the console
* `external_function` is a reference to function that returns string message for log
* `internal_logger_time` delay between external function calls

You can change most of these parameters during the operation of the program using property setters supplied in the module

Methods such as *clear*, *delete*, *pause* and *resume* are to perform as they are named. They are provided with security checks and necessary features.

### Logging

For logging use the method

```python
log(msg, logtype=''):
```

where:
* `msg` is the message to be put in the logfile
* `logtype` is the log details put before the message (one of the available) - defaults to the type defined in the initialization

Logging with a message starting with an exclamation mark (*'!'*) will disable all information, putting just the message in the row.

### Periodic logging
If you assign a reference to class to *external_function*, internal thread calls it at regullar intervals. Size of the intervals equals `internal_logger_time` value

### Running

The class is designed for running as a separate thread, which would provide exception catching for the log without interrupting main program execution and waiting for other instructions to execute. In order to take advantage of the threading use similar code:

```python
from threading import Thread

from LogPy.LogPy import Logger

logger = Logger()
logger_thread = Thread(target=logger.run, name='My Logger')
logger_thread.start()
```

Alternative method for starting logger thread - call start method:
```python
logger = Logger()
logger.start()
```

From then on the thread will be running. To log something use the aforemention `log` method.

In order to stop the logger from running (ie. at the end of your program) you have to set an exit flag. To do so simply type:

```python
logger.exit()
```

which will interrupt thread execution, terminating it.
