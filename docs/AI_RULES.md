# Rules to paste into your AI assistant

## Every session

Paste this block at the start of every AI coding session, and again if the output drifts:

```
This project has a Python server (FastAPI, Pydantic) and a React + TypeScript frontend.
Python: type hints on every function, no `Any`, data shapes as Pydantic models, snake_case names.
TypeScript: strict mode, no `any`, camelCase names, PascalCase components, plain CSS, built-in React state only.
Follow clean code, KISS, DRY, YAGNI and SOLID, but when they conflict, prefer KISS and YAGNI.
Use full-word, descriptive names. No abbreviations, no single-letter variables, no magic numbers (use named constants).
Functions are small, do one thing, and are named as verbs. Booleans start with is/has/should.
One main thing per file, and the file name matches it.
Keep external services (Gemini, ElevenLabs) behind small interfaces so they can be faked in tests.
Do not add features, options, libraries, or abstractions that were not asked for.
No clever one-liners. Prefer plain, readable code that a beginner can follow.
Comments explain why, not what.
After writing code, briefly explain it so I can explain it back.
```

## Styling work

Paste this as well whenever you work on the UI:

```
Follow docs/DESIGN.md for all styling.
Use only the CSS variables in client/src/styles/tokens.css; no raw hex values, no new colors.
Plain CSS, one CSS file per component, named like the component. No CSS framework, no animation library.
Layout: session screen is a video call: big kid tile, small "You" tile, bottom control bar with the mic, transcript panel on the right.
Style: flat white cards with 2px borders, rounded corners, chunky buttons with a darker bottom edge, Nunito font.
Kid moods map to sprite rows through one constant; listening and thinking reuse row 0 with an overlay.
The report has no score, never uses red X marks, and never says "wrong" or "copied".
Status is shown with text and an icon, never color alone.
Do not add UI that the spec does not ask for.
```
