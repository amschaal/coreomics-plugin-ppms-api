from django.db import models
from dnaorder.models import PI, Institution, PIInstitution

class PPMSGroup(models.Model):
    ppms_id = models.BigIntegerField(null=True, unique=True)
    imported = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=75, unique=True, primary_key=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=75)
    name = models.CharField(max_length=75)
    department = models.CharField(max_length=100, null=True)
    institution = models.CharField(max_length=100, null=True)
    meta = models.JSONField(default=dict) # store addional data such as import data
    pi = models.OneToOneField(PI, null=True, on_delete=models.CASCADE)
    group_map = {}
    groups = {}
    @staticmethod
    def get_group_map(institution: Institution):
        groups = PPMSGroup.get_groups(institution)
        group_map = {}
        for g in groups:
            group_map[g['head'].strip().lower()] = g
        PPMSGroup.group_map[institution.id] = group_map
        return group_map
    @staticmethod
    def get_groups(institution: Institution):
        if institution.id in PPMSGroup.groups:
            return PPMSGroup.groups[institution.id]
        from . import api
        from .plugin import PPMSPlugin
        settings = institution.get_plugin_settings_by_id(PPMSPlugin.ID, private=True)
        groups = api.get_groups(settings)
        PPMSGroup.groups[institution.id] = groups
        return groups
    def create_pi(self):
        if not self.pi:
            institution = PIInstitution.objects.filter(name__iexact=self.institution[:75]).first()
            if not institution:
                institution = PIInstitution.objects.create(name=self.institution[:75])
            self.pi = PI.objects.create(email=self.email, first_name=self.first_name.strip(), last_name=self.last_name.strip(), department=self.department[:75], institution=institution, meta={'ppms':self.meta})
            self.save()
        return self.pi
    @staticmethod
    def create_group(group: dict, save=False):
        name_parts = group['name'].split(',')
        if len(name_parts) == 2:
            last_name, first_name = name_parts
        else:
            last_name = group['name']
            first_name = ''
        g = PPMSGroup(ppms_id=group['id'], email=group['head'], first_name=first_name[:50], last_name=last_name[:75], name=group['name'][:75], department=group['department'][:75], institution=group['institution'][:75], meta=group)
        if save:
            g.save()
        return g
    # def map_pi(self):
    #     if self.pi:
    #         return self.pi
