# Twenty-step rubber-duck review

September 10, 2026. A cumulative review of signal-to-noise ratio, navigation, grammar, spacing and readability. Each pass uses the previous pass to decide what to change next. The scientific question and its uncertainty remain intact.

## 01 — Identify the visitor's first task

**Ask:** What should a newcomer understand first?

The old opening used several statements to introduce one question. Replace them with “Is energy density the right problem?” The next pass can now assess whether the research stage is equally clear.

## 02 — Explain the current stage

**Ask:** Does the page look more established than the evidence warrants?

Replace the large assessment panel and oversized “01” with a short “Where we stand” summary: the question is open, a model and study plan exist, and no project study is complete. Keep that status visible while simplifying the navigation.

## 03 — Separate the visitor's tasks

**Ask:** Must everyone read the model, protocols and contribution form in one sitting?

No. Split the experience into Question, Explore, Research guide and Contribute. Retain the framing review as supporting evidence. This makes it possible to give each page a clear first action.

## 04 — Make the first action useful

**Ask:** Should a first-time visitor read a long review before understanding the question?

Make “Start with an example” the homepage's main action. Keep the ten-step framing review beside the research status. With the route clearer, remove prose that repeats the same purpose.

## 05 — Remove repeated framing

**Ask:** How many times do we say that the hypothesis is unresolved?

The old homepage repeated that message across the hero, assessment card, hypothesis strip, model and research records. Keep the initial status and context-specific evidence labels; move technical details to their relevant pages. The homepage can now explain the concepts directly.

## 06 — Define unfamiliar terms early

**Ask:** Will an interested reader know what density or a binding constraint means?

Explain energy per volume and energy per mass before asking visitors to compare them. Use “what limits it” in the main question. Keep technical definitions and full system boundaries in the research guide. Then simplify the surrounding sentences.

## 07 — Replace awkward and abstract wording

**Ask:** Can the reader say what each sentence means without translating it?

Replace “solve energy density” with a question about choosing the right problem. Change “Move the same load, over the same route” to “Move the same load over the same route.” Use direct questions in examples and forms. Preserve precise language where a technical distinction matters.

## 08 — Use consistent spelling

**Ask:** Are harmless spelling variations adding editorial friction?

Use US spelling consistently in the edited prose, including “labeled” and “liter.” Do not describe valid British spellings as errors. With the vocabulary consistent, review punctuation and labels next.

## 09 — Make punctuation help the reader

**Ask:** Are slashes, arrows and capital letters doing useful work?

Remove the numbered all-caps section labels and slash-heavy headings from the main journey. Use sentence case and ordinary conjunctions. Keep arrows where they explain a relationship or research sequence. The next pass checks actual word boundaries.

## 10 — Fix the missing-space mechanism

**Ask:** What happens when a visual line break disappears?

The old closing heading contained `reality<br>make`. A mobile rule hid the break and produced “realitymake.” Remove forced breaks from headings and let text wrap naturally. The brand also becomes ordinary text. The typography no longer depends on layout markup to separate words.

## 11 — Establish a readable type scale

**Ask:** Can important text be read without zooming?

At the original 719-pixel viewport, 58 sampled rendered text elements were below 14 pixels. Raise labels and supporting text, reduce oversized headings, and remove negative letter spacing. Use relative font sizes so text enlargement is respected. Then check the length of each line.

## 12 — Limit reading width

**Ask:** Does a long sentence become a full-width strip?

Constrain reading columns and give examples a consistent question-and-answer layout. Keep longer documents in a narrower content column. This reduces eye travel without shrinking the text, and makes spacing easier to standardize.

## 13 — Reduce competing decoration

**Ask:** Which borders, backgrounds and labels identify a meaningful group?

Replace the large dark model section and repeated status panels with a restrained reading surface. Use borders to separate sections and a soft background for examples, selected details and draft previews. Standardize the spacing instead of assigning every section its own visual treatment.

## 14 — Simplify the model explorer

**Ask:** Does a web of lines help someone answer a specific question?

Highlight only connections to the selected factor. Keep the first assumption visible and make other details expandable. On narrow screens, replace the spatial diagram with a readable button grid and the same connection details. Preserve all 13 proposed connections and their untested status.

## 15 — Keep both feedback loops legible

**Ask:** Can a reader compare the possible benefit and the possible offset?

Show the two loops together, with shorter headings and consistent spacing. Say “Lower costs can increase demand” to preserve uncertainty. This supports the calculator's next task: showing when growth offsets a saving.

## 16 — Explain the calculator result

**Ask:** Is “100%” a gain, a loss or no change?

Label the output “Energy use, compared with today” and explain that 100% means no change. Rename the inputs “Energy saved per task” and “Increase in task count.” Keep the assumptions nearby. A browser check confirmed that 20% savings with 100% task growth produces 160% of the original operational energy use.

## 17 — Make link destinations predictable

**Ask:** Will a person expecting an explanation land in raw data?

Give the first study a readable guide section. Identify JSON and Markdown links by format. Keep direct data access for researchers and AI systems, while using normal pages for the main journey. That distinction also informs the contribution export choices.

## 18 — Make drafts readable and difficult to misread

**Ask:** Can someone review a contribution without reading code?

Replace the monospace preview with labeled paragraphs. Make a text download the primary export; keep JSON as an explicit secondary choice. Preserve the declared-missing-evidence option, safety acknowledgment and preview-before-posting behavior. Browser checks confirmed that an invalid old source cannot block a draft after evidence is marked unavailable, and editing a field hides the stale preview.

## 19 — Check reading order and smaller screens

**Ask:** Does the simpler layout remain usable by keyboard and at larger text sizes?

Move the contribution form before secondary information in both the document order and the narrow-screen layout. Correct skipped heading levels. Verify keyboard focus, the skip link and keyboard selection of an example. Check all five product pages at 320 and 1,280 pixels, plus 200% root text size at 390 pixels: no horizontal page overflow or clipped text was detected in the sampled headings, paragraphs, buttons, summaries and labels.

## 20 — Preserve the fixes

**Ask:** What prevents the next content update from recreating the problem?

Keep shared headers, styles and generated pages consistent. Add checks for heading hierarchy and forced heading breaks, including a regression case for the missing-space bug. Retain the research schema, reference, calculator and draft-validation tests. Record the review and publish only after the checks pass.

## Measured change

At the same 719-pixel viewport with default controls and closed disclosures, the homepage changed from 1,287 visible main-content words to 341, and from 10,889 pixels tall to 2,581. That is about 74% fewer visible words and 76% less vertical scrolling. The sampled text below 14 pixels fell from 58 elements to zero. The material was reorganized, not removed from the research record.

## Verification scope

The review included rendered-page inspection, desktop and narrow-screen checks, a temporary local 200% root-font check, keyboard interaction, model selection, calculator updates, contribution preview behavior and browser error logs. No browser runtime errors were reported in the checked local session. The enlarged-text override was removed after testing. These are targeted checks, not a usability study with participants or a complete accessibility certification.
