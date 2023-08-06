#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# Middleware for FastAPI

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .localization import localization_middleware


def add_cors_middleware(_app, **allow_params):
    _app.add_middleware(CORSMiddleware, **allow_params)


def add_localization_middleware(_app):
    _app.add_middleware(BaseHTTPMiddleware, dispatch=localization_middleware)


def add_gzip_middleware(_app, minimum_size=1000):
    _app.add_middleware(GZipMiddleware, minimum_size=minimum_size)
