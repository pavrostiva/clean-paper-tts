"""PDF reader. Pipeline: lines -> regions (figures/tables/formulas) -> reading order -> paragraphs."""

from .reader import read_pdf

__all__ = ["read_pdf"]
