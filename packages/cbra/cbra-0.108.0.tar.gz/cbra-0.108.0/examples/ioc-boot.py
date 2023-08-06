import cbra
import uvicorn
from cbra.ext import ioc


class Foo:

    async def on_asgi_boot(self, app: cbra.Application):
        print("Running boot function")

    async def on_asgi_shutdown(self, app: cbra.Application):
        print("Running shutdown function")


ioc.provide('Foo', Foo())
app = cbra.Application()

if __name__ == '__main__':
    uvicorn.run('__main__:app', port=5000)
