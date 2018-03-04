INCLUDE_KEYWORD = "#include"
INCLUDE_LEN = len(INCLUDE_KEYWORD)

import sys

source = sys.argv[1]
output   = sys.argv[2]

reader = open(source, 'r', encoding='utf-8')
writer = open(output, 'w+', encoding="utf-8")

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
        writer.write(line)
        return
    
    print("including \"{}\"".format(filepath))
    with open(filepath, 'r') as ireader:
        for iline in ireader:
            parse_line(indent + iline)
def parse_line(line):
    if line.strip().startswith(INCLUDE_KEYWORD): 
        include(line)
        writer.write('\n')
    else: writer.write(line)

for line in reader:
    parse_line(line)

writer.close()
reader.close()