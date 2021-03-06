from osv import osv, fields
from openerp import modules, tools
from datetime import datetime

class vehiculo(osv.osv):
  _name = "estacionamiento.vehiculo"

  def _get_monto(self, cr, uid, ids, field, arg, context=None):
      ve = self.pool.get('estacionamiento.vehiculo').browse(cr,uid,ids,context=context)
      monto = {}
      format = '%Y-%m-%d %H:%M:%S'
      for each in ve:
          monto[each.id] = 0
          if not (each.excento_pago):
              if (each.fecha_entrada and each.fecha_salida):
                  entrada = datetime.strptime(each.fecha_entrada, format)
                  salida = datetime.strptime(each.fecha_salida, format)
                  days = (salida - entrada).days
                  if days:
                      tiempo =  ((24 * days)+(24 - ((entrada - salida).seconds/3600)))
                  else:
                      tiempo =  (24 - ((entrada - salida).seconds/3600))
                  monto[each.id] = tiempo * each.t_tarifa.tarifa
      return monto

  def _check_length(self, cr, uid, ids, context=None):
      record = self.browse(cr, uid, ids, context=context)
      for data in record:
        if (len(data.matricula) < 6) or (len(data.matricula) > 7):
          return False
      return True

  def change_monto(self, cr, uid, ids, excento_pago, monto_pagar, context=None):
      if (excento_pago):
          return {"value":{"monto_pagar":0,}}
      else:
          return {"value":{"monto_pagar":monto_pagar,}}

  # Metodos del flujo trabajo
  def estacionamiento_entrada(self, cr, uid, ids):
    self.write(cr, uid, ids, { 'state' : 'entrada' })
    return True

  def estacionamiento_salida(self, cr, uid, ids):
    self.write(cr, uid, ids, { 'state' : 'salida' })
    return True

  def estacionamiento_cobrar(self, cr, uid, ids):
    self.write(cr, uid, ids, { 'state' : 'cobrar' })
    return True


  _columns = {
    "matricula" : fields.char("Matricula",size=10,required=True),
    "marca" : fields.char("Marca",size=256),
    "tipo" : fields.selection([("s", "sedan"), ("ca", "camioneta"), ("co", "camion"),
                              ], "Tipo de Vehiculo"),
    "fecha_entrada" : fields.datetime('Fecha de Entrada'),
    "fecha_salida" : fields.datetime('Fecha de Salida'),
    "excento_pago" : fields.boolean("Excento de pago"),
    "t_tarifa" : fields.many2one('estacionamiento.tarifa', "Tipo de Tarifa", required=True),
    "conductor": fields.one2many("estacionamiento.conductor",
                                 "vehiculo_id", "Cedula del conductor", ondelete="cascade"),
    "monto_pagar": fields.function(_get_monto, method=True, type="float", string="Monto a Pagar"),

    # Atributo para el flujo de trabajo
    "state": fields.selection([
        ("entrada", "Entrada"),
        ("salida", "Salida"),
        ("cobrar", "Cobrar")], "Estado", readonly=True),
  }

  _defaults = {
    "tipo" : "s",
  }

  _constraints = [(_check_length, "Error: Matricula", ["matricula"])]

  _sql_constraints = [("matricula_uniq", "unique(matricula)",
                       "La matricula debe ser unica")]
vehiculo()

class tarifa(osv.osv):
  _name = "estacionamiento.tarifa"
  _columns = {
    "t_tarifa" : fields.char("Tipo de Tarifa", size=100, required=True),
    "tarifa" : fields.float("Tarifa", digits=(3,2)),
  }
tarifa()

class conductor(osv.osv):
  _name = "estacionamiento.conductor"
  _columns = {
    "cedula" : fields.char("Cedula del Conductor", size=20, required=True),
    "nombre" : fields.char("Nombre del Conductor", size=20),
    "vehiculo_id" : fields.many2one("estacionamiento.vehiculo", "Vehiculo ID", required=True, ondelete="cascade"),
  }
conductor()
