from ..common import logger
from ..main.models import TestSubject, Experiment, TaskHistory
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
import os

def import_depot(dir_depot = settings.DEPOT_DIR):
    
    if dir_depot is None:
        logger.error("There is no DEPOT_DIR configured")
        return

    if not os.path.exists(dir_depot):
        logger.error("I cannot find the deposit dir")
        return

    _all = 0   
    for file in os.listdir(dir_depot):
        if file.endswith(".txt"):
            
            _f = os.path.join(dir_depot,file)
            logger.info("Found valid file {}".format(_f))
            _all+=import_file(_f)
    
    return _all


def import_file(fname, blocking=True):
    
    from django.core.files.base import File
    import ntpath
    from nextmng.main.tasks import exp_compute_values, exp_generate_pdf, exp_send_pdf_by_mail
    from celery import chain
    
    
    _base_fname   = ntpath.basename(fname)
    (_code, _ext) = _base_fname.split(".")
    
    try:
        _subject = TestSubject.objects.get(code=_code)
    except:
        logger.error("There is no TestSubject with code {}".format(_code))
        return 0
    
    logger.info("Match found for file {} with user {}".format(fname, _subject.name))
    
    try:
        if _subject.experiment is None:
            _subject.experiment = Experiment()
    except ObjectDoesNotExist:
        _subject.experiment = Experiment()
    
    with open(fname, "r") as _fr:
        _subject.experiment.file.save(_base_fname, File(_fr))
    
    _subject.experiment.save()
    
    logger.info("New experimental file stored, computing values and updating statistics")
    chain = exp_compute_values.s(_subject.experiment.pk) | exp_generate_pdf.s() | exp_send_pdf_by_mail.s()
    
    res = chain()
    
    os.remove(fname)
    
    return 1
    