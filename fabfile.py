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
        local(".secret/config_local.sh python manage.py runserver")
            
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
    
    