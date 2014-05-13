from . import logger
from numpy import average, array, std, arange

def compute_zscores(f):
    
    content = None
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
            #logger.debug("Empty line")
            continue
    
        try:
            _parts = [float(n) for n in content[i].split(",")]
        except:
            #logger.debug("Error parsing line -{}-".format(content[i]))
            continue
    
        if not len(_parts) == 3:
            continue
    
        if _parts[2] > 0:
            #logger.debug("Trigger arrived: {}".format(_parts[2]))
            _new_group = True
    
        if _new_group and _parts[2]<0:
            #logger.debug("Trigger ended: {}".format(_parts[2]))
            
            _arr = array(_group)
            _avg = average(_arr)
    
            #logger.debug("Group: {}".format(_arr))
            #logger.debug("Average: {}".format(_avg))
    
            _groups.append(_arr)
            _averages.append(_avg)
    
            _group     = []
            _new_group = False
    
        if not _new_group:
            _group.append(_parts[1])
    
    # Last bin even if there is no trigger
    _arr = array(_group)
    _avg = average(_arr)
    _groups.append(_arr)
    _averages.append(_avg)
    
    _mean    = average(_averages)
    _std     = std(_averages)
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
        #_avg_agg.m_stages     = Experiment.objects.filter(m_stages__isnull=False).aggregate(Avg('m_stages')).values()[0]
        _avg_agg.m_positives  = Experiment.objects.filter(m_positives__isnull=False).aggregate(Avg('m_positives')).values()[0]
        _avg_agg.m_salties    = Experiment.objects.filter(m_salties__isnull=False).aggregate(Avg('m_salties')).values()[0]
        
        _avg_agg.save()
        
        
        _avg_std, _new = Aggregation.objects.get_or_create(operation="StdDev")
        
        logger.info("Computing standard deviation")
        _avg_std.m_objects    = Experiment.objects.filter(m_objects__isnull=False).aggregate(StdDev('m_objects')).values()[0]
        _avg_std.m_vegetables = Experiment.objects.filter(m_vegetables__isnull=False).aggregate(StdDev('m_vegetables')).values()[0]
        _avg_std.m_sweets     = Experiment.objects.filter(m_sweets__isnull=False).aggregate(StdDev('m_sweets')).values()[0]
        _avg_std.m_fruits     = Experiment.objects.filter(m_fruits__isnull=False).aggregate(StdDev('m_fruits')).values()[0]
        #_avg_std.m_stages     = Experiment.objects.filter(m_stages__isnull=False).aggregate(StdDev('m_stages')).values()[0]
        _avg_std.m_positives  = Experiment.objects.filter(m_positives__isnull=False).aggregate(StdDev('m_positives')).values()[0]
        _avg_std.m_salties    = Experiment.objects.filter(m_salties__isnull=False).aggregate(StdDev('m_salties')).values()[0]
        
        _avg_std.save()
    
    except Exception as e:
            
            logger.error("Error computing new stats, {}".format(e))
    


def generate_pdf(experiment):

    # This is a demo of creating a pdf file with several pages.
    
    import datetime
    from matplotlib.backends.backend_pdf import PdfPages
    import matplotlib.pyplot as plt
    from os.path import join
    from django.conf import settings
    from django.db.models import Avg, StdDev
    from ..main.models import Experiment, Aggregation
    from django.core.files.storage import default_storage as storage
    
    logger.info("Generating PDF file")
    
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
    
    ind = arange(len(_avg))  # the x locations for the groups
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
    
    # Storing with the
    fname = experiment.subject.code+".png"
    fh    = storage.open(fname, "w")
    plt.savefig(fh)
    fh.close()
    
    return fname


