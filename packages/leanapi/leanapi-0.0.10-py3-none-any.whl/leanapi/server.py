from typing import List, Callable

import uvicorn
from fastapi import FastAPI
from pydantic import BaseSettings
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware

from .config import ApiConfig
from .router import LeanRouter

router = LeanRouter()


class Modules:
    @classmethod
    def controllers(cls, modules: List[any]):
        return cls


class ApiServer:

    def __init__(self, r, configs):
        self.settings: ApiConfig = ApiConfig.load() if configs is None else configs
        self.host = ""
        self.port = 8001
        self.router = r
        self.app = FastAPI(
            title=self.settings.NAME,
            description=self.settings.DESCRIPTION,
            version=self.settings.VERSION,
            docs_url=f"{self.settings.BASE_URL}/docs",
            redoc_url=None,
            openapi_url=f"{self.settings.BASE_URL}/openapi.json"
        )

    @classmethod
    def config(cls, configs: BaseSettings = None):
        """
        Class configuration set and create instance
        """
        _class = cls(router, configs)
        return _class

    def loads(self, modules: List[any]):
        return self

    def middleware(self, func: Callable[[Request, Response], None]):
        @self.app.middleware("http")
        async def appmiddleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
            response = await call_next(request)
            func(request, response)
            return response

        return self

    def request_middleware(self, func: Callable[[Request], None]):
        @self.app.middleware("http")
        async def appmiddleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
            func(request)
            response = await call_next(request)
            return response

        return self

    def server(self):
        """
        Configuration server

        ApiServer.config().loads().server().start()
        """
        if self.settings.BACKEND_CORS_ORIGINS:
            self.app.add_middleware(
                CORSMiddleware,
                allow_origins=[str(origin) for origin in self.settings.BACKEND_CORS_ORIGINS],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        self.app.include_router(router)
        return self

    def start(self, host="127.0.0.1", port=8001):
        """
        Server will be start with uvicorn
        if host and post not defined then server use default values
        """
        self.host = host
        self.port = port
        print(f"[Host]: http://{self.host}:{self.port}")
        print(f"[Swagger]: http://{self.host}:{self.port}/{self.settings.BASE_URL.lstrip('/').rstrip('/')}/docs")
        print("*" * 87)
        uvicorn.run(self.app, host=self.host, port=self.port)
