from django.db import models
from dnaorder.models import PI, Institution

class PPMSGroup(models.Model):
    ppms_id = models.BigIntegerField(null=True)
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
    @staticmethod
    def get_group_map(institution):
        if institution.id in PPMSGroup.group_map:
            return PPMSGroup.group_map[institution.id]
        from . import api
        from .plugin import PPMSPlugin
        settings = institution.get_plugin_settings_by_id(PPMSPlugin.ID, private=True)
        groups = api.get_groups(settings)
        group_map = {}
        for g in groups:
            group_map[g['head'].strip().lower()] = g
        PPMSGroup.group_map[institution.id] = group_map
        return group_map
    



