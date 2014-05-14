from django.core.management.base import NoArgsCommand
from nextmng.common import logger
import os
from nextmng.common.importer import import_depot

class Command(NoArgsCommand):
    
    def handle_noargs(self, **opts):
    
        import_depot()        
        
        
        