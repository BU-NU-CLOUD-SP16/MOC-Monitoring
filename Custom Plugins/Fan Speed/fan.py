# Make sure ipmitool and sdr_cache is created
import subprocess
import logging

import monasca_agent.collector.checks as checks

log = logging.getLogger(__name__)

class Fan(checks.AgentCheck):

    def __init__(self, name, init_config, agent_config):
        super(Fan, self).__init__(name, init_config, agent_config)

    def check(self, instance):
        ## Capture Power Stats
        dimensions = self._set_dimensions(None, instance)

		sensorListProc = subprocess.Popen(['sudo','ipmitool','sensor','list'] ,stdout=subprocess.PIPE)
		sensorList = sensorListProc.stdout.read()
		sensorList = sensorList.split("\n")

		stats ={}
		for s in range(0,len(sensorList)-1):
			sensor = [x.strip() for x in sensorList[s].split('|')]
			if "FAN" in sensor[0] and "TACH" in sensor[0]:
				# fanNum = sensor[0]
				# fanNum = fanNum[fanNum.index('N')+1:fanNum.index('_')]
				# tachNum = sensor[0]
				# tachNum = tachNum[len(tachNum)-1:]
				data = int(float(sensor[1]))
				fanTach = sensor[0].lower()
				stats["fan."+str(fanTach)+".speed"] = data 
		for key, value in stats.iteritems():
        	# Writes data to monasca that will go to InfluxDB
        	self.gauge(key, value, dimensions)
		log.debug('Collected {0} fan metrics'.format(len(stats)))
