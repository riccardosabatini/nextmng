from django.db import models
from django.core.exceptions import ValidationError, FieldError
from ..common.mixins import ValidateModelMixin
from ..common import logger
from django.db import models

# Get an instance of a logger

CODE_LEN = 5


class TestSubject(ValidateModelMixin, models.Model):
    
    name       = models.CharField('Subject name', max_length=500, blank=False)
    mail       = models.EmailField('Subject email', unique=True)
    registered = models.DateTimeField(auto_now_add=True, editable=False)
    send_to    = models.BooleanField(default=False)
    
    code       = models.CharField('Registration code', max_length=CODE_LEN, unique=True)
    
    # ----------------
    #
    # ----------------
    
    KID    = 0
    YOUNG  = 1
    ADULT  = 2
    SENIOR = 3
    
    AGE_CHOICES = (
        (KID,    'Kid'),
        (YOUNG,  'Young'),
        (ADULT,  'Adult'),
        (SENIOR, 'Senior'),
    )
    
    MALE    = 0
    FEMALE  = 1
    
    GENDER_CHOICES = (
        (MALE,    'Male'),
        (FEMALE,  'Female'),
    )

    
    age    = models.IntegerField(default=KID, choices=AGE_CHOICES)
    gender = models.IntegerField(default=MALE, choices=GENDER_CHOICES)
    
    def __init__(self, *args, **kwargs):
        
        super(TestSubject, self).__init__(*args, **kwargs)
        
        if self.code is None or str(self.code.strip())=='':
            self.code = self.promotion_code_generate
        
    class Meta:
        ordering        = ["registered"]
        get_latest_by   = "registered"
    
    @property
    def promotion_code_generate(self):
        
        import random
        
        while 1:
            trial_code = ''.join(random.choice('0123456789ABCDEF') for i in range(CODE_LEN))
            try:
                TestSubject.objects.get(code=trial_code)
            except:
                return trial_code
          
    # Utility
    def clean(self):
        
        # Name check
        if self.name.strip() == '':
            raise ValidationError('Empty name')
    
    def __unicode__(self):
        return "{} - {}".format(self.name, self.mail)  


class Aggregation(models.Model):
    
    operation    = models.CharField('Operation done', max_length=500, blank=False)
    
    m_objects    = models.FloatField(blank=True, null=True)
    m_vegetables = models.FloatField(blank=True, null=True)
    m_sweets     = models.FloatField(blank=True, null=True)
    m_fruits     = models.FloatField(blank=True, null=True)
    m_positives  = models.FloatField(blank=True, null=True)
    m_salties    = models.FloatField(blank=True, null=True)
    
    def get_array(self):
        return [self.m_objects, self.m_vegetables, self.m_sweets, self.m_fruits, self.m_positives, self.m_salties]
    
class Experiment(ValidateModelMixin, models.Model):
    
    subject    = models.OneToOneField(TestSubject, related_name='experiment')
    executed   = models.DateTimeField(auto_now_add=True, editable=False)
    file       = models.FileField(upload_to='files/%Y/%m/%d')
    pdf_file   = models.FileField(blank=True, null=True, upload_to='not_used')
    
    m_objects    = models.FloatField(blank=True, null=True)
    m_vegetables = models.FloatField(blank=True, null=True)
    m_sweets     = models.FloatField(blank=True, null=True)
    m_fruits     = models.FloatField(blank=True, null=True)
    m_positives  = models.FloatField(blank=True, null=True)
    m_salties    = models.FloatField(blank=True, null=True)
    
    def get_array(self):
        return [self.m_objects, self.m_vegetables, self.m_sweets, self.m_fruits, self.m_positives, self.m_salties]
        
        
#-------------------------------------
#         Lock
#-------------------------------------

class TaskHistory(models.Model):
    
    RUNNING        = 0
    FINISHED_OK    = 1
    FINISHED_ERROR = 3
    
    STATUS_CHOICES = (
        (RUNNING,    'Running'),
        (FINISHED_OK,  'FinishedOk'),
        (FINISHED_ERROR,  'FinishedError'),
    )
    
    name       = models.CharField(max_length=100, verbose_name="Task name")
    created    = models.DateTimeField(auto_now_add=True, editable=False)
    finished   = models.DateTimeField(null=True, blank=True)
    status     = models.IntegerField(default=RUNNING, choices=STATUS_CHOICES)
    notes      = models.TextField(blank=True, null=True)
    
    # Meta & unicode
    class Meta:
        ordering        = ["-created"]
        get_latest_by   = "finished"
        
    def __unicode__(self):
        return "Task History of Task: {}".format(self.name)
    


class DbLock(models.Model):
    
    key        = models.TextField(primary_key=True)
    creation   = models.DateTimeField(auto_now_add=True, editable=False)
    timeout    = models.IntegerField(editable=False)
    owner      = models.CharField(max_length=255, blank=False)
    
    