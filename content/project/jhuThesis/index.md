---
title: JHU Systems Engineering Masters Thesis
summary: "Applying Trade-Space Analysis to Modeling and Simulations as a Service (MSaas): A Study in Applying Established Systems Engineering Methodologies in a Novel Setting" 
tags:
  - analytics
date: '2021-05-13T00:00:00Z'

# Optional external URL for project (replaces project detail page).
external_link: ''

links:
  - icon: file-powerpoint
    icon_pack: fa
    name: Final Presentation
    url: /uploads/projects/jhuThesis/FinalThesisPresentation.pdf
  - icon: book
    icon_pack: fas
    name: Final Paper
    url: uploads/projects/jhuThesis/FinalThesisPaper.pdf
  - icon: github
    icon_pack: fab
    name: Custom Thesis R Package {modSim}
    url: https://github.com/nkester/JHU-Thesis-ModSim-Package
  - icon: github
    icon_pack: fab
    name: Custom Thesis Helm Chart - Kubernetes Deployment
    url: https://github.com/nkester/JHU-Thesis-Helm-Chart
  - icon: github
    icon_pack: fab
    name: Thesis Analysis Scripts {R}
    url: https://github.com/nkester/JHU-Thesis-Analysis
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

## Abstract

Techniques of trade-space analysis have been successfully employed for decades to support acquisition decisions. Likewise, large scale discrete event combat simulations have been successfully employed for a similar period to explore performance and effectiveness of systems and concepts considered in those trade-space analyses. Recently, great progress has been made breaking the paradigm of executing large and complex combat simulations as monolithic software systems run on local machines and primarily in serial. Teams like the North Atlantic Treaty Organization Science and Technology Office’s (NATO STO) Modeling and Simulation Group have developed a novel way of serving these simulations as decoupled microservices in the cloud. They refer to this as Modeling and Simulation as a Service (MSaaS). The purpose of this paper is to demonstrate the suitability of integrating cloud based analytic resources into the immerging MSaaS field. It describes the composition of these cloud based analytic resources, extends NATO’s existing MSaaS Reference Architecture to include these resources, and executes a simple trade-space design of experiments to demonstrate its utility.

## Background

North Atlantic Treaty Organization (NATO) Science and Technology Office (STO) Modeling and Simulation Group (MSG) 164 defines MSaaS in the following way:  


> An enterprise-level architecture that promotes modularity, loose coupling, agility, and resuability of Modeling & Simulation resources for different suppliers by making them available on-demand to a large number of disparate users in order to reduce the cost and time for implementating Modeling & Simulation capability to improve operational effectiveness." 

Of the NATO MSaaS user communities, those focused on training and operations currently dominate its development priorities. That focus is appropriate as it shows value to leaders in those nations and enjoys a larger user base.

The identified problem this research intends to address is that NATO’s MSaaS lacks an integrated analytic framework capable of supporting concept development and analytic support to procurement decisions. It should be said that these analytic capabilities could benefit the training and operations communities as well as the analytic community.

## Study Purpose

Given that context and the initially described gap, the purpose of this study is to determine if Modeling and Simulation as a Service (MSaaS), a novel approach to traditional Modeling and Simulation solutions, is suitable for conducting trade-space analyses. These trade-space analyses support systems engineering questions during the requirements analysis and architectural design technical processes of the US DoD Systems Engineering Process.

## Study Hypothesis

he author’s hypothesis is that a NATO MSaaS instance, integrated with an analytic environment, is suitable to support trade-space analysis by measuring the robustness of military systems.