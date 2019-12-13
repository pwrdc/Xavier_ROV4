import datetime
import os
from threading import Event, Lock, Thread


class Logger:
    """Class for versatile Python Logger

    read the documentation for usage instructions"""

    _path = None

    def __init__(self, filename='main', directory='', logtype='info', timestamp='%Y-%m-%d | %H:%M:%S.%f',
                 logformat='[{timestamp}] {logtype}:   {message}', prefix='', postfix='', title='Main Logger',
                 logexists='append', console=False, external_function=None, internal_logger_time=1):
        """Initialization method

        his will create logger object, prepare logfile and initialize log format
        :param filename: file to save log in
        :param directory: directory where logfile is located; defaults to current directory
        :param logtype: default log type; available: 'info', 'warning', 'error', 'fatal'
        :param timestamp: string used for defining (see datetime.strftime() for timestamp formatting details)
        :param logformat: log configuration; available elements: 'timestamp', 'logtype', 'message', 'prefix', 'postfix'
        :param prefix: string to prepend in the log
        :param postfix: string to append to the log
        :param title: string to be put on the top of the file
        :param logexists: default action if logfile exists; available: 'append', 'overwrite', 'rename'
        :param console: print log messages
        :param external_function: reference to function returning string called periodically to create log in logger
        :param internal_logger_time: delay between external function calls in seconds
        """

        # delay between external function calls
        self.internal_logger_time = internal_logger_time
        # reference to external function returning string for log message if None internal logger doesn't start
        self.external_function = external_function
        # lock for multithread access to logger
        self.log_lock = Lock()
        # boolean for running logger
        self._enabled = False
        # print messages in console
        self._console = console
        # create logfile and its directory
        self.filename = filename
        self.directory = directory
        # available log methods:
        self._logtypes = {'info': 'INFO        ', 'warning': '  WARNING   ',
                          'error': '    ERROR   ', 'fatal': '       FATAL'}
        self.logtype = logtype
        # timestamp format
        self.timestamp = timestamp
        # message format
        self.logformat = logformat
        # prefix & postfix
        self.prefix = prefix
        self.postfix = postfix
        # log title
        self.title = title
        # log-exists actions
        self._ifexists = {'append': self._append, 'overwrite': self._overwrite, 'rename': self._rename}
        self.logexists = logexists
        self._exit_flag = Event()
        # resume logger
        self.resume()

    @property
    def enabled(self):
        return self._enabled

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value):
        self.pause()
        assert isinstance(value, str)
        self._directory = value

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self.pause()
        assert isinstance(value, str)
        self._filename = value + '.log'

    @property
    def logtype(self):
        return list([key for key, exists in self._logtypes.items() if exists is self._logtype])[0]

    @logtype.setter
    def logtype(self, value):
        assert value in self._logtypes.keys()
        self._logtype = self._logtypes[value]

    @property
    def timestamp(self):
        return datetime.datetime.now().strftime(self._timestamp)

    @timestamp.setter
    def timestamp(self, value):
        assert isinstance(value, str)
        self._timestamp = value

    @property
    def logformat(self):
        return self._logformat.format(timestamp=self.timestamp, logtype=self._logtype, message='logformat test',
                                      prefix=self.prefix, postfix=self.postfix)

    @logformat.setter
    def logformat(self, value):
        assert isinstance(value, str)
        self._logformat = value

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        assert isinstance(value, str)
        self._prefix = value

    @property
    def postfix(self):
        return self._postfix

    @postfix.setter
    def postfix(self, value):
        assert isinstance(value, str)
        self._postfix = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        assert isinstance(value, str)
        self._title = value

    @property
    def logexists(self):
        return list([key for key, exists in self._ifexists.items() if exists is self._logexists])[0]

    @logexists.setter
    def logexists(self, value):
        assert value in self._ifexists.keys()
        self._logexists = self._ifexists[value]

    def start(self):
        """Start logger in separate thread

        this will create separate thread which start run method
        """
        log = Thread(target=self.run, name=self.title+' Thread')
        log.start()

    def pause(self):
        """Pause the logger

        this will set boolean attribute to False, which will stop saving log to the logfile"""
        if self._enabled:
            self._enabled = False

    def resume(self):
        """Resume logging

        this will set boolean attribute to True, which will resume logging to the logfile"""
        if not self._enabled:
            if self.directory is not '':
                if not os.path.exists(self.directory):
                    print(f'WARNING: directory does not exist. Creating directory "{self.directory}"')
                    os.makedirs(self.directory)
                self.directory = self.directory + '/'
            self._path = f'{self.directory}{self.filename}'
            trials = 0
            # check if file exists
            if os.path.isfile(self._path):
                # actions for existing file
                while trials < 3:
                    # user input defaulting to preset log-exists action
                    actions = list(self._ifexists.keys())
                    for i in range(len(actions)):
                        if actions[i] is self.logexists:
                            actions[i] = actions[i].upper()
                        actions[i] = f'({actions[i][0]}){actions[i][1:]}'
                    valid = {'a': 'append', 'A': 'append',
                             'o': 'overwrite', 'O': 'overwrite',
                             'r': 'rename', 'R': 'rename'}
                    prompt = 'Log file already exists. Choose action: {}/{}/{}: '.format(*actions)
                    answer = input(prompt) or self.logexists[0]
                    # set default action
                    try:
                        self.logexists = valid[answer]
                        break
                    except KeyError:
                        print('Incorrect choice. You have to select one of available actions.')
                        trials += 1
                    finally:
                        self._logexists()
            else:
                # create empty file
                open(self._path, 'a').close()
            self.log(f'!    --== {self.title} ==--    ')
            self._enabled = True

    def clear(self):
        """Clear current logfile

        this will clear current logfile without deleting it"""
        open(self._path, 'w').close()

    def delete(self):
        """Delete current logifle

        this will remove current logfile from hard drive"""
        self.pause()
        os.remove(self._path)

    def log(self, msg, logtype=''):
        with self.log_lock:
            if msg[0] == '!':
                with open(self._path, 'a') as file:
                    log = msg[1:]
                    print(log, file=file)
                    if self._console:
                        print(f'  LOGGER: {self.filename}')
                        print(log)
            else:
                if logtype is not '':
                    self.logtype = logtype
                with open(self._path, 'a') as file:
                    log = self._logformat.format(timestamp=self.timestamp, logtype=self._logtype, message=msg,
                                                prefix=self.prefix, postfix=self.postfix)
                    print(log, file=file)
                    if self._console:
                        print(f'  LOGGER: {self.filename}')
                        print(log)

    def _append(self):
        self.log('! --- APPENDED --- ')

    def _overwrite(self):
        self.clear()
        self.log('! --- FILE OVERWRITTEN --- ')

    def _rename(self):
        while os.path.isfile(self._path):
            filename = self.filename[:-4]
            num = 0
            i = 0
            for sign in reversed(filename):
                try:
                    num += int(sign) * 10 ** (-i)
                    i -= 1
                except ValueError:
                    if i != 0:
                        self.filename = f'{filename[:i]}{num+1}'
                    else:
                        self.filename = f'{filename}_{num+1}'
                    break
            self._path = f'{self.directory}{self.filename}'
        self.log('! --- FILE RENAMED --- ')

    def exit(self):
        self._exit_flag.set()

    def run(self):
        try:
            if self.external_function:
                while not self._exit_flag.wait(timeout=self.internal_logger_time):
                    msg = self.external_function()
                    self.log(msg)
            else:
                while not self._exit_flag.wait(timeout=10):
                    pass
        except Exception as ex:
            self.log(msg=f'{type(ex)}: {ex.args}; {ex}', logtype='fatal')
            raise ex
        finally:
            self.log('!  -- PROGRAM TERMINATED --  ')
