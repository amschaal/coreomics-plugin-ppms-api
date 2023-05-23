from rest_framework import serializers
from plugins import PaymentType, BasePaymentSerializer
from .api import group_exists, get_group
import sys
class PPMSPaymentSerializer(BasePaymentSerializer):
    pi_email= serializers.CharField(required=False)
    display = serializers.SerializerMethodField(read_only=True)
    group = serializers.DictField(read_only=True)
    def get_display(self, obj):
        return {'PPMS PI Email/Login': obj.get('pi_email','')}
    # def validate(self, data):
    #     pi_email = data.get('pi_email', None)
    #     if not pi_email:
    #         raise serializers.ValidationError({"pi_email":"PPMS PI Email is required."})
    #     self.group = get_group(self._settings, pi_email)
    #     if not self.group:
    #         raise serializers.ValidationError({"pi_email":"Group account with PI login '{0}' does not exist in PPMS.".format(pi_email)})
    #     return data
    def to_internal_value(self, data):
        pi_email = data.get('pi_email', None)
        if not pi_email:
            raise serializers.ValidationError({"pi_email":"PPMS PI Email is required."})
        group = get_group(self._settings, pi_email)
        if not group:
            raise serializers.ValidationError({"pi_email":"Group account with PI login '{0}' does not exist in PPMS.".format(pi_email)})
        data['group'] = group.pop()
        return data# super().to_internal_value(data)

class PPMSPaymentType(PaymentType):
    id = 'PPMSPaymentType'
    name = 'PPMS Payment'
    serializer = PPMSPaymentSerializer