import logging
import time
import pathlib
import dill
import yaml

class timer:
    """ utility for calculate time duration
    """
    def __init__(self):
        """ init and tik() the timer """
        self.start = None
        self.stop  = None
        self.tik()

    def tik(self):
        self.start = time.time()
        return self.start

    def tok(self):
        self.stop  = time.time()
        return self.stop

    def taketime(seconds=None):
        """ static function for calc the time """
        if seconds:
            seconds  = seconds % (24 * 3600) 
            hour     = seconds // 3600
            seconds %= 3600
            minutes  = seconds // 60
            seconds %= 60
            return "%d:%02d:%02d" % (hour, minutes, seconds) 
        else:
            return 'no given time (seconds)'


    def reset(self):
        """ reset start & stop timer to None, then tik() the timer """
        self.start = None
        self.stop  = None
        self.tik()

    def time(self, seconds=None):
        """ in-house function for calc timer """
        if seconds == None:
            seconds = self.stop - self.start if self.start and self.stop else None
 
        return timer.taketime(seconds)



class configure:
    def load(filename):
        """ load yaml file to configure """
        with open(filename, 'r') as f:
            conf = yaml.full_load(f)
        return conf


    def write(data, filename):
        """ write data to yaml file configure """
        with open(filename, 'w') as f:
            yaml.dump(data, f, allow_unicode=True)



class data:
    def exist(path, pathtype='any'):
        """ check if given path exist """
        thing = pathlib.Path(path)
        if thing.exists():
            if   pathtype == 'file':   return True if thing.is_file() else False
            elif pathtype == 'folder': return True if thing.is_dir()  else False
            else:                      return True
        else:
            return False


    def make_path(path, pathtype='file'):
        """ make folder in the path, return True if success, else False """
        # setup folder path
        if pathtype == 'file':
            tokens = path.split('/')
            folder = '/'.join(tokens[:-1])
            fname  = tokens[-1]
        else:
            folder = path
        # create folder
        try: 
            if len(folder) > 0: pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f'error: {str(e)}')
            return False
        return True


    def save_object(obj, filename):
        """ save any data to dill object file """
        data.make_path(filename)
        with open(filename, 'wb') as f:
            dill.dump(obj, f)
            print(f'> saving data to "{filename}"')


    def load_object(filename):
        """ load content in a file to dill data object """
        print(f'> loading data from "{filename}"')
        with open(filename, 'rb') as f:
            data = dill.load(f)
        return data


    def save(lines, filename):
        """ save text in lines to a file """
        data.make_path(filename)
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line+'\n')
            print(f'> saving content to "{filename}"')


    def load(filename, loadtype='original'):
        """ load text content in a file """
        print(f'> loading "{loadtype}" content from "{filename}"')
        with open(filename, 'r') as f:
            if loadtype == 'original': lines = [line[:-1]    for line in f.readlines()]
            else:                      lines = [line.strip() for line in f.readlines()]
        return lines


    def load_file_list(f_list, n_char:int=0):
        """ load content from a file list, each content line > n_char """
        content = []
        n_fail  = 0
        for f in f_list:
            try:
                content += [v for v in data.load(f, loadtype='strip') if len(v) > n_char]
            except Exception as e:
                n_fail  += 1
        print(f'>>> load content from {len(f_list)} file(s) .. failed {n_fail} file(s)')
        return content
            



class log:
    import logging.handlers

    """ static class for creating logger instance """
    DEBUG   =10
    INFO    =20
    WARNING =30
    ERROR   =40
    CRITICAL=50

    def info(logger, message=''):
        """ print information of the given handler """
        print(f'--- {message} logger "{logger.name}" info ---')
        print(f'logger: {logger}')
        print(f'handlers: {len(logger.handlers)}')
        for hand in logger.handlers:
            print(f'  {hand}')
        print()


    def GetHandler(filename=None, when=None, level=logging.DEBUG, formatter='minimal'):
        """ formatter will be in f-string format
            formatter: [nothing, minimal, basic, full, custom]
            o nothing: only message
            o minimal: time, message
            o basic:   level, name, message (exclude time)
            o full:    level, time, name, message
            o custom:  any format, but in f-string format only

            when: preset is [daily, weekly] or logging format e.g., W0
        """
        if   formatter == None: formatter = 'minimal'
        if   formatter == 'nothing':      formatter = '{message}'
        elif formatter == 'minimal':      formatter = '{asctime} || {message}'
        elif formatter == 'basic':        formatter = '{levelname:<8} || {name} || {message}'
        elif formatter == 'full':         formatter = '{levelname:<8} || {asctime} || {name} || {message}'

        fmt = logging.Formatter(formatter, style='{')
        if filename:
            # make sure the folder is exist
            data.make_path(filename)
            # create log_handler
            w = 'midnight' if when == 'daily' else 'W0' if when=='weekly' else when
            if w is not None:
                handler = logging.handlers.TimedRotatingFileHandler(filename, when=w, encoding='utf8')
            else:
                handler = logging.FileHandler(filename, encoding='utf8')
            
        else:
            handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(fmt)
        return handler



    def GetLogger(name='muuusiiik', filename=None, when=None, level=logging.DEBUG, formatter='minimal'):
        """ generate Logger """
        # manage logger
        if not name: name = __name__
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        # manage handler
        handler = log.GetHandler(filename=filename, when=when, level=level, formatter=formatter) 
        logger.addHandler(handler)
        return logger
