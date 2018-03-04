REPLACE_KEYWORD = ">>>>>>>REPLACE\n"

import sys

template = sys.argv[1]
data     = sys.argv[2]
output   = sys.argv[3]


treader = open(template, 'r', encoding='ASCII')
dreader = open(data, 'r', encoding="utf-8")
owriter = open(output, 'w+', encoding="utf-8")

for line in treader:
    if line == REPLACE_KEYWORD:
        for rline in dreader:
            owriter.write(rline)
    else: owriter.write(line)

owriter.close()
dreader.close()
treader.close()