import logging
import sys

import sbatcher

logger = logging.getLogger(sbatcher.__name__)

formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
handler = logging.StreamHandler(sys.out)
handler.setFormatter(formatter)
logger.addHandler(handler)
