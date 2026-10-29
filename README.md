# Cine De Riesgo

Current bilingual website migrated from the Sites version, source commit f7e3aa8f21cb5c4304089d02aa80d79ef1d1938f.

## Deploy on Vercel

Import this GitHub repository. Framework: Other. Root directory: repository root. Output directory: `dist`. No installation or build command is needed: the generated static site is committed. `vercel.json` supplies these settings.

The Spanish homepage is `/`; English is `/en/`. Directory URLs use trailing slashes. All images, fonts, styles, and scripts are self-hosted. No credentials or Sites-specific hosting configuration are required.

## Update content

Use Python 3 to regenerate pages after editing source:

```sh
python3 build.py
python3 -m http.server 4173 --directory dist
```

Review http://localhost:4173, then commit both source and regenerated `dist` pages. Vercel publishes the connected production branch automatically once Git integration is configured.

- `content.json`: original film and company content.
- `microdrama-additions.json`: new microdrama content, poster references, and provenance.
- `press.py`: press links and publication dates.
- `redesign.py`: homepage carousel, microdrama gallery, and detail layouts.
- `i18n.py`: Spanish/English translations.
- `build.py`: shared page layout, biography, contact, and film formatting.
- `dist/redesign.css`, `dist/style.css`, `dist/app.js`: styles and browser interactions; edited directly.

The homepage rotates Agent of Shadows, Marco Polo, and CVALT after six idle seconds. Dot navigation, touch scrolling, and reduced-motion handling are included.

## Current functionality

56 pages: 28 per language. Includes four films, 17 microdramas, Press, About, Contact, and legal information. The contact form prepares an email in the visitor's mail application; it does not send server-side. There is no connected editing dashboard in this version.

## Domain cutover

Test the Vercel deployment before pointing cinederiesgo.com and www.cinederiesgo.com to it. Use the DNS records Vercel provides; preserve email-related MX/TXT records. The existing Sites site and original domain have not been changed by preparing this repository.
