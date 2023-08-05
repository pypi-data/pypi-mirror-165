#!/usr/bin/env python3

print("设置gitpod开发环境")
import os


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



