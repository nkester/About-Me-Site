---
# An instance of the Contact widget.
widget: contact

# This file represents a page section.
headless: true
active: true

# Order that this section appears on the page.
weight: 130

title: Contact
subtitle: 

content:
  # Automatically link email and phone or display as text?
  autolink: true

  # Email form provider
#  form:
#    provider: netlify
#    formspree:
#      id:
#    netlify:
      # Enable CAPTCHA challenge to reduce spam?
#      captcha: false

  # Contact details (edit or remove options as required)
 # email: neilkester@yahoo.com
  address:
    city: Richmond
    region: VA
    postcode: '23219'
    country: USA
    country_code: US
  coordinates:
    latitude: '37.536361'
    longitude: '-77.463139'
#  directions: Enter Building 1 and take the stairs to Office 200 on Floor 2
#  office_hours:
#    - 'Monday 10:00 to 13:00'
#    - 'Wednesday 09:00 to 10:00'
  #appointment_url: 'https://calendly.com'
  contact_links:
    - icon: address-card
      icon_pack: fas
      name: Download my vCard
      link: 'uploads/neil.vcf'
    - icon: whatsapp
      icon_pack: fab
      name: 'WhatsApp: +1 804 245 0085'
    - icon: briefcase
      icon_pack: fas
      name: Work Email
      link: mailto:neil.e.kester.mil@army.mil
    - icon: house
      icon_pack: fas
      name: Personal Email
      link: mailto:neilkester@yahoo.com
    - icon: linkedin
      icon_pack: fab
      name: LinkedIn
      link: https://www.linkedin.com/in/neilkester
    - icon: images
      icon_pack: fas
      name: Photo Portfolio
      link: https://photoportfolio.nkester.com/      
design:
  columns: '1'
---

{{< icon name="download" pack="fas" >}}Click to download my {{< staticref "uploads/neil.vcf" "newtab" >}}virtual contact card{{< /staticref >}}