from dnaorder.models import PI, PIInstitution
from .api import get_group, get_user_info

def get_or_create_pi(settings, email):
    email = email.strip().lower()
    pi = PI.objects.filter(email = email).first()
    if pi:
        return pi
    user_info = get_user_info(settings, email)
    groups = get_group(settings, email)
    if not groups or not user_info:
        return None
    user = user_info.pop()
    # PPMS is very inconsistent with these headers, so we have to clean them up
    data = {}
    for k, v in user.items():
        if k:
            data[k.lower().replace(' ', '')] = v
    group = groups.pop()
    for k, v in group.items():
        if k:
            data[k.lower().replace(' ', '')] = v
    institution = PIInstitution.objects.filter(name__iexact=data['institution']).first()
    if not institution:
        institution = PIInstitution.objects.create(name=data['institution'][:75])
    pi = PI.objects.create(email=email, first_name=data['firstname'], last_name=data['lastname'], department=data['department'][:75], institution=institution, meta={'ppms':data})
    return pi