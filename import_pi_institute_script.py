import json
from dnaorder.models import PI, PIInstitution, Submission

# first curl groups from PPMS into ppms_groups.json

with open('ppms_groups.json', 'r') as f:
    groups = json.load(f)

# Create lookup by pi email
pis = {}
for g in groups:
    pis[g['head'].strip().lower()] = g

def import_pi(submission, pi_mapping):
    email = submission.pi_email.strip().lower()
    pi = PI.objects.filter(email = email).first()
    if pi:
        submission.pi = pi
        submission.save()
    else:
        ppms_pi = pi_mapping.get(email)
        if ppms_pi:
            institution = PIInstitution.objects.filter(name__iexact=ppms_pi['institution']).first()
            if not institution:
                institution = PIInstitution.objects.create(name=ppms_pi['institution'][:75])
            pi = PI.objects.create(email=email, first_name=submission.first_name, last_name=submission.last_name, phone=submission.phone, department=ppms_pi['department'][:75], institution=institution, meta={'ppms':ppms_pi})
            submission.pi = pi
            submission.save()
        else:
            print(f"Could not map {email}")


for s in Submission.objects.filter(pi_email__contains='@', pi__isnull=True):
    import_pi(s, pis)
