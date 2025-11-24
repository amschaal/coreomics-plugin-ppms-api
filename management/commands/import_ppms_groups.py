from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from dnaorder.models import PIInstitution, Submission, Institution, PI
from plugins.ppms import api
from plugins.ppms.models import PPMSGroup
from plugins.ppms.utils import import_ppms_group

class Command(BaseCommand):
    help = 'Import PPMS groups.'

    def handle(self, *args, **options):
        for i in Institution.objects.all():
            ppms_groups = PPMSGroup.get_groups(i)
            print(f"{len(ppms_groups)} PPMS existing groups.")
            existing_ids = set(PPMSGroup.objects.all().values_list('ppms_id', flat=True))
            print(f"{len(existing_ids)} previously imported.")
            new_groups = []
            for group in ppms_groups:
                if group['id'] not in existing_ids:
                    try:
                        new_groups.append(PPMSGroup.create_group(group, save=False))
                    except:
                        print('Unable to import: ', group)
            groups_created = PPMSGroup.objects.bulk_create(new_groups, batch_size=100)
            print(f"{len(groups_created)} groups newly imported.")