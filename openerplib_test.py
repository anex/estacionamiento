import openerplib
connection = openerplib.get_connection(hostname="localhost", port=8069,
                                       database="curso",
                                       login="admin", password="123456")
connection.check_login()
print "Logged in as %s (uid:%d)" % (connection.login, connection.user_id)
vehiculo_model = connection.get_model("estacionamiento.vehiculo")
vehiculo = {
  "matricula": "aaa333",
  "marca": "ford",
}
vehiculo_id = vehiculo_model.create(vehiculo)
