import os
from . import admin_blue


# admin模块
@admin_blue.route('')
def adminHome():
    return 'admin home'


@admin_blue.route('/deluser')
def deluser():
    return 'deluser'


@admin_blue.route('/env')
def api_info():
    items = {k: os.environ.get(k) for k in os.environ.keys()}
    return {
        "success": True,
        "data": {
            "env": items,
            "__file__": __file__
        }
    }
