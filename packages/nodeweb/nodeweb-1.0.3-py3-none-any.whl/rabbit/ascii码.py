def ascii编码(text:str):
    code = []
    for txt in text:
        code.append(bin(ord(txt)))
    return code
def ascii解码(code:list):
    text = ''
    for cd in code:
        text += chr(int(cd,2))
    return text