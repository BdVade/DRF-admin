from django.core.management import call_command

from utils.boot_django import boot_django

# call the django setup routine
boot_django()

call_command("makemigrations", "restadmin")

