"""域名从定向
"""
from mitmproxy import http
from lib.aaa import foo

class MtHttpRedirectRequest:
    def __init__(self):
        pass

    def request(self, flow: http.HTTPFlow) -> None:
        if flow.request.pretty_host == "mt.l":
            """转发到nextjs api 后台（此后台的功能，将会逐步迁移到mitmproxy 插件的形式实现）"""
            flow.request.host = "localhost"
        if flow.request.pretty_host.endswith("baidu.com") and flow.request.path == "/hello":
            """范例：改写特定网址的路径内容"""
            flow.response = http.Response.make(
                200,  # (optional) status code
                # b"Hello World",  # (optional) content
                foo(),
                {"Content-Type": "text/html"}  # (optional) headers
            )

addons = [
    MtHttpRedirectRequest()
]
