import os
import json

class ComposerManager:
    @staticmethod
    def init_extra_repos():
        # COMPOSER_REPOSITORIES -- variable in module repo settings
        extraRepositories = os.environ.get('COMPOSER_REPOSITORIES', "")
        if not extraRepositories:
            print('COMPOSER_REPOSITORIES variable is empty or unset. This is ok if you need no external composer repositories.')
        else:
            try:
                composer = json.loads(extraRepositories)
                for item in composer:
                    os.system(f"composer config -g repositories.{item['name']} {item['type']} {item['url']}")
            except:
                print(f'COMPOSER_REPOSITORIES variable contains invalid JSON:{extraRepositories}')

    @staticmethod
    def require_magento_module(module_name):
        old_cwd = os.getcwd()
        os.system(f"cd /var/www/html && composer require {module_name}")
        os.system(f"cd {old_cwd}")
