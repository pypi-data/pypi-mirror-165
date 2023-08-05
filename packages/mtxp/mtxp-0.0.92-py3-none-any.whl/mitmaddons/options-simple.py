"""
Basic skeleton of a mitmproxy addon.
Run as follows: mitmproxy -s anatomy.py
"""
from mitmproxy import ctx
import typing
class Counter2:
    def __init__(self):
        self.num = 0

    def request(self, flow):
        self.num = self.num + 1
        ctx.log.info("自2222s定2s义计数器2插件 %d flows：" % self.num)

    def load(self, loader):
        loader.add_option(
            name = "addheader",
            typespec = typing.Optional[int],
            default = None,
            help = "Add a header to responses",
        )
    # def configure(self, updates):
    #     if "addheader" in updates:
    #         if ctx.options.addheader is not None and ctx.options.addheader > 100:
    #             raise exceptions.OptionsError("addheader must be <= 100")
    def response(self, flow):
        if ctx.options.addheader is not None:
            flow.response.headers["addheader"] = str(ctx.options.addheader)
        flow.response.headers["aaaaaaa"] = str("ssssss")


addons = [
    Counter2()
]