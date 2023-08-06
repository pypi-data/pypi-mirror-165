from typing import TYPE_CHECKING, Dict, List, Optional, Sequence, Set
from collections import OrderedDict

from django.db import models

from pxd_combinable_groups.services import permissions_collector

from ..models import ObjectAccess
from ..utils import ObjectDefinition, upset, obj_to_definition

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser as User


USER_CACHE_KEY_TEMPLATE = '_object_access_{content_type}_{pk}'
EMPTY = object()


def gather_object_accesses(
    accesses: Sequence[ObjectAccess],
    update: bool = True,
) -> List[ObjectAccess]:
    collected = permissions_collector.collect_sets(
        access.group_ids
        for access in accesses
    )
    accesses = accesses if isinstance(accesses, list) else list(accesses)

    for i, permissions in enumerate(collected):
        accesses[i].gathered_permission_ids = list(upset(
            permissions, accesses[i].permission_ids
        ))

    if update:
        ObjectAccess.objects.bulk_update(accesses, fields=(
            'gathered_permission_ids',
        ))

    return accesses


def objects_for_user_raw(
    user: 'User',
    objects: Sequence[ObjectDefinition],
) -> List[Optional[ObjectAccess]]:
    total = len(objects)

    if total == 0:
        return []

    definitions = OrderedDict(
        (
            USER_CACHE_KEY_TEMPLATE.format(content_type=content_type.pk, pk=pk),
            (content_type, pk),
        )
        for content_type, pk in objects
    )
    resolved: Dict[str, ObjectAccess] = {
        key: value
        for key, value in
        ((k, getattr(user, k, EMPTY)) for k in definitions.keys())
        if value is not EMPTY
    }

    if len(resolved) != total:
        diff = definitions.keys() - resolved.keys()
        q = models.Q()
        whens = []

        for key in diff:
            content_type, pk = definitions[key]
            condition = models.Q(content_type=content_type, object_id=pk)
            q |= condition
            whens.append(models.When(condition, then=models.Value(key)))

        accesses = (
            ObjectAccess.objects.filter(q)
            .annotate(cache_key=models.Case(
                *whens, output_field=models.TextField(),
            ))
            .select_related('content_type')
        )

        for obj in accesses:
            setattr(user, obj.cache_key, obj)
            resolved[obj.cache_key] = obj

    return [resolved.get(key) for key in definitions]


def objects_for_user(
    user: 'User',
    objects: Sequence[models.Model],
) -> List[Optional[ObjectAccess]]:
    return objects_for_user_raw(user, [obj_to_definition(x) for x in objects])


def permissions_for_user_raw(
    user: 'User',
    objects: Sequence[ObjectDefinition],
) -> Set[int]:
    accesses = objects_for_user_raw(user, objects)

    return set(
        y
        for x in accesses
        if x is not None
        for y in x.gathered_permission_ids
    )


def permissions_for_user(
    user: 'User',
    objects: Sequence[models.Model],
) -> Set[int]:
    return permissions_for_user_raw(user, [obj_to_definition(x) for x in objects])
