import uuid

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db.models import Manager


class RevisionManagerMixin(Manager):
    def revisions(self, instance):
        pk = instance.pk
        if isinstance(pk, uuid.UUID):
            pk = str(pk)

        return self.revision_model.objects.filter(
            content_type__id=self.content_type.pk,
            data__pk=pk
        )

    @property
    def revision_model(self):
        """This method is used for avoid circular imports on Revision Model."""
        return apps.get_model(app_label='core', model_name='Revision')

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.model)


class AbstractBaseManager(RevisionManagerMixin):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseManager(AbstractBaseManager):
    def from_user(self, user):
        return self.get_queryset().filter(user__id=user.pk)