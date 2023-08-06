#!/usr/bin/env python3
from aheadworks_core.api.composer_manager import ComposerManager
from aheadworks_core.model.cd import Cd as cd
import subprocess
import click
from os.path import join as _
import os
import re
import json
import pathlib
import time

def remove_listeners(path):
    with open(path) as phpunit_config:
        data = phpunit_config.read()
        reg = re.compile("<listeners.*</listeners>", re.S)
        data = re.sub(reg, '', data)
    with open(path, 'w') as phpunit_config:
        phpunit_config.write(data)

def di_compile():
    proc = subprocess.Popen(['php', '/var/www/html/bin/magento', 'module:enable', '--all'])
    proc.communicate()
    ec3 = proc.returncode
    proc = subprocess.Popen(['php', '/var/www/html/bin/magento', 'setup:di:compile'])
    ec4 = proc.returncode

    if ec3 or ec4:
        print("Failed to di:compile")

def install(path):
    """
    Install extension(s) to path from path or zip
    """
    repo_type = 'path'

    click.echo("Installing from %s" % path)

    with open(path / 'composer.json') as f:
        composer = json.load(f)
        repo_name = re.sub(r'[^a-z0-9_]', '_', composer['name'])

    with cd(BASIC_PATH):
        f = open('auth.json.sample')
        composer_auth = json.load(f)
        f.close()

        proc = subprocess.Popen(['php', '-d', 'memory_limit=4G', '/usr/local/bin/composer', 'config', '-g', 'repositories.aheadworks', 'composer', 'https://composer.do.staging-box.net'])
        proc.communicate()

        # composer_auth["http-basic"]["repo.magento.com"]["username"] = "ca6f970bb96d25614c90874edc90f42b"
        # composer_auth["http-basic"]["repo.magento.com"]["password"] = "74ce69e7288fc3232fb3b038410e9ae6"
        composer_auth["http-basic"]["repo.magento.com"]["username"] = "bf08744e4b4b3aee1d54fcd7cd56194a"
        composer_auth["http-basic"]["repo.magento.com"]["password"] = "f5b232eab5158a4597ecb00f8cacdf4a"
        os.system('touch auth.json')
        with open('auth.json', 'w') as file:
            json.dump(composer_auth, file, indent=2)
        os.system('composer config repositories.magento composer https://repo.magento.com/')
        proc = subprocess.Popen(['composer', 'config', 'repositories.' + repo_name, repo_type, path])
        proc.communicate()
        ec1 = proc.returncode

        proc = subprocess.Popen(['php', '-d', 'memory_limit=4G', '/usr/local/bin/composer', 'require', '--prefer-dist', '{e[name]}:{e[version]}'.format(e=composer)])
        proc.communicate()
        ec2 = proc.returncode

        if ec1 or ec2:
            raise click.ClickException("Failed to install extension")
    result_path = BASIC_PATH / 'vendor' / composer['name']
    return result_path


@click.group()
def cli():
    click.echo("Removing phpunit listeners")
    remove_listeners(BASIC_PATH / 'dev' / 'tests' / 'static' / 'phpunit.xml.dist')
    remove_listeners(BASIC_PATH / 'dev' / 'tests' / 'unit' / 'phpunit.xml.dist')


