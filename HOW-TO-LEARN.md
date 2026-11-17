# How to add to the Learn section

The Learn section lives at robertjpark.co.uk/learn/. Each explainer is one Markdown file in the `_learn` folder. You can add an explainer, or an example to an existing one, from the GitHub app on your phone or in a browser. This file is not published on the site.

## Add an example to an explainer

1. Open the explainer in `_learn/` (for example `_learn/carbon-life-cycle.md`) and tap the pencil to edit.
2. Find the `## Examples` heading. Copy one existing example block, from `<div class="example" markdown="1">` down to its closing `</div>`, and paste it below the last one.
3. Change the four parts:

   ```
   <div class="example" markdown="1">
   <p class="sector">Sector name, e.g. Food and drink</p>

   ### Example title, e.g. A pint of milk

   What happens at each stage, in a few short paragraphs or a list.

   | Stage | What emits carbon | Who usually counts it |
   |---|---|---|
   | Farm | ... | ... |

   **The lesson:** one sentence on what the example shows.
   </div>
   ```

4. Keep the blank line after `<p class="sector">…</p>` and before `</div>`, or the Markdown inside will not format.
5. Add any new source to the `## Sources` list at the bottom, with its date.
6. Change `checked:` near the top of the file to today's date if you rechecked the facts.
7. Tap **Commit changes**. Website rules still apply: make the change on a new branch and open a pull request, so the PR check runs before it goes live.

## Add a new explainer

1. In `_learn/`, choose **Add file → Create new file**. Name it after the question, in lower case with hyphens, e.g. `what-is-a-carbon-offset.md`. That becomes the address: robertjpark.co.uk/learn/what-is-a-carbon-offset/.
2. Paste this at the top and fill it in:

   ```
   ---
   title: "What is a carbon offset?"
   answer: "One plain sentence that answers the question. It appears in a box at the top and on the Learn page."
   description: "The summary search engines and LinkedIn show, under 160 characters."
   order: 3
   level: "Introductory"
   read_time: "6-minute"   # shows as "6-minute read"
   checked: 2026-11-17
   ---
   ```

   `order` sets its place in the list on the Learn page. `level` can be Introductory, Intermediate or Technical.
3. Write the explainer underneath. A good order is: the short answer in more detail; a diagram; "Why it matters in Northern Ireland"; `## Examples`; "Common mistakes"; `## Sources`.
4. Commit it on a new branch and open a pull request. It appears on the Learn page automatically.

## Add a diagram

Diagrams are SVG files in `assets/learn/`. The existing ones are drawn by `_scripts/learn/diagrams.py`, so they can be redrawn with the brand colours. To use one in an explainer:

```
<figure class="learn-figure"><img src="{{ '/assets/learn/your-diagram.svg' | relative_url }}" alt="Describe everything the diagram shows, in full sentences" loading="lazy"><figcaption>One line on what to notice.</figcaption></figure>
```

Always write the `alt` text in full: it is what screen readers and search engines read. Photos still follow the house rule: Robert's Adobe Stock licences or his own photos only.

## House rules

- British English, plain words, no ESG puffery.
- Official sources only for rules and figures (legislation.gov.uk, EUR-Lex, GOV.UK, HMRC, DAERA, the standards bodies). Never energy-broker websites.
- Give a date for every rule or regulatory status.
- If a number is illustrative rather than measured, say so next to it.
