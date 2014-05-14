from django.contrib import admin
from . import models
from ..common import logger


# Register your models here.
def resend_pdf(modeladmin, request, queryset):
    
    from ..common.analytics import send_pdf_by_mail
    for subject in queryset:
        send_pdf_by_mail(subject.experiment, force=True)
        
resend_pdf.short_description = "Resend the PDF"


def regenerate_pdf(modeladmin, request, queryset):
    
    from ..common.analytics import generate_pdf
    for subject in queryset:
        generate_pdf(subject.experiment)
        
regenerate_pdf.short_description = "Rebuild the PDF"

class ExperimentInline(admin.StackedInline):
    
    model           = models.Experiment
    readonly_fields = ['pdf_file', 'm_fruits', 'm_salties', 'm_positives', 'm_sweets', 'm_objects', 'm_vegetables']
    
class TestSubjectAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'mail', 'code', 'experiment']
    inlines      = [ExperimentInline]
    actions      = [resend_pdf, regenerate_pdf]
    
    def save_model(self, request, obj, form, change):
        
        from ..common.analytics import generate_stats
        from .tasks import *
        from celery import chain
        
        obj.save()
        
        if obj.experiment is not None:
            obj.experiment.save()
            
            logger.info("New experimental file stored, computing values and updating statistics")
            res = chain(exp_compute_values.s(obj.experiment.pk) | exp_generate_pdf.s() | exp_send_pdf_by_mail.s())()
            

class AggregationAdmin(admin.ModelAdmin):

    list_display    = ['operation']
    readonly_fields = ['m_fruits', 'm_salties', 'm_positives', 'm_sweets', 'm_objects', 'm_vegetables']
    
admin.site.register(models.TestSubject, TestSubjectAdmin)
admin.site.register(models.Aggregation, AggregationAdmin)

class TaskHistoryAdminModel(admin.ModelAdmin):
    
    list_display = ["name","status","created"]
    class Meta:
        models.TaskHistory
admin.site.register(models.TaskHistory, TaskHistoryAdminModel)

