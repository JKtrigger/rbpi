# -*- coding: utf-8 -*-

from django.core.management import CommandError, BaseCommand

from core.models import BaseRBPIUser


class Command(BaseCommand):
    help = u"Add super user"

    def handle(self, *args, **options):

        username = raw_input('Type username: ')
        while not username:
            username = raw_input('Type username: ')

        email = raw_input('Type email: ')
        while not email:
            # TODO Валидатор
            email = raw_input('Type email: ')

        password1 = raw_input('type password : ')
        password2 = raw_input('type password again: ')

        while not (password1 and password2 and password1 == password2):
            password1 = raw_input('type password : ')
            password2 = raw_input('type password again: ')

        try:
            new_user = BaseRBPIUser(
                is_superuser=True,
                is_staff=True,
                is_admin=True,
                username=username,
                email=email,
                password=password1
            )
            new_user.save()
            # todo заменить Exception
        except Exception as err:
            self.stdout.write(err)
        else:
            self.stdout.write('Successfully')
