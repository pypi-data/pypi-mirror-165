import pathlib

from tree_sitter import Language, Parser


candidates = list(pathlib.Path(__file__).parent.glob('*.so'))
assert len(candidates) == 1


_binary_path = str(candidates[0])
rst = Language(_binary_path, "rst")
parser = Parser()
parser.set_language(rst)
