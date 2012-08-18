import logging

logging.root.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
#fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fmt = logging.Formatter('%(name)s - %(message)s')
ch.setFormatter(fmt)
logging.root.addHandler(ch)
