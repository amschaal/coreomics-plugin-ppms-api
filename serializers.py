from rest_framework import serializers
from plugins import PaymentType, BasePaymentSerializer
from .api import group_exists, get_group, get_user_info
import sys
class PPMSPaymentSerializer(BasePaymentSerializer):
    ppms_email= serializers.CharField(required=False)
    display = serializers.SerializerMethodField(read_only=True)
    group = serializers.DictField(read_only=True)
    user_info = serializers.DictField(read_only=True)
    def get_display(self, obj):
        return {'PPMS Email/Login': obj.get('ppms_email','')}
    # def validate(self, data):
    #     pi_email = data.get('pi_email', None)
    #     if not pi_email:
    #         raise serializers.ValidationError({"pi_email":"PPMS PI Email is required."})
    #     self.group = get_group(self._settings, pi_email)
    #     if not self.group:
    #         raise serializers.ValidationError({"pi_email":"Group account with PI login '{0}' does not exist in PPMS.".format(pi_email)})
    #     return data
    def to_internal_value(self, data):
        ppms_email = data.get('ppms_email', None)
        if not ppms_email:
            raise serializers.ValidationError({"ppms_email":"PPMS Email is required."})
        if ppms_email not in [self._submission_data.get('email'), self._submission_data.get('pi_email')]:
            raise serializers.ValidationError({"ppms_email":"PPMS Email must match either submitter or PI email."})
        user_info = get_user_info(self._settings, ppms_email)
        # raise Exception(user_info)
        if not user_info:
            raise serializers.ValidationError({"ppms_email":"PPMS account with email '{0}' does not exist in PPMS.".format(ppms_email)})
        data['user_info'] = user_info.pop()
        data['ppms_email'] = ppms_email
        data['group'] = get_group(self._settings, data['user_info'].get('GroupPIUnitLogin')).pop()
        return data# super().to_internal_value(data)

class PPMSPaymentType(PaymentType):
    id = 'PPMSPaymentType'
    name = 'PPMS Payment'
    serializer = PPMSPaymentSerializer