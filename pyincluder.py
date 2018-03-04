INCLUDE_KEYWORD = "#include"
INCLUDE_LEN = len(INCLUDE_KEYWORD)

MOVE_IMPORTS = True

import sys

source = sys.argv[1]
output   = sys.argv[2]

reader = open(source, 'r', encoding='utf-8')

include_list = []
imports_list = []

class output_scope(object):
    outtext = ""

def count_whitespace(line):
    count = 0
    for c in line:
        if c == ' ': count += 1
        else: break
    return count
def get_include_file(line):
    filepath = line.strip()[INCLUDE_LEN:]
    filepath = filepath.strip()
    if filepath[0] == '<' and filepath[-1] == '>':
        filepath = filepath[1:-1]
        return filepath
    else:
        return None

def include(line):
    indent = ' ' * count_whitespace(line)
    filepath = get_include_file(line)
    if not filepath: # not a valid include
        simple_write(line)
        return
    else:
        if filepath in include_list:
            print("already copied \"{}\"".format(filepath))
        else:
            include_list.append(filepath)

    print("including \"{}\"".format(filepath))
    with open(filepath, 'r') as ireader:
        for iline in ireader:
            parse_line(indent + iline)
def simple_write(line):
    output_scope.outtext += line
    # writer.write(line)
def is_import_line(strip):
    return strip.startswith("import") or ( strip.startswith("from") and "import" in strip )
def parse_line(line):
    strip = line.strip()
    if strip.startswith(INCLUDE_KEYWORD): 
        include(line)
        simple_write('\n')
    elif MOVE_IMPORTS and is_import_line(strip):
        if not strip in imports_list: imports_list.append(strip)
    else: simple_write(line)

for line in reader:
    parse_line(line)

reader.close()

if MOVE_IMPORTS:
    output_scope.outtext = "\n".join(imports_list) + output_scope.outtext

with open(output, 'w+', encoding="utf-8") as writer:
    writer.write(output_scope.outtext)
