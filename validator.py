from rest_framework import serializers
from dnaorder.models import PI
from .utils import get_or_create_pi

def validate_submission(plugin, data, serializer):
    email = data.get('pi_email')
    pi = PI.get_pi(email)
    if not pi:
        lab = getattr(serializer, '_lab', None)
        if lab:
            settings = lab.get_plugin_settings_by_id(plugin.ID, private=True, institution=True)
            pi = get_or_create_pi(settings, email)
            if not pi:
                raise serializers.ValidationError({'pi_email':f'No group has been registered in the system with the email "{email}", lab ({serializer._lab.name}).'})
    serializer.instance.pi = pi
    return data