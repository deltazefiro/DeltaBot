import logging
import sys

logger = logging.getLogger('DeltaBot')
handler = logging.StreamHandler(sys.stdout)

handler.setFormatter(
    logging.Formatter('[%(asctime)s][%(name)s.%(filename)s] %(levelname)s: %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S'))

logger.addHandler(handler)
logger.setLevel('INFO')