# Free & Open Source Tools for Campaigning

A take-home resource list from the *Free & Open Source Campaigning* session at Public Interest Alberta, 2026. Curated for advocacy organizations, labour groups, non-profits, and grassroots campaigns operating in Canada.

The goal: replace extractive, surveillance-funded SaaS with tools you control, on infrastructure that lives in this country, run by people who answer to your members instead of a quarterly earnings call.

Maintained by [The Bunker Operations](https://bnkops.com). Suggestions and corrections welcome — this is a living document.

---

## The Starter Stack — Run This First

The session shipped a working stack you can clone and run on your own hardware. Two services, one `docker-compose.yml`, ten minutes from `git clone` to live URLs. The same stack PIA itself ran on n3-pia during the session.

**[git.publicinterestalberta.org/pia-starter-stack](https://git.publicinterestalberta.org/pia-starter-stack)**

Includes:
- **MkDocs Material** — your org's public knowledge base, written in markdown. Replaces Squarespace.
- **Listmonk** — newsletter and mass email. Replaces Mailchimp.

That's it. Two services, no database to set up beyond what compose handles for you, no admin wizard for the docs site. Edit `docs/*.md`, save, refresh — the site rebuilds.

If you only do one thing on this list: clone that, run `docker compose up -d`, and have your org's first sovereign service live by tonight. Issues and pull requests welcome.

### Want a desktop app for editing markdown?

The starter stack site is just markdown files in a folder. You can edit them with any text editor. If you want something purpose-built:

- **[Obsidian](https://obsidian.md)** — easiest on-ramp. Free, every OS. Not fully FOSS but the most welcoming for non-technical users.
- **[Logseq](https://logseq.com)** — fully open-source. Closer to a knowledge graph than a document editor.
- **[Joplin](https://joplinapp.org)** — fully open-source. Closer to Evernote in feel.

All three open the same `.md` files. Pick whichever fits your brain.

---

## Other Directories Worth Knowing

When the starter stack doesn't cover what you need, these are the directories to search.

- **awesome-selfhosted** — [github.com/awesome-selfhosted/awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted) and the readable mirror at [awesome-selfhosted.net](https://awesome-selfhosted.net). The canonical, community-maintained directory of self-hostable software, organized by category.
- **European Alternatives** — [european-alternatives.eu](https://european-alternatives.eu). Frames replacements by *the corporate tool you're trying to escape*, which is the question most organizers are actually asking.
- **Privacy Guides** — [privacyguides.org](https://www.privacyguides.org). Audited, regularly-updated recommendations for privacy-respecting tools, free of affiliate-driven nonsense.

---

## Replace What Your Org Already Pays For

These are concrete substitutions for tools advocacy organizations commonly use. Each entry names the corporate tool, the FOSS replacement, and what kind of effort it takes to switch.

### Email and Mass Communications

- Mailchimp / Constant Contact / Campaign Monitor → **[Listmonk](https://listmonk.app/)**. Self-hosted newsletter and mailing list manager. Fast, single binary, scales to millions of subscribers. Switching effort: moderate (need to bring your own SMTP relay).
- HubSpot / Marketo → **[Mautic](https://www.mautic.org/)**. Marketing automation, drip campaigns, lead scoring. More complex to run, but full-featured.

### Events and Mobilization

- Eventbrite / Meetup / Facebook Events → **[Mobilizon](https://joinmobilizon.org/)**. Federated event organizing platform. Built by Framasoft (a French non-profit) specifically as an alternative to surveillance event platforms.
- Doodle / When2Meet → **[Rallly](https://rallly.co/)** or **[Cal.com](https://cal.com/)**. Scheduling and meeting polls without harvesting attendee data.

### Office, Docs, and File Sharing

- Google Workspace / Microsoft 365 → **[Nextcloud](https://nextcloud.com/)**. The flagship FOSS office stack — files, calendar, contacts, shared docs (with Collabora or OnlyOffice), video calls, the lot. Most advocacy orgs can run their entire back office on it.
- Google Docs (just docs) → **[CryptPad](https://cryptpad.org/)**. End-to-end encrypted collaborative documents. Built by a French co-op. Excellent for sensitive drafting work.
- Dropbox / Google Drive → **[Nextcloud](https://nextcloud.com/)** or **[Seafile](https://www.seafile.com/en/home/)**.

### Chat and Calls

- Slack / Discord → **[Mattermost](https://mattermost.com/)** (Slack-shaped) or **[Element](https://element.io/) / [Matrix](https://matrix.org/)** (federated, end-to-end encrypted). Matrix is the better choice if you ever need to talk securely across organizations.
- Zoom → **[Jitsi Meet](https://meet.jit.si/)** for quick calls (free public instance available, or self-host) or **[BigBlueButton](https://bigbluebutton.org/)** for structured webinars and trainings with breakout rooms.

### Publishing and Newsletters

- Substack → **[Ghost](https://ghost.org/)**. Self-hostable, open-source publishing platform with built-in memberships and newsletters. Or just pair a static site with **Listmonk** if you only need email.
- WordPress (still fine, still FOSS) → **[WordPress](https://wordpress.org/)** self-hosted, not WordPress.com. **Note**: open-source remains, but the project's recent governance turbulence is worth a read before committing.

### CRM and Member Management

- Salesforce / HubSpot / NationBuilder → **[CiviCRM](https://civicrm.org/)**. The canonical non-profit CRM, designed specifically for advocacy and member organizations. Steep learning curve, deep capability.

### Surveys and Data Collection

- Google Forms / SurveyMonkey → **[LimeSurvey](https://www.limesurvey.org/)** for general surveys, or **[KoboToolbox](https://www.kobotoolbox.org/)** for field data collection. Kobo is what humanitarian organizations use in disaster zones — credibility-grade tool.
- Typeform → **[Formbricks](https://formbricks.com/)** or **[Tally](https://tally.so/)** (Tally is freemium, not FOSS, but worth knowing).

### Analytics

- Google Analytics → **[Plausible](https://plausible.io/)** or **[Umami](https://umami.is/)**. Privacy-respecting, cookie-free, GDPR-friendly out of the box. Both can be self-hosted.

### Maps and Geospatial

- Google Maps for embedded campaign maps → **[uMap](https://umap.openstreetmap.fr/en/)** on top of **[OpenStreetMap](https://www.openstreetmap.org/)**.

### Participatory Democracy and Engagement

- Town-hall input platforms, online consultations → **[Decidim](https://decidim.org/)**. Used by the City of Barcelona and dozens of other municipalities for participatory budgeting and civic engagement. An Alberta-relevant story given recent municipal-engagement debates.

### Visual Collaboration

- Figma / Miro → **[Excalidraw](https://excalidraw.com/)** for whiteboarding, **[Penpot](https://penpot.app/)** for design.

### Issue Tracking and Project Management

- Asana / Trello / Monday → **[Vikunja](https://vikunja.io/)**, **[Kanboard](https://kanboard.org/)**, or **[OpenProject](https://www.openproject.org/)**.
- GitHub-flavoured project boards → **[Gitea](https://about.gitea.com/)** or **[Forgejo](https://forgejo.org/)**.

---

## The Canadian Angle

This is the part most international FOSS lists miss. Some of these are funding pathways; others are organizations and references worth knowing.

- **[CIRA Community Investment Program](https://www.cira.ca/en/community-investment-program/)** — the Canadian Internet Registration Authority funds Canadian civic-tech and digital-literacy projects. Member orgs can and should apply.
- **[Open North](https://opennorth.ca/)** — Canadian civic-tech non-profit. Runs the **[Represent API](https://represent.opennorth.ca/)** for elected-official data.
- **[OpenParliament.ca](https://openparliament.ca/)** — searchable interface to House of Commons proceedings.
- **[Lobby Canada / Office of the Commissioner of Lobbying](https://lobbycanada.gc.ca/)** — the registry, free and queryable.
- **[The Tyee](https://thetyee.ca/) / [Press Progress](https://pressprogress.ca/)** — independent Canadian outlets worth supporting and worth studying as examples of mission-driven publishing operations.

---

## Background Reading — "Why Urgent"

Pieces that help articulate the case for FOSS to a board, a funder, or a skeptical executive director.

- **["Tiktok's enshittification"](https://pluralistic.net/2023/01/21/potemkin-ai/#hey-guys)** — Cory Doctorow. The five-minute version of the entire urgency argument. Quote it.
- **[Public Money, Public Code](https://publiccode.eu/)** — Free Software Foundation Europe's campaign. Useful framing when talking to municipal or provincial bodies.
- **[Mozilla Privacy Not Included](https://foundation.mozilla.org/en/privacynotincluded/)** — annual buyer's guides. Gives concrete examples of what surveillance products actually do with member data.
- **Munich, Barcelona, Schleswig-Holstein FOSS migrations** — search any of these. Government-scale evidence that this works.

---

## Operational Reality Check

A short list of things nobody mentions in the inspirational keynote but that decide whether self-hosting works for your org.

- **Backups are not optional.** Whatever you self-host, decide the backup story before you turn it on. A second copy in a different physical location, tested at least quarterly.
- **Someone has to do the updates.** "Free" software still costs maintenance hours. Either someone on staff owns it, or you contract it out (hi).
- **Email deliverability is its own discipline.** Self-hosting outbound email to thousands of supporters without landing in spam folders takes work. Most orgs should use a transactional provider (Postmark, SES, Mailgun, Scaleway) as the SMTP relay underneath Listmonk rather than running their own mail server.
- **Domains and DNS are your foundation.** Own your domains directly with a registrar you trust ([Cloudflare](https://www.cloudflare.com/products/registrar/), [Porkbun](https://porkbun.com/), [Hover](https://www.hover.com/)) — not bundled with your hosting.
- **Pick boring infrastructure.** Docker Compose on a single Linux box is enough for almost every advocacy organization. You do not need Kubernetes.

---

## Get In Touch

If your organization is curious about any of this and wants to talk through what a sovereign stack looks like for your campaign work, that conversation is free.

**The Bunker Operations** — [bnkops.com](https://bnkops.com) — admin@thebunkerops.ca

We are a worker co-op based in Edmonton building Canadian-sovereign, open-source digital infrastructure for grassroots organizations. Sliding-scale rates for non-profits and labour organizations.

---

*This handout is itself a markdown file in a self-hosted documentation vault. Fork it, host it, edit it for your members. That's the point.*
