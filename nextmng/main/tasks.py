from __future__ import absolute_import
from celery import shared_task, Task, task
from ..common.analytics import compute_zscores
from ..common import logger
from ..main.models import Experiment, TaskHistory

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
        
        exp.m_objects    = z_scores[0] if len(z_scores)>=1 else None
        exp.m_vegetables = z_scores[1] if len(z_scores)>=2 else None
        exp.m_sweets     = z_scores[2] if len(z_scores)>=3 else None
        exp.m_fruits     = z_scores[3] if len(z_scores)>=4 else None
        exp.m_positives  = z_scores[4] if len(z_scores)>=5 else None
        exp.m_salties    = z_scores[5] if len(z_scores)>=6 else None
        
        exp.save()
        
        logger.info("Experiment correctly stored for {} with z_scores {}".format(exp.subject, z_scores))
        
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


    import pystmark
    from django.conf import settings
    from django.core.files.storage import default_storage as storage
    
    try:
        
        exp = Experiment.objects.get(pk=pk)
        
        if not exp.subject.send_to:
            return pk
        
        message = pystmark.Message(sender=settings.POSTMASTER['sender'],
                                   to=exp.subject.mail,
                                   subject='FoodCAST Neuroscience Experiment result',
                                   text='Dear {},\nwe\'re happy to send you the resuts for the experiment you took part in WiredNext 2014 at the FoodCAST stand.\n\nBest regard,\nThe FoodCAST Team'.format(exp.subject.name))

        # Attach using filename
        fh = storage.open(exp.pdf_file.name, "r")
        
        message.attach_binary(fh.read(), exp.pdf_file.name.split("/")[-1])
        
        pystmark.send(message, api_key=settings.POSTMASTER['key'])
        
        logger.info("Mail sent to the recipient {}".format(exp.subject.mail))
        fh.close()
        
        return pk
    
    except Exception as e:
        
        logger.error("Cannot send a mail to the recipient {}: {}".format(exp.subject.mail, e))
        raise
    
    