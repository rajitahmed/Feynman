# Feynman: Discussion History

How we got from "we're stuck on ideas" to a finished spec. Each step lists the question, the options we weighed, and what was chosen. Planning ran October 9-10, 2026.

## Starting point

Two teammates, a 48-hour hackathon (Hack Knight), and no idea yet. One teammate is stronger technically; the other is less technical. They wanted something unique but doable with AI help, and wanted to learn from it instead of handing everything to the AI.

Hackathon tracks: Best Overall, Runner-Up, Financial, Health, Environmental, Beginner. Sponsor tracks: ElevenLabs, Gemini API, Solana, Tiger Data, Presage, Snowflake API, GoDaddy Registry domain. A hardware lab (Raspberry Pi, Arduino, webcams, Nest Minis) was also available.

## Step 1: What does success look like?

- **Options:** win a prize, ship something that demos well, or learn as much as possible.
- **Chosen:** ship something that works and demos well, with the real priority being learning, especially for the less technical teammate. Prizes don't matter.
- **Effect:** pick a project with a small, understandable core instead of a lot of code nobody can follow.

## Step 2: What can each teammate do?

- The stronger teammate has used several languages, called APIs, built web pages, and often vibe codes.
- The less technical teammate has never really programmed, but has vibe coded a static site.
- **Conclusion:** a web app with one or two APIs is a good fit. Skip hardware.

## Step 3: Problems you've actually felt

Four ideas came out:

1. **Feynman:** explain a topic to an AI "kid" to find the gaps in your understanding.
2. **DubberSubber:** real-time translation and dubbing for YouTube videos.
3. **StudentSleep:** an optimal sleep schedule for college students.
4. **SaveLateNotificator:** reminders to revisit saved Instagram reels.

A fifth thought, an alert for sudden MTA train delays or reroutes, came from the less technical teammate's own commute.

## Step 4: Narrowing the list

- **Feynman:** strong; fits ElevenLabs and Gemini.
- **MTA delays:** strong; real personal pain and free real-time data.
- **DubberSubber:** risky; audio capture, latency, and getting audio out of YouTube.
- **SaveLate:** risky; Instagram has no public API for saved reels.
- **StudentSleep:** safe but thin, and many apps already do it.
- **Chosen:** Feynman, because it best matches the goal of learning and building something both can understand.

## Step 5: What makes it different from a plain chatbot?

Anyone can ask a chatbot to pretend to be 5 years old. The differentiators we looked at were voice-first, a strict confused kid, a gap report, and progress over time.

- **Chosen:** voice-first, a strict kid, and a gap report. Progress over time was dropped.

## Step 6: The shape of a session

