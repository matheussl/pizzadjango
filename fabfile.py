from fab_deploy import *
from fabric.api import run

from fab_deploy.utils import run_as_sudo
from fab_deploy.utils import upload_config_template
import fab_deploy.deploy

import httplib2

DEFAULT_SERVER_ADMIN = 'contato@pizzadjango.com.br'

# Settings.
STANDARD_SETTINGS = {
    'VCS': 'git',
    'SERVER_ADMIN': DEFAULT_SERVER_ADMIN,
    'USER': 'vagrant',
    'SUDO_USER': 'vagrant',
    'INSTANCE_NAME': 'pizzadjango',
    'DB_NAME': 'pizzadjango',
    'DB_USER': 'root',
    'DB_PASSWORD': 'vagrant',
    'DB_ROOT_PASSWORD': 'vagrant',
    'SRC_DIR': '/home/vagrant/src/pizzadjango',
    'PROJECT_PATH': '',
    'PROJECT_DIR': '/home/vagrant/src/pizzadjango',
    'ENV_DIR': '/home/vagrant/envs/pizzadjango',
    'CONFIG_TEMPLATES_PATHS': ['pizzadjango/config_templates'], # relative
    'REMOTE_CONFIG_TEMPLATE': 'pizzadjango/settings/settings_local.server.py', # relative
    'LOCAL_CONFIG': 'pizzadjango/settings/settings_local.py', # relative
    'PIP_REQUIREMENTS_PATH': 'pizzadjango/reqs/', # relative (starts in repository)
    'PIP_REQUIREMENTS': 'deploy.txt',
    'OS': 'lucid',
    'GIT_BRANCH': 'master',
}




@define_host('vagrant@pizzadjango.com.br')
def local():
    """local server."""
    return STANDARD_SETTINGS


# Commands & utilities.
@run_as_sudo
def aptitude_update():
    run('DEBIAN_FRONTEND=noninteractive sudo aptitude update')


def mysql_drop_db():
    """WARNING: drops the entire database."""
    mysql_execute('DROP database pck')


def profile_template():
    """Installs profile (shell) template."""
    upload_config_template('profile', '~/.profile', use_sudo=False)


@inside_project
def compilemessages():
    """compile django translations."""
    django_commands.manage('compilemessages')


@run_as_sudo
def install_gettext():
    """intall gettext."""
    run("sudo apt-get install gettext")


@run_as_sudo
def install_pil_dependences():
    """intall gettext."""
    run("sudo apt-get build-dep python-imaging")
    run("""
        sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/;
        sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/;
        sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/;
    """)


def _send_campfire_message(message=None):
    """Send message to Campfire using your campfire login"""
    # SETUP: go to https://<your-campfire-subdomain>.campfirenow.com/member/edit
    # put your api key in ~/.fabricrc like:
    # campfire_api_key = abafdc8391ae67ce829accc9198df832f5f821eb13cac9fb
    site = env.hosts[0].split('@')[1]
    if not message:
        message = "Deploy do site %s feito." % site
    message += " visite: http://%s/" % site

    if env.conf.has_key('CAMPFIRE_API_KEY'):
        data = '{"message":{"body":"-- %s --"}}' % message
        conn = httplib2.Http(timeout=3)
        conn.add_credentials(env.conf['CAMPFIRE_API_KEY'], 'X')
        headers = {'content-type':'application/json'}
        url = "https://popcode-bc.campfirenow.com/room/394521/speak.json"
        conn.request(url, "POST", data, headers)


# Full deploy.
@run_as_sudo
def full_deploy():
    """Full, complete deploy."""

    #aptitude_update()
    #install_pil_dependences()

    #mysql_install()
    #mysql_create_db()
    #mysql_create_user()
    #mysql_grant_permissions()

    fab_deploy.deploy.full_deploy()

    collectstatic()

    #install_gettext()
    #compilemessages()

    apache_restart()
    _send_campfire_message()


# Deploy.
@run_as_sudo
def deploy():
    """Deploy project and restart apache."""

    fab_deploy.deploy_project()
    collectstatic()
    #compilemessages()
    apache_restart()
    _send_campfire_message()
