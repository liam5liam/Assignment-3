# Code passes the PEP8 check. 4/04/19

# Ignore errors here.
from pythonscripts.FileHandler import FileConverter
from pythonscripts.FileView import FileView
from pythonscripts.FileWriter import FileWriter
import os
from pythonscripts.DataBase import DataBase

fconv = FileConverter()
fw = FileWriter()
fv = FileView()
db = DataBase()


class FileController:
    def __init__(self):
        self.command = ''
        self.data = 'empty'
        self.file_location = ''

        self.command_dict = {
            "load": self.load_cmd,
            "absload": self.load_cmd
        }

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
        else:
            if file_location == "":
                fv.fc_file_not_found(file_location, "", "absload")
            else:
                fv.fc_syntax_error("absload")
            fv.general_error()
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
            fconv.read_file(filename)
            fconv.convert_file()
            fconv.return_program()
            self.data = fconv.codeToText
            fw.write_file(self.data, "Output.txt")
            fw.write_file(self.data, "Output.py")
            db.data_entry(self.data)
            # fv.file_written("Output.txt, Output.py")
        except AttributeError as e:
            print(e)
        except IOError:
            print("System failed to save to file")
        except ValueError and TypeError:
            fv.output("Please enter an integer")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

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
        self.data = db.get_code(code_id)
        try:
            fw.write_file(db.get_code(code_id), file_name)
        except AttributeError as e:
            print(e)
        except IOError as e:
            print("System failed to save to file")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def load_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                self.data = code
                fv.output("Code has loaded successfully")
            else:
                fv.output("ERROR: code failed to load:")
                fv.output('\t' + code)
        except AttributeError as e:
            print(e)
        except IOError:
            print("System failed to save to file")
        except ValueError and TypeError:
            fv.output("Please enter an integer")
        except Exception as e:
            fv.general_error()
            print("An error has occurred")
            print(e)

    # Liam
    def print_code(self, code_id):
        try:
            code = db.get_code(code_id)
            if code != '':
                fv.output(code)
            else:
                fv.output("ERROR: code failed to load:")
                fv.output('\t' + code)
        except ValueError and TypeError:
            fv.output("Please enter an integer")
        except IOError as e:
            print("System failed to load to file")
            print(e)

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
