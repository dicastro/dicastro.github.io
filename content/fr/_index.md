---
# Leave the homepage title empty to use the site title
title: ""
date: 2025-11-24
type: landing

design:
  # Default section spacing
  spacing: "6rem"

sections:
  - block: resume-biography-3
    content:
      # Choose a user profile to display (a folder name within `content/authors/`)
      username: admin
      text: ""
      button:
        text: Télécharger CV
        url: uploads/cv-diego-castro-viadero-fr.pdf
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
      username: admin
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
      title: Compétences
      username: admin
    design:
      spacing:
        padding: [1rem, 0, 1rem, 0]
      show_skill_percentage: false
      columns: 5
      css_class: "mx-auto custom-resume-skills-width"
  - block: resume-awards
    id: accomplishments
    content:
      title: Réalisations
      username: admin
    design:
      spacing:
        padding: [1rem, 0, 1rem, 0]
      css_class: "mx-auto custom-resume-awards-width"
---
