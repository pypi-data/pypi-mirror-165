"""
Package for extracting metadata from pictures.
"""

import logging

from typing import Dict
from PIL import Image


def get_dimensions(picture_path: str) -> Dict[str, str]:
    """
    Returns a dictionary containing the dimension of
    the picture found at `picture_path`.
    """
    picture = None
    try:
        picture = Image.open(picture_path)
        width, height = picture.size
        logging.info("Got image size")
        return {"height": str(height), "width": str(width)}
    finally:
        if picture:
            picture.close()
