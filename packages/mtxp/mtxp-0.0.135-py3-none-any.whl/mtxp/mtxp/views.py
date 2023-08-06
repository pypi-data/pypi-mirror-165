from . import mtxp_blue
from ..services.openvpn import startup_openvpn
from ..services.mtxtun import startup_mtxtun
import yaml
import logging
from os.path import join
from pathlib import Path
logger = logging.getLogger(__name__)


data_dir = join(Path(__file__).parent.parent, "data")

@mtxp_blue.route('/')
def home():
    return 'mtxphome'

 

# @mtxp_blue.route("/start_tor")
# def api_start_tor():
#     logger.info("api_startup_tor")
#     try:
#         startup_tor("logs/.tor.log")
#         return {"success": True}
#     except Exception as unknow:
#         # traceback.print_exception(unknow)
#         logger.exception(unknow)
#         return {
#             "success": False,
#             "data": str(unknow)
#         }

# @mtxp_blue.route("/start_openvpn")
# def api_start_openvpn():
#     """openvpn 功能未完成, 目前也用不上"""
#     logger.info("api_startup_openvpn")
#     logger.info("openvpn 功能未完成，原因是打包时,ta.key文件不知道为什么打包不进去。")
#     try:
#         startup_openvpn("logs/.openvpn.log")
#         return {"success": True}
#     except Exception as unknow:
#         logger.exception(unknow)
#         return {
#             "success": False,
#             "data": str(unknow)
#         }

# @mtxp_blue.route(f"/start_clash")
# def api_start_clash():
#     logger.info("api_start_clash")
#     try:
#         startup_clash("logs/.clash.log")
#         return {"success": True}
#     except Exception as unknow:
#         logger.exception(unknow)
#         return {
#             "success": False,
#             "data": str(unknow)
#     }


@mtxp_blue.route(f"/start_mtxtun")
def api_start_mtxtun():
    logger.info("api start_mtxtun")
    try:
        startup_mtxtun("logs/.mtxtun.log")
        return {"success": True}
    except Exception as unknow:
        logger.exception(unknow)
        return {
            "success": False,
            "data": str(unknow)
        }


# @mtxp_blue.route(f"/start_pf")
# def api_start_pf():
#     """旧的mtxtun端口加密转发改版"""
#     logger.info("api start_mtxtun2")
#     try:
#         # 加载配置
#         yaml_content = None
#         with open(join(data_dir, "mtxtun.yml"), 'r', encoding="utf-8") as f:
#             yaml_content = yaml.load(f, Loader=yaml.FullLoader)
#         pf_items = yaml_content["pf"]["items"]
#         # 启动端口转发
#         for item in pf_items:
#             startup_pf(item["lhost"],item["lport"],item["rhost"],item["rport"])
#         return {"success": True,
#                 "data": pf_items
#             }
#     except Exception as unknow:
#         logger.exception(unknow)
#         return {
#             "success": False,
#             "data": str(unknow)
#         }

@mtxp_blue.route(f"/tun_config")
def api_tun_config():
    try:
        with open(join(data_dir, "mtxtun.yml"), 'r', encoding="utf-8") as f:
            yaml_content = yaml.load(f, Loader=yaml.FullLoader)
            return {
                "success": True,
                "data": yaml_content
            }
    except Exception as unknow:
        logger.exception(unknow)
        return {
            "success": False,
            "data": str(unknow)
        }