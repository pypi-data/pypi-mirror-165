from aheadworks_bitbucket_manager.api.bitbucket_api_manager import BitbucketApiManager
from aheadworks_bitbucket_manager.model.data.bitbucket import BitbucketConfig
from aheadworks_core.api.composer_manager import ComposerManager
from aheadworks_core.api.jira_api_manager import JiraApiManager
from aheadworks_core.api.discord_api_manager import DiscordApiManager
from aheadworks_core.api.magento_manager import MagentoManager
from aheadworks_core.api.file_manager import FileManager
from aheadworks_core.model.parser.json import Json as JsonParser
from aheadworks_core.model.http.api_request import ApiRequest
from aheadworks_core.model.data.data_object import DataObject
from datetime import datetime
from urllib.parse import urlparse
import os
import json
import shutil
import boto3


class ReleaseManager:
    """api manager for release"""

    RELEASE_PACK_TASK_LABEL = 'RELEASE-PACK'
    PD_TASK_LABEL = 'PD'
    TEST_TASK_LABEL = 'TEST'

    def __init__(self, jira_api_config):
        self.jira_api_config = jira_api_config
        self.jira_api_manager = JiraApiManager(config=self.jira_api_config)
        self.discord_api_manager = DiscordApiManager()
        self.magento_manager = MagentoManager()
        self.file_manager = FileManager()
        self.json_parser = JsonParser()
        self.aws_s3 = boto3.resource('s3')

    def jira_release(self, jira_project_key, composer_file, discord_bot_url, path_to_files, assign_to):
        module_version = self.json_parser.get_variable_from_file('version', composer_file)
        # module_version = self.magento_manager.get_module_version(path_to_module)

        print(f"jira project key: {jira_project_key}")
        print(f"module version: ' {module_version}")
        print(f"discord bot url: {discord_bot_url}")
        print(f"path to files: {path_to_files}")
        print(f"assign to, account id: {assign_to}")

        if not jira_project_key:
            print('jira_project_key is empty, skip jira release.')
            return False

        jira_instance = self.jira_api_manager.get_jira_instance()

        files_to_upload = []
        file_names = os.listdir(path_to_files)
        for file_name in file_names:
            files_to_upload.append(('file', (file_name, open(f"{path_to_files}/{file_name}", 'rb'))))

        jql = 'labels%3D{}-{}'.format(jira_project_key, module_version)
        links = self.get_release_tasks(jql)

        release_task_key = links[self.RELEASE_PACK_TASK_LABEL]['key']
        pd_task_key = links[self.PD_TASK_LABEL]['key']
        test_task_key = links[self.TEST_TASK_LABEL]['key']

        # add attachments
        self.add_attachments_to_task(release_task_key, files_to_upload)

        # module_dependencies = self.magento_manager.get_module_dependencies(path_to_module)
        module_dependencies = self.magento_manager.get_module_dependencies_from_composer(composer_file)
        composer_package_name = ','.join(list(map(lambda x: x['full_module_name'], module_dependencies.values())))

        # assign release pack to user
        release_issue = jira_instance.issue(release_task_key)
        release_issue.update(assignee={'accountId': assign_to})
        jira_instance.add_comment(release_issue, f'Composer Package Name:\n{composer_package_name}')

        # uncomment if needed check transitions for issue
        # transitions = jira_instance.transitions(release_issue)
        # set done to pd and test issue. transition=31 - Task Done
        pd_issue = jira_instance.issue(pd_task_key)
        jira_instance.transition_issue(pd_issue, transition=31)

        test_issue = jira_instance.issue(test_task_key)
        jira_instance.transition_issue(test_issue, transition=31)

        # release current version
        version = jira_instance.get_project_version_by_name(jira_project_key, module_version)
        release_date = datetime.today().strftime('%Y-%m-%d')
        version.update(released=True, releaseDate=release_date)

        project = jira_instance.project(jira_project_key)

        msg = '{} {}\n'.format(project.name, module_version)
        msg += '\n'.join(list(map(lambda x: x['url'], links.values())))
        msg += '\n' + self.jira_api_manager.get_release_report_all_issues_url(jira_project_key, version.id)

        self.discord_api_manager.send_msg(discord_bot_url, msg)

        return True

    def get_release_tasks(self, jql):
        print(f" https://aheadworks.atlassian.net/issues/?jql={jql}")
        links = dict()
        search_labels = [self.RELEASE_PACK_TASK_LABEL, self.PD_TASK_LABEL, self.TEST_TASK_LABEL]
        tasks = self.jira_api_manager.search_tasks_jql(jql)
        if 'issues' in tasks and len(tasks['issues']):
            for task in tasks['issues']:
                if 'labels' in task['fields']:
                    task_labels = task['fields']['labels']
                    label_intersection = list(set(task_labels) & set(search_labels))
                    if len(label_intersection) == 1:
                        task_key = task['key']
                        task_url = self.jira_api_manager.get_issue_url(task_key)
                        links[label_intersection[0]] = dict({'url': task_url, 'key': task_key})
                    else:
                        raise Exception('Incorrect release labels count.')
                else:
                    raise Exception('Tasks data returned by JIRA has no data on labels')
        else:
            print(tasks)
            raise Exception('Release Tasks not found.')

        return links

    def add_attachments_to_task(self, task_key, files):
        tasks = self.jira_api_manager.add_attachments_to_task(task_key, files)

    def build_swagger_web_api_doc(
            self,
            path_to_module,
            magento_url,
            magento_path_on_server='/var/www/html',
            ssh_port=22,
            ssh_user='root',
            ssh_pass='root'
    ):
        obj = DataObject()
        obj.url = magento_url
        obj.auth_type = 'none'
        magento_request = ApiRequest(obj)

        aws_bucket_name = 'aheadworks_cdn'
        aws_swagger_web_api_doc_path = 'swagger_web_api_doc/'
        magento_app_code_path_on_server = f"{magento_path_on_server}/app/code"
        tmp_dir_m2_modules = '/var/tmp/m2_modules'

        parent_module_name = self.magento_manager.get_module_name(path_to_module)
        if not os.path.isfile(f"{path_to_module}/etc/webapi.xml"):
            return f'Skip Web API doc generation: file etc/webapi.xml has been not found for module {parent_module_name}'

        parsed_url = urlparse(magento_url)

        try:
            list_of_module_paths = self.magento_manager.download_modules_from_git(path_to_module, tmp_dir_m2_modules)
            self.magento_manager.upload_modules_to_server_by_ssh(
                list_of_module_paths['dir_app_code'],
                magento_app_code_path_on_server,
                parsed_url.hostname,
                ssh_port,
                ssh_user,
                ssh_pass
            )
            module_names = ','.join(list_of_module_paths['module_names'])
            magento_request_url = '/generate_web_api_json.php?module_names={}'.format(module_names)
            # workaround, for generate magento cache
            magento_request.get(location=magento_request_url)
            # here we generate json with cache from previous step
            swagger_json = magento_request.get(location=magento_request_url)

            try:
                json.loads(swagger_json)
            except Exception as error:
                print(f"Invalid respone from Swagger:\n{swagger_json}\n\n")
                raise Exception(error)

            s3_result = self.aws_s3.Bucket(aws_bucket_name).put_object(
                Key=f"{aws_swagger_web_api_doc_path}{parent_module_name.lower()}_latest.json",
                Body=swagger_json,
                ACL='public-read'
            )
        except Exception as error:
            raise Exception(error)
        finally:
            os.system(f"rm -rf {tmp_dir_m2_modules}")

        result = f'Web Api Doc Path: https://media.aheadworks.com/{s3_result.key}\n'
        result += f'Magento Request Url: {magento_request_url}\n'
        return result

    def build_ecommerce_pack(self, bitbucket_workspace, bitbucket_repo_slug):
        ComposerManager.init_extra_repos()

        build_dir = os.getcwd()
        artifacts_dir = "/build_archives"
        path = f"{build_dir}/app/code/Aheadworks"
        self.file_manager.create_empty_dir("app/code/Aheadworks")
        self.file_manager.create_empty_dir(artifacts_dir)

        with open('./composer.json') as f:
            composer = json.load(f)
        core_module_name = composer['name']
        module_dependencies = self.magento_manager.get_module_dependencies('./')
        ComposerManager.require_magento_module(core_module_name)

        # @todo use self.magento_manager.download_modules_from_git(path_to_module, tmp_dir_m2_modules)
        magento_module_info = dict()
        artifacts = list()
        # Preinstall suggested modules with composer into /var/www/html/vendor/aheadworks
        for full_module_name, module_item in module_dependencies.items():
            if self.magento_manager.is_suggested_module(build_dir, full_module_name):
                ComposerManager.require_magento_module(full_module_name)

        # full_module_name          vendor/module-name
        # module_name               module-name
        # magento_package_name      ModuleName
        for full_module_name, module_item in module_dependencies.items():
            module_name = module_item['module_name']
            composer_install_path = f"/var/www/html/vendor/aheadworks/{module_name}"
            path_to_composer = f"{composer_install_path}/composer.json"
            path_to_registration = f"{composer_install_path}/registration.php"
            if not os.path.isfile(path_to_composer) or not os.path.isfile(path_to_registration):
                os.system(f"ls {composer_install_path}")
                raise Exception(f"Can not build module {full_module_name}: composer.json or/and registration.php is missing")

            magento_package_name = self._get_magento_package_name(composer_install_path)
            magento_module_info[full_module_name] = magento_package_name
            module_path = f"{path}/{magento_package_name}"

            print(f"Building {full_module_name} as {module_name} in {module_path}...")
            shutil.copytree(composer_install_path, module_path)

            print("\t\u21E8 Cleanup filesystem...")
            self.file_manager.remove_files_and_dirs_ignore_case(
                module_path,
                ['bitbucket-pipelines.yml', 'readme.md', '.gitignore'],
                ['.git']
            )

            print("\t\u21E8 Writing license headers...")
            self.file_manager.add_license_to_php_files(
                module_path,
                magento_package_name,
                self.json_parser.get_variable_from_file('version', f"{module_path}/composer.json")
            )
            os.system(f"echo See https://aheadworks.com/end-user-license-agreement/ >> {module_path}/license.txt")
            artifacts.append(
                self._pack_module(module_path, f"{artifacts_dir}/{module_name}.zip")
            )

        # Now build store packages
        for filename in self._get_store_package_names(magento_module_info[core_module_name], composer['version']):
            artifacts.append(
                self._pack_module(build_dir, f"{artifacts_dir}/{filename}", "app")
            )

        self._upload_artifacts(bitbucket_workspace, bitbucket_repo_slug, artifacts)

    def build_mm_pack(self, bitbucket_workspace, bitbucket_repo_slug):
        # basically marketplace pack is a ecommerce pack where all modules have -subscription postfix in their names
        # so we assume that the ecommerce pack has been built so far
        prebuilt_packages_dir = "/build_archives"
        working_dir = "/tmp/unpack"
        package_dir = "/tmp/packages"
        self.file_manager.create_empty_dir(working_dir)
        self.file_manager.create_empty_dir(package_dir)
        os.system(f"ls -l {prebuilt_packages_dir}")
        # Extract all packages first
        for filename in os.listdir(prebuilt_packages_dir):
            package_fullpath = os.path.join(prebuilt_packages_dir, filename)
            # TODO: process *.zip only
            if os.path.isfile(package_fullpath):
                sources_dir = os.path.join(working_dir, filename)
                print(package_fullpath)
                os.system(f"unzip -q {package_fullpath} -d {sources_dir}")

        # Now gather module names
        module_names = []
        composer_files = self.file_manager.find_all('composer.json', working_dir)
        print(composer_files) # debug
        for composer_file in composer_files:
            package_name = self.json_parser.get_variable_from_file('name', composer_file)
            if not package_name in module_names:
                module_names.append(package_name)

        print(module_names) # debug
        # Replace all found modules names from "vendor/module_name" to "vendor/module_name-subscription"
        # across all composer.json (this includes requires/suggests sections and possibly even more)
        for composer_file in composer_files:
            self._replace_dependencies(composer_file, module_names, "subscription")

        # Create '-subscription' packages
        for originalname in os.listdir(working_dir):
            sources_fullpath = os.path.join(working_dir, originalname)

            split_name, split_extension = os.path.splitext(originalname)
            target_filename = f"{split_name}-subscription{split_extension}"
            target_fullpath = os.path.join(package_dir, target_filename)
            print(target_fullpath) # debug
            self._pack_module(sources_fullpath, target_fullpath)

        # Copy newly built -subscription packages to /build_archives
        os.system(f"cp {package_dir}/* {prebuilt_packages_dir}")

    # Sample metapackage product: https://bitbucket.org/awm2ext/b2b-suite/
    def build_metapackage_pack(self, bitbucket_workspace, bitbucket_repo_slug, artifacts_dir):
        upload_env = f"REPO_URL={os.getenv('AW_COMPOSER_API_URL')} REPO_LOGIN={os.getenv('AW_COMPOSER_API_LOGIN')} REPO_TOKEN={os.getenv('AW_COMPOSER_API_PASSWORD')}"

        # prepare FS
        build_dir = os.getcwd()
        if not artifacts_dir:
            artifacts_dir = "/build_archives"
        path = f"{build_dir}/app/code/Aheadworks"
        self.file_manager.create_empty_dir(artifacts_dir)
        self.file_manager.create_empty_dir(path)

        # Get dependent packages list
        with open("./composer.json") as f:
            composer = json.load(f)

        # Install dependent packages via Composer first
        for full_module_name in composer["require"]:
            ComposerManager.require_magento_module(full_module_name)

        artifacts = []
        for full_module_name in composer["require"]:
            module = full_module_name.split('/')[1]
            metapackage_module_name = f"{module}-{bitbucket_repo_slug}"

            composer_install_path = f"/var/www/html/vendor/aheadworks/{module}"
            magento_package_name = self._get_magento_package_name(composer_install_path)
            module_path = f"{path}/{magento_package_name}"

            print(f"Building {full_module_name} as {module} in {module_path}...")
            shutil.copytree(composer_install_path, module_path)

            print("\t\u21E8 Cleanup filesystem...")
            self.file_manager.remove_files_and_dirs_ignore_case(
                module_path,
                ['bitbucket-pipelines.yml', 'readme.md', '.gitignore'],
                ['.git']
            )

            with open(f"{module_path}/composer.json") as f:
                module_composer = json.load(f)

            print("\t\u21E8 Writing license headers...")
            self.file_manager.add_license_to_php_files(
                module_path,
                magento_package_name,
                module_composer['version']
            )
            os.system(f"echo See https://aheadworks.com/end-user-license-agreement/ >> {module_path}/license.txt")

            old_name = module_composer['name']
            new_name = f"{module_composer['name']}-{bitbucket_repo_slug}"

            print(f"\t\u21E8 Renaming {old_name} to {new_name}...")
            module_composer['name'] = new_name
            with open(f"{module_path}/composer.json", 'w') as f:
                json.dump(module_composer, f, indent=4)

            self._replace_dependencies(f"{module_path}/composer.json", composer["require"], bitbucket_repo_slug)

            zip_package_path = f"{artifacts_dir}/{metapackage_module_name}.zip"
            artifacts.append(
                self._pack_module(module_path, zip_package_path)
            )

            upload_as = f"{metapackage_module_name}-{module_composer['version']}.zip"
            os.system(
                f"echo '{upload_env} python3 -m aheadworks_composer_manager send-package --filename={upload_as} {zip_package_path}' >> {artifacts_dir}/upload")
            # ??? Why we upload to Composer server in this noobish manner instead of using API ???
            composer_server_base_path = f"{os.getenv('AW_COMPOSER_PACKAGES_ROOT')}/aheadworks"
            os.system(
                f"ssh -T {os.getenv('AW_COMPOSER_SSH_URL')} 'mkdir -p {composer_server_base_path}/{metapackage_module_name}'")
            os.system(
                f"scp {zip_package_path} {os.getenv('AW_COMPOSER_SSH_URL')}:{composer_server_base_path}/{metapackage_module_name}/{upload_as}")

        core_version = composer['version']
        with open('composer.json') as f:
            lines = f.readlines()
            for line in f.readlines():
                lines.append(line)
            result_lines = list()
            for line in lines:
                if line.find('aheadworks/module') != -1:
                    line = line.split(':')[0][:-1] + f'-{bitbucket_repo_slug}"' + f":{line.split(':')[1]}"
                result_lines.append(line)
        with open('/tmp/composer.json', 'w') as f:
            for line in result_lines:
                f.write(line)

        # build marketplace package
        artifacts.append(
            self._pack_module("/tmp", f"{artifacts_dir}/{bitbucket_repo_slug}.zip", "composer.json")
        )

        # store package
        for filename in self._get_store_package_names(bitbucket_repo_slug, core_version):
            artifacts.append(
                self._pack_module(build_dir, f"{artifacts_dir}/{filename}", "app")
            )

        self._upload_artifacts(bitbucket_workspace, bitbucket_repo_slug, artifacts)

    def _replace_dependencies(self, path_to_composer, module_names, slug):
        fin = open(path_to_composer, "rt")
        data = fin.read()
        fin.close()

        for module_name in module_names:
            # we intentionally quote vendor/package_name string to be "vendor/package_name".
            # otherwise vendor/package_name_subname could be renamed
            # into vendor/package_name-subscription_subname
            # instead of vendor/package_name_subname-subscription
            data = data.replace(f'"{module_name}"', f'"{module_name}-{slug}"')

        fin = open(path_to_composer, "wt")
        fin.write(data)
        fin.close()

    def _pack_module(self, source_module_path, target_package_path, base_dir="."):
        print(f"\t\u21E8 Packing {source_module_path} into {target_package_path}\n")
        base_name, extension = os.path.splitext(target_package_path)
        shutil.make_archive(base_name, extension.lstrip('.'), source_module_path, base_dir)
        return target_package_path

    def _get_store_package_names(self, magento_package_name, version):
        return [
            f"aw_m2_{magento_package_name}-{version}.community_edition.zip",
            f"aw_m2_{magento_package_name}-{version}.enterprise_edition.zip"
        ]

    def _get_magento_package_name(self, module_path):
        with open(f"{module_path}/registration.php") as reg:
            l = reg.readlines()
            for line in l:
                if line.find("Aheadworks_") != -1:
                    return line.strip().strip('\"\',').split('_')[1]
        return ""

    def _upload_artifacts(self, bitbucket_workspace, bitbucket_repo_slug, filepath):
        print(f"\nUploading artifacts\n{filepath}...\n")
        bitbucket_manager = BitbucketApiManager(
            BitbucketConfig(
                bitbucket_workspace=bitbucket_workspace,
                bitbucket_repo_slug=bitbucket_repo_slug
            )
        )
        print(bitbucket_manager.upload_artifacts(filepath))
