import microscope.testsuite.devices
from time import sleep;

import logging
logging.basicConfig()

c = microscope.testsuite.devices.TestCamera()

c._logger.setLevel( logging.DEBUG )

c.initialize()
c.enable()
c.set_client("FAIRSIM:localhost")


for i in range(0,10000):
    c.soft_trigger()
    sleep(0.1)

sleep(1)    # wait for image send to complete
c.shutdown()
