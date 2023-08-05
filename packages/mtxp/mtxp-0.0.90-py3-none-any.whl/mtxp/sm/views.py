from . import sm_blue
from ..services.openvpn import startup_openvpn
from ..services.mtxtun import startup_mtxtun
import yaml
import logging
from os.path import join
from pathlib import Path
logger = logging.getLogger(__name__)


data_dir = join(Path(__file__).parent.parent, "data")

@sm_blue.route('/')
def home():
    return 'sm home'

   