from dnaorder.models import PI, PIInstitution
from .models import PPMSGroup
from .api import get_group, get_user_info

def map_submission_pi(submission, save=True):
    print('map_submission_pi')
    from .plugin import PPMSPlugin
    settings = submission.lab.get_plugin_settings_by_id(PPMSPlugin.ID, private=True, institution=True)
    pi = get_or_create_pi(settings, submission.pi_email)
    submission.pi = pi
    if save:
        submission.save()
    return pi

def get_pi_data(settings, email):
    data = {}
    try:
        user_info = get_user_info(settings, email)
        user = user_info.pop()
        print(user)
        for k, v in user.items():
            if k:
                data[k.lower().replace(' ', '')] = v
    except Exception as e:
        print('user info exception', e)
    try:
        groups = get_group(settings, email) #It might actually be necessary to get the group using the data from get_user_info
        group = groups.pop()
        print(group)
        for k, v in group.items():
            if k:
                data[k.lower().replace(' ', '')] = v
    except Exception as e:
        print('get_group excetpion', e)
    return data if data else None

def get_or_create_pi(settings, email):
    email = email.strip().lower()
    pi = PI.objects.filter(email__iexact = email).first()
    if pi:
        return pi
    data = get_pi_data(settings, email)
    if not data or 'institution' not in data:
        return None

    institution = PIInstitution.objects.filter(name__iexact=data['institution']).first()
    if not institution:
        institution = PIInstitution.objects.create(name=data['institution'][:75])
    if 'firstname' in data:
        first_name = data['firstname']
        last_name = data['lastname']
    else:
        last_name, first_name = data['unitname'].split(',')
    pi = PI.objects.create(email=email, first_name=first_name.strip(), last_name=last_name.strip(), department=data['department'][:75], institution=institution, meta={'ppms':data})
    return pi

def import_ppms_group(email, groups_list_dict):
    institution = PIInstitution.objects.filter(name__iexact=groups_list_dict['institution']).first()
    if not institution:
        institution = PIInstitution.objects.create(name=groups_list_dict['institution'][:75])
    if ', ' in groups_list_dict['name']:
        last_name, first_name = groups_list_dict['name'].split(', ')
    else:
        last_name = groups_list_dict['name']
        first_name = ''
    pi = PI.objects.create(email=email, first_name=first_name, last_name=last_name, department=groups_list_dict['department'][:75], institution=institution, meta={'ppms':groups_list_dict})
    return PPMSGroup.objects.create(ppms_id=groups_list_dict['id'], email=email, first_name=first_name, last_name=last_name, name=groups_list_dict['name'], department=groups_list_dict['department'][:75], institution=groups_list_dict['institution'][:75], meta=groups_list_dict, pi=pi)
