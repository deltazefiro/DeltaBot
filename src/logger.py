import logging
import sys

logger = logging.getLogger('DeltaBot')
logger.setLevel('INFO')
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('[%(asctime)s][%(name)s][%(pathname)s] %(levelname)s: %(message)s'))
logger.addHandler(handler)