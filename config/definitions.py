import os
import yaml
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

_CFG = yaml.load(open(os.path.join(ROOT_DIR, 'config', 'config.yaml'), 'r'), Loader=yaml.FullLoader)

