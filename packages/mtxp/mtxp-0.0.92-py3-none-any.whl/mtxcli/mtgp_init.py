#!/usr/bin/env python3

import os
from dotenv import load_dotenv, find_dotenv



ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

load_dotenv(".env")


import logging
logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_env():
    env_names = [
        "GIT_TOKEN",
        "DOCKER_HUB_USER",
        "DOCKER_HUB_PASSWORD",
    ]

    # print(os.environ)
    for item in env_names:
        print(f"---{item}")
        
        if not os.environ.get(item):            
            print(f"error: need env {item}")
            return False

    return True
    
def main():
    if not check_env():
        print("please setup dev envroments")
        exit()

    else:
        print("TODO: continue..")



if __name__ == '__main__':
    main()