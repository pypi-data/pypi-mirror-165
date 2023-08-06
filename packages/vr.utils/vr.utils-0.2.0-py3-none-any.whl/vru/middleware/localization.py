#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# A class for translating messages (mainly for error text)

import os
from fastapi import Request
from ..translate import get_gettext
from fastapi.responses import JSONResponse
from ..exceptions.exceptions import build_internal_error_detail


# =============================================================================
class SystemLocalizationMiddleware:
    """
    Middleware that creates gettext.GNUTranslations.gettext by Accept-Language
    and save to request.state.
    """
    def __init__(self, domain: str, translation_dir: str, lang: str = "ru"):
        self.translation_dir = translation_dir
        self.domain = domain
        self._lang = lang

    # -------------------------------------------------------------------------
    async def __call__(self, request: Request, call_next):
        language_code = request.headers.get("accept-language", self._lang)

        if language_code and "," in language_code:
            language_code = language_code.split(",")[0]
        request.state.gettext = get_gettext(
            self.domain, self.translation_dir, language_code)

        try:
            return await call_next(request)
        except Exception as exc:
            content = {"detail": build_internal_error_detail(exc)}
            return JSONResponse(content, status_code=500)


# =============================================================================
localization_middleware = SystemLocalizationMiddleware(
    domain="base", translation_dir=os.environ.get("LOCALE_DIR", "/locales"))
