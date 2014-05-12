from django.db import models
from django.core.exceptions import ValidationError, FieldError
from ..common.mixins import ValidateModelMixin
from ..common.analytics import compute_zscores
from ..common import logger

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
    m_stages     = models.FloatField(blank=True, null=True)
    m_positives  = models.FloatField(blank=True, null=True)
    m_salties    = models.FloatField(blank=True, null=True)
    
    def get_array(self):
        return [self.m_objects, self.m_vegetables, self.m_sweets, self.m_fruits, self.m_stages, self.m_positives, self.m_salties]
    
class Experiment(ValidateModelMixin, models.Model):
    
    subject    = models.OneToOneField(TestSubject, related_name='experiment')
    executed   = models.DateTimeField(auto_now_add=True, editable=False)
    file       = models.FileField(upload_to='files/%Y/%m/%d')
    pdf_file   = models.FileField(blank=True, null=True, upload_to='not_used')
    
    m_objects    = models.FloatField(blank=True, null=True)
    m_vegetables = models.FloatField(blank=True, null=True)
    m_sweets     = models.FloatField(blank=True, null=True)
    m_fruits     = models.FloatField(blank=True, null=True)
    m_stages     = models.FloatField(blank=True, null=True)
    m_positives  = models.FloatField(blank=True, null=True)
    m_salties    = models.FloatField(blank=True, null=True)
    
    def get_array(self):
        return [self.m_objects, self.m_vegetables, self.m_sweets, self.m_fruits, self.m_stages, self.m_positives, self.m_salties]
    
    def compute_values(self):
        
        from django.conf import settings
        
        fname = self.file.path
        
        try:
            
            z_scores = compute_zscores(fname)
            
            self.m_objects    = z_scores[0] if len(z_scores)>=1 else None
            self.m_vegetables = z_scores[1] if len(z_scores)>=2 else None
            self.m_sweets     = z_scores[2] if len(z_scores)>=3 else None
            self.m_fruits     = z_scores[3] if len(z_scores)>=4 else None
            self.m_stages     = z_scores[4] if len(z_scores)>=5 else None
            self.m_positives  = z_scores[5] if len(z_scores)>=6 else None
            self.m_salties    = z_scores[6] if len(z_scores)>=7 else None
            
            self.save()
            
            logger.info("Experiment correctly stored for {} with z_scores {}".format(self.subject, z_scores))
            
        except Exception as e:
            
            logger.error("Error storing experiment for {} with exception {}".format(self.subject, e))
    
    def generate_pdf(self):
        
        from ..common.analytics import generate_pdf
        
        try:
            _f = generate_pdf(self)
            self.pdf_file = _f
            self.save()
            return True
        except Exception as e:
            
            logger.error("Error generating pdf for {} with exception {}".format(self.subject, e))
            return False
    
    
    def send_pdf_by_mail(self):
    

#         import sendgrid
#         from django.conf import settings
#         sg = sendgrid.SendGridClient(settings.SENDGRID['user'], settings.SENDGRID['pass'])
#             
#         message = sendgrid.Mail()
#         message.add_to(self.subject.mail)
#         message.set_subject('FoodCAST @WiredNext - Results')
#         message.set_text('Salve {}, siamo felici di inviarti il risultato del tuo esperimento. FoodCAST Team')
#         message.set_from('FoodCAST <foodcast@sissa.it>')
#         message.add_attachment('results.pdf', self.pdf_file.path)
#         status, msg = sg.send(message)

        import pystmark
        from django.conf import settings
        
        try:
            
            message = pystmark.Message(sender=settings.POSTMASTER['sender'],
                                       to=self.subject.mail,
                                       subject='FoodCAST Neuroscience Experiment result',
                                       text='Dear {},\nwe\'re happy to send you the resuts for the experiment you took part in WiredNext 2014 at the FoodCAST stand.\n\nBest regard,\nThe FoodCAST Team'.format(self.subject.name))

            # Attach using filename
            message.attach_file(self.pdf_file.path)
            
            pystmark.send(message, api_key=settings.POSTMASTER['key'])
            
            logger.info("Mail sent to the recipient {}".format(self.subject.mail))
            
            return True
        
        except Exception as e:
            
            logger.error("Cannot send a mail to the recipient {}: {}".format(self.subject.mail, e))
            return False
        
        
#-------------------------------------
#         Lock
#-------------------------------------

class DbLock(models.Model):
    
    key        = models.TextField(primary_key=True)
    creation   = models.DateTimeField(auto_now_add=True, editable=False)
    timeout    = models.IntegerField(editable=False)
    owner      = models.CharField(max_length=255, blank=False)
    
    