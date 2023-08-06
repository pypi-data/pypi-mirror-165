def read(fileName,encoding="UTF-8"):
    with open(fileName,"r",encoding=encoding) as f:
        return f.read()
def write(fileName,content="",encoding="UTF-8"):
    with open(fileName,"w",encoding=encoding) as f:
        f.write(content)
def add(fileName,content="",encoding="UTF-8"):
    with open(fileName,"a",encoding=encoding) as f:
        f.write(content)
def read_binary(fileName,encoding="UTF-8"):
    with open(fileName,"rb",encoding=encoding) as f:
        return f.read()
def write_binary(fileName,content="",encoding="UTF-8"):
    with open(fileName,"wb",encoding=encoding) as f:
        f.write(content)
def add_binary(fileName,content="",encoding="UTF-8"):
    with open(fileName,"ab",encoding=encoding) as f:
        f.write(content)