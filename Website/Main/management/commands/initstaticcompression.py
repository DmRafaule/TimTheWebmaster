# your_app/management/commands/your_command_name.py
import subprocess

from django.core.management.base import BaseCommand

from Main.utils import get_apps_root_dirs

class Command(BaseCommand):
    help = 'Run \'python manage.py initstaticcompression\' command to init nodejs modules and packages'

    def handle(self, *args, **options):
        apps_root_dirs = get_apps_root_dirs()
        
        # Запускаем NODE JS для компиляции статики (JS и CSS)
        for app_root_dir in apps_root_dirs:
            check_if_node_js_configured = subprocess.run("npm run", cwd=app_root_dir, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            if check_if_node_js_configured.returncode == 0:
                command = subprocess.run("npm install", cwd=app_root_dir, shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
                if command.stderr is None:
                    self.stdout.write(f"{self.style.HTTP_INFO(app_root_dir)}:\t{self.style.SUCCESS('Successfully init nodejs app.')}")
                else:
                    self.stdout.write(f"{self.style.HTTP_INFO(app_root_dir)}:\t{self.style.ERROR('Failed to init nodejs app.')}")
            else:
                self.stdout.write(f"{self.style.HTTP_INFO(app_root_dir)}:\t{self.style.WARNING(f"Didn't find any scripts to run.")}")

            