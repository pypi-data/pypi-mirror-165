import os
import sys
import threading
import logging
from services.clash import ClashService
from services.tor import TorService
from services.pf import PfService
from services.nginx import NginxService
from services.phpfpm import PhpFpmService
from services.wordpress import WordPressService
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
