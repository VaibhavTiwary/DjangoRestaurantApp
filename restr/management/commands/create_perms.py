import itertools
import operator

from django.db.models import Q
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group

from restr.lib.owner_perms import allow_access


class Command(BaseCommand):
    help = "setup owner group and add permissions"

    # TODO: read https://docs.djangoproject.com/en/5.0/topics/migrations/#data-migrations
    def __add_perms_to_owner(self):
        owner, _ = Group.objects.get_or_create(name="owner")
        owner.save()

        or_queries = [Q(codename__contains=x) for x in allow_access]
        iter = itertools.accumulate(or_queries, func=operator.xor)

        cond = None

        # take last of iter in cond
        for cond in iter:
            pass

        perms = Permission.objects.filter(cond)
        # perms = Permission.objects.filter(Q(codename_in='') | Q(codename_in=''))

        for perm in perms:
            owner.permissions.add(perm)

    def handle(self, *args, **options):
        self.__add_perms_to_owner()
