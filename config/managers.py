from django.db.models import Manager, QuerySet
from django.utils import timezone


class BaseQuerySet(QuerySet):
    def delete(self):
        now = timezone.now()
        return self.update(deleted_at=now)

    def hard_delete(self):
        return super().delete()

    def restore(self):
        return self.update(deleted_at=None)


class SoftDeleteManager(Manager.from_queryset(BaseQuerySet)):

    # Base queryset
    def _get_base_queryset(self):
        return super().get_queryset()

    # Non deleted objects
    def get_queryset(self):
        return self._get_base_queryset().filter(deleted_at__isnull=True)

    # With deleted
    def with_deleted(self):
        return self._get_base_queryset()
