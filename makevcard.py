"""
This little script can generate a valid .vcf (vCard). It will ask you to fill
in some details and write the vcf-file.  

vCard specifications are here: https://www.rfc-editor.org/rfc/rfc6350#section-6.2.1
Run this script with: 
"""

# Contact information
first_name = 'Neil'
last_name = 'Kester'
email_home = 'neilkester@yahoo.com'
email_work = 'neil.e.kester.mil@army.mil'
company = 'U.S. Army'
title = 'Senior Operations Research / Systems Analyst'
address = 'Vicenza, Italy'
gender = 'M'
nickname = 'Neil'
name_prefix = 'Mr.'
name_suffix = 'PMP'
work_phone = '+39-0444-109-5021'
language_pref = 'en'
work_role = 'Division Chief'
personal_url = 'https://about.nkester.com'
photo_uri = 'https://www.about.nkester.com/uploads/vcard-photo.jpeg'
vcf_file = './static/uploads/neil.vcf'

def make_vcard(
        first_name,
        last_name,
        name_prefix,
        name_suffix,
        nickname,
        photo_uri,
        gender,
        company,
        title,
        personal_url,
        work_phone,
        email_work,
        email_home,
        language_pref,
        work_role,
        address):
    address_formatted = ';'.join([p.strip() for p in address.split(',')])
    return [
        'BEGIN:VCARD',
        'VERSION:4.0',
        f'N:{last_name};{first_name};{name_prefix};{name_suffix}', # Family Name, Given Name, Additional Names, Honorific Prefix, Honorific Suffix
        f'FN:Mr. {first_name} {last_name}\, {name_suffix}', #Required, the name of the vCard object
        f'NICKNAME:{nickname}',
        f'PHOTO:{photo_uri}',
        f'GENDER:{gender}',
        f'ORG:{company}',
        f'TITLE:{title}',
        f'URL:{personal_url}',
        f'TEL;VALUE=uri;PREF=1;TYPE="voice,work":tel:{work_phone}',
        f'EMAIL;TYPE=work:{email_work}',
        f'EMAIL;TYPE=home:{email_home}',
        f'ADR;WORK;PREF:;;{address_formatted}',
        f'LANG;TYPE=home:{language_pref}',
        f'ROLE:{work_role}',
        f'REV:2',
        'END:VCARD'
    ]

def write_vcard(f, vcard):
    with open(f, 'w') as f:
        f.writelines([l + '\n' for l in vcard])


vcard = make_vcard(first_name,last_name,name_prefix,name_suffix,nickname,photo_uri,gender,company,title,personal_url,work_phone,email_work,email_home,language_pref,work_role,address)
write_vcard(vcf_file, vcard)