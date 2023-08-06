from typing import TYPE_CHECKING, Callable, Optional, Sequence, Set, Tuple, Type, TypeVar
from functools import wraps, cached_property
from django.db import models
from django.contrib.contenttypes.models import ContentType

from pxd_combinable_groups.services import permissions_collector
from pxd_combinable_groups.utils import resolve_on_cached_object

from . import gatherer
from ..models import ObjectAccess
from ..exceptions import CheckError
from ..utils import make_random_code

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser as User


CHECKER_ANNOTATION_FIELD_TEMPLATE = '_permissions_{name}_exists'


def require_permissions(permission_ids: Sequence[int] = None):
    if permission_ids is None or len(permission_ids) == 0:
        raise CheckError('At least one permission required to compare against.')


def wrap_require_permissions(fn):
    @wraps(fn)
    def wrapped(*a, permission_ids: Optional[Sequence[int]] = None, **kw):
        require_permissions(permission_ids)

        return fn(*a, permission_ids, **kw)

    return wrapped


class CheckCMP:
    def cmp_Q(self):
        raise NotImplementedError()

    def cmp(self):
        raise NotImplementedError()


class RawCheckCMP(CheckCMP):
    def __init__(self, cmp_Q: Callable, cmp: Callable):
        self.cmp_Q = cmp_Q
        self.cmp = cmp


ALL_CMP = RawCheckCMP(
    wrap_require_permissions(
        lambda field, pids: models.Q(**{f'{field}__contains': pids})
    ),
    wrap_require_permissions(
        lambda ids, pids: len(set(ids) & set(pids)) == len(pids)
    )
)
ANY_CMP = RawCheckCMP(
    wrap_require_permissions(
        lambda field, pids: models.Q(**{f'{field}__overlap': pids})
    ),
    wrap_require_permissions(
        lambda ids, pids: len(set(ids) & set(pids)) > 0
    )
)


class Checkable:
    def get_permissions(self, obj: models.Model, user: 'User') -> Set[int]:
        raise NotImplementedError()

    def with_annotation(
        self,
        queryset: models.QuerySet,
        user: 'User',
        permission_ids: Optional[Sequence[int]] = None,
        cmp: Optional[CheckCMP] = None,
        annotation_field_name: Optional[str] = None,
    ) -> Tuple[str, models.QuerySet]:
        raise NotImplementedError()

    def for_object(
        self,
        obj: models.Model,
        user: 'User',
        permission_ids: Sequence[int],
        cmp: Optional[CheckCMP] = None,
    ) -> bool:
        raise NotImplementedError()

    def for_queryset(
        self,
        queryset: models.QuerySet,
        user: 'User',
        permission_ids: Optional[Sequence[int]] = None,
        cmp: Optional[CheckCMP] = None,
        annotation_field_name: Optional[str] = None,
    ) -> models.QuerySet:
        raise NotImplementedError()


class Checker(Checkable):
    path: str
    model: Type[models.Model]
    root_model: Type[models.Model]
    cmp: CheckCMP = ALL_CMP
    should_check_global: bool = True

    def __init__(
        self,
        model: Type[models.Model],
        path: str,
        root_model: Optional[Type[models.Model]] = None,
        cmp: Optional[CheckCMP] = None,
        should_check_global: Optional[bool] = None,
    ):
        self.path = path
        self.model = model
        # TODO: Remove this.
        # self.reverse_path, founded_model = self._resolve_reverse(path, model)
        self.root_model = root_model
        self.cmp = cmp if cmp is not None else self.cmp
        self.should_check_global = (
            should_check_global if should_check_global is not None
            else self.should_check_global
        )

        assert self.root_model is not None, (
            'Cant resolve root model provide it manually please.'
        )

    def __hash__(self):
        return hash((self.model, self.path, self.root_model))

    @cached_property
    def content_type(self):
        return ContentType.objects.get_for_model(self.model)

    @cached_property
    def root_content_type(self):
        return ContentType.objects.get_for_model(self.root_model)

    # TODO: Remove this.
    # def _resolve_reverse(self, path: str, model: Type[models.Model]):
    #     resolve_reverse(path.split('__'), model)
    #     return path, model

    def _make_annotation_field_name(self, name: str) -> str:
        return CHECKER_ANNOTATION_FIELD_TEMPLATE.format(name=name)

    def _prepare_access_query(
        self,
        user: 'User',
        permission_ids: Optional[Sequence[int]] = None,
        cmp: Optional[CheckCMP] = None,
    ) -> models.QuerySet:
        # TODO: Separate query somewhere.
        return ObjectAccess.objects.filter(
            (cmp or self.cmp).cmp_Q(
                'gathered_permission_ids',
                permission_ids=permission_ids,
            ),
            user_id=user.id, content_type=self.root_content_type,
        )

    def has_global_access(
        self,
        user: 'User',
        permission_ids: Optional[Sequence[int]] = None,
        cmp: Optional[CheckCMP] = None,
    ) -> bool:
        if not self.should_check_global:
            return False

        ids = set(permissions_collector.keys_to_ids(user.get_all_permissions()))

        return (cmp or self.cmp).cmp(ids, permission_ids=permission_ids)

    def get_permissions(self, obj: models.Model, user: 'User') -> Set[int]:
        root_content_type = self.root_content_type

        return resolve_on_cached_object(
            user, f'_permissions_{self.content_type.pk}_{obj.pk}',
            lambda *a: gatherer.permissions_for_user_raw(
                # FIXME: An ugly query here. try to change it somehow.
                user,
                [
                    (root_content_type, pk)
                    for pk in (
                        self.model.objects
                        .filter(pk=obj.pk)
                        .values_list(self.path, flat=True)
                    )
                ]
            )
        )

    def with_annotation(
        self,
        queryset: models.QuerySet,
        user: 'User',
        permission_ids: Optional[Sequence[int]] = None,
        cmp: Optional[CheckCMP] = None,
        annotation_field_name: Optional[str] = None,
    ) -> Tuple[str, models.QuerySet]:
        annotation_field_name = (
            annotation_field_name
            or
            self._make_annotation_field_name(make_random_code(6))
        )

        if self.has_global_access(user, permission_ids=permission_ids, cmp=cmp):
            return annotation_field_name, queryset.annotate(**{
                annotation_field_name: models.Value(True)
            })

        subquery = self._prepare_access_query(
            user, permission_ids=permission_ids, cmp=cmp,
        ).filter(
            # This comparison produces joins for every '__' in a root query.
            # That is not the expected behaviour, so for some cases `.distinct`
            # should be called...
            object_id=models.OuterRef(self.path)
        )

        return annotation_field_name, queryset.annotate(**{
            annotation_field_name: models.Exists(subquery)
        })

    def for_object(
        self,
        obj: models.Model,
        user: 'User',
        permission_ids: Sequence[int],
        cmp: Optional[CheckCMP] = None,
    ) -> bool:
        if self.has_global_access(user, permission_ids=permission_ids, cmp=cmp):
            return True

        return (cmp or self.cmp).cmp(
            self.get_permissions(obj, user), permission_ids=permission_ids,
        )

    def for_queryset(
        self,
        queryset: models.QuerySet,
        user: 'User',
        permission_ids: Optional[Sequence[int]] = None,
        cmp: Optional[CheckCMP] = None,
        annotation_field_name: Optional[str] = None,
    ) -> models.QuerySet:
        name, q = self.with_annotation(
            queryset, user,
            permission_ids=permission_ids, cmp=cmp,
            annotation_field_name=annotation_field_name,
        )

        return q.filter(**{name: True})
