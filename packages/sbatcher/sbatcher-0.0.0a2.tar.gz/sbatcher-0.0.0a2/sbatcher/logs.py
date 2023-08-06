import logging
import sys

import sbatcher

logger = logging.getLogger(sbatcher.__name__)

formatter = logging.Formatter('%(name)s %(levelname)s: %(message)s')
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.addHandler(handler)
