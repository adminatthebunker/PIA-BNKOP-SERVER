I am giving approximately 1:20hr talk at PIA this year. What I have given already: 

Email: 

**Title for Session:** Free & Open Source Campaigning 

**Name:** Reed Larsen

**Pronouns:** They/Them

**Headshot**: attached

**Short Bio:**   
Reed Larsen is an Edmonton-based communications generalist and co-founder of The Bunker Operations, a worker co-op building Canadian-sovereign, open-source digital infrastructure for grassroots organizations. After four years as external communications lead for Edmonton City Councillor Michael Janz, Reed now supports advocacy groups including AB for Abortion, Pride Corner, and Public Interest Alberta — running self-hosted servers, custom databases, and AI systems that free community organizers from extractive corporate platforms. They are a political scientist by training and a stubborn generalist by practice.  

**Fun Fact:** 
Started their career at 21 teaching English to 120 elementary kids in Shenzhen, China. Claims this is where their tolerance for controlled chaos was first forged.

Site: https://publicinterestalberta.org/#tour

I am currently thinking it would be cool to do a "live" server build - not even a changemaker deployment. Get the crowd to design a server in real time, and put up the resources for fun 

Random Dump: 

Good foss resource: https://github.com/sindresorhus/awesome

So basically got about 80 mins


**The session is hands-on writing, no installs required.** Everything happens in a browser. Reed projects a CryptPad pad **hosted on PIA's own n3-pia server** at `pad.publicinterestalberta.org`. Each group writes their FOSS-alternative research into their section. Reed SSHs into n3-pia and pastes each section into a MkDocs site **also running on PIA's server**, exposed at `live.publicinterestalberta.org` (hot-reload dev server) via a Pangolin/Newt tunnel. The room watches their words go public, in real time, on PIA's own domain. At the end, Reed runs `mkdocs build` once to "freeze" the room's work into a static site at `pia2026.publicinterestalberta.org` — the permanent post-session record.

Reed's laptop is the operator station only — SSH terminal, CryptPad browser tab, projector. Nothing critical to the session runs locally.

The take-home deliverable is the `pia-starter-stack` repo — MkDocs Material + Listmonk — for any attendee who wants to run the same setup on their own hardware later.

| Section | Description | Time |
| --- | --- | --- |
| Intro | Casual chatter, names in the room, set the tone | 0 – 5 mins |
| Frame the stakes | Doctorow's enshittification, the Twitter/X exodus, a CIRA stat or two | 5 – 10 mins |
| FOSS + urgency talk | Hard-capped at 10 mins. Campaign outcomes, not tech names. | 10 – 20 mins |
| The setup | Project the empty live site at `live.publicinterestalberta.org`. Project the CryptPad URL. Explain the loop: write in pad → Reed pulls → site updates. Each group opens the pad. | 20 – 28 mins |
| Group writing in CryptPad | Groups of 4. One laptop per group on the pad. Pick a corporate tool to replace. Find FOSS alternatives. Write a 200-word section under the group's heading. | 28 – 55 mins |
| Pull + publish | Reed SSHs into n3-pia, copy-pastes each group's section from CryptPad into `docs/research/group-N.md`. Site rebuilds. Each group's URL goes live as their section lands. Read titles aloud, applaud. | 55 – 70 mins |
| The site is now real | Refresh `live.publicinterestalberta.org/research/` — every group's work, on the public internet, contributed by the room. Then: "and now we make it permanent." Reed runs `mkdocs build`; refresh `pia2026.publicinterestalberta.org` — same content, now served as a static site that survives the dev container dying. *That's the climax.* | 70 – 73 mins |
| Closing | Repo URL slide ("everything you just saw, fork it"). CMlite pitch. BNKops. **The ask.** | 73 – 80 mins |

## Pre-Conference Logistics

**The session runs entirely on PIA's n3-pia server, with attendees writing in a browser and Reed driving from a laptop terminal.** No pre-conference comms with attendees, no audience-side installs. CryptPad and the `pia-starter-stack` (MkDocs dev + Nginx static + Listmonk) all run on PIA's own server, fronted by a Pangolin/Newt tunnel routing `*.publicinterestalberta.org` subdomains to n3-pia loopback ports. Full prep is in `presenter-laptop-prep.md`. Take-home repo scaffold lives at `bunker-ops/trainings/pia-session/pia-starter-stack/`.

- **Starter stack repo published** before the session. Hosting target: `git.publicinterestalberta.org/pia-starter-stack` (or `repo.bnkops.com/pia-starter-stack`).
- **CryptPad deployed on n3-pia** at `pad.publicinterestalberta.org` (and a sandbox subdomain `pad-sandbox.publicinterestalberta.org` — required by CryptPad's security model).
- **Starter stack deployed on n3-pia** at `live.publicinterestalberta.org` (MkDocs dev server, hot-reload — used during the session), `pia2026.publicinterestalberta.org` (Nginx serving the built static site — the permanent post-session record), and `mail.publicinterestalberta.org` (Listmonk, optional).
- **All five subdomains routed via Pangolin/Newt.** Newt runs as a service in the starter-stack compose; Pangolin's admin UI gets one resource per subdomain pointing at the matching loopback port on n3-pia.
- **CryptPad pad created in advance** with section headers for ~6–8 groups. URL goes on every table card and on a slide.
- **Live debug agent on standby** — Claude Code instance with SSH to n3-pia, ready to triage if anything misbehaves.
- **QR cards on every table from minute 0**: repo + handout + CryptPad URL. No second wave needed.
- **Backup screen recording** of a successful pad-to-publish flow — 60 seconds, in case the live version stalls.

Bonus narrative beat: every component is FOSS — the CryptPad we're writing in, the MkDocs Material site we're publishing to, the Listmonk we'll send the announcement from, the Pangolin/Newt tunnel routing the traffic, the Linux/Docker host running it all. The session uses FOSS tools to write about FOSS tools, hosted on FOSS infrastructure. One sentence on stage during the publish moment.

## Audience and Framing Notes

- PIA crowd is policy / advocacy / labour, not sysadmins. Every "Docker container" loses three people. Frame everything as outcomes ("send 50,000 emails without paying Mailchimp") and save the technical names for the handout.
- Visible countdown timer on stage. 80 minutes evaporates.
- Repeat audience questions into the mic.
- Ask permission to record at the top.
- Sign-up form for the resource handout = warm lead list. Use a Listmonk form on the PIA server — eat the dog food.
- **Decide pricing before the conference.** "What does a pilot cost?" will get asked Friday at 8pm. Have a number.

## Take-home Artifacts

Attendees leave with **three** URLs:

1. **The starter stack repo** — `pia-starter-stack/` scaffold in this folder; canonical deployment target TBD (`git.publicinterestalberta.org/pia-starter-stack` or `repo.bnkops.com/pia-starter-stack`). The closing slide is this URL.
2. **The FOSS resource handout** — `foss-resources-handout.md` in this folder, deployed under `publicinterestalberta.org/resources/foss-campaigning/` before the session.
3. **The site they helped build** — `pia2026.publicinterestalberta.org`. Stays up after the session as a permanent record of what the room produced, on PIA's own domain. Worth screenshotting on the closing slide.

Repo + handout QRs on every table from minute 0. Live-site URL projected during the publish segment and on the final slide.
