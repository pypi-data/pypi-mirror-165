import string
import random
from functools import lru_cache
from typing import Sequence, Tuple
from django.utils.module_loading import import_string
from django.contrib.contenttypes.models import ContentType
from django.db import models


ObjectDefinition = Tuple[ContentType, int]
ALPHABET = list(string.ascii_letters)


@lru_cache
def cached_import_string(path: str):
    return import_string(path)


def upset(current, add):
    return (
        (current if isinstance(current, set) else set(current))
        |
        (add if isinstance(add, set) else set(add))
    )


def make_random_code(symbols: int, alphabet: Sequence[str] = ALPHABET) -> str:
    return ''.join(random.sample(alphabet * symbols, symbols))


def obj_to_definition(objects: Sequence[models.Model]):
    cache = ContentType.objects.get_for_models(*{x.__class__ for x in objects})

    return [(cache[x.__class__], x.pk) for x in objects]
