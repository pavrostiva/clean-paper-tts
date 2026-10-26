"""Convert scientific papers (PDF / HTML / MHTML) into clean, TTS-friendly HTML."""

from .convert import ConversionResult, convert
from .options import Options

__all__ = ["convert", "ConversionResult", "Options"]
__version__ = "0.1.0"
