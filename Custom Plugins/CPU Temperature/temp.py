# Require lm_sensor and PySensors python package
import logging
import sensors

import monasca_agent.collector.checks as checks

log = logging.getLogger(__name__)

class Temp(checks.AgentCheck):

    def __init__(self, name, init_config, agent_config):
        super(Temp, self).__init__(name, init_config, agent_config)

    def check(self, instance):
        ## Capture CPU temperature stats
        dimensions = self._set_dimensions(None, instance)

        sensors.init()
        stats ={}
        try:
          for chip in sensors.iter_detected_chips():
            # Only temps from ISA adpters that are deteced by lm_sensors
            if (chip.adapter_name == "ISA adapter"):
              for feature in chip:
                if "Core" in feature.label:
                  name = feature.label.replace(" ", "_")
                  name = name.lower()
                  stats["cpu."+str(chip)+"."+str(name)+"_temperature"] = feature.get_value()
                elif "Physical id" in feature.label:
                  name = feature.label.replace(" ", "_")
                  name = name.lower()
                  stats["cpu."+str(chip)+".max_temperature"] = feature.get_value()
        finally:
          sensors.cleanup()
        for key, value in stats.iteritems():
          # Writes data to monasca that will go to InfluxDB
          self.gauge(key, value, dimensions)
        log.debug('Collected {0} cpu metrics'.format(len(stats)))                                                                                        1,1           Top