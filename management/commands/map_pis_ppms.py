from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from dnaorder.models import PIInstitution, Submission, Institution, PI
from plugins.ppms import api
from plugins.ppms.models import PPMSGroup
from plugins.ppms.utils import import_ppms_group

class Command(BaseCommand):
    help = 'Map submissions to pis based on submission.pi_email. Can accept the number of days to go back.'
    pi_map = None
    existing_pi_map = None
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Number of days to subtract from now (default: 7)'
        )

    def handle(self, *args, **options):
        days = options['days']
        since_date = datetime.now() - timedelta(days=days)
        self.bulk_map(since=since_date)

    def bulk_map(self, since):
        # Create map of existing PIs
        existing_pis = {}
        for pi in PI.objects.all():
            existing_pis[pi.email.lower()] = pi
        existing_groups = {}
        for group in PPMSGroup.objects.all():
            existing_groups[group.email.lower()] = group

        # For bulk updating    
        submissions = []
        unmapped = []

        # for i in Institution.objects.all():
            # pi_map = PPMSGroup.get_group_map(i)

        for s in Submission.objects.filter(pi_email__contains='@', pi__isnull=True):
            email = s.pi_email.strip().lower()
            pi = existing_pis.get(email)
            if not pi and email in existing_groups:
                pi = existing_groups[email].create_pi()
            # If no PI match try checking pi email pulled from the PPMS payment plugin if it exists. 
            if not pi:
                try:
                    email = s.payment['user_info']['GroupPIUnitLogin'].strip().lower()
                    pi = existing_pis.get(email)
                    if not pi and email in existing_groups:
                        pi = existing_groups[email].create_pi()
                except Exception as e:
                    # print ('Exception', e)
                    pass
            if pi:
                s.pi = pi
                submissions.append(s)

                # else: #This is currently being done in the import_ppms_groups, which should be run right before this.  No need to import them on an individual basis
                    # ppms_pi = pi_map.get(email)
                    # if ppms_pi:
                    #     ppms_group = import_ppms_group(email, ppms_pi)
                    #     existing_pis[email] = ppms_group.pi
                    #     s.pi = ppms_group.pi
                    #     s.save()
            else:
                unmapped.append(email)
        Submission.objects.bulk_update(submissions, ['pi'], batch_size=100)
        self.stdout.write(self.style.SUCCESS(f'Updated {len(submissions)} submission PIs.  Unable to update {len(unmapped)}'))
        self.stdout.write(', '.join(unmapped))