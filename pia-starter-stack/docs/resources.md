# Free & Open Source Tools for Campaigning

A resource list from the *Free & Open Source Campaigning* session at Public Interest Alberta, 2026. Curated for advocacy organizations, labour groups, non-profits, and grassroots campaigns operating in Canada.

The goal: replace extractive, surveillance-funded SaaS with tools you control, on infrastructure that lives in this country, run by people who answer to your members instead of a quarterly earnings call.

Maintained by [The Bunker Operations](https://bnkops.com). Suggestions and corrections welcome — this is a living document.

!!! tip "Just want the bottom line?"

    Clone **[github.com/adminatthebunker/PIA-BNKOP-SERVER](https://github.com/adminatthebunker/PIA-BNKOP-SERVER)** and `cd` into `pia-starter-stack/`, set a handful of environment variables, run `docker compose up -d`, and have your org's first sovereign service live tonight. The rest of this page is what you reach for after that.

---

## :material-server-network: The Starter Stack — Run This First

The session shipped a working stack you can clone and run on your own hardware. One `docker-compose.yml`, a handful of services, about ten minutes from `git clone` to live URLs. The same stack PIA itself ran during the session — and the page you're reading is being served by it right now.

What's in the box:

<div class="grid cards" markdown>

-   :material-tunnel-outline:{ .lg .middle } **Newt**

    ---

    Pangolin tunnel client. Public-internet ingress without opening firewall ports.

    *Replaces:* Cloudflare Tunnel

-   :material-book-open-page-variant:{ .lg .middle } **MkDocs Material**

    ---

    Your org's public knowledge base, written in markdown. Edit `docs/*.md`, save, refresh.

    *Replaces:* Squarespace

-   :material-server:{ .lg .middle } **Nginx**

    ---

    Serves the built static site for production traffic. Run `mkdocs build` to refresh.

-   :material-email-fast-outline:{ .lg .middle } **Listmonk + Postgres**

    ---

    Newsletter and mass email. Subscriber lists, campaigns, sending.

    *Replaces:* Mailchimp

-   :material-laptop:{ .lg .middle } **Code Server**

    ---

    Browser-based VS Code over the same files. Lets non-technical staff edit markdown without SSH.

-   :material-help-circle-outline:{ .lg .middle } **Apache Answer**

    ---

    Self-hosted Q&A platform for member questions and public help pages. SQLite by default — no extra database to wire up.

    *Replaces:* Stack Overflow Teams

-   :material-view-dashboard-outline:{ .lg .middle } **Homepage**

    ---

    Service dashboard at `lander.<your-domain>` listing every tool in the stack with live status. One door for staff and members; config is plain YAML in `configs/homepage/`.

    *Replaces:* a half-built `index.html`, "where do I log in to ___?" Slack threads

-   :material-shield-lock-outline:{ .lg .middle } **CryptPad** *(optional)*

    ---

    End-to-end-encrypted collaborative pads. Behind a `--profile session` flag.

    *Replaces:* Google Docs for sensitive drafting

</div>

!!! info "Architecture note"

    No service binds a host port. Everything is reachable only through the Pangolin tunnel — TLS terminates at the tunnel edge, and the host firewall stays closed. Sovereign by design.

### Want a desktop editor?

The bundled Code Server gives you a browser-based VS Code over the same files. If you'd rather edit on your laptop:

| Editor | Open source? | Best for |
| --- | --- | --- |
| **[Obsidian](https://obsidian.md)** | Free, not fully FOSS | Easiest on-ramp for non-technical users |
| **[Logseq](https://logseq.com)** | Fully FOSS | Knowledge-graph thinkers |
| **[Joplin](https://joplinapp.org)** | Fully FOSS | People migrating from Evernote |

All three open the same `.md` files. Pick whichever fits your brain.

---

## :material-folder-search-outline: Other Directories Worth Knowing

When the starter stack doesn't cover what you need, these are the directories to search.

| Directory | Strength |
| --- | --- |
| **[awesome-selfhosted](https://github.com/awesome-selfhosted/awesome-selfhosted)** ([readable mirror](https://awesome-selfhosted.net)) | The canonical, community-maintained directory of self-hostable software, organized by category. |
| **[European Alternatives](https://european-alternatives.eu)** | Frames replacements by *the corporate tool you're trying to escape* — the question most organizers actually ask. |
| **[Privacy Guides](https://www.privacyguides.org)** | Audited, regularly-updated recommendations for privacy-respecting tools. No affiliate-driven nonsense. |

---

## :material-swap-horizontal: Replace What Your Org Already Pays For

Concrete substitutions for tools advocacy organizations commonly use. The :material-package-variant-closed:{ title="In the starter stack" } icon flags tools already in the starter stack — no extra setup needed.

!!! success "Featured: CMLite — open-source campaign management"

    **[cmlite.org](https://cmlite.org/)** is the FOSS replacement most directly aimed at the work this page is about: running a campaign. Voter contact, canvassing, phone banks, volunteer coordination, GOTV — the full campaign toolkit, without renting it from NationBuilder or NGP VAN. If your org runs election or issue campaigns, this is the one to evaluate first.

### :material-email: Email and Mass Communications

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Mailchimp, Constant Contact, Campaign Monitor | **[Listmonk](https://listmonk.app/)** :material-package-variant-closed: | Single binary, scales to millions of subscribers. Bring your own SMTP relay. |
| HubSpot, Marketo | **[Mautic](https://www.mautic.org/)** | Marketing automation, drip campaigns, lead scoring. More complex to operate. |

### :material-calendar-multiple: Events and Mobilization

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Eventbrite, Meetup, Facebook Events | **[Mobilizon](https://joinmobilizon.org/)** | Federated event organizing platform. Built by Framasoft (French non-profit). |
| Doodle, When2Meet | **[Rallly](https://rallly.co/)** or **[Cal.com](https://cal.com/)** | Scheduling and meeting polls without harvesting attendee data. |

### :material-folder-multiple: Office, Docs, and File Sharing

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Google Workspace, Microsoft 365 | **[Nextcloud](https://nextcloud.com/)** | The flagship FOSS office stack — files, calendar, contacts, shared docs (Collabora / OnlyOffice), video calls. Most advocacy orgs can run their entire back office on it. |
| Google Docs (just docs) | **[CryptPad](https://cryptpad.org/)** :material-package-variant-closed: | End-to-end encrypted collaborative documents. Built by a French co-op. Excellent for sensitive drafting. |
| Dropbox, Google Drive | **[Nextcloud](https://nextcloud.com/)** or **[Seafile](https://www.seafile.com/en/home/)** | Either works for shared file storage. |

### :material-help-circle-outline: Community Q&A and Member Support

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Stack Overflow Teams, Zendesk Guide, paid Discourse hosting | **[Apache Answer](https://answer.apache.org/)** :material-package-variant-closed: | Apache Software Foundation project. SQLite-by-default; scales up to MySQL/Postgres when you outgrow it. Good fit for a public "ask us anything" page or an internal member support board. |
| Discourse Cloud | **[Discourse](https://www.discourse.org/)** self-hosted | Forum-shaped rather than Q&A-shaped. Heavier to operate (Postgres + Redis + Sidekiq) but the canonical choice for long-running community forums. |

### :material-message-text: Chat and Calls

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Slack, Discord | **[Mattermost](https://mattermost.com/)** *(Slack-shaped)* or **[Element](https://element.io/) / [Matrix](https://matrix.org/)** *(federated, E2EE)* | Matrix is the better choice if you ever need to talk securely across organizations. |
| Zoom (quick calls) | **[Jitsi Meet](https://meet.jit.si/)** | Free public instance, or self-host. |
| Zoom (structured webinars / training) | **[BigBlueButton](https://bigbluebutton.org/)** | Built for education — breakout rooms, polls, whiteboarding. |

### :material-newspaper-variant: Publishing and Newsletters

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Squarespace, Wix, Webflow | **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** :material-package-variant-closed: | For documentation-shaped sites. |
| Squarespace (more layout control) | **[Hugo](https://gohugo.io/)** or **[Astro](https://astro.build/)** | Static-site generators with template flexibility. |
| Substack | **[Ghost](https://ghost.org/)** | Self-hostable publishing with built-in memberships and newsletters. Or pair a static site with **Listmonk** if you only need email. |
| WordPress.com | **[WordPress](https://wordpress.org/)** self-hosted | Open-source remains, but the project's recent governance turbulence is worth a read before committing. |

### :material-cloud-tags: Tunnels and Public Ingress

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Cloudflare Tunnel | **[Pangolin + Newt](https://docs.fossorial.io/)** :material-package-variant-closed: | Self-hosted reverse-tunnel. Public HTTPS without opening firewall ports or running a public-IP server. |
| ngrok, port-forwarding | **[Tailscale Funnel](https://tailscale.com/kb/1223/funnel)** or **[Cloudflared](https://github.com/cloudflare/cloudflared)** | Reasonable alternatives if Pangolin doesn't fit. |

### :material-laptop: Web IDE and Remote Editing

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| GitHub Codespaces, Replit | **[code-server](https://github.com/coder/code-server)** :material-package-variant-closed: | Full VS Code in a browser, against your own filesystem. Lets non-technical staff edit markdown without learning SSH. |

### :material-view-dashboard-outline: Service Dashboards and Start Pages

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Browser-bookmark folders, hand-rolled `index.html`, Notion "team links" page | **[Homepage](https://gethomepage.dev/)** :material-package-variant-closed: | Configurable dashboard with service cards, live up/down status, container CPU/memory widgets, bookmarks, and search. Drop it at `lander.<your-domain>` and every other tool in your stack is one click away. |
| Same | **[Heimdall](https://heimdall.site/)** or **[Dashy](https://dashy.to/)** | Reasonable alternatives. Heimdall is the OG; Dashy has more widgets but heavier ops. |

### :material-bullhorn: Campaign Management

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| NationBuilder, NGP VAN, Action Network *(campaign-side functions)* | **[CMLite](https://cmlite.org/)** | Open-source campaign-management platform purpose-built for political and issue campaigns. Voter contact, canvassing, phone banks, volunteer coordination, GOTV. Distinct from a non-profit CRM — built for the cadence of an active campaign. |

### :material-account-group: CRM and Member Management

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Salesforce, HubSpot, NationBuilder *(member-org functions)* | **[CiviCRM](https://civicrm.org/)** | The canonical non-profit CRM, designed for advocacy and long-running member organizations. Steep learning curve, deep capability. Pair with **CMLite** above when you need active-campaign tooling on top. |

### :material-poll: Surveys and Data Collection

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Google Forms, SurveyMonkey | **[LimeSurvey](https://www.limesurvey.org/)** | General-purpose surveys. |
| Field surveys, disaster-zone data | **[KoboToolbox](https://www.kobotoolbox.org/)** | What humanitarian organizations use in disaster zones — credibility-grade tool. |
| Typeform | **[Formbricks](https://formbricks.com/)** or **[Tally](https://tally.so/)** | Tally is freemium, not FOSS, but worth knowing. |

### :material-chart-line: Analytics

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Google Analytics | **[Plausible](https://plausible.io/)** or **[Umami](https://umami.is/)** | Privacy-respecting, cookie-free, GDPR-friendly out of the box. Both can be self-hosted. |

### :material-map: Maps and Geospatial

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Google Maps (embedded campaign maps) | **[uMap](https://umap.openstreetmap.fr/en/)** on **[OpenStreetMap](https://www.openstreetmap.org/)** | Embeddable, themeable, no API key juggling. |

### :material-vote: Participatory Democracy and Engagement

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Town-hall input platforms, online consultations | **[Decidim](https://decidim.org/)** | Used by the City of Barcelona and dozens of municipalities for participatory budgeting and civic engagement. Alberta-relevant given recent municipal-engagement debates. |

### :material-palette: Visual Collaboration

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Figma, Miro (whiteboarding) | **[Excalidraw](https://excalidraw.com/)** | Hand-drawn-feel diagrams. Self-hostable, also a great desktop app. |
| Figma (design) | **[Penpot](https://penpot.app/)** | Open-source design tool with Figma-like ergonomics. |

### :material-clipboard-list: Issue Tracking and Project Management

| Currently paying for | FOSS alternative | Notes |
| --- | --- | --- |
| Asana, Trello, Monday | **[Vikunja](https://vikunja.io/)**, **[Kanboard](https://kanboard.org/)**, or **[OpenProject](https://www.openproject.org/)** | Vikunja is the lightest; OpenProject the most enterprise-shaped. |
| GitHub-flavoured project boards | **[Gitea](https://about.gitea.com/)** or **[Forgejo](https://forgejo.org/)** | Forgejo is the community fork; both are drop-in for most GitHub workflows. |

---

## :material-leaf-maple: The Canadian Angle

The part most international FOSS lists miss. Some of these are funding pathways; others are organizations and references worth knowing.

| Resource | What it offers |
| --- | --- |
| **[CIRA Community Investment Program](https://www.cira.ca/en/community-investment-program/)** | The Canadian Internet Registration Authority funds Canadian civic-tech and digital-literacy projects. Member orgs can and should apply. |
| **[Open North](https://opennorth.ca/)** | Canadian civic-tech non-profit. Runs the **[Represent API](https://represent.opennorth.ca/)** for elected-official data. |
| **[OpenParliament.ca](https://openparliament.ca/)** | Searchable interface to House of Commons proceedings. |
| **[Lobby Canada](https://lobbycanada.gc.ca/)** | Office of the Commissioner of Lobbying. The registry, free and queryable. |
| **[The Tyee](https://thetyee.ca/) / [Press Progress](https://pressprogress.ca/)** | Independent Canadian outlets worth supporting and worth studying as examples of mission-driven publishing operations. |

---

## :material-book-open-variant: Background Reading — "Why Urgent"

Pieces that help articulate the case for FOSS to a board, a funder, or a skeptical executive director.

- **["Tiktok's enshittification"](https://pluralistic.net/2023/01/21/potemkin-ai/#hey-guys)** — Cory Doctorow. The five-minute version of the entire urgency argument. Quote it.
- **[Public Money, Public Code](https://publiccode.eu/)** — Free Software Foundation Europe's campaign. Useful framing when talking to municipal or provincial bodies.
- **[Mozilla Privacy Not Included](https://foundation.mozilla.org/en/privacynotincluded/)** — annual buyer's guides. Concrete examples of what surveillance products actually do with member data.
- **Munich, Barcelona, Schleswig-Holstein FOSS migrations** — search any of these. Government-scale evidence that this works.

---

## :material-tools: Operational Reality Check

The things nobody mentions in the inspirational keynote but that decide whether self-hosting actually works for your org.

!!! warning "Backups are not optional"

    Whatever you self-host, decide the backup story **before** you turn it on. A second copy in a different physical location, tested at least quarterly. The starter stack's two volumes worth backing up are the **Listmonk database** and `./data/cryptpad/` — the rest of the content lives in Git.

!!! warning "Someone has to do the updates"

    "Free" software still costs maintenance hours. Either someone on staff owns it, or you contract it out (hi). Run `docker compose pull && docker compose up -d` once a month minimum.

!!! info "Email deliverability is its own discipline"

    Self-hosting outbound email to thousands of supporters without landing in spam folders takes work. Most orgs should use a transactional provider — **Postmark, SES, Mailgun, Scaleway** — as the SMTP relay underneath Listmonk rather than running their own mail server.

!!! info "Domains and DNS are your foundation"

    Own your domains directly with a registrar you trust — [Cloudflare](https://www.cloudflare.com/products/registrar/), [Porkbun](https://porkbun.com/), [Hover](https://www.hover.com/) — not bundled with your hosting. The day you change hosts is the day you'll be glad.

!!! tip "Pick boring infrastructure"

    Docker Compose on a single Linux box plus a tunnel in front is enough for almost every advocacy organization. You do not need Kubernetes.

---

## :material-handshake: Get In Touch

If your organization is curious about any of this and wants to talk through what a sovereign stack looks like for your campaign work, that conversation is free.

**The Bunker Operations** — a worker co-op based in Edmonton building Canadian-sovereign, open-source digital infrastructure for grassroots organizations. Sliding-scale rates for non-profits and labour organizations.

[:material-web: bnkops.com](https://bnkops.com){ .md-button .md-button--primary }
[:material-email: admin@thebunkerops.ca](mailto:admin@thebunkerops.ca){ .md-button }

---

*This page is itself a markdown file in a self-hosted documentation vault. Fork it, host it, edit it for your members. That's the point.*
