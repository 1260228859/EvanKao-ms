from sanic import response

import logging

from views import order_bp

from sanicms.server import app
from sanicms.client import Client

logger = logging.getLogger('sanic')

# add blueprint
app.blueprint(order_bp)

@app.listener('before_server_start')
async def before_srver_start(app, loop):
    # TODO: 改为配置文件读取相关依赖应用服务
    app.user_client = Client('user-service', app=app)

@app.listener('before_server_stop')
async def before_server_stop(app, loop):
    app.user_client.close()

@app.route("/")
async def index(request):
    return 'order service Evankao'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=app.config['PORT'], debug=True)
