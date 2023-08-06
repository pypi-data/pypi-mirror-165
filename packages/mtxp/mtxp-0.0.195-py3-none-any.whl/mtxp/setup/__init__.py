# import os
# from pathlib import Path
# from . import setup_nginx
# from mtxp import settings
# import logging
# logger = logging.getLogger(__name__)



# def setup():
#     logger.info("setup __init__")
#     if Path("/.dockerenv").exists():
#         html_root = settings.getHtmlRoot()
#         logger.info(f"html root {html_root}")
#         setup_nginx.setup_nginx(html_root, smApiPrefix="/smapi")