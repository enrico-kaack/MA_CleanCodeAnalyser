import ast
from pathlib import Path


def _walk_for_all_python_files_in(folder):
    folder = Path(folder)
    all_python_file = [i.resolve() for i in list(folder.glob("**/*.py"))]  #TODO: exclude hidden directorys
    return all_python_file


def parse_ast_from_folder(folder):
    list_of_python_files = _walk_for_all_python_files_in(folder)
    list_of_ast = []
    for python_file in list_of_python_files:
        with open(python_file, "r") as opened_python_file:
            try:
                python_ast = ast.parse(opened_python_file.read(), str(python_file))
                list_of_ast.append(ParsedSourceFile(python_file, python_ast, opened_python_file.read()))
            except SyntaxError:
                print(f"Syntax error on file:{str(python_file)}. Ignoring file")

    return list_of_ast


class ParsedSourceFile():
    
    def __init__(self, file_path, a, content):
        self.file_path = file_path
        self.ast = a
        self.content = content