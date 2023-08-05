#!/usr/bin/env python3

import os
from dotenv import load_dotenv, find_dotenv
import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv(".env")

def check_env():
    env_names = [
        "GIT_TOKEN",
        "DOCKER_HUB_NAME",
        "DOCKER_HUB_PASSWORD",
    ]
    for item in env_names:
        print(item)
        if not os.environ.get(item):
            print(f"error: need env {item}")
        return False

    return True
    
if not check_env():
    print("please setup dev envroments")
    exit()



