# Ignore errors below this line.
import sys
import cmd
from typing import Dict, List

from pythonscripts.FileController import FileController
from pythonscripts.FileView import FileView

# Execute code here
# Matthew Whitaker's code.
fv = FileView()
fc = FileController()


# 4/04/19 Code passes the PEP8 Check.
# CMD based code - Matt


class Main(cmd.Cmd):
    def __init__(self):
        super(Main, self).__init__()
        self.intro = \
            "===============================================\n" \
            "PlantUML to Python Converter\n" \
            "Please type 'help' for all available commands.\n" \
            "Please type 'allhelp' to view the help file.\n" \
            "To continue with a default graph.txt in the\n" \
            "root directory, press [Enter]\n" \
            "=============================================="

    # CMD - Matt
    def cmdloop(self, intro=None):
        print(self.intro)
        while True:
            try:
                super(Main, self).cmdloop(intro="")
                break
            except KeyboardInterrupt:
                print("Ctrl + C pressed, but ignored. "
                      "Please use 'exit' or 'quit' "
                      "to stop the program.")
            except TypeError and ValueError:
                fv.general_error()
                print("Please verify your command, and try again.")
            except Exception:
                fv.general_error()
                print("An error has occurred.")

    # Continues when no command is entered - Matt
    def emptyline(self):
        fv.fe_defaults()
        fc.handle_command('', '')

    # Load method - Matt
    def do_load(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the current working directory.
        Usage: LOAD [filename.txt]
        """
        fc.handle_command("load", line)

    # Absload method - Matt
    def do_absload(self, line):
        """
        LOADS your SOURCE PlantUML text file, and translates it
        into a python file, from the directory of your choosing.
        Usage: ABSLOAD [path_to_filename.txt]
        """
        if "\\" in line:
            fc.handle_command("absload", line)
            fv.next_command()
        else:
            fv.general_error()
            fv.fe_abs_path_error()

    # View help file - Matt and Liam
    def do_allhelp(self, line):
        """
        SHOWS all HELP relating to this program.
        Usage: ALLHELP
        """
        fv.print_help()

    # Exit method - Matt
    def do_exit(self, line):
        """
        EXITS the program cleanly. (same as QUIT)
        Usage: exit
        """
        exit()

    # Quit method - Matt
    def do_quit(self, line):
        """
        QUITS the program cleanly. (same as EXIT)
        Usage: quit
        """
        self.do_exit(line)

    # Save method - Liam
    def do_save(self, line):
        """
        Saves the converted plantuml code from the database to a textfile
        Usage: save {filename.txt} {code_id}
        """
        line = line.split(' ')
        fc.save_file(line[0], line[1])

    # Printcode method - Liam
    def do_printcode(self, line):
        """
        Prints the converted plantuml code from the database to the cmd
        Usage: printcode {code_id}
        """
        fc.print_code(line)

    # Loadcode method - Liam
    def do_loadcode(self, line):
        """
        Loads code from the database into self.data
        Usage: loadcode {code_id}
        """
        fc.load_code(line)

    # Printfile method - Liam
    def do_printfile(self, line):
        """
        Prints the data saved inside self.data to the cmd
        Usage: printfile
        """
        fc.print_file()

    fv.next_command()

# Liam
def print_to_screen():
    their_answer = input("Would you like to print the "
                         "code to the screen? y/n: ")
    if their_answer == "y":
        fc.print_file()

    their_answer = input("Would you like to save the code to Output.txt y/n: ")
    if their_answer == "y":
        fc.save_file("Output.txt")


m = Main()

class CheckDictionary():

    def __init__(self, sysargv):
        self.cmd = ''
        self.length = 0
        self.sysargv = sysargv
        self.command_dict = {
            "save": self.save,
            "help": fc.view_help,
            "loadcode": self.loadcode,
            "printcode": self.printcode,
            "load": self.load,
            "absload": self.absload
        }

    def check_correct(self):
        out = False
        if self.cmd == "save" and self.length == 4:
            out = True
        elif self.length == 3:
            out = True

        return out

    def save(self):
        if self.check_correct():
            fc.save_file(self.sysargv[2], self.sysargv[3])
        else:
            fv.fe_command_syntax("Save")

    def loadcode(self):
        if self.check_correct():
            fc.load_code(self.sysargv[2])
        else:
            fv.fe_loadcode_syntax("loadcode")

    def printcode(self):
        if self.check_correct():
            fc.print_code(self.sysargv[2])
        else:
            fv.fe_loadcode_syntax("printcode")

    def load(self):
        if self.check_correct():
            fc.handle_command("load", str(self.sysargv[2]))
        else:
            fv.fe_loadcode_syntax("load")

    def absload(self):
        if self.check_correct():
            fc.handle_command("absload", str(self.sysargv[2]))
        else:
            fv.fe_loadcode_syntax("absload")

    def check(self):
        if self.cmd in self.command_dict:
            self.command_dict[self.cmd]()
        else:
            fv.general_error()
            fv.output("Command not found!")


    def handle_sysargv(self):
        self.length = len(self.sysargv)
        self.cmd = str(self.sysargv[1]).lower()

        try:
            checkDictionary.check()
        except IndexError:
            pass
        except PermissionError:
            print("Permission Error!\n"
                  "Check you have the permission to read the file!")


if __name__ == "__main__":
    checkDictionary = CheckDictionary(sys.argv)
    checkDictionary.handle_sysargv()
    #m.cmdloop()