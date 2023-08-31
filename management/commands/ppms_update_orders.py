from django.core.management.base import BaseCommand, CommandError
from dnaorder.models import Submission, Lab
from plugins.ppms import api
class Command(BaseCommand):
    help = 'update orders'
    def add_arguments(self, parser):
        pass
        # parser.add_argument('test', nargs='+', type=int)
    def handle(self, *args, **options):
        # raise CommandError('Poll "%s" does not exist' % poll_id)
        all_submissions = []
        for lab in Lab.objects.filter(plugins__ppms__enabled=True):
            self.stdout.write(str(lab))
            settings = api.get_lab_settings(lab)
            submissions = Submission.objects.filter(lab=lab, plugin_data__ppms__order_details__contains=[{'paid':False,'cancelled':False}])
            ids = [s.id for s in submissions]
            orderrefs = []
            for s in submissions:
                orderrefs += s.plugin_data['ppms']['orders']
            self.stdout.write('{}'.format(', '.join(ids)))
            self.stdout.write('{}'.format(', '.join(orderrefs)))
            if orderrefs:
                order_details = api.search_orders(settings, order_ids=orderrefs)
                ordermap = {o['orderref']: o for o in order_details}
            for s in submissions:
                s.plugin_data['ppms']['order_details'] =  [ordermap[o] for o in s.plugin_data['ppms']['orders']]
                # s.save()  # inefficient, do in bulk
                all_submissions.append(s)
            self.stdout.write(self.style.SUCCESS('Orders updated!'))
        Submission.objects.bulk_update(all_submissions, ['plugin_data'], batch_size=100)