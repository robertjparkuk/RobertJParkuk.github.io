---
layout: page
title: Privacy
permalink: /privacy/
lead: This website collects almost nothing. Anything you type into a tool, quiz or puzzle stays in your browser. The exceptions are the optional document readers (bills, safety data sheets and site reports), which send a file you choose to have read and keep nothing.
description: "No analytics, no cookies, no forms. Tool inputs stay in your browser. How the optional document readers handle your file, the weekly digest, GitHub hosting and your rights."
---

*Last updated: 17 November 2026*

## The short version

- **No tracking.** There are no analytics, no advertising or social-media pixels, and no tracking cookies.
- **No cookies at all.** This site does not set cookies.
- **No forms that send anything to me.** If you want to get in touch, you choose to email me or message me yourself.
- **Your tool inputs stay on your device.** The Carbon Jigsaw, the Carbon Crossword and the other tools run in your web browser. Anything you type is processed on your own device and is never sent to me.
- **Opt-in exceptions: the document readers.** You can choose to have a bill (Carbon Jigsaw), a safety data sheet (Safety Data Sheet Checker) or a land report (Site Report Reader) read for you. Only then does a file leave your device, and only to be read. It isn't stored, and I never see it. [Details below](#readers).

## Who is responsible

This website is run by Robert J. Park, an independent environmental, carbon and public affairs consultant based in Larne, Northern Ireland. For any privacy question, email [{{ site.email }}](mailto:{{ site.email }}).

## What the tools save, and where

Three tools remember your progress so you don't lose it if you close the page:

| Tool | What it remembers | Where it's kept |
|---|---|---|
| The Carbon Jigsaw | The figures you enter for each piece, including any filled in by the bill reader | Your browser's local storage, on your device only |
| The Carbon Crossword | Your filled-in letters and difficulty setting | Your browser's local storage, on your device only |
| The Farm Carbon Data Checker | Your enterprises, record statuses and notes | Your browser's local storage, on your device only |

This is not a cookie, and it is never sent to me or anyone else. I cannot see it. To delete it, use **Start again** (Carbon Jigsaw), **Clear** (Crossword) or **Start my own farm** (Farm Carbon Data Checker), or clear this site's data in your browser settings. A private or incognito window keeps nothing after you close it.

The other tools and guides don't save anything.

<h2 id="readers">The document readers</h2>

<span id="bill-reader"></span>Three tools can read a document for you, so you don't have to type the details in:

| Tool | What you can send | What comes back |
|---|---|---|
| The Carbon Jigsaw | A photo or PDF of an electricity, gas, oil or water bill | Usage figures, billing period and supplier name |
| The Safety Data Sheet Checker | A safety data sheet (PDF or photo) | Product name, supplier, date and the substances listed in it |
| The Site Report Reader | A land contamination or ground investigation report (PDF) | A summary of the findings, with no names or street addresses |

Each reader is off unless you tick the box to agree and then choose a file. You can always type the details in instead.

**What happens to your file**

1. If it's a photo, your browser shrinks it first. The file then goes to a small service I run on Cloudflare (a "Worker").
2. The Worker passes it to Anthropic's Claude AI, which reads it and returns only the details listed above. It is told not to record people's names, addresses, account numbers or contact details.
3. The Worker sends those details back to your browser, which shows them. The Carbon Jigsaw keeps its figures on your device, as with anything you type. The other two tools keep nothing once you close the page.

**What is kept, by whom**

- **Me:** nothing. Your file and what is read from it are never stored by the Worker or sent to me. I have no way to see them.
- **Cloudflare** runs the Worker. Request logging is switched off. To stop the readers being overused, the Worker counts how many files each visitor sends in a day. It does this with a scrambled, one-way code made from your IP address, which can't be turned back into the address, and deletes the count after two days. It also keeps a running total for the month, with no link to anyone. See [Cloudflare's privacy policy](https://www.cloudflare.com/privacypolicy/).
- **Anthropic** reads the file through its API, under its commercial terms. It does not use API content to train its models. It deletes API inputs and outputs within 30 days, unless it needs them longer to enforce its usage policy or the law requires it. Anthropic is based in the United States, so your file is processed there. See [Anthropic's privacy centre](https://privacy.claude.com/).

**Before you send a file**, you can cover or remove names, addresses and account numbers; the readers only need the technical content. Please only send documents you're entitled to share. A site report written for a client may be confidential, so check before sending one that isn't yours.

**Lawful basis:** your consent, given by ticking the box for each file. You can stop at any time by not using the readers. Because nothing is kept by me, there is nothing for me to delete. The two-day counter deletes itself.

## The weekly digest

The [weekly digest]({{ '/digest/' | relative_url }}) pages and feeds are ordinary web pages: reading them, or following a feed in a news reader, sends me nothing. The digests are drafted with the help of Anthropic's Claude from the public data in my dashboards. No information about readers is used.

{% if site.digest_signup_url and site.digest_signup_url != "" -%}
**Weekly digest by email.** If you sign up to get the digest by email, the sign-up page and the mailing list are run by my newsletter provider, whose page you'll see when you sign up. I receive your email address and the sectors you choose, and use them only to send the digest. Every email has an unsubscribe link, and I delete your address when you unsubscribe. The lawful basis is your consent.
{%- endif %}

## Things outside my control that you should know about

Even a site that collects nothing has to be hosted somewhere:

- **Hosting (GitHub Pages).** The site is hosted by GitHub. When any GitHub Pages site is visited, GitHub logs the visitor's IP address for security purposes. I don't receive or have access to these logs. See [GitHub's privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement).
- **No other third parties when you browse.** Fonts, images and scripts are all served from this site itself. Your browser doesn't contact Google, social networks, advertisers or any other outside service when you read a page or use a tool. The only exceptions are the document readers, and only when you choose to use them.

Links to LinkedIn, WhatsApp and other websites take you to services with their own privacy policies.

## If you contact me

If you email or message me, I'll receive whatever you choose to send: your name, contact details and message. I use it only to reply and, if we work together, to deliver that work. I keep business correspondence only as long as needed for that purpose and for legal and accounting requirements. I don't sell or share it, and I don't add you to mailing lists without asking.

The lawful basis for handling your message is legitimate interests (replying to an enquiry you sent) or steps towards a contract you've asked about.

## Your rights

Under UK data protection law you can ask to see, correct or delete any personal information I hold about you, or object to how I use it. Email [{{ site.email }}](mailto:{{ site.email }}).

If you're unhappy with how I've handled your information, you can complain to the Information Commissioner's Office at [ico.org.uk](https://ico.org.uk) or on 0303 123 1113.

## Changes

If anything about how this site works changes, this page is updated first and the date at the top changed. The last change, on 17 November 2026, added the document readers and the weekly digest.
