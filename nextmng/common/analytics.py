import numpy as np
from . import logger

def compute_zscores(fname):
    
    content = None
    with open(fname) as f:
        content = f.readlines()
    
    # Get first line
    f_line = -1
    for i in range(len(content)):
        if content[i].startswith("Time,SC-Pro/Flex"):
            f_line = i+2
            break
    
    _groups    = []
    _averages  = []
    _group     = []
    
    _new_group = False
    
    for i in range(f_line, len(content)):
        
        if len(content[i].strip())==0:
            logger.debug("Empty line")
            continue
    
        try:
            _parts = [float(n) for n in content[i].split(",")]
        except:
            logger.debug("Error parsing line -{}-".format(content[i]))
            continue
    
        if not len(_parts) == 3:
            continue
    
        if _parts[2] > 0:
            logger.debug("Trigger arrived", _parts[2])
            _new_group = True
    
        if _new_group and _parts[2]<0:
            logger.debug("Trigger ended", _parts[2])
            
            _arr = np.array(_group)
            _avg = np.average(_arr)
    
            logger.debug("Group", _arr)
            logger.debug("Average", _avg)
    
            _groups.append(_arr)
            _averages.append(_avg)
    
            _group     = []
            _new_group = False
    
        if not _new_group:
            _group.append(_parts[1])
    
    
    _mean    = np.average(_averages)
    _std     = np.std(_averages)
    _zscores = (_averages-_mean)/_std
    
    
    return _zscores


def generate_stats():
    
    from django.db.models import Avg, StdDev
    from ..main.models import Experiment, Aggregation
    
    try:
        
        _avg_agg, _new = Aggregation.objects.get_or_create(operation="Avg")
        
        logger.info("Computing averages")
        _avg_agg.m_objects    = Experiment.objects.filter(m_objects__isnull=False).aggregate(Avg('m_objects')).values()[0]
        _avg_agg.m_vegetables = Experiment.objects.filter(m_vegetables__isnull=False).aggregate(Avg('m_vegetables')).values()[0]
        _avg_agg.m_sweets     = Experiment.objects.filter(m_sweets__isnull=False).aggregate(Avg('m_sweets')).values()[0]
        _avg_agg.m_fruits     = Experiment.objects.filter(m_fruits__isnull=False).aggregate(Avg('m_fruits')).values()[0]
        _avg_agg.m_stages     = Experiment.objects.filter(m_stages__isnull=False).aggregate(Avg('m_stages')).values()[0]
        _avg_agg.m_positives  = Experiment.objects.filter(m_positives__isnull=False).aggregate(Avg('m_positives')).values()[0]
        _avg_agg.m_salties    = Experiment.objects.filter(m_salties__isnull=False).aggregate(Avg('m_salties')).values()[0]
        
        _avg_agg.save()
        
        
        _avg_std, _new = Aggregation.objects.get_or_create(operation="StdDev")
        
        logger.info("Computing standard deviation")
        _avg_std.m_objects    = Experiment.objects.filter(m_objects__isnull=False).aggregate(StdDev('m_objects')).values()[0]
        _avg_std.m_vegetables = Experiment.objects.filter(m_vegetables__isnull=False).aggregate(StdDev('m_vegetables')).values()[0]
        _avg_std.m_sweets     = Experiment.objects.filter(m_sweets__isnull=False).aggregate(StdDev('m_sweets')).values()[0]
        _avg_std.m_fruits     = Experiment.objects.filter(m_fruits__isnull=False).aggregate(StdDev('m_fruits')).values()[0]
        _avg_std.m_stages     = Experiment.objects.filter(m_stages__isnull=False).aggregate(StdDev('m_stages')).values()[0]
        _avg_std.m_positives  = Experiment.objects.filter(m_positives__isnull=False).aggregate(StdDev('m_positives')).values()[0]
        _avg_std.m_salties    = Experiment.objects.filter(m_salties__isnull=False).aggregate(StdDev('m_salties')).values()[0]
        
        _avg_std.save()
    
    except Exception as e:
            
            logger.error("Error computing new stats, {}".format(e))
    


def generate_pdf(experiment):

    # This is a demo of creating a pdf file with several pages.
    
    import datetime
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    from os.path import join
    from django.conf import settings
    from django.db.models import Avg, StdDev
    from ..main.models import Experiment, Aggregation
    
    
    fname = settings.MEDIA_ROOT+"/files/"+experiment.subject.code+".pdf"
    
    logger.info("Generating PDF file at {}".format(fname))
    
    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
        
    _avg = Aggregation.objects.get(operation="Avg").get_array()
    _std = Aggregation.objects.get(operation="StdDev").get_array()
    _exp = experiment.get_array()
    
    if None in _exp:
        _idn = _exp.index(None)
        _avg = _avg[0:_idn]
        _std = _std[0:_idn]
        _exp = _exp[0:_idn]
    
    
    logger.info("_avg {}".format(_avg))
    logger.info("_std {}".format(_std))
    logger.info("_exp {}".format(_exp))
    
    ind = np.arange(len(_avg))  # the x locations for the groups
    width = 0.35       # the width of the bars
    
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, _avg, width, color='b', yerr=_std)
    rects2 = ax.bar(ind+width, _exp, width, color='g')
    
    # add some
    ax.set_ylabel('Abs. Values')
    ax.set_title('Experiment for {}'.format(experiment.subject.name))
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('Objects', 'Veggies', 'Sweets', 'Fruits', 'Stages', 'Positives', 'Salts') )
    
    ax.legend( (rects1[0], rects2[0]), ('All', experiment.subject.name) )
    
    def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height), ha='center', va='bottom')
    
    autolabel(rects1)
    autolabel(rects2)
    
    plt.savefig(fname)
        
    return fname