The team described the flow: paste notes, press start, and a Gemini "kid" asks questions. If the answer is good enough it moves on; if not it asks follow-ups. Then the next angle (how does it relate to derivatives, what's it used for), for 3-4 rounds, ending with a small gap report that shows where the user only repeated the notes.

## Step 7: How does the app decide "understood enough"?

- **Options:** a gut-check yes/no from Gemini, a rubric built from the notes, or a 1-5 score.
- **Chosen:** a rubric built from the notes, with a hard cap of 2 follow-ups. It's predictable, can't loop forever, and produces the gap report for free.

## Step 8: Speak, type, or both?

- **Options:** speak and hear, type and hear, or speak with a typed fallback.
- **Chosen:** speak with a typed fallback, turn-based. The demo is spoken because speaking exposes gaps best. Interrupting is too big a technical jump for 48 hours.

## Step 9: Who is the kid?

- **Options:** one fixed character, a selectable level, or an adaptive one.
- **Chosen:** one fixed character. The kid never teaches or corrects. It's only confused or says "oh I get it" with a simple restatement. The "that sounds like what you just read" call-out moves to the end report.

## Step 10: What happens at the follow-up cap?

- **Options:** say "I get it" anyway, stay honest and move on, or stay stuck until it's right.
- **Chosen:** stay honest and move on. The kid says it's still a bit fuzzy, and the gap goes in the report.

## Step 11: Where do the rounds come from?

- **Options:** a fixed template of question types, fully Gemini-generated, or user-picked.
- **Chosen:** a fixed arc of **what, how, why, example**. The team controls the notes, so thin notes aren't a concern.

## Step 12: What goes in the gap report?

- **Chosen:** four round cards (status plus 1-2 bullets), then missed key points, parroting flags (user phrase next to the matching note line), and one re-explain prompt per gap. No score. It's a scrolling page; I had first misread the "four round cards" as the whole report.

## Step 13: What's on screen during the conversation?

- **Chosen:** kid avatar with mood states, round tracker, live transcript, and a press-to-talk mic. The rubric stays hidden so it doesn't teach the answer. Avatar style is still open.

## Step 14: Which services?

- **Chosen:** Gemini for the brain, ElevenLabs for the kid's voice, and ElevenLabs speech-to-text for hearing the learner (the team has an MLH promo code). I'd suggested the browser's built-in recognition first; the team preferred ElevenLabs for accuracy. They have a laptop with Chrome.

## Step 15: Where does the code run?

- **Options:** everything in the browser, a small backend, or serverless functions.
- **Chosen:** a small local **Python** server on the demo laptop, with no deployment. The keys stay on the server in a file that never goes in git. The stronger teammate found Python easier to work with.

## Step 16: One Gemini call per turn or two?

- **Options:** one structured call, or two (judge, then reply).
- **Chosen:** one call with structured output, to keep the delay short. If the kid leaks answers during rehearsal, switch to two calls.

## Step 17: When is the rubric created?

- **Options:** one planning call up front, one round at a time, or hand-written.
- **Chosen:** one planning call up front, saved to a file the team can read and fix. A hand-checked rubric for the demo notes is kept as a fallback.

## Step 18: The demo plan

- **Topic:** recursion, with AI-generated notes the team reads and understands, and both good and weak sample answers.
- **Plan:** one behavior per round. Round 1 covered, round 2 follow-up then covered, round 3 fuzzy at the cap, round 4 parroting.
- **Learner on stage:** the less technical teammate.

## Step 19: How to work with AI while building

- **Options:** AI writes whole files, small slices with "explain it back", or the less technical teammate writes first.
- **Chosen:** small slices with explain-back. Letting the AI write bigger chunks isn't ruled out if time runs short. With only about a day left, the formal ownership split was dropped in favor of pairing.

## Step 20: Build order and cut line

- **Proposed:** text-only logic first, then voice out, voice in, and polish, with voice cuttable.
- **Team change:** voice in and out are **required**. Only polish (avatar moods, styling) can be cut.

## Writing the spec

The conversation was turned into a product spec document with problem, solution, user stories, implementation decisions, testing decisions, build order, out of scope, and notes. No repo exists yet, so it wasn't published to an issue tracker.

## ElevenLabs API key permissions

The team showed their ElevenLabs permissions screen and asked what the key should access. Only **Text to Speech** and **Speech to Text** are needed. Speech to Speech should be turned off. Voices (Read) and Models are optional, and everything else, especially anything about the workspace, members, webhooks, or service accounts, should stay off.

## Revision after the spec: frontend stack and code quality (October 10)

**1. Frontend stack: React with TypeScript.**
- **Request:** use TypeScript and React, "or something," or just TypeScript with HTML and CSS.
- **What went wrong:** I read this as "make the whole project TypeScript" and rewrote the server in Node and Express, which replaced the Python server the team had already chosen. The team asked why. I should have asked first, since the message could have been about the frontend only.
- **Chosen (final):** **React + TypeScript (Vite, plain CSS)** for the browser and **Python (FastAPI with Pydantic)** for the server. React fits because the app is a few state-driven screens (avatar mood, round tracker, transcript) built from small components. The fallback is plain TypeScript with HTML and CSS if React feels heavy; the server is unchanged either way.
- **Trade-off accepted:** with two languages, the data shapes (rubric, judgment, report) exist twice. They're defined once as Pydantic models and mirrored by hand in one small TypeScript types file, with the same `snake_case` field names on both sides. Generating the TypeScript from the server isn't worth the setup.
- **Tooling:** Ruff and pytest on the server, Prettier and ESLint on the frontend, and no frontend test suite.

**2. Readable, understandable code as a requirement.**
- **Request:** emphasize clean, composable code following SOLID, KISS, DRY and YAGNI, with no poorly named variables the team couldn't replicate on their own.
- **Chosen:**
  - A plain-words table of the principles, and a rule that KISS and YAGNI win when principles conflict.
  - Naming and style rules for both languages: full-word names, verbs for functions, named constants instead of magic numbers, small single-purpose functions, one main thing per file, type hints and Pydantic models in Python, strict TypeScript with no `any`, no dead code.
  - Gemini and ElevenLabs sit behind tiny interfaces (Python `Protocol`s) with one adapter file per vendor, so tests can use fakes.
  - A "could I replicate this?" check at the end of every slice: explain-back, rewrite one function from its name, check names, check for duplicates and extras, run the tests.
  - A block of rules to paste into the AI assistant at the start of every session.
  - A short readability pass added to the build order before demo prep.

## Still open

- Avatar style (drawn or generated) and four mood images.
- Whether to test at the server endpoints with fake services, as proposed in the spec.
- Whether React feels manageable once setup starts.