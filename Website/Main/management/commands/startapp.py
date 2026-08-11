from django.core.management.commands.startapp import Command as BaseCommand
from django.core.management.base import CommandParser


class Command(BaseCommand):
    help = 'Улучшенная версия создания приложений, которая позволяет создавать приложения и сразу их подключать'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-M', action='store_true', help="To add the default middleware")
        parser.add_argument('-S', action='store_true', help="To add the static folder")
        parser.add_argument('-T', action='store_true', help='To add the templates folder')
        parser.add_argument('-U', action='store_true', help='To add the urls path')
        
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        super().handle(*args, **options)