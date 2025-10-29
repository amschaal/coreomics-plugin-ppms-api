from rest_framework import serializers
from dnaorder.models import PI

def validate_submission(plugin, data, serializer):
    email = data.get('pi_email')
    pi = PI.get_pi(email)
    if not pi:
        raise serializers.ValidationError({'pi_email':f'No group has been registered in the system with the email "{email}".'})
    return data