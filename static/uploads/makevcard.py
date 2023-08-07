"""
This little script can generate a valid .vcf (vCard). It will ask you to fill
in some details and write the vcf-file.
"""

# Contact information
first_name = 'Neil'
last_name = 'Kester'
email = 'neilkester@yahoo.com'
company = 'U.S. Army'
title = 'Senior Operations Research / Systems Analyst'
address = 'Vicenza, Italy'
vcf_file = './static/uploads/neil.vcf'

def make_vcard(
        first_name,
        last_name,
        company,
        title,
        address,
        email):
    address_formatted = ';'.join([p.strip() for p in address.split(',')])
    return [
        'BEGIN:VCARD',
        'VERSION:2.1',
        f'N:{last_name};{first_name}',
        f'FN:{first_name} {last_name}',
        f'ORG:{company}',
        f'TITLE:{title}',
        f'EMAIL;PREF;INTERNET:{email}',
        f'ADR;WORK;PREF:;;{address_formatted}',
        f'REV:1',
        'END:VCARD'
    ]

def write_vcard(f, vcard):
    with open(f, 'w') as f:
        f.writelines([l + '\n' for l in vcard])


vcard = make_vcard(first_name, last_name, company, title, address, email)
write_vcard(vcf_file, vcard)