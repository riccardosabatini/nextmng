import os
from fabric.api import local, task, abort, puts, settings
from fabric.contrib import django

# ------------------------------
#   Fabric management functions
# ------------------------------
DJANGO_PROJECT = 'nextmng'
django.project(DJANGO_PROJECT)

BACKUP_DIR = './backups'
BACKUP_PATH = os.path.join(BACKUP_DIR, 'pgdump.db')

# Needed for Ubuntu multi-tenant setup.
# NOTE: this has to match with the db specified in local settings.
DB_CLUSTER = '9.2/main'

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

########################################################################
# Parameters
########################################################################

# For the daemon, to be hard-coded when ok

########################################################################
# Utility commands
########################################################################

@task
def shell():
    
    local("./run_in_env.sh .secret/local.env python manage.py shell")


@task
def runserver(type="django"):
    
    if type.startswith("dj"):
        local("./run_in_env.sh .secret/local.env python manage.py runserver")
    elif type.startswith("gu"):
        local("./run_in_env.sh .secret/local.env foreman start -f Procfile.local")


@task
def collect(env="local", test=True, clear=False):
    
    import os
    
    _args = "--noinput"
    if booleanize(test): _args = _args+" --dry-run"
    if booleanize(clear): _args = _args+" -c"
    
    local("./run_in_env.sh .secret/local.env python manage.py collectstatic {} --settings={}.settings.{}".format(_args, DJANGO_PROJECT, env))
            
########################################################################
# Installation commands
########################################################################

@task
def install():
    
    local("./run_in_env.sh .secret/local.env python manage.py syncdb")
    local("./run_in_env.sh .secret/local.env python manage.py migrate")

@task
def test():
    
    local("./run_in_env.sh .secret/local.env python manage.py test")
        
def commit():
    
    local("git add -p && git commit")

@task
def migrate(app, env="local"):
    
    local("./run_in_env.sh .secret/local.env python manage.py schemamigration "+app+" --auto")
    local("./run_in_env.sh .secret/local.env python manage.py migrate "+app+"")
            
            
    
########################################################################
# Heroku commands
########################################################################

@task
def heroku(action, app, branch="master", create=False):
    
    if action.lower()=="init":
        heroku_init(app, branch=branch, create=create)
    
    elif action.lower().startswith("conf"):
        heroku_conf(app)
        
    elif action.lower()=="install":
        heroku_install(app)
    
    elif action.lower()=="migrate":
        heroku_migrate(app)
        
    elif action.lower()=="push":
        heroku_push(app, branch=branch)
    
    elif action.lower()=="logs":
        heroku_logs(app)
    
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
    heroku_migrate(app)

@task
def heroku_logs(app):
         
    local("heroku logs --app {app}".format(app=app))
    
@task    
def heroku_migrate(app):
    
    local("heroku run python manage.py migrate --all --app {app}".format(app=app))
        
@task
def heroku_conf(app):
    
    
    with open(".secret/heroku.env") as f:
        _common = f.readlines()
    
    _confs = {}
    
    for l in _common:
        if not l.strip().startswith("#") and not l.strip() == "":
            #_parts = [i.strip().replace('\\"',"__VERYSTRAGE__").replace('"','').replace("__VERYSTRAGE__",'"').decode('string_escape') for i in l[l.index("export")+len("export"):].split("=")]
            _parts = [p.strip() for p in l.split("=")]
            _confs[_parts[0]] = _parts[1] 
    
    for k in _confs.keys():
         local("heroku config:set {0}={1} --app {2}".format(k, _confs[k], app))
    
    local("heroku config --app {0}".format(app))
    
########################################################################
# Database commands
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
            local("./run_in_env.sh .secret/local.env python manage.py clear_all")

def db_fill_demo(env="local"):
    
    if env=="local":
        
        print "Installing demo sensors ..."
        local("./run_in_env.sh .secret/local.env python manage.py fill_demo")
    

