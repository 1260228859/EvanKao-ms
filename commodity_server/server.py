from sanic import response

import logging

from views import commodity_bp

from sanicms.server import app
from sanicms.client import Client

logger = logging.getLogger('sanic')

# add blueprint
app.blueprint(commodity_bp)


@app.listener('before_server_start')
async def before_srver_start(app, loop):
    # TODO: 改为配置文件读取相关依赖应用服务 或则获取统一的服务注册中心 获取相关服务
    app.user_client = Client('user-service', app=app)
    # app.order_client = Client('order-service', app=app)


@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    app.user_client.close()
    # app.order_client.close()


@app.route("/")
async def index(request):
    return 'commodity service Evankao'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config['PORT'], debug=True)
