import xmlrpclib
username = "admin"
pwd = "123456"
dbname = "curso"
model = "estacionamiento.uso"
def connect(username, pwd, dbname):
    # Get the uid
    sock_common = xmlrpclib.ServerProxy ('http://localhost:8069/xmlrpc/common')
    uid = sock_common.login(dbname, username, pwd)
    sock = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/object')
    return sock, uid
(sock, uid) = connect(username, pwd, dbname)
print sock.execute(dbname, uid, pwd, model, 'search', "")
