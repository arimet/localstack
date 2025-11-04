"""
Custom utilities package for Lambda functions.

This package provides reusable utilities that can be shared
across Lambda functions using Lambda Layers.
"""

from .display import format_response, get_greeting

__all__ = ['format_response', 'get_greeting']

__version__ = '1.0.0'
