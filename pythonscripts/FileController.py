# Code passes the PEP8 check. 4/04/19

# Ignore errors here.
from pythonscripts.FileHandler import FileConverter
from pythonscripts.FileView import FileView
from pythonscripts.FileWriter import FileWriter
import os
from pythonscripts.DataBase import DataBase
from abc import abstractmethod, ABCMeta

fconv = FileConverter()
fw = FileWriter()
fv = FileView()
db = DataBase()


class Observer(metaclass=ABCMeta):
    def __init__(self):
        self._subject = None
        self._state = None

    @abstractmethod
    def update(self, arg): pass


# Read Event handler
class ObserverRead(Observer):
    def update(self, arg):
        self._state = arg
        if self._state == 1:
            self._state = arg
            print("Checking for Errors...")
            print("Done!")


# Write File Wrapper Observer
class ObserverWrite(Observer):
    def update(self, arg):
        self._state = arg
        if self._state == 1:
            fv.print_minus()


OR = ObserverRead()
OW = ObserverWrite()


# Observes Errors.
class ObserverCheck(Observer):
    def update(self, arg):
        self._state = arg
        if self._state != 1:
            fv.general_error()
            fv.output(self._state)


OC = ObserverCheck()


class FileController:
    _state = 0
    _observers = set()

    def __init__(self):
        self.command = ''
        self.data = 'empty'
        self.file_location = ''

        self.command_dict = {
            "load": self.load_cmd,
            "absload": self.load_cmd
        }

    self.attach(OW)
    self.attach(OR)
    self.attach(OC)

    def attach(self, observer):
        observer._subject = self
        self._observers.add(observer)
        print("Attached an observer: " + observer.__class__.__name__)

    def _notify(self):
        for observer in self._observers:
            observer.update(self._state)

    @property
    def subject_state(self):
        return self._state

    def is_file(self, string):
        if os.path.isfile(string):
            fv.fc_file_found()
            self.read_file(string)

    def load_cmd(self, file_location):
        try:
            if os.path.isfile("./{}".format(file_location)):
                fv.fc_file_found()
                self.read_file("./{}".format(file_location))
        except FileNotFoundError:
            fv.fc_file_not_found(file_location, "r", "load")
        except PermissionError:
            fv.fc_permission_error()

    def absload_cmd(self, file_location):
        try:
            if os.path.isfile("{}".format(file_location)):
                fv.fc_file_found()
                self.read_file("../{}".format(file_location))
        except FileNotFoundError:
            fv.fc_file_not_found(file_location, "a", "absload")
        except PermissionError:
            fv.fc_permission_error()

    def cmd_checker(self, file_location):
        out = False
        if file_location.endswith(".txt"):
            out = True
        return out

    # Command Handler - Made by Matthew
    def handle_command(self, cmd, file_location):
        try:
            if self.cmd_checker(file_location):
                self.command_dict[cmd](file_location)
        except FileNotFoundError:
            fv.fc_file_not_found(file_location, "lf", "")

# Reads file - Liam
    def read_file(self, filename):
        try:
            self.data = fconv.read_file(filename)

            fw.write_file(self.data, "Output.txt")
            fw.write_file(self.data, "Output.py")
            db.data_entry(self.data)
            # fv.file_written("Output.txt, Output.py")

            # The code has been built
            # The observers must be notified
            self._notify()
            self.write_file()
        except IOError:  # pragma: no cover
            self._state = "Error: System Failed to Save to File!"
            self._notify()

    # Liam
    def print_file(self):
        try:
            fv.output(self.data)
        except IOError:
            print("System failed to load to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def save_file(self, file_name, code_id):
        is_saved = True
        self.data = db.get_code(code_id)
        try:
            fw.write_file(db.get_code(code_id), file_name)
        except IOError as e:  # pragma: no cover
            is_saved = False
            self._state = "System failed to save to file" + e
            self._notify()
        if is_saved:
            fv.file_written(file_name)

    # Liam
    def load_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                self.data = code
                fv.output("Code has loaded successfully")
            else:
                self._state = "ERROR: code failed to load:" + '\t' + code
                self._notify()
        except IOError:  # pragma: no cover
            self._state = "System failed to save to file"
            self._notify()

    # Liam
    def print_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                fv.output(code)
            else:
                self._state = "ERROR: code failed to load:" \
                              "\t" + code
                self._notify()
        except ValueError and TypeError:  # pragma: no cover
            self._state = "Please enter an integer"
            self._notify()
        except IOError as e:  # pragma: no cover
            self._state = "System failed to load to file" + e
            self._notify()

    # Matthew
    def quit(self):
        pass

    # Matthew
    @staticmethod
    def view_help():
        fv.print_help()

    # Matthew
    @staticmethod
    def output_error(message):
        fv.general_error()
        fv.output(message)
