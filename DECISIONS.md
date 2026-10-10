# Feynman: Decisions Log

Everything important we decided while planning, with the reason. Last updated October 10, 2026. Items marked **Revised** replaced an earlier decision.

## Project goals

| # | Decision | Why |
| --- | --- | --- |
| 1 | Ship something that works and demos well. Prizes don't matter. | Judges reward a reliable demo, and the team cares about shipping and learning. |
| 2 | Both teammates should understand what they built and be able to extend it without the AI. | The main goal is learning, especially for the less technical teammate. |
| 3 | Pair on everything, with no formal ownership split. | Only about one day remains. The less technical teammate drives the prompts and is the learner in the demo. |
| 4 | Work in thin slices that always run, with a quick "explain it back" after each work block. | Keeps the code understandable. Letting the AI write bigger chunks is allowed if time runs short. |

## Idea selection

| # | Decision | Why |
| --- | --- | --- |
| 5 | Chose **Feynman** (explain a topic to an AI "kid"). | Best fit for the learning goal, and a good match for Gemini and ElevenLabs. |
| 6 | Dropped DubberSubber, SaveLateNotificator and StudentSleep. | DubberSubber needs real-time audio capture and is hard to finish. SaveLate has no Instagram API for saved reels. StudentSleep is thin and already common. |
| 7 | Dropped the MTA delay alert idea. | Feynman won; the MTA alert was a strong runner-up but it's out. |
| 8 | No hardware (Raspberry Pi, Arduino). | Wiring and drivers can eat a day, and nobody on the team has hardware experience. |

## What makes it different from a plain chatbot

| # | Decision | Why |
| --- | --- | --- |
| 9 | Voice-first, a strict confused kid, and a gap report at the end. | Anyone can type "pretend you're 5" into a chatbot. These three things are what make it feel different. |
| 10 | Progress tracking over time is out. | It needs storage and isn't needed to prove the idea. |

## Session design

| # | Decision | Why |
| --- | --- | --- |
| 11 | Paste notes, press start, run 3-4 rounds, show the gap report. | Matches the team's own demo idea. |
| 12 | A hidden rubric decides when to move on (not a gut check or a numeric score). | It's predictable, produces the gap report for free, and keeps the logic readable. |
| 13 | Hard cap of **2 follow-ups** per round. | Prevents endless loops during a live demo. |
| 14 | At the cap the kid says "I'm still a bit fuzzy, but let's try the next part", and the gap goes in the report. | The kid's reaction always matches the rubric result, so "I get it" really means the points were covered. |
| 15 | Fixed arc of four rounds: **what, how, why, example**. | It's a good test of understanding and easy to test. The rubric key points tie to each type. |
| 16 | Notes are always long enough for 4 rounds. | The team controls the notes, so thin-notes handling is dropped. |

## The kid character

| # | Decision | Why |
| --- | --- | --- |
| 17 | One fixed character, one ElevenLabs voice. | Easier to build and test, and more memorable than a settings menu. |
| 18 | The kid only gets confused, or says "oh I get it" plus a simple restatement of what the user said. | It never teaches or corrects, so the understanding shown is the user's own. |
| 19 | The kid never says "that sounds like what you just read". | Parroting feedback only appears in the end report. |
| 20 | The restatement uses only the user's words, never the notes. | Stops the kid from accidentally teaching the answer. |
| 21 | Kid replies are 1-2 short sentences. | Keeps the turn delay short. |

## Gap report

| # | Decision | Why |
| --- | --- | --- |
| 22 | Four round cards (status plus 1-2 bullets), then missed key points, parroting flags, and one re-explain prompt per gap. | Every part comes from the rubric checks, so no extra logic is needed. |
| 23 | Parroting flag shows the user's phrase next to the matching note line. | It's the most memorable moment in the demo. |
| 24 | No overall score. | Scores are arbitrary and invite arguments. Per-round labels are more honest. |
| 25 | The report is a scrolling page, not one screen. | The cards are only the summary at the top. |

## Screen and voice

