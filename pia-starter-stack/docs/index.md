<div class="hero-split" markdown>

<div markdown>

<span class="eyebrow">A campaign in a box</span>

<h1 class="hero-h1">Your <em>org</em>, your stack, your <em>data</em>.</h1>

<p class="lead">A campaign for <strong>[issue]</strong>. Built and run by <strong>[people]</strong>. Find us, join us, support the work.</p>

<div class="cta-row" markdown>
[Subscribe →](subscribe.md){ .cta-primary }
[Slides](slides.md){ .cta-secondary }
[Writing](writing.md){ .cta-secondary }
[Resources](resources.md){ .cta-secondary }
</div>

</div>

<div class="frame" markdown>
![A wooden shelf holding six Lenovo ThinkCentre mini-PCs, with a network switch and tangled ethernet cables — the actual hardware running this site.](presentation/assets/server.jpg)
<div class="caption">
<span>n3-pia · the actual hardware</span>
<span class="accent">★ ★ ★</span>
</div>
</div>

</div>

<div class="stat-strip" markdown>

<div class="stat" markdown>
<span class="num">$0</span>
<span class="label">License fees</span>
</div>

<div class="stat" markdown>
<span class="num">7</span>
<span class="label">Services, one compose file</span>
</div>

<div class="stat" markdown>
<span class="num">~$10</span>
<span class="label">Per month, SMTP relay</span>
</div>

<div class="stat" markdown>
<span class="num">$149</span>
<span class="label">For the actual server</span>
</div>

</div>

## Why this stack

<div class="pull-block" markdown>
<span class="quote">A thousand neighbourhood lists will out-organize any single national list.</span>
<span class="attrib">— The thesis</span>
</div>

This site, plus a newsletter system, plus a live writing pad — runs entirely on free, open-source software your org controls. Nothing rented from Substack, Squarespace, or Mailchimp. The whole thing is one `docker-compose.yml` file you can fork, modify, and host anywhere.

If you're seeing this page, your starter stack is working. **Now make it yours.**

## What's running

<div class="stack-grid" markdown>

<div class="svc" markdown>
<span class="replaces">replaces · <b>Squarespace</b></span>
### [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
The site you're reading. Markdown in, static site out.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>Mailchimp</b></span>
### [Listmonk](https://listmonk.app/)
Email lists and campaigns. No per-contact billing, your sending reputation.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>Google Docs</b></span>
### [CryptPad](https://cryptpad.org/)
End-to-end encrypted collaborative pads. No Google account.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>Cloudflare Tunnel</b></span>
### [Pangolin / Newt](https://docs.fossorial.io/)
Outbound tunnel to a public TLS endpoint. No exposed ports.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>Stack Overflow Teams</b></span>
### [Apache Answer](https://answer.apache.org/)
Member Q&A and a public help centre that grows over time.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>SSH + vim</b></span>
### [Code Server](https://github.com/coder/code-server)
Browser-based VS Code for editing the site from any device.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>a half-built `index.html`</b></span>
### [Homepage](https://gethomepage.dev/)
Service dashboard at `lander.<your-domain>`. One door for staff and members.
</div>

<div class="svc" markdown>
<span class="replaces">replaces · <b>nothing</b></span>
### [The repo itself](https://github.com/adminatthebunker/PIA-BNKOP-SERVER)
Every config, every secret-template, every diagram. Forkable.
</div>

</div>

## How to edit this site

<div class="roster" markdown>
<div class="t">01</div>
<div class="l"><strong>In a text editor on your laptop.</strong> Open a markdown file under <code>docs/</code>, edit, save. The container rebuilds automatically.</div>
<div class="t">02</div>
<div class="l"><strong>Through Git.</strong> Clone the repo, edit, commit, push. Pull on the server — the site rebuilds.</div>
<div class="t">03</div>
<div class="l"><strong>Hand it off to a generalist.</strong> Markdown is plain text. Anyone on your team can write it.</div>
</div>

[Read the install guide →](install.md){ .cta-primary }

## Where to next

<div class="deck-grid" markdown>

<div class="cell" markdown>
[**Research**](research.md) — what we've found, what we're learning.
</div>

<div class="cell" markdown>
[**Writing**](writing.md) — short pieces from the room.
</div>

<div class="cell" markdown>
[**Resources**](resources.md) — the tools and patterns we recommend.
</div>

<div class="cell" markdown>
[**Subscribe**](subscribe.md) — get our updates by email.
</div>

</div>

<div class="footline" markdown>
<span>// stack: mkdocs · listmonk · cryptpad · pangolin · code-server · homepage</span>
<span class="red">co-designed at PIA 2026 · maintained by [The Bunker Operations](https://bnkops.com)</span>
</div>
