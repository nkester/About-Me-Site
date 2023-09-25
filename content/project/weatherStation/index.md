---
title: Home Weather Station
summary: We live in Italy but our family does not. We thought they may be interested to get real-time information about the weather near us. This was a chance to expose my kids to the basics about coding, networks, databases, sensors, and cloud tools. It was ambitious but I wanted the experience to be tangilble and rewarding.  
tags:
  - In Development
  - With Kids
  - Raspberry Pi
  - Home Projects
date: '2023-08-07T00:00:00Z'

# Optional external URL for project (replaces project detail page).
external_link: ''

image:
  caption: Crushing Keys
  focal_point: Smart

links:
  - icon: github
    icon_pack: fab
    name: Code
    url: https://github.com/nkester/Kester-Weather-Station
  - icon: github
    icon_pack: fab
    name: Viz
    url: /uploads/sites/WeatherStation.html
url_code: ''
url_pdf: ''
url_slides: ''
url_video: ''

# Slides (optional).
#   Associate this project with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides: "" #example
---

## Why

...Why not? 

Through this project the kids can learn basics of sensors in the real world, wireless networks, databases, and the power of cloud technologies. At the end, they will be able to point their friends and family from around the world to a website to see how hot it is, how much rain we've gotten, the air quality, etc. near their home. 

## High Level Diagram  

The diagram below show, at a high level, what we want to set up. Essentially, we want to have one SEEED sensor (to start), the 8-in-1 Weather sensor, that is connected to a computer inside the house and communicates over a Long Range Wide Area Network (LoRaWAN). The sensor will connect to a LoRaWAN gateway that will convert the wireless communication into a digital, computer readable format. That will then connect to a ChirpStack server on our local Raspberry Pi computer. This ChirpStack server will feed the data recieved from the sensor into a PostgreSQL Database stored on the Raspberry Pi. The Raspberry Pi will then push that data periodically to a Google Cloud Platform (GCP) managed database (likely PostgreSQL initially for ease of use). Finally, we will create a static web-page using Quarto and Observable JS, deployed to Google Firebase to query the GCP database and chart the results.

![alt text](SeeedSolutionDiagram.png "Seeed Solution Diagram")  