from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from dnaorder.models import PIInstitution, Submission, Lab, PI
from plugins.ppms import api
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
        # for s in Submission.objects.filter(updated__gte=since_date, pi_email__contains='@', pi__isnull=True):
        #     s.map_pi()

    def get_pi_map(self, settings):
        if self.pi_map:
            return self.pi_map
        groups = api.get_groups(settings)
        pis = {}
        for g in groups:
            pis[g['head'].strip().lower()] = g
        self.pi_map = pis
        return self.pi_map

    def bulk_map(self, since):
        # Create map of existing PIs
        existing_pis = {}
        for pi in PI.objects.all():
            existing_pis[pi.email.lower()] = pi

        # For bulk updating    
        submissions = []
        unmapped = []

        settings = None
        for lab in Lab.objects.all():
            settings = api.get_lab_settings(lab)
            if settings:
                break
        
        pi_map = self.get_pi_map(settings)

        for lab in Lab.objects.all():
            print(lab, settings)
            for s in Submission.objects.filter(pi_email__contains='@', lab=lab, pi__isnull=True):
                email = s.pi_email.strip().lower()
                pi = existing_pis.get(email)
                if pi:
                    s.pi = pi
                    submissions.append(s)
                else:
                    ppms_pi = pi_map.get(email)
                    if ppms_pi:
                        ppms_group = import_ppms_group(email, ppms_pi)
                        # institution = PIInstitution.objects.filter(name__iexact=ppms_pi['institution']).first()
                        # if not institution:
                        #     institution = PIInstitution.objects.create(name=ppms_pi['institution'][:75])
                        # pi = PI.objects.create(email=email, first_name=s.pi_first_name, last_name=s.pi_last_name, phone=s.pi_phone, department=ppms_pi['department'][:75], institution=institution, meta={'ppms':ppms_pi})
                        existing_pis[email] = ppms_group.pi
                        s.pi = ppms_group.pi
                        s.save()
                    else:
                        unmapped.append(email)
        Submission.objects.bulk_update(submissions, ['pi'], batch_size=100)
        self.stdout.write(self.style.SUCCESS(f'Updated {len(submissions)} submission PIs.  Unable to update {len(unmapped)}'))