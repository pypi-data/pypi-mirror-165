#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# Exception handlers

import time
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY as HTTP_422
from tortoise.exceptions import ValidationError

from vru.translate import TranslateJsonResponse, lazy_gettext, T
from .exceptions import build_error_detail, build_internal_error_detail


# =============================================================================
# noinspection PyUnusedLocal
async def _orm_validation_exception_handler(request, exc: ValidationError):
    err_str = str(exc)

    # text formation error for too long or short value
    if "Length of" in err_str and err_str.count("'") >= 2:
        name, val = (s := err_str.replace("Length of", "").split("'"))[0], s[2]
        name = name.split(':')[0] if ":" in err_str else name
        err_str = T("Incorrect field length <<{name}>> [{val.strip()}]")

    detail = build_error_detail(typ="TortoiseValidationError", msg=err_str)
    return JSONResponse({"detail": detail}, status_code=HTTP_422)


# =============================================================================
async def _http_exception_handler(request, exc: HTTPException):
    """
    Http exception handler with localization
    """
    response = TranslateJsonResponse(
        {"detail": exc.detail},
        status_code=exc.status_code
    )
    return response.translate_content(request.state.gettext)


# =============================================================================
async def _validation_exception_handler(request, exc: RequestValidationError):
    """
    Validation exception handler with localization
    """
    for error in exc.errors():
        error["msg"] = lazy_gettext(error["msg"])
    response = TranslateJsonResponse({"detail": exc.errors()},
                                     status_code=HTTP_422)
    return response.translate_content(request.state.gettext)


# =============================================================================
async def exception_handling(request: Request, call_next):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    except Exception as exc:
        return JSONResponse({
            "detail": build_internal_error_detail(exc)},
            status_code=500)


# =============================================================================
def add_exception_handlers(_app):
    handlers = [
        (ValidationError, _orm_validation_exception_handler),
        (HTTPException, _http_exception_handler),
        (RequestValidationError, _validation_exception_handler),
    ]
    for handler in handlers:
        _app.add_exception_handler(*handler)

    _app.middleware("http")(exception_handling)
