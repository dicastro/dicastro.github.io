---
# Leave the homepage title empty to use the site title
title: ""
date: 2025-11-24
type: landing
description: |
  Personal website of Diego Castro Viadero, Software Engineer with extensive experience. Specialist in delivering solid solutions to complex problems, with a career combining the rigor of large multinationals and the agility of startups.

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: me
      text: ""
      button:
        text: Download CV
        url: /uploads/cv-diego-castro-viadero-en.pdf
      headings:
        about: ""
        education: ""
        interests: ""
    design:
      spacing:
        padding: [0, 0, 0, 0]
      # Apply a gradient background
      css_class: "hbx-bg-gradient text-justify custom-resume-biography-width"
      # Avatar customization
      avatar:
        size: medium # Options: small (150px), medium (200px, default), large (320px), xl (400px), xxl (500px)
        shape: circle # Options: circle (default), square, rounded
  - block: resume-experience
    id: experience
    content:
      username: me
    design:
      spacing:
        padding: [2rem, 0, 1rem, 0]
      # Hugo date format
      date_format: "January 2006"
      # Education or Experience section first?
      is_education_first: false
      css_class: "mx-auto custom-resume-experience-width"
  - block: resume-skills
    id: skills
    content:
      title: Skills
      username: me
    design:
      spacing:
        padding: [1rem, 0, 1rem, 0]
      show_skill_percentage: false
      columns: 5
      css_class: "mx-auto custom-resume-skills-width"
  - block: resume-awards
    id: accomplishments
    content:
      title: Accomplishments
      username: me
    design:
      spacing:
        padding: [1rem, 0, 1rem, 0]
      css_class: "mx-auto custom-resume-awards-width"
---
