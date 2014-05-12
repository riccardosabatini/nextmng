import os
import subprocess
import re
import nextmng as nxt
import getpass

from fabric.api import local, task, abort, puts, settings
from fabric.contrib import django

# ------------------------------
#   Fabric management functions
# ------------------------------

django.project('nextmng')

BACKUP_DIR = './backups'
BACKUP_PATH = os.path.join(BACKUP_DIR, 'pgdump.db')

# Needed for Ubuntu multi-tenant setup.
# NOTE: this has to match with the db specified in local settings.
DB_CLUSTER = '9.2/main'


########################################################################
# Parameters
########################################################################

# For the daemon, to be hard-coded when ok
daemon_subdir    = "daemon"
log_dir          = "daemon/log"

eipscheduler_dir        = os.path.join(os.path.dirname(os.path.dirname(nxt.__file__)), "serverconf") 
eipscheduler_daemon_dir = os.path.join(eipscheduler_dir,daemon_subdir)
eipscheduler_log_dir    = os.path.join(eipscheduler_dir,log_dir)
eipscheduler_user       = getpass.getuser()
eipscheduler_daemon_conf_file = "eipscheduler_daemon.conf"
eipscheduler_module_dir = os.path.dirname(os.path.dirname(nxt.__file__))

########################################################################
# Utility commands
########################################################################

@task
def shell(env="local"):
    
    if env=="local":
        local(".secret/config_local.sh python manage.py shell")


@task
def runserver(env="local"):
    
    if env=="local":
        local(".secret/config_local.sh foreman start -f Procfile.local")


@task
def collect(env="local", test=True):
    
    import os
    
    if env=="local":
        local(".secret/config_local.sh python manage.py collectstatic {} --noinput".format("--dry-run" if booleanize(test) else ""))
    elif env=="s3":
        local(".secret/config_local_s3.sh python manage.py collectstatic {} --noinput".format("--dry-run" if booleanize(test) else ""))
            
########################################################################
# Installation commands
########################################################################

@task
def install(env="local"):
    
    if env=="local":
        local(".secret/config_local.sh python manage.py syncdb")
        local(".secret/config_local.sh python manage.py migrate")
        setup_files(env=env)

@task
def test(env="local"):
    
    if env=="local":
        local(".secret/config_local.sh python manage.py test")
        
def commit():
    local("git add -p && git commit")

@task
def migrate(app, env="local"):
    
    if env=="local":
        
        local(".secret/config_local.sh python manage.py schemamigration "+app+" --auto")
        local(".secret/config_local.sh python manage.py migrate "+app+"")
            
            
@task
def setup_files(env="local"):

    create_base_dirs()
    
    
def create_base_dirs():
    
    if (not os.path.isdir(eipscheduler_dir)):
        os.makedirs(eipscheduler_dir)
     
    if (not os.path.isdir(eipscheduler_daemon_dir)):
        os.makedirs(eipscheduler_daemon_dir)
       
    if (not os.path.isdir(eipscheduler_log_dir)):
        os.makedirs(eipscheduler_log_dir)
         
    
########################################################################
# Heroku commands
########################################################################

@task
def heroku(action, app, branch="master", create=False):
    
    if action.lower()=="init":
        heroku_init(app, branch=branch, create=create)
    
    elif action.lower()=="conf":
        heroku_conf(app, branch=branch)
        
    elif action.lower()=="install":
        heroku_install(app)
    
    elif action.lower()=="push":
        heroku_push(app, branch=branch)
    
    
@task
def heroku_init(app, branch="master", create=False):

    if booleanize(create):
        local("heroku apps:create {app} -s cedar".format(app=app, branch=branch))
        local("git remote add {app} git@heroku.com:{app}.git".format(app=app))
        
    heroku_conf(app)
    heroku_push(app, branch=branch)
    heroku_install(app)
    
@task
def heroku_push(app, branch="master"):
    
    local("git push {app} {branch}".format(app=app, branch=branch))

@task
def heroku_install(app):
         
    local("heroku run python manage.py syncdb --app {app}".format(app=app))
    local("heroku run python manage.py migrate --all --app {app}".format(app=app))
    
@task
def heroku_conf(app):
    
    
    with open(".secret/config_common.sh") as f:
        _common = f.readlines()
    
    _confs = {}
    
    for l in _common:
        if l.strip().startswith("export"):
            _parts = [i.strip().replace('\\"',"__VERYSTRAGE__").replace('"','').replace("__VERYSTRAGE__",'"').decode('string_escape') for i in l[l.index("export")+len("export"):].split("=")]
            _confs[_parts[0]] = _parts[1] 
    
    for k in _confs.keys():
         local("heroku config:set {0}={1} --app {2}".format(k, _confs[k], app))
    
    local("heroku config --app {0}".format(app))
    
########################################################################
# Daemon commands
########################################################################

@task
def db(action, env="local"):
    
    commands = {"wipe" : db_wipe,
                "filldemo" : db_fill_demo,
               }
    
    if action in commands:
        commands[action](env=env)
    else:
        print "Available commands:"
        print commands.keys()    
        
def db_wipe(env="local"):
    """
    Wipe the database
    """
    from fabric.contrib.console import confirm
    
    if env=="local":
        
        if confirm("Are you sure you want to wipe the DB?"):
            print "Clearing all locks ..."
            local(".secret/config_local.sh python manage.py clear_all")

def db_fill_demo(env="local"):
    
    if env=="local":
        
        print "Installing demo sensors ..."
        local(".secret/config_local.sh python manage.py fill_demo")
    

########################################################################
# Utility funcitons for files
########################################################################

def booleanize(value):
    """Return value as a boolean."""

    true_values = ("yes", "true", "1", "y")
    false_values = ("no", "false", "0", "n")

    if isinstance(value, bool):
        return value

    if value.lower() in true_values:
        return True

    elif value.lower() in false_values:
        return False

    raise TypeError("Cannot booleanize ambiguous value '%s'" % value)