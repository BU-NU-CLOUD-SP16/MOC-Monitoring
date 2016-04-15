# Make sure ipmitool and sdr_cache is created
import subprocess
import logging

import monasca_agent.collector.checks as checks

log = logging.getLogger(__name__)

class Power(checks.AgentCheck):

    def __init__(self, name, init_config, agent_config):
        super(Power, self).__init__(name, init_config, agent_config)

    def check(self, instance):
        ## Capture Power Stats
        dimensions = self._set_dimensions(None, instance)
		sensorListProc = subprocess.Popen(['sudo','ipmitool','sensor','list'] ,stdout=subprocess.PIPE)
		sensorList = sensorListProc.stdout.read()
		sensorList = sensorList.split("\n")

		for s in range(0,len(sensorList)-1):
			temp = [x.strip() for x in sensorList[s].split('|')]
			if "POWER_USAGE" in temp[0]:
				data = float(temp[1])
				self.gauge('power.usage', data, dimensions)
				log.debug('Collected power metric')
				break
