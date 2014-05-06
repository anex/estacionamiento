import time
from datetime import datetime
from openerp.report import report_sxw

class report_vehiculo(report_sxw.rml_parse):
  def __init__(self, cr, uid, name, context):
    super(report_vehiculo, self).__init__(cr, uid, name, context=context)
    self.localcontext.update({
      'time': time, 
      'datetime': datetime, 
    })  

report_sxw.report_sxw('report.estacionamiento.vehiculo', 'estacionamiento.vehiculo', 'addons/estacionamiento/report/vehiculo.rml', parser=report_vehiculo, header="False")
