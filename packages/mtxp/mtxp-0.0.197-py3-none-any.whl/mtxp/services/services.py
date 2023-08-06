import os
import sys
import threading
import logging
from .clash import ClashService
from .tor import TorService
from .pf import PfService
from .nginx import NginxService
from .phpfpm import PhpFpmService
from .wordpress import WordPressService
from .tailscale import TailscaleService
# from services.mtsm import MtsmService
logger = logging.getLogger(__name__)

def start_all_services():
    logger.info(f"start_all_services() {os.getpid()}")
    ClashService().start()
    TorService().start()
    PfService().start()
    NginxService().start()
    PhpFpmService().start()    
    # MtsmService().start()
    WordPressService().start()
    TailscaleService().start()