@cli.command()
@click.option('--severity', default=10, help='Severity level.')
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["full", "xml", "checkstyle", "csv",
                                                                             "json", "junit", "emacs", "source",
                                                                             "summary", "diff", "svnblame", "gitblame",
                                                                             "hgblame", "notifysend"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def eqp(severity, report, path, report_file):
    """Run EQP tests for path"""

    proc = subprocess.Popen([_('/magento-coding-standard', 'vendor/bin/phpcs'), path, '--standard=Magento2',
                             '--severity='+str(severity), '--extensions=php,phtml', '--report='+report],
                            stdout=subprocess.PIPE
                            )
    stdout, stderr = proc.communicate()

    if report_file:
        with open(report_file, 'wb') as fp:
            fp.write(stdout)
    else:
        click.echo(stdout)
    exit(proc.returncode)


@cli.command()
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["junit"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def unit(report, path, report_file):
    """Run unit tests for extension at path"""

    path = pathlib.Path(path)
    path = install(path)
    di_compile()

    options = [
        _(BASIC_PATH, 'vendor/bin/phpunit'),
        '--configuration',  _(BASIC_PATH, 'dev/tests/unit/phpunit.xml.dist')
    ]

    if report_file:
        options += ['--log-%s' % report, report_file]

    proc = subprocess.Popen(options + [_(path, 'Test/Unit')])
    proc.communicate()

    if not report_file:
        exit(proc.returncode)

    exit(proc.returncode)


@cli.command()
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["junit"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_path', type=click.Path(), required=False)
def static(report, path, report_path):
    """
    Run static tests against path
    :param report:
    :param path:
    :param report_file:
    :return:
    """

    path = pathlib.Path(path)

    phpcs_report_file = path / 'test-results' / 'test-phpcs.xml'

    #path = install(path)

    path_changed_files = BASIC_PATH / 'dev' / 'tests' / 'static' / 'testsuite' / 'Magento' / 'Test' / 'Php' / '_files' / 'whitelist' / 'common.txt'
    path_blacklist = BASIC_PATH / 'dev' / 'tests' / 'static' / 'testsuite' / 'Magento' / 'Test' / 'Php' / '_files' / 'phpstan' / 'blacklist' / 'common.txt'

    options = [os.path.join(BASIC_PATH, 'vendor/bin/phpunit'), '--configuration',
               BASIC_PATH / 'dev/tests/static/phpunit.xml.dist']

    output_base = report_path or os.environ.get('RESULTS_DIR', '/results')

    with open(os.path.join(BASIC_PATH, 'dev/tests/static/phpunit.xml.dist')) as phpunit_config:
        suites = {}
        reg = re.compile('<testsuite[^>]+name="([^"]+)"')
        for line in phpunit_config:
            try:
                suite = re.search(reg, line).groups()[0]
                suites[suite.lower().replace(' ', '_')] = suite
            except (IndexError, AttributeError):
                pass

    # Collect php iles
    f = open(path_blacklist, 'r')
    lines = f.readlines()
    f.close()

    newLines = []
    for line in lines:
        linePath = line
        linePath = linePath.rstrip()
        if line[0] != '#' and os.path.isfile(BASIC_PATH / linePath):
            newLines.append(line)

    lines = newLines

    with open(path_blacklist, 'w') as fp:
        fp.writelines(lines)
    f = open(path_changed_files, 'r')
    lines = f.readlines()
    f.close()
    lines = lines[0:2]
    with open(path_changed_files, 'w') as fp:
        fp.writelines(lines)
        for root, dirs, files in os.walk(path):
            fp.writelines([os.path.relpath(os.path.abspath(os.path.join(root, f)), BASIC_PATH) + '\n' for f in files if
                           os.path.splitext(f)[1] in (
                               '.php',
                               '.phtml'
                           )])

    exit_code = 0
    print(suites.items())
    for fname, name in suites.items():

        outfile = os.path.join(output_base, fname + '.xml')

        if re.search(re.compile('integrity'), fname):
            continue
        if re.search(re.compile('less'), fname):
            continue
        if re.search(re.compile('html'), fname):
            continue

        args = options + ['--testsuite=%s' % name]
        args += ['--log-%s' % report, outfile]
        proc = subprocess.Popen(args)
        proc.communicate()

        # Remove copy-paste results from report
        with open(os.path.join(output_base, fname + '.xml')) as f:
            data = f.read()
            data = re.sub('<testcase[^>]+name="testCopyPaste".+</testcase>', '', data,
                          flags=re.MULTILINE and re.DOTALL)

        with open(outfile, 'w') as f:
            f.write(data)

        exit_code = proc.returncode or exit_code

    # test code style
    severity = '9'
    if 'SEVERITY' in os.environ:
        if not os.getenv('SEVERITY') == '':
            severity = str(os.getenv('SEVERITY'))
    proc = subprocess.Popen(
        ['/var/www/html/vendor/bin/phpcs', path, '--standard=Magento2', '--extensions=php,phtml', '--severity={}'.format(severity),
         '--report=' + report],
        stdout=subprocess.PIPE
        )
    stdout, stderr = proc.communicate()

    if phpcs_report_file:
        with open(phpcs_report_file, 'wb') as fp:
            fp.write(stdout)
    else:
        click.echo(stdout)
    if proc.returncode != 0:
        exit_code = proc.returncode

    exit(exit_code)


@cli.command()
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["junit"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def install_magento(report, path, report_file):
    """Run install magento with extension at path"""

    global output
    path = pathlib.Path(path)
    path = install(path)

    try:
        output = subprocess.run(
            ['sh', "/tmp/create-install-dump.sh", '--withoutdump'],
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        os.system("mkdir logs1")
        os.system("mysqldump -uroot -proot magento >> logs1/dump.sql")
        os.system(f"cp /var/www/html/var/log/* logs1")
        os.system("cp /var/www/html/app/etc/* logs1")
        exit(e.returncode)

    exit(output.returncode)

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def validate_m2_package(path):
    """
    Test marketplace package
    :param path:
    :return:
    """
    #proc = subprocess.Popen(['php', '-f', '/usr/local/bin/validate_m2_package.php', path])
    #proc.communicate()
    #exit(proc.returncode)

if __name__ == '__main__':
    BASIC_PATH = pathlib.Path(os.environ.get('MAGENTO_ROOT', '/var/www/html'))
    ComposerManager.init_extra_repos()
    cli()
