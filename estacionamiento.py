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
          try:
              entrada = datetime.strptime(each.fecha_entrada, format)
              salida = datetime.strptime(each.fecha_salida, format)
              tiempo =  (24 - ((entrada - salida).seconds/3600))
              monto[each.id] = tiempo * each.t_tarifa.tarifa
          except:
              monto[each.id] = 0
      return monto

  _columns = {
    "matricula" : fields.char("Matricula",size=10,required=True),
    "marca" : fields.char("Marca",size=256,required=True),
    "tipo" : fields.selection([("s", "sedan"), ("ca", "camioneta"), ("co", "camion"),
                              ], "Tipo de Vehiculo"),
    "fecha_entrada" : fields.datetime('Fecha de Entrada'),
    "fecha_salida" : fields.datetime('Fecha de Salida'),
    "excento_pago" : fields.boolean("Excento de pago"),
    "t_tarifa" : fields.many2one('estacionamiento.tarifa', "Tipo de Tarifa"),
    "conductor": fields.one2many("estacionamiento.conductor",
                                 "vehiculo_id", "Cedula del conductor", ondelete="cascade"),
    "monto_pagar": fields.function(_get_monto, method=True, type="float", string="Monto a Pagar"),
  }

  _defaults = {
    "tipo" : "s",
  }
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
