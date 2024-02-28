from rest_framework import serializers
from plugins import PaymentType, BasePaymentSerializer
from .api import group_exists, get_group, get_user_info
import sys
class PPMSPaymentSerializer(BasePaymentSerializer):
    ppms_email= serializers.CharField(required=False)
    account = serializers.CharField(required=False)
    display = serializers.SerializerMethodField(read_only=True)
    group = serializers.DictField(read_only=True)
    user_info = serializers.DictField(read_only=True)
    def get_display(self, obj):
        return {'PPMS Email/Login': obj.get('ppms_email',''), 'Financial Account': obj.get('account', 'not specified')}
    # def validate(self, data):
    #     pi_email = data.get('pi_email', None)
    #     if not pi_email:
    #         raise serializers.ValidationError({"pi_email":"PPMS PI Email is required."})
    #     self.group = get_group(self._settings, pi_email)
    #     if not self.group:
    #         raise serializers.ValidationError({"pi_email":"Group account with PI login '{0}' does not exist in PPMS.".format(pi_email)})
    #     return data
    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        ppms_email = data.get('ppms_email', data)
        if not ppms_email:
            raise serializers.ValidationError({"ppms_email":"PPMS Email is required."})
        if ppms_email not in [self._submission_data.get('email'), self._submission_data.get('pi_email')]:
            raise serializers.ValidationError({"ppms_email":"PPMS Email must match either submitter or PI email."})
        try:
            user_info = get_user_info(self._settings, ppms_email)
        except Exception as e:
            raise serializers.ValidationError({"ppms_email":"An error has occured trying to confirm the PPMS email address.  Error: {}".format(str(e))})
        # raise Exception(user_info)
        if not user_info:
            raise serializers.ValidationError({"ppms_email":"PPMS account with email '{0}' does not exist in PPMS.".format(ppms_email)})
        data['user_info'] = user_info.pop()
        data['ppms_email'] = ppms_email
        try:
            data['group'] = get_group(self._settings, data['user_info'].get('GroupPIUnitLogin')).pop()
        except Exception as e:
            raise serializers.ValidationError({"ppms_email":"An error has occured trying to retrieve the PPMS group.  Error: {}".format(str(e))})
        return data# super().to_internal_value(data)

class PPMSPaymentType(PaymentType):
    id = 'PPMSPaymentType'
    name = 'PPMS Payment'
    serializer = PPMSPaymentSerializer