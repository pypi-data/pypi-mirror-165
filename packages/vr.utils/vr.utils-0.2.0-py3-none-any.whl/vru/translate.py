#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CRC:0:0
# A class for translating messages

import os
import gettext
import typing
from inspect import currentframe
from fastapi.responses import JSONResponse


# =============================================================================
# installing translations
try:
    localedir_ = os.environ.get("LOCALE_DIR", "/locales")
    ru = gettext.translation("base", localedir=localedir_, languages=["ru"])
    ru.install()
    ru_gettext = ru.gettext
except (FileNotFoundError, AttributeError):
    ru_gettext = gettext.gettext


# =============================================================================
# noinspection PyPep8Naming
def T(s):
    """Replacing f-strings"""
    _s = ru_gettext(s).replace("'", '"')
    frame = currentframe().f_back
    return eval(f"f'{_s}'", frame.f_locals, frame.f_globals).replace('"', "'")


# =============================================================================
class LazyString(str):
    """
    LazyString object to localization

    Example:
        lazy = LazyString('my string')
        TranslateJsonResponse(lazy)

    Or if you want with dynamic values:
        lazy = LazyString('My name is {name}', name='Edvard')
        TranslateJsonResponse(lazy)
    """
    def __new__(cls, value, **kwargs):
        obj = super().__new__(cls, value)
        obj.named_placeholders = kwargs
        return obj


# =============================================================================
class TranslatableStringField(LazyString):
    """Object for register localization. Use like pydantic type."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return cls(v)


# =============================================================================
def lazy_gettext(string: str, **kwargs):
    """
    lazy gettext wrapper.

    Example:
        lazy = lazy_gettext('my string')
        TranslateJsonResponse(lazy)

    Or if you want with dynamic values:
        lazy = lazy_gettext('My name is {name}', name='Edvard')
        TranslateJsonResponse(lazy)
    """
    return LazyString(string, **kwargs)


# =============================================================================
def get_gettext(domain: str, localedir: str, language_code: str = None):
    """Get gettext func by locale or default gettext"""
    try:
        gnu = gettext.translation(domain,
                                  localedir=localedir,
                                  languages=[language_code])
        return gnu.gettext
    except (FileNotFoundError, AttributeError):
        return gettext.gettext


# =============================================================================
def prepare_content_to_translate(value: typing.Any, content: gettext.gettext):
    """Prepare data structure to localization"""
    if isinstance(value, LazyString):
        prepared_content = str(content(value))
        return (prepared_content.format(**value.named_placeholders)
                if value.named_placeholders else prepared_content)
    elif isinstance(value, dict):
        return {k: prepare_content_to_translate(v, content)
                for k, v in value.items()}
    elif isinstance(value, list):
        return [prepare_content_to_translate(item, content) for item in value]
    return value


class TranslateJsonResponse(JSONResponse):
    """Response that localization content"""
    def __init__(self, content: typing.Any = None, *args, **kwargs):
        self.original_content = content
        super().__init__(content, *args, **kwargs)

    def translate_content(self, content: gettext.GNUTranslations.gettext):
        content = prepare_content_to_translate(self.original_content, content)
        return TranslateJsonResponse(content,
                                     status_code=self.status_code,
                                     background=self.background)
