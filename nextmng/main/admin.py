from django.contrib import admin
from . import models
from ..common import logger


# Register your models here.
def resend_pdf(modeladmin, request, queryset):
    for subject in queryset:
        subject.experiment.send_pdf_by_mail()
resend_pdf.short_description = "Resend the PDF"

def recompute(modeladmin, request, queryset):
    
    from ..common.analytics import generate_stats
    
    for subject in queryset:
        subject.experiment.compute_values()
        subject.experiment.generate_pdf()

    generate_stats()
    
recompute.short_description = "Recompute file"


def regenerate_pdf(modeladmin, request, queryset):
    for subject in queryset:
        subject.experiment.generate_pdf()
regenerate_pdf.short_description = "Rebuild the PDF"

class ExperimentInline(admin.StackedInline):
    
    model           = models.Experiment
    #readonly_fields = ['pdf_file', 'm_objects', 'm_vegetables', 'm_sweets', 'm_fruits', 'm_stages', 'm_positives', 'm_salties']
    readonly_fields = ['pdf_file', 'm_objects', 'm_vegetables', 'm_sweets', 'm_fruits', 'm_positives', 'm_salties']
    
class TestSubjectAdmin(admin.ModelAdmin):
    
    list_display = ['name', 'mail', 'code', 'experiment']
    inlines      = [ExperimentInline]
    actions      = [resend_pdf, regenerate_pdf, recompute]
    
    def save_model(self, request, obj, form, change):
        
        from ..common.analytics import generate_stats
        
        obj.save()
        
        if obj.experiment is not None:
            obj.experiment.save()
            
            logger.info("New experimental file stored, computing values and updating statistics")
            
            obj.experiment.compute_values()
            generate_stats()
            if obj.experiment.generate_pdf():
                if obj.send_to:
                    obj.experiment.send_pdf_by_mail()
            

class AggregationAdmin(admin.ModelAdmin):

    list_display    = ['operation']
    #readonly_fields = ['m_objects', 'm_vegetables', 'm_sweets', 'm_fruits', 'm_stages', 'm_positives', 'm_salties']
    readonly_fields = ['m_objects', 'm_vegetables', 'm_sweets', 'm_fruits', 'm_positives', 'm_salties']
    
admin.site.register(models.TestSubject, TestSubjectAdmin)
admin.site.register(models.Aggregation, AggregationAdmin)


# class ExperimentAdmin(admin.ModelAdmin):
#     list_display = ['subject']
# 
# class TestSubjectAdmin(admin.ModelAdmin):
#     list_display = ['name', 'mail', 'code', 'experiment']
#     
#     def get_experiments(self, obj):
#         return '%s' % obj.experiment
#     get_experiments.short_description = 'Experiments'
#     
# admin.site.register(models.Experiment, ExperimentAdmin)
# admin.site.register(models.TestSubject, TestSubjectAdmin)

