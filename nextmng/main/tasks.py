from __future__ import absolute_import
from celery import shared_task, Task, task
from celery.task import PeriodicTask
from ..common.analytics import compute_zscores, generate_stats
from ..common import logger
from ..main.models import Experiment, TaskHistory
from django.core.management import call_command
from datetime import timedelta
from celery.utils.log import get_task_logger
from django.core.cache import cache

LOCK_EXPIRE = 60 * 15 # Lock expires in 5 minutes


#--------------------------------------------
# Wrapper class
#--------------------------------------------

class ExperimentTask(Task):
    
    abstract = True
    lock     = None
    
    def __call__(self, *args, **kwargs):
        
        self.taskhistory = TaskHistory.objects.get_or_create(name=self.name+"-"+self.request.id)[0]
        
        try:   
            self.pk    = args[0]
            self.exp   = Experiment.objects.get(pk=self.pk)
            self.taskhistory.name = self.name+"-"+self.exp.subject.name+"-"+self.request.id
            self.taskhistory.save()
            
            return self.run(*args, **kwargs)
        
        except Exception, e:
            import traceback
            self.taskhistory.status = TaskHistory.FINISHED_ERROR
            self.taskhistory.notes  = traceback.format_exc()
            self.taskhistory.save()
            return
        
            
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        
        import datetime
        from django.utils.timezone import utc
        
        if einfo is None:
            self.taskhistory.status = TaskHistory.FINISHED_OK
        else:
            self.taskhistory.notes  = einfo.traceback
            self.taskhistory.status = TaskHistory.FINISHED_ERROR
            
        self.taskhistory.finished =  datetime.datetime.utcnow().replace(tzinfo=utc)
        self.taskhistory.save()             


@task.task(base=ExperimentTask)
def exp_compute_values(pk):
    
    
    from django.core.files.storage import default_storage as storage
    
    try:
        exp   = Experiment.objects.get(pk=pk)
        
        fh = storage.open(exp.file.name, "r")
        z_scores = compute_zscores(fh)
        fh.close()
        
        def get_field(arr, n):
            return arr[n] if len(arr)>=n+1 else None
            
        exp.m_fruits     = get_field(z_scores, 1)
        exp.m_salties    = get_field(z_scores, 2)
        exp.m_positives  = get_field(z_scores, 3)
        exp.m_sweets     = get_field(z_scores, 4)
        exp.m_objects    = get_field(z_scores, 5)
        exp.m_vegetables = get_field(z_scores, 6)
        
        exp.save()
        logger.info("Experiment z_scores correctly computed for {}".format(exp.subject))
        
        generate_stats()
        logger.info("Statistics correctly updated")
        
        return pk
        
    except Exception as e:
        logger.error("Error storing experiment for {} with exception {}".format(exp.subject, e))
        raise

@task.task(base=ExperimentTask)
def exp_generate_pdf(pk):
        
    from ..common.analytics import generate_pdf, generate_new_pdf
    
    try:
        
        exp = Experiment.objects.get(pk=pk)
        #_f = generate_pdf(self)
        _f = generate_new_pdf(exp)
        exp.pdf_file = _f
        exp.save()
        
        return pk
    
    except Exception as e:
        import traceback
        logger.error("Error generating pdf for {} with exception {}".format(exp.subject, traceback.format_exc()))
        raise
    
@task.task(base=ExperimentTask)
def exp_send_pdf_by_mail(pk):


    from ..common.analytics import send_pdf_by_mail
    from django.utils.timezone import utc
    import datetime
    
    try:
        
        exp = Experiment.objects.get(pk=pk)
        
        send_pdf_by_mail(exp)
        
        exp.subject.sent = datetime.datetime.utcnow().replace(tzinfo=utc)
        exp.subject.save()
        
        return pk
    
    except Exception as e:
        
        logger.error("Cannot send a mail to the recipient {}: {}".format(exp.subject.mail, e))
        raise



@task
def check_deposit_task():
    
    from nextmng.common.importer import import_depot
    
    logger.info('Check deposit started')
    
    # The cache key consists of the task name and the MD5 digest
    # of the feed URL.
    lock_id = '{0}-lock'.format("check_deposit_task")

    # cache.add fails if if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)
    
    _imported    = 0
    
    if acquire_lock():
        try:
            _imported = import_depot()
        finally:
            release_lock()
            logger.info('Check deposit is finished')
        return _imported

    logger.info('Check deposit is already running by another worker')
    
