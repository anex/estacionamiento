from osv import osv, fields
from openerp import modules, tools
from datetime import datetime

class taller_vehiculo(osv.osv):
  _name = "taller.vehiculo"
  _inherit = "estacionamiento.vehiculo"
  _columns = {
    "color" : fields.char("Color",size=100),
  }
taller_vehiculo()