def generate_new_pdf(experiment):

    # This is a demo of creating a pdf file with several pages.
    
    import datetime
    from numpy import sort, arange, append
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    from matplotlib.image import BboxImage,imread
    from matplotlib.transforms import Bbox
    from matplotlib._png import read_png
    from matplotlib.offsetbox import AnnotationBbox, OffsetImage
    from matplotlib import gridspec
    import matplotlib.ticker as ticker
    import matplotlib.patches as patches
    
    from os.path import join
    from django.conf import settings
    from django.db.models import Avg, StdDev
    from ..main.models import Experiment, Aggregation
    from django.core.files.storage import default_storage as storage
    from django.contrib.staticfiles.templatetags.staticfiles import static
    import urllib2

    logger.info("Generating PDF file")
    
    
    # Parameters
    
    _icons      = ['objects.png', 'vegetables.png', 'sweets.png', 'fruit.png', 'sets.png', 'salties.png']
    _colors     = ['#FFD136', '#A1D5D4', '#4788AE', '#D4516D', '#DD8907', '#86B469']
    _color_gray = '#D9D9D9'
    _grid_gray  = '#999999'
    
    _bar_widtgh_inch      = 0.695
    _bar_separation_inch  = 0.512
    
    _fig_width_inch  = 11.6
    _fig_height_inch = 9.2
    
    _nticks          = 4
    
    # ------------------------
    #     Data
    # ------------------------
     
    _std = Aggregation.objects.get(operation="StdDev").get_array()
    _all = Aggregation.objects.get(operation="Avg").get_array()
    _user = experiment.get_array()
    
    if None in _user:
        _idn = _user.index(None)
        _all = _all[0:_idn]
        _std = _std[0:_idn]
        _user = _user[0:_idn]
    
    ind = arange(len(_user))
    
    def grow(val, perc):
        return val + val/100.0*perc
    
    def shrink(val, perc):
        return val - val/100.0*perc
    
    logger.info("A")
    # Figure
    # ------------
    
    fig = plt.figure(num=None, figsize=(_fig_width_inch, _fig_height_inch), dpi=600, facecolor='w')
    gs  = gridspec.GridSpec(2, 1, height_ratios=[9, 2]) 
    
    
    # Limits
    # ------------
    _xborder   = 0.5
    #ymin, ymax = (shrink(min(_user), 20), grow(ymax, max(_user)))
    ymin, ymax = (settings.PLOT_DATA['ymin'], settings.PLOT_DATA['ymax'])
    xmin, xmax = [-_xborder, len(_colors)+_xborder]
    
    # Plotting
    # ------------
    ax = plt.subplot(gs[0])
    
    # Plot data
    for i in range(len(_user)):
        p = patches.Rectangle((i+0.125, 0), 0.75, _all[i], fill=True, transform=ax.transData, lw=0, facecolor=_color_gray, alpha=0.75)
        ax.add_patch(p)
        
        # New cases
        p = patches.Rectangle((i+0.25, 0), 0.5, _user[i], fill=True, transform=ax.transData, lw=0, facecolor=_colors[i], alpha=1.0)
        ax.add_patch(p)
    
    logger.info("B")
      
    # Spines
    # ------------
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color(_grid_gray)
    
    # Ticks
    # ------------
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    ax.tick_params(axis='x', colors=_grid_gray)
    ax.tick_params(axis='y', colors=_grid_gray)
    
    ax.yaxis.set_ticks(sort(append([0], arange(ymin, ymax+0.1, (ymax-ymin)/_nticks))))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
    ax.xaxis.set_ticks([])  
    
                     
    # Grid
    # ------------
    ax.grid(axis = 'y', color =_grid_gray, linestyle='-')
    ax.set_axisbelow(True)
    ax.axhline(0, color=_grid_gray)
    
    ax.set_ylabel("Indice di interesse", fontsize=20, color=_color_gray)
    
    
    # Limits
    # ------------
    ax.set_ylim(ymin, ymax)
    ax.set_xlim(xmin, xmax)
    
    # Sub chart
    # ------------
    
    
    ax1 = plt.subplot(gs[1])
    ax1.set_ylim(ymin, ymax)
    ax1.set_xlim(xmin, xmax)
    
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    
    ax1.yaxis.set_ticks_position('none')
    ax1.xaxis.set_ticks_position('none')
    
    ax1.yaxis.set_ticks([])
    ax1.xaxis.set_ticks([])
    
    # Icons
    # ------------
    _arts_to_keep = []
    for i in range(len(_icons)):
        
        if settings.DEBUG:
            _url     = "http://localhost:8000"+static("resources/"+_icons[i])
        else:
             _url     = static("resources/"+_icons[i])
        
        fimg     = urllib2.urlopen(_url)
        img1     = read_png(fimg)
        imagebox = OffsetImage(img1, zoom=1.0)
        
        xy       = [i+0.5, 0] # coordinates to position this image
         
        ab       = AnnotationBbox(imagebox, xy, xybox=(00., 10.), frameon=False, xycoords='data', boxcoords="offset points", annotation_clip=True)                                  
        ax1.add_artist(ab)
     
        _arts_to_keep.append(imagebox)
    
    logger.info("D")
    
#     plt.tight_layout()
#     plt.draw()
#     
    # Storing with the
    fname = experiment.subject.code+".pdf"
    fh    = storage.open(fname, "w")
    fig.savefig(fh, format='pdf')
    fh.close()
    