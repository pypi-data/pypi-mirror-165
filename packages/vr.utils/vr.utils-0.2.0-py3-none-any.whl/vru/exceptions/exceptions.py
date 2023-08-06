#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# Classes for exceptions

import os
from fastapi import HTTPException
from inspect import stack, getframeinfo
from loguru import logger


# =============================================================================
def _build_loc():
    """Generating information about the file and function from where the
    exception was caused"""
    for row in stack():
        info = getframeinfo(row[0])
        if info.filename == __file__:
            continue
        return [f"FILE: {info.filename}",
                f"LINE: {info.lineno}",
                f"FUNC: {info.function}"]
    return []


# =============================================================================
def build_error_detail(**kwargs):
    """Forming a string for exception information"""
    msg = kwargs.get("msg", "")
    typ = kwargs.get("typ", "")
    logger.warning(msg)
    return [{"loc": _build_loc(), "msg": msg, "type": typ}]


# =============================================================================
def build_internal_error_detail(exc: Exception):
    msg = str(exc)
    typ = type(exc).__name__
    loc = []

    tb = exc.__traceback__
    while tb is not None:
        if "/python3." not in (filename := tb.tb_frame.f_code.co_filename):
            err_line = "?"
            if os.path.exists(filename):
                with open(filename) as src:
                    err_line = src.readlines()[tb.tb_lineno-1].strip()
            loc.append({"filename": filename,
                        "name": tb.tb_frame.f_code.co_name,
                        "lineno": tb.tb_lineno,
                        "line": err_line.replace('"', "'")})
        tb = tb.tb_next

    return [{"loc": loc, "msg": msg.replace('"', "'"), "type": typ}]


# =============================================================================
class AppException(HTTPException):
    """Application exception base class"""
    def __init__(self, status_code: int, **kwargs) -> None:
        super().__init__(status_code=status_code,
                         detail=build_error_detail(**kwargs),
                         headers=kwargs.get("headers"))


# =============================================================================
class BadRequestError(AppException):
    def __init__(self, **kwargs) -> None:
        if not kwargs.get("typ"):
            kwargs.update({"typ": "bad request"})
        super().__init__(status_code=400, **kwargs)


# =============================================================================
class UnauthorizedError(AppException):
    def __init__(self, **kwargs) -> None:
        if not kwargs.get("typ"):
            kwargs.update({"typ": "unauthorized"})
        super().__init__(status_code=401, **kwargs)


# =============================================================================
class ForbiddenError(AppException):
    def __init__(self, **kwargs) -> None:
        if not kwargs.get("typ"):
            kwargs.update({"typ": "forbidden"})
        super().__init__(status_code=403, **kwargs)


# =============================================================================
class NotFoundError(AppException):
    def __init__(self, **kwargs) -> None:
        if not kwargs.get("typ"):
            kwargs.update({"typ": "not found"})
        super().__init__(status_code=404, **kwargs)


# =============================================================================
class InternalServerError(AppException):
    def __init__(self, **kwargs) -> None:
        if not kwargs.get("typ"):
            kwargs.update({"typ": "internal server error"})
        super().__init__(status_code=500, **kwargs)


# =============================================================================
class LockedServerError(AppException):
    def __init__(self, **kwargs) -> None:
        if not kwargs.get("typ"):
            kwargs.update({"typ": "locked server error"})
        super().__init__(status_code=423, **kwargs)
