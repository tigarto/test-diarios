"""
Para correr:

1. Copiar el archivo en la carpeta ext de pox.

2. Ejecutar el siguiente comando ./pox.py log.level --DEBUG dia3_pox2flow.py

"""

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpid_to_str
from pox.lib.util import str_to_bool
import time

log = core.getLogger()

rules = [
          {'in_port': 2, 'out_port': 1},
          {'in_port': 1, 'out_port': 2}
        ]


class POX2flow (object):
    def __init__ (self):
        core.openflow.addListeners(self)
        
    def _handle_ConnectionUp (self, event):
        log.debug("*** Switch %s has come up ***", dpid_to_str(event.dpid))
        for v in rules:
            msg = of.ofp_flow_mod()                                # Mensaje FlowMod
            match = of.ofp_match(in_port = v['in_port'])           # Instancia asociada al match
            action = of.ofp_action_output(port = v['out_port'])    #Instancia asociada a la action
            msg.match = match                                      # Agregando el match al mensaje FlowMod
            msg.actions.append(action)                             # Agregando el action al mensaje FlowMod
            event.connection.send(msg)                             # Envio del flujo al switch
            log.debug("+ Installing flow --> in_port: %d, out_port: %d.",v['in_port'],v['out_port'])

def launch ():
    core.registerNew(POX2flow)

