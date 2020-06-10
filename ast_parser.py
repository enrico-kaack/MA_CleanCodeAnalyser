import ast 
import os
from pathlib import Path

def _walk_for_all_python_files_in(folder):
    folder = Path(folder)
    all_python_file = [i.resolve() for i in list(folder.glob("**/*.py"))] #TODO: exclude hidden directorys
    return all_python_file


def parse_ast_from_folder(folder):
    list_of_python_files = _walk_for_all_python_files_in(folder)
    list_of_ast = []
    for python_file in list_of_python_files:
        with open(python_file, "r") as opened_python_file:
            python_ast = ast.parse(opened_python_file.read(), str(python_file))
            list_of_ast.append(python_ast)
    return list_of_ast