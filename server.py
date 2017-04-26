import web
import socketserver

##
# WEB SERVER
##

PORT = 8000

socketserver.TCPServer.allow_reuse_adress = True #Para que no tenga que cambiar de puerto

#Handler = http.server.SimpleHTTPRequestHandler --> handler de la biblioteca python
Handler = web.testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
