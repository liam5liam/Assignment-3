""" Made by 3 students:
    Matthew Whitaker
    Liam Brydon
    Sarah Ball (providing the model)
"""
# Code passes the PEP8 Check. 4/04/19

import datetime
import re
from pythonscripts.FileView import FileView
from abc import ABCMeta, abstractmethod
fv = FileView()


class AbstractBuilder(metaclass=ABCMeta):
    def __init__(self, uml_classes):
        self.uml_classes = uml_classes
        self.all_my_converted_classes = []
        self.all_my_classes = []

    def get_code(self):
        out = ''
        for a_class in self.all_my_classes:
            out += a_class.return_class()
        return out

    @abstractmethod
    def add_classes(self): pass


class CodeBuilder(AbstractBuilder):

    def add_classes(self):
        fv.fc_plantuml_converting()

        for uml_class in self.uml_classes:
            converted_class = ClassConverter(uml_class)
            converted_class.make_class()

            new_class = Class(converted_class.class_name, converted_class.attributes,
                              converted_class.methods, converted_class.relationships)
            new_class.add_class_attributes()
            new_class.add_class_methods()
            self.all_my_classes.append(new_class)


class ClassConverter:
    def __init__(self, uml_class):
        self.uml_class = uml_class
        self.class_name = ''
        self.attributes = []
        self.methods = []
        self.relationships = []

    def make_class(self):
        self.class_name = self.uml_class.split(' ')[1]
        for line in self.uml_class.split("\n"):
            if line.find(":") != -1:
                self.attributes.append(line)

        for line in self.uml_class.split("\n"):
            if line.find("()") != -1:
                self.methods.append(line)

        for relationship in self.uml_class.split("\n"):
            if self.find_relationship(relationship, self.class_name):
                self.relationships.append(
                    self.find_relationship(relationship, self.class_name))

    def find_relationship(self, relationship, class_name):
        if relationship.startswith(class_name):
            pass
        elif relationship.endswith(class_name):
            if len(relationship.split(" ")) < 2:
                pass
            elif re.search(r"-->", relationship):
                ext_class = relationship.split(" ")[0]
                return tuple(("association of", ext_class))
            elif re.search(r"\*--", relationship):
                com_class = relationship.split(" ")[0]
                return tuple(("composition of", com_class))
            elif re.search(r"o-", relationship):
                as_class = relationship.split(" ")[0]
                return tuple(("aggregation of", as_class))


class Director(object):
    def __init__(self, builder):
        self.builder = builder

    def get_code(self):
        self.builder.add_classes()

        return self.builder.get_code()


class FileConverter:
    def __init__(self):
        self.code = ''
        self.uml_classes = []

    def read_file(self, filename):
        with open(filename, "r") as filename:
            data = filename.read()

        rduml = FileReader(data)
        uml_classes = rduml.find_classes()

        self.code = (Director(CodeBuilder(uml_classes)).get_code())
        return self.code


fc = FileConverter()


# Made by Liam & Matt
class FileReader:
    def __init__(self, filename):
        self.allMyClasses = []
        self.code = filename

    # Made by Matt
    def check_if_plantuml(self, code):
        is_plantuml = False
        try:
            if code.startswith("@startuml") and code.endswith("@enduml"):
                return True
        except IOError:
            fv.general_error()
            print("The file cannot be read.")
        except EOFError:
            fv.general_error()
            print("Unexpected End of File.")
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return False

    # Made by Liam
    # Check if the file contains the word "Class"
    def count_occurrences(self, word, sentence):
        try:
            lower = sentence.lower()
            split = lower.split()
            count = split.count(word)
            if count == 0:
                fv.fr_plantuml_classes_not_found()
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return count

    # Made by Liam Finds and splits up the classes then stores them in an array
    def find_classes(self):
        try:
            isplantuml = self.check_if_plantuml(self.code)
            if isplantuml:
                fv.fr_file_accepted()
                value = self.count_occurrences("class", self.code)

                for i in range(0, value):
                    self.allMyClasses.append(self.code.split("}\nclass")[i])
                return self.allMyClasses
            else:
                fv.fr_plantuml_error()
        except TypeError:
            fv.general_error()
            print("The file must contain a string.")
        except Exception as e:
            fv.general_error()
            print("An Error Occurred" + str(e))
        return


# Made by Sarah
class Class:
    def __init__(self, class_name, new_attributes, new_methods, relationships):
        self.name = class_name
        self.attributes = new_attributes
        self.methods = new_methods
        self.relationships = relationships
        self.all_my_attributes = []
        self.all_my_methods = []
        self.all_my_relationships = []
        self.all_my_associated_classes = []
        self.all_my_aggregated_classes = []
        self.all_my_composite_classes = []

    def add_class_attributes(self):
        for an_attribute in self.attributes:
            new_a_name = an_attribute.split(": ")[0]
            new_a_return = an_attribute.split(": ")[1]
            new_a = Attribute(new_a_name, new_a_return)
            self.all_my_attributes.append(new_a)

    def add_class_methods(self):
        for a_method in self.methods:
            new_m_name = a_method.split(":")[0]
            new_m_return = a_method.split("()")[1]
            new_m = Method(new_m_name, new_m_return)
            self.all_my_methods.append(new_m)

    # Some work on relationships
    def add_class_relationships(self):
        for a_relationship in self.all_my_relationships:
            if "comp" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_composite_classes.append(new_relationship)
            if "aggreg" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_aggregated_classes.append(new_relationship)
            if "assoc" in a_relationship:
                new_relationship = Relationship(a_relationship)
                self.all_my_associated_classes.append(new_relationship)

    # Liam Brydon's modified code (originally created by Sarah Ball)
    # Used only for debug!
    def print_class(self):
        print("class", self.name, ":", end="\n\n")
        for x in self.all_my_attributes:
            print(x)
        print("")
        print("\tdef __init__(self):")
        print("\t\tpass")
        for x in self.all_my_methods:
            print(x)
        print("\n")

    # Made by Liam
    def return_class(self):
        out = str("\nclass {}:\n\n").format(self.name)

        for x in self.all_my_attributes:
            out += str("{}".format(x) + "\n")

        out += str("\n    " + "def __init__(self):\n")
        for a_class in self.relationships:
            out += str("        " f"self.{str(a_class[1]).lower()}" f" = {a_class[1]}()  " f"# {a_class[0]}\n")
        out += str("\n        " + "pass\n\n")

        for x in self.all_my_methods:
            out += str("{}".format(x) + "\n\n")
        return out


"""
Sarah Ball's code - Modified by Liam + Matt
for compatibility with PEP8
"""


class Attribute:
    def __init__(self, new_name, new_return):
        self.name = new_name
        self._return = new_return
        self.name = self.name.strip(' ')

        self.output = {
            "String": f"    {self.name}: str",
            "Integer": f"    {self.name}: int",
            "ArrayObject": f"    {self.name}: list",
            "Object": f"    {self.name}: object"
        }

    def __str__(self):
        return self.output[self._return]


"""
Sarah Ball's code - Modified by Liam + Matt
for compatibility with PEP8
"""


class Method:
    def __init__(self, new_name, new_return):
        self.name = new_name.replace("()", "")
        self._return = new_return

    def __str__(self):
        return f"    def {self.name}(self):\n        pass"


"""
Matt's Relationship code
"""


class Relationship:
    def __init__(self, new_type):
        self.name = new_type[1]
        self.type = new_type[0]

    def __str__(self):
        return f"{self.name}s"
