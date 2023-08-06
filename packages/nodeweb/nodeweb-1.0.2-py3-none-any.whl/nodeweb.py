import os
os.popen('chcp 65001')

class NotHaveThisHTMLFileError(Exception):
    def __init__(self,msg):
        self.msg = msg

def web(port,hostname,htmlfile):
    try:
        f1 = open(htmlfile,'r')
    except FileNotFoundError:
        raise NotHaveThisHTMLFileError(f'htmlfile "{htmlfile}" is not have')
    else:
        html = f1.read()
        f1.close()
        try:
            f2 = open('.\\build\\web.js', 'w', encoding='utf-8')
        except FileNotFoundError:
            os.popen('md build')
            f2 = open('.\\build\\web.js', 'w', encoding='utf-8')
        js = """const http = require(\"http\");
const server = http.createServer((require, respose) => {
    respose.setHeader(\'content-type\',\'text/html;charset=utf-8\')
    respose.end(`%s`);
});
server.listen(%d,\'%s\',() => {
    console.log("服务器启动成功，请在 http://%s:%d 进行访问......");
});""" % (html,port,hostname,hostname,port)
        f2.write(js)
        f2.close()
        os.system('node build\\web.js')

def easyweb(port,hostname,text):
    f1 = text
    html = f1.read()
    f1.close()
    try:
        f2 = open('.\\build\\web.js', 'w', encoding='utf-8')
    except FileNotFoundError:
        os.popen('md build')
        f2 = open('.\\build\\web.js', 'w', encoding='utf-8')
    js = """const http = require(\"http\");
const server = http.createServer((require, respose) => {
    respose.setHeader(\'content-type\',\'text/html;charset=utf-8\')
    respose.end(`%s`);
});
server.listen(%d,\'%s\',() => {
    console.log("服务器启动成功，请在 http://%s:%d 进行访问......");
});""" % (html,port,hostname,hostname,port)
        f2.write(js)
        f2.close()
        os.system('node build\\web.js')