| # | Decision | Why |
| --- | --- | --- |
| 26 | On screen: kid avatar with mood states, round tracker, live transcript, press-to-talk mic. | The avatar makes the kid feel like a character, and the transcript is the safety net. |
| 27 | The rubric stays hidden until the report. | Showing it would teach the answer. |
| 28 | Press-to-talk (click to start, click to send). | More reliable than always-listening. |
| 29 | Voice in and voice out are both **required**. Typing is a fallback. The demo is spoken. | Speaking exposes gaps best. |
| 30 | Turn-based conversation, with no interrupting or streaming. | Streaming audio is a big technical jump. |
| 31 | Speech-to-text is **ElevenLabs** (not the browser's built-in), using the MLH promo credits. | More accurate and keeps everything with one vendor. |
| 32 | Demo in Chrome on a laptop. | The team confirmed they have one. |

## Technology

| # | Decision | Why |
| --- | --- | --- |
| 33 | **Gemini** is the brain, **ElevenLabs** does voice in and out. | Both are sponsor tools, and the team already has ElevenLabs credits. |
| 34 | **Revised:** a **Python (FastAPI)** server with a **React + TypeScript (Vite, plain CSS)** frontend. | The team asked for TypeScript and React for the frontend. I mistakenly applied that to the server too; the team chose to keep **Python** on the server because the stronger teammate finds it faster to work with. |
| 35 | Run locally on the demo laptop. No deployment, no database. | Hosting and deployment are a time sink for a one-laptop demo. |
| 36 | API keys live on the server in an env file excluded from git. | Keeps the keys out of the browser so credits can't leak. |
| 37 | **One Gemini call per turn** with structured output (covered points, parroting, decision, kid reply). | Two calls would add delay to every turn. If the kid leaks answers, switch to two calls. |
| 38 | The server, not Gemini, enforces the 2-follow-up cap. | Keeps the rule predictable and easy to read as plain `if` statements. |
| 39 | **One planning call up front** builds the four-round rubric, saved to a file. | Keeps each turn fast and lets the team read and fix the rubric before the demo. |
| 40 | Keep a hand-checked rubric for the recursion demo notes as a fallback. | The demo survives if the live planning call fails. |
| 41 | Session state lives in server memory. | One session at a time is enough. |
| 64 | Data shapes are defined once as **Pydantic** models on the server and mirrored by hand in one small TypeScript types file. Both sides use the same `snake_case` field names. | Two languages means two copies of the shapes; keeping the copy small and the names identical avoids conversion code. Generating the types is not worth the setup. |

## ElevenLabs API key permissions

| # | Decision | Why |
| --- | --- | --- |
| 42 | Enable only **Text to Speech** and **Speech to Text**. Turn Speech to Speech off. | Limits damage if the key leaks to spending credits on speech. |
| 43 | Voices (Read) and Models are optional. Skip them by pasting the voice ID and model name into config. | Fewer permissions and simpler code. |
| 44 | Keep Workspace, Service Accounts, Webhooks, Workspace Members, User and Terms of Service Accept off. | The app never touches them. |

## Demo plan

| # | Decision | Why |
| --- | --- | --- |
| 45 | Demo topic is **recursion**, with AI-generated notes that the team reads and understands. | The CS audience will know right away whether the kid and report are accurate. |
| 46 | One behavior per round: round 1 covered, round 2 follow-up then covered, round 3 fuzzy, round 4 parroted. | The report ends with one card per behavior. |
| 47 | The less technical teammate is the learner on stage. | They're the most believable learner. |
| 48 | Rehearse talking points, not memorized scripts. Test the bad answers in advance. | Natural speech sounds better, and failures show where the prompts need fixing. |

## Build order and cut line

| # | Decision | Why |
| --- | --- | --- |
| 49 | **Revised:** build order is setup, hello server, planner, text-only loop, report, voice out, voice in, readability pass, demo prep, polish. | The logic is the riskiest part, so build it first. The readability pass was added with the code quality requirement. |
| 50 | **Revised:** only polish can be cut (avatar moods, styling). The planner, judge, report, voice, and readability pass are required. | Without the logic and voice it's just a chatbot, and readable code is a core goal. |

## Testing

| # | Decision | Why |
| --- | --- | --- |
| 51 | **Revised:** test at the server endpoints with **pytest** and fake Gemini and ElevenLabs adapters. Prompt quality is checked by rehearsal. No frontend test suite. | Fake services make the turn logic testable in seconds, and the logic lives on the server. *Proposed; confirm before building.* |

## Code quality (added October 10)

| # | Decision | Why |
| --- | --- | --- |
| 52 | **Readable, understandable code is a top requirement.** Both teammates must be able to read, explain, and rewrite every line on their own. | It's the core of the learning goal, and judges may ask about the code. |
| 53 | Follow **clean code, composable design, SOLID, KISS, DRY and YAGNI.** When they conflict, KISS and YAGNI win unless ignoring SOLID would hurt testing or readability. | SOLID is a tool for clarity, not a reason to add layers. |
| 54 | Names are full words that say what a thing is. No abbreviations, no single-letter variables, no vague names like `res`, `tmp`, `data2`, `handle_it`. Python uses `snake_case`, TypeScript uses `camelCase`. | The team wants no names they couldn't replicate on their own. |
| 55 | No magic numbers or strings. The follow-up cap is a named constant (`MAX_FOLLOW_UPS_PER_ROUND`), and the fuzzy line is a named constant. | One place to read and change each rule. |
| 56 | Functions are small, do one job, and are named as verbs. One main thing per file, named after the file. | Each piece can be explained in a sentence. |
| 57 | **Revised:** Python has type hints on every function, no `Any`, and Pydantic models for data. TypeScript runs in strict mode with no `any`. The data shapes are written first. | Types double as documentation. |
| 58 | **Revised:** external services (Gemini, ElevenLabs) sit behind tiny interfaces (Python `Protocol`s), one adapter file per vendor. Tests use fakes. | Dependency inversion, which also makes testing easy. |
| 59 | **Revised:** **Ruff** formats and checks the Python in one tool. Prettier and ESLint handle the TypeScript. | Style is never a debate, and one Python tool is simpler than two. |
| 60 | No dead code, no duplicated logic, no speculative features, no state library, CSS framework, or frontend test suite. | KISS, DRY and YAGNI. |
| 61 | Every slice ends with the "could I replicate this?" check: explain it back, rewrite one function from its name, check the names, check for duplicates and extras, and run the tests. | Turns the readability goal into a repeatable habit. |
| 62 | **Revised:** paste a short code-rules block into the AI assistant at the start of every session. It now covers both Python and TypeScript. | Keeps the AI's output in the team's style. The block is in the spec. |
| 63 | Add a short readability pass before demo prep: read everything once and rename, delete, merge and split as needed. | Catches drift that builds up during a fast build. |

## Out of scope

Selectable kid levels, adaptive difficulty, interrupting or streaming audio, progress over time, accounts or a database, deployment, an overall score, hardware, and extra tooling such as a state library, a CSS framework, a frontend test suite, or generated TypeScript types.

## Still open

- Avatar style (drawn or generated) and four mood images.
- Whether the testing approach (#51) is what the team wants.
- Whether React feels manageable once setup starts. The fallback is plain TypeScript with HTML and CSS; the Python server is unchanged.