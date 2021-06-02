

def read(path: str):
    content = dict()
    file = open(path)
    for line in file:
        # if re.match(line_localize_rex, line, re.RegexFlag.DOTALL):
        pairs = line.split(' = ')
        key = pairs[0][1:-1]
        content[key] = pairs[1][1:-3]
        content.keys()
        a = list(map(str, content.keys())).sort()
    return content
