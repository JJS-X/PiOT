import re
import sys
import crypt
import cherrypy
def checkpass(username, password):
    passwd = open("/etc/shadow","r")
    goodpassword = None
    for line in passwd:
        if username in line:
            goodpassword = line
    if not goodpassword is None:
        table=goodpassword.split(":")
        hash=table[1].split("$")

        if (crypt.crypt(password, "$"+hash[1]+"$"+hash[2]+"$") == table[1]):
            return "True"
        else:
            return "False"
    else:
        return "not user"

def setCookie():
    cookie = cherrypy.response.cookie
    cookie['cookieName'] = 'test'
    cookie['cookieName']['path'] = '/'
    cookie['cookieName']['max-age'] = 3600
    cookie['cookieName']['version'] = 1


def readCookie():
    cookie = cherrypy.request.cookie
    for name in cookie.keys():
        if name == "cookieName":
            if cookie[name].value == "test":
                return True
    return False


# def readCookie():
#     cookie = cherrypy.request.cookie
#     res = """<html><body>Hi, you sent me %s cookies.<br />
#             Here is a list of cookie names/values:<br />""" % len(cookie)
#     for name in cookie.keys():
#         res += "name: %s, value: %s<br>" % (name, cookie[name].value)
#     return res + "</body></html>"
