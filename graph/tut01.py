import os, os.path
import random
import string
import time
import cherrypy
import sys
sys.path.insert(1, '/opt/projetmaster-master/')
import mac.APImysql as mac
import ip.scan as scan
import ip.sendMail as mail
import graph.connexion.checkpassword as passwd
from jinja2 import Template

class Webpage(object):

    @cherrypy.expose
    def index2(self):
        html = open('connexion/index.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def indexwithoutuser(self):
        html = open('connexion/indexwithoutuser.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def wrongpassword(self):
        html = open('connexion/passwdincorrect.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def login(self,username=None,password=None):
        response = passwd.checkpass(username,password)
        html = """
        <script type="text/javascript">
        setTimeout("CallButton()",5)
        function CallButton()
        {
           document.getElementById("button").click();
        }
        </script>"""
        if response == "not user":
            html += '<form action="indexwithoutuser" method="post"><button hidden="hidden" id="button"></button></form>'
        elif response == "False":
            html += '<form action="wrongpassword" method="post"><button hidden="hidden" id="button"></button></form>'
        elif response =="True":
            passwd.setCookie()
            html += '<form action="accueil" method="post"><button hidden="hidden" id="button"></button></form>'
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def index(self):
        html = open('begin.html','r').read()
        #html += open('index.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def Scan(self, length=8):
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += open('Scan/index.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def Manage(self):
        if passwd.readCookie():
            html = open('html.html','r').read()
            table_mac = mac.display_base()
            table_mac = table_mac.replace("(","")
            table_mac = table_mac.split("),")
            html += """      <section id="home" class="p-10 md-p-l5">
                  <div id="slider-2">
                      <div class="px-3">
                        <div class="p-8 br-8 bg-indigo-lightest-10 relative justify-center items-center text-center"><table class="table table-dark table-bordered">
                    <thead class="thead-light">
                      <tr class="table-dark">
                        <th scope="col">ID</th>
                        <th scope="col">Device</th>
                        <th scope="col">IP Address</th>
                        <th scope="col">Mac Address</th>
    		            <th scope="col">Supprimer</th>
                        <th scope="col">Tester la connection</th>
                        <th scope="col">Tester ports ouverts</th>
                      </tr>
                    </thead><tbody>"""
            for macs in table_mac:
                macs = macs.replace(")","")
                macs = macs.replace("'","")
                macs = macs.replace(" ","")
                macs = macs.split(',')
                html += "<tr>"
                for a in macs:
                    html += "<td>"
                    html += a
                    html += "</td>"
                try:
                    html += '<td><form action="deletemac" method="POST"><input type="hidden" name="name" value="'+macs[0]+'" /> <button type="submit"> <img src=""/></button></form></span></td>'
                    html += '<td><form action="testconnection" method="POST"><input type="hidden" name="name" value="'+macs[2]+'" /> <input type="hidden" name="mac" value="'+macs[3]+'" /><button type="submit"> <span class="iconify" data-icon="mdi-connection" data-height="49"></button></form></span></td>'
                    html += '<td><form action="openport" method="POST"><input type="hidden" name="name" value="'+macs[2]+'" /> <button type="submit"> <span class="iconify" data-icon="mdi:server-network" data-height="49"></button></form></span></td>'
                    pass
                except Exception as e:
                    print(e)
                    pass
                html += "</tr>"
            html += "</table></div></div></div>"
            #lien pour ajouter une mac :
            html += """<form action="AddMac" method="GET"><button type="submit">Ajouter une adresse MAC</button></form>"""
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def Connection(self):
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += open('IPAd.html','r').read()
            html += open('footer.html','r').read()
            #lien pour ajouter une mac :
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def testconnection(self, name=None, mac=None):
        if passwd.readCookie():
            result=scan.attempt_con(name,mac)
            html = open('html.html','r').read()
            html +=  "<h1>"+str(result)+"YEEEEESSSS</h1>"
            if result :
                html += "<h1>"+name+"YEEEEESSSS</h1>"
                html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def openport(self, name=None):
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += name
            ports = scan.port_open(name)
            html += ports
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def deletemac(self, name=None):
        if passwd.readCookie():
            mac.delete_mac(name)
            html = open('html.html','r').read()
            html += "<h1>"+name+"bien supprimé</h1>"
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()
#################################A REFGAIURE #################
    @cherrypy.expose
    def AddMac(self, Add=None):
        if passwd.readCookie():
            html = open('html.html','r').read()
            html +=  open('Manage/Add.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def shodan(self):
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += '<form action="index" method="post"><button type="Submit">retour à l\'accueil</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def shodanip(self, IP=None):
        if passwd.readCookie():
            ports=scan.public_ip()
            html = open('html.html','r').read()
            html += ports
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def public_scan_load(self):
        #ports=scan.public_ip()
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += """
            <script type="text/javascript">
            setTimeout("CallButton()",3000)
            function CallButton()
            {
               document.getElementById("button").click();
            }
            </script>"""
            html += """<div class="load">
      <p class="load">l</p>
      <p class="load">o</p>
      <p class="load">a</p>
      <p class="load">d</p>
      <p class="load">i</p>
      <p class="load">n</p>
      <p class="load">g</p>
    </div>
    """
            html += '<form action="public_scan" method="post"><button hidden="hidden" id="button"></button></form>'

        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def public_scan(self):
        if passwd.readCookie():
            ports=scan.public_ip()
            time.sleep(3)
            html = open('html.html','r').read()
            html += ports
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def addIPExt(self, IP=None):
        #mac.delete_mac(name)
        if passwd.readCookie():
            mac.authorize_ip(IP)
            html = open('html.html','r').read()
            html += '<form action="index" method="post"><button type="Submit">retour à l\'accueil</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def addsolo(self):
        #mac.delete_mac(name)
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += open('Manage/FormAdd.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def addsolomac(self):
        #mac.delete_mac(name)
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += open('Manage/FormAddMac.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

    @cherrypy.expose
    def addsolomac2(self, MAC=None):
        if passwd.readCookie():
            mac.add_mac(MAC)
            html = open('html.html','r').read()
            html += "<h1>La machine avec l'adresse mac : "+MAC+" à bien été ajoutée</h1>"
            html += '<form action="Manage" method="post"><button type="Submit">retour a la liste</button></form>'
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()


    @cherrypy.expose
    def scans(self):
        #mac.delete_mac(name)
        if passwd.readCookie():
            html = open('html.html','r').read()
            html += open('Manage/Add.html','r').read()
            html += open('footer.html','r').read()
        else:
            html = open('error.html','r').read()
        template = Template(html)
        return template.render()

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on':'True',
            'tools.staticdir.dir':'static'
        },
        '/img':{
            'tools.staticdir.on':'True',
            'tools.staticdir.dir':'img'
                }
    }
    server_config={
        'server.socket_host': '192.168.1.38',
        'server.socket_port':443,
        'server.ssl_module':'builtin',
        'server.ssl_certificate':'/root/keys/cert.pem',
        'server.ssl_private_key':'/root/keys/privkey.pem'
    }
    cherrypy.config.update(server_config)
    webapp = Webpage()
    cherrypy.quickstart(webapp, '/', conf)
