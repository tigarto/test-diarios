
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

rules = [{'in_port': 2, 'out_port': 1},{'in_port': 1, 'out_port': 2}]

class Ryu2flow(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]
    def __init__(self, *args, **kwargs):
        super(Ryu2flow, self).__init__(*args, **kwargs)
        
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        self.logger.debug('*** Switch 0x%016x has come up ***',  ev.msg.datapath_id)
        for v in rules:
            msg = ev.msg
            datapath = msg.datapath
            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser
            match = parser.OFPMatch(in_port = v['in_port'])
            actions = [parser.OFPActionOutput(v['out_port'])]
            mod = datapath.ofproto_parser.OFPFlowMod(datapath=datapath, match=match, actions=actions)
            datapath.send_msg(mod)
            self.logger.debug("+ Installing flow --> in_port: %d, out_port: %d.",v['in_port'],v['out_port'])
