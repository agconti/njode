import os
import random
import string

from fabric.api import env, local, require, lcd
from fabric.colors import (
    cyan,
    magenta,
    yellow
)

current_dir = os.getcwd()
project_name = 'njode'


def deploy():
    """fab [environment] deploy"""
    require('environment')
    maintenance_on()
    push()
    migrate()
    collectstatic()
    maintenance_off()
    ps()


def maintenance_on():
    """fab [environment] maintenance_on"""
    require('environment')
    print yellow('Starting maintenance mode ...')
    local('heroku maintenance:on --remote {}'.format(env.environment))


def maintenance_off():
    """fab [environment] maintenance_off"""
    require('environment')
    print cyan('Turning maintenance mode off...')
    local('heroku maintenance:off --remote {}'.format(env.environment))


def push():
    """fab [environment] push"""
    require('environment')
    local('git push {} {}:master'.format(env.environment, env.branch))


def migrate(app=None):
    """fab [environment] migrate"""
    require('environment')
    local('heroku run python {}/manage.py migrate --remote {}'.format(project_name,
                                                                      env.environment))


def collectstatic(app=None):
    """fab [environment] collectstatic"""
    require('environment')
    local('heroku run python {}/manage.py collectstatic --noinput --remote {}'.format(project_name, env.environment))


def ps():
    """fab [environment] ps"""
    require('environment')
    local('heroku ps --remote {}'.format(env.environment))


def open_heroku():
    """fab [environment] open"""
    require('environment')
    local('heroku open --remote {}'.format(env.environment))


def manage(cmd):
    local('python {}/manage.py {}'.format(project_name, cmd))


def shell():
    """fab shell"""
    manage('shell_plus')


def serve():
    manage('runserver')


def dev():
    """fab dev [command]"""
    env.environment = 'dev'
    env.branch = 'master'


def qa():
    """fab staging [command]"""
    env.environment = 'qa'
    env.branch = 'qa'


def prod():
    """fab prod [command]"""
    env.environment = 'prod'
    env.branch = 'master'


def create_server():
    """ creates a new unconfigured server on heroku """
    require('environment')
    local("heroku create {}-{} --buildpack https://github.com/heroku/heroku-buildpack-python"
          .format(project_name, env.environment))


def create_superuser():
    """ Creates a django superuser """
    require('environment')
    local("heroku run python {}/manage.py createsuperuser --remote {}".format(project_name, env.environment))


def set_aws_keys():
    """ Sets S3 Keys """
    local("heroku config:set DJANGO_AWS_ACCESS_KEY_ID={} --remote {}"
          .format(secrets.AWS_ACCESS_KEY_ID, env.environment))
    local("heroku config:set DJANGO_AWS_SECRET_ACCESS_KEY={} --remote {}"
          .format(secrets.AWS_SECRET_ACCESS_KEY, env.environment))
    local("heroku config:set DJANGO_AWS_STORAGE_BUCKET_NAME=dayo-{0} --remote {0}"
          .format(env.environment))


def create_secret_key():
    """ Creates a random string of letters and numbers """
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(16))


def configure_sever():
    """ Configures server with a general configuration """
    require('environment')
    local("heroku addons:add heroku-postgresql:dev --remote {}".format(env.environment))
    local("heroku addons:add pgbackups:auto-month --remote {}".format(env.environment))
    local("heroku addons:add sendgrid:starter --remote {}".format(env.environment))
    local("heroku addons:add memcachier:dev --remote {}".format(env.environment))
    local("heroku pg:promote DATABASE_URL --remote {}".format(env.environment))
    local("heroku config:set DJANGO_CONFIGURATION=Production --remote {}".format(env.environment))
    local("heroku config:set DJANGO_SECRET_KEY='{}' --remote {}"
          .format(create_secret_key(), env.environment))
    set_aws_keys()


def create_standard_server():
    """ Creates a sever with a standard build """
    create_server()
    configure_sever()
    push()
    migrate()
    create_superuser()
    open_heroku()


def set_remotes():
    """ Sets git remotes based on project structure """
    local('git remote add dev git@heroku.com:{}-dev.git'.format(project_name))
    local('git remote add qa git@heroku.com:{}-qa.git'.format(project_name))
    local('git remote add prod git@heroku.com:{}-prod.git'.format(project_name))


def test():
    """ Runs nose test suite """
    with lcd(current_dir):
        local('python {}/manage.py test --with-progressive'.format(project_name))


def deploy_docs():
    """" Builds docs and deploys to github pages """
    with lcd(current_dir):
        print magenta("Building docs ...")
        local('mkdocs build --clean')
        local('git add _docs_html/')
        local('git commit -m "docs(api): updated documentation"')
        local('git subtree push --prefix _docs_html/ origin gh-pages')
        print cyan("Docs Deployed.")
