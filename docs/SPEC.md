# Feynman: Hackathon Spec

Hack Knight, 48-hour hackathon. Two-person team (one stronger coder, one less technical). Spec written October 9, 2026. Revised October 10, 2026: React + TypeScript frontend with a Python server, and code readability made a first-class requirement.

## Problem Statement

Students who use the Feynman method usually explain a topic to nobody, so nothing pushes back when they skip a step, hide behind jargon, or recite their notes. They feel like they understand it, but they can't see the gaps.

Asking a chatbot to "pretend to be a 5-year-old" doesn't fix this. It tends to nod along, it often teaches the answer back, and it never tells you afterwards which ideas you missed or which parts you simply read off your notes.

## Solution

Feynman is a voice-first practice tool. You paste your notes, press start, and explain the topic out loud to a curious kid character who only ever does one of two things: gets confused, or says "oh I get it" and restates your explanation in simple words.

- **Four fixed rounds** follow the arc what, how, why, example (for recursion: what is it, how does it relate to loops, what is it for, give an example).
- **A hidden rubric** built from your notes decides whether each answer covered the key points. The kid asks at most 2 follow-ups per round, then says "I'm still a bit fuzzy, but let's try the next part" and moves on.
- **The kid never teaches or corrects.** It never reveals what is in the notes.
- **A gap report** at the end shows four round cards, the key points you missed, the answers that mirrored your notes (your words next to the matching note line), and one "try re-explaining this" prompt per gap. There is no score.

You talk with press-to-talk, and you can always type instead. A live transcript shows what the app heard.

## Code Quality Requirements

**Both teammates must be able to read, explain, and rewrite every line of this code on their own.** If a name, function, or file can't be understood on first read, it gets rewritten. This matters more than speed, and it is the main way the project meets the team's goal of learning.

### The principles, in plain words

| Principle | What it means here |
| --- | --- |
| **Clean / readable** | Code reads top to bottom like a short explanation. A teammate seeing a file for the first time can say what it does. |
| **Composable** | Small pieces that plug together. Screens are built from small components; the server is built from small functions that each do one step. |
| **S: Single responsibility** | Each file, function, class, and component has one job and one reason to change. If you need "and" to describe it, split it. |
| **O: Open/closed** | Add new behavior by adding something new, not by editing working code. For example, a new round type is a new entry in the round list, not a new `if` buried in the turn logic. |
| **L: Liskov substitution** | The fake speech service used in tests must behave like the real one, so either can be plugged in without changing the code that uses it. |
| **I: Interface segregation** | Interfaces stay tiny. The speech-to-text interface has one method; it doesn't also carry text-to-speech methods. |
| **D: Dependency inversion** | The turn logic depends on small interfaces (`SpeechToText`, `TextToSpeech`, `LanguageModel`), not on ElevenLabs or Gemini directly. The vendor code lives in one adapter file each. |
| **KISS** | Choose the simplest thing that works. No clever one-liners, no tricks the team can't explain. |
| **DRY** | One place for each piece of logic or text. Copy-paste of the same logic is a bug. But don't merge two things that merely look alike (wait until a third copy appears). |
| **YAGNI** | Build only what the spec asks for. No "we might need this later" code, no unused options, no extra layers. |

**When principles conflict:** KISS and YAGNI win, unless ignoring SOLID would make the code harder to test or harder to read. SOLID is a tool for clarity, not a reason to add layers.

### Naming and style rules

These apply to both languages. Python uses `snake_case` for functions and variables, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants. TypeScript uses `camelCase` for functions and variables, `PascalCase` for components and types.

- **Names are full words that say what a thing is.** Good: `covered_key_points`, `follow_up_count`, `kid_reply_text`, `is_round_fuzzy` (Python) and `coveredKeyPoints`, `RoundTracker`, `isRecording` (TypeScript). Bad: `res`, `d`, `tmp`, `data2`, `handle_it`, `x`.
- **No abbreviations** unless everyone knows them (`id`, `url`). `STT` and `TTS` are not obvious; use `speech_to_text` and `text_to_speech`.
- **Functions are verbs** that say what they do: `plan_rounds`, `judge_answer`, `build_gap_report`. **Booleans start with `is`, `has`, or `should`.**
- **No magic numbers or strings.** The follow-up cap is `MAX_FOLLOW_UPS_PER_ROUND = 2`, defined once and named. The fuzzy line the kid says is one named constant.
- **File names match what they hold.** A file named `judge_answer.py` contains `judge_answer`. One main thing per file.
- **Small functions.** If a function doesn't fit on one screen, or needs a comment to explain its middle, split it into named steps.
- **Types explain the data.** Every Python function has type hints on its inputs and outputs, with no `Any`. Data shapes are Pydantic models. The TypeScript side runs in strict mode with no `any`. The shapes for the rubric, the judgment, and the report are written first and double as documentation.
- **Comments explain why, not what.** If a comment is needed to say what the code does, rename or restructure instead.
- **No dead code.** Delete unused functions, files, and commented-out code.
- **Same formatting everywhere.** Ruff formats and checks the Python, Prettier and ESLint handle the TypeScript, so style is never a discussion.

### The "could I replicate this?" check

Before any slice counts as done, both teammates confirm all of these:

1. **Explain-back:** one teammate explains the new code in their own words, line by line, without reading the AI's explanation.
2. **Rewrite test:** pick one new function, hide it, and check you could write it again from just its name and a one-sentence description.
3. **Name check:** no name made you pause. If one did, rename it now.
4. **No duplicates, no extras:** nothing copy-pasted, nothing unused, nothing "for later".
5. **Tests pass and the app still runs.**

### Rules to paste into your AI assistant

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

## User Stories

**Setup**

1. As a learner, I want to paste my study notes into a text box, so that the app knows what topic I'm explaining.
2. As a learner, I want to press one start button, so that the session begins without any configuration.
3. As a learner, I want to see a "preparing your session..." state while the rounds are planned, so that I know the app isn't frozen.
4. As a learner, I want the four rounds planned from my own notes, so that the questions fit what I'm actually studying.

**The conversation**

5. As a learner, I want the kid to open each round by asking its question out loud, so that it feels like talking to a person.
6. As a learner, I want to see which round I'm on (for example "Round 2 of 4: How does it work?"), so that I know how far along I am.
7. As a learner, I want to click the mic to start talking and click again to send, so that I control when my answer is finished.
8. As a learner, I want my spoken answer transcribed and shown on screen, so that I can check the app heard me correctly.
9. As a learner, I want to type my answer instead of speaking, so that I can keep going if the mic or the room fails.
10. As a learner, I want to see a "the kid is thinking..." state after I answer, so that the delay doesn't feel broken.
11. As a learner, I want the kid to reply out loud in a consistent kid voice, so that it feels like the same character all session.
12. As a learner, I want the kid's replies to also appear in the transcript, so that I can reread what it asked.
13. As a learner, I want the kid to say "oh I get it" and restate my explanation in simple words when I cover the key points, so that I know my explanation landed.
14. As a learner, I want the kid to ask one specific confused question when I miss a key point, so that I'm nudged toward the gap without being told the answer.
15. As a learner, I want the kid never to correct me or add facts from the notes, so that the understanding I show is my own.
16. As a learner, I want the kid's restatement to use only my words, so that it doesn't accidentally teach me the answer.
17. As a learner, I want the kid to stop asking after 2 follow-ups and say it's still a bit fuzzy, so that I never get stuck in a loop.
18. As a learner, I want the kid's replies kept to 1-2 short sentences, so that the conversation moves quickly.
19. As a learner, I want the avatar to change mood (listening, thinking, confused, "I get it"), so that I can read the kid's reaction at a glance.
20. As a learner, I want the rubric hidden during the session, so that I'm not just ticking off a checklist.

**The gap report**

21. As a learner, I want the report to appear automatically after round 4, so that the session has a clear ending.
22. As a learner, I want four round cards with a status (covered, partly covered, or fuzzy) and 1-2 bullets each, so that I see my overall result quickly.
23. As a learner, I want a list of the specific key points I never mentioned, so that I know exactly what to study next.
24. As a learner, I want answers that closely mirrored my notes flagged, with my words shown next to the matching note line, so that I can see where I recited instead of explained.
25. As a learner, I want one "try re-explaining this" prompt per gap, so that I have something concrete to practice without being handed the answer.
26. As a learner, I want no overall score, so that I focus on the gaps rather than a number.
27. As a learner, I want the report to scroll as one page, so that I can read the details below the summary cards.

**Team and demo**

28. As the team, we want the planned rubric saved to a file we can open, so that we can check its key points before the demo.
29. As the team, we want a hand-checked rubric for the recursion notes that we can load instead of the live planning call, so that the demo survives if that call fails.
30. As the team, we want the API keys kept on the local server and out of the browser and git, so that our credits can't leak.
31. As the team, we want each turn's judgment returned as structured fields, so that the server logic is simple enough for both of us to read.
32. As the team, we want to rehearse a good, a vague, a weak, and a parroted answer, so that the demo shows every behavior once.

**Code quality**

33. As the team, we want every variable, function, and file named in full words that say what it is, so that either of us can read and rewrite it without help.
34. As the team, we want small, single-purpose functions and components, so that each one fits on a screen and can be explained in one sentence.
35. As the team, we want the Gemini and ElevenLabs calls hidden behind small interfaces, so that we can use fakes in tests and swap vendors without touching the turn logic.
36. As the team, we want each data shape defined once on the server and mirrored in one small types file in the browser, so that the two sides can't quietly disagree and the copy is easy to check.
37. As the team, we want no unused code, no duplicated logic, and no speculative features, so that the whole codebase stays small enough to keep in our heads.
38. As the team, we want to explain every new slice back in our own words before moving on, so that neither of us ends up owning code we don't understand.

## Implementation Decisions

The browser never talks to an AI service directly; a small local Python server holds the keys and does every call. The frontend is React with TypeScript, the server is Python.

```
 Browser (React + TypeScript)   Local server (Python, FastAPI)   Services
 ----------------------------   ----------------------------     --------
 Press-to-talk mic         <->  Holds the API keys            <->  1. ElevenLabs speech-to-text
 Typed fallback box             Session state in memory       <->  2. Gemini (judge + kid reply, one structured call)
 Avatar, round tracker          Planner call at start         <->  3. ElevenLabs text-to-speech (kid voice)
 Live transcript                Enforces 2 follow-up cap
 Plays the kid audio            Builds the gap report
 Gap report page
```

Each turn runs steps 1 to 3 in order through the server. The planner runs once before round 1.

### Tech stack

- **Server:** Python with **FastAPI**, run on the demo laptop. No deployment, no database. FastAPI is easy to read, and it checks incoming and outgoing data against the Pydantic models for free.
- **Data shapes on the server:** **Pydantic** models, defined first. They document the data and validate it, including the structured output coming back from Gemini.
- **Frontend:** **React with TypeScript**, built with **Vite**, with plain CSS. The app is a few state-driven screens made of small components, which is what React is good at and keeps the code composable. If React feels like too much, the fallback is plain TypeScript with HTML and CSS; the server doesn't change either way.
- **State on the frontend:** React's built-in state only. No state library, no CSS framework (YAGNI).
- **Two languages, one set of shapes:** the data shapes (rubric, judgment, report) are defined once as Pydantic models, and mirrored by hand in one small TypeScript types file in the browser. Both sides use the same `snake_case` field names in the JSON, so nothing needs converting. Generating the TypeScript from the server is not worth the setup (YAGNI).
- **Keys:** Gemini and ElevenLabs keys live in a local env file that is excluded from git.
- **Services:** Gemini is the brain (planning, judging, report). ElevenLabs does speech-to-text for the learner and text-to-speech for the kid, using the MLH promo credits. Use the official Python SDKs or plain HTTP calls, whichever is simpler to read.
- **Recording audio:** the browser's built-in audio recording.
- **Tooling:** **Ruff** (formats and checks the Python in one tool) and **pytest** on the server; **Prettier** and **ESLint** on the frontend. No frontend test suite, since the logic lives on the server (YAGNI).
- **Demo browser:** Chrome on the demo laptop.

### Suggested project layout (a starting point, not a rule)

```
feynman/
  docs/                    SPEC.md, DECISIONS.md, DISCUSSION_HISTORY.md
  server/
    models/                Pydantic models: rubric, judgment, session, report
    routes/                Thin: receive a request, call one function, return the result
    session/               Session state and turn flow (the rules)
    planning/              plan_rounds: notes in, four rounds out
    judging/               judge_answer: answer in, structured judgment out
    report/                build_gap_report
    services/              Interfaces plus one adapter file each for Gemini, ElevenLabs speech-to-text, ElevenLabs text-to-speech
    tests/                 pytest tests and the fake adapters
  client/
    components/            Small pieces: KidAvatar, RoundTracker, Transcript, MicButton, TypedAnswerBox, RoundCard...
    screens/               NotesScreen, SessionScreen, ReportScreen (each assembled from components)
    api/                   One small file that calls the server, and the mirrored types file
```

### Modules

1. **Data models:** written first. The rubric, round, judgment, session, and report shapes as Pydantic models on the server, mirrored in one TypeScript file on the client.
2. **Session state:** in memory on the server. Holds the notes, the rubric, the current round, the follow-up count, covered points so far, and every judged answer. One session at a time is enough.
3. **Planner (`plan_rounds`):** one Gemini call when the session starts. Reads the notes and returns all four rounds. Saves the rubric to a file the team can open.
4. **Judge (`judge_answer`):** one Gemini call per turn with structured output. Decides covered points, parroting, the next move, and the kid's reply text.
5. **Turn flow:** applies the rules (move on, follow up, or fuzzy after 2 follow-ups) with plain `if` statements on the judge's fields. Depends only on the interfaces below.
6. **Service interfaces and adapters:** `SpeechToText`, `TextToSpeech`, and `LanguageModel`, each a tiny interface (a Python `Protocol`). One adapter file per vendor implements it. Tests use fake adapters.
7. **Report builder (`build_gap_report`):** assembles the gap report from the stored judgments. May use one final Gemini call only to write the re-explain prompts.
8. **Frontend:** three screens (notes, session, report) built from small components. Each component does one visible thing.

### Server endpoints (one browser call each)

- **Start session:** takes the notes; returns round 1's question as text and kid audio.
- **Submit turn:** takes recorded audio or typed text; returns the transcript, the kid's reply text and audio, the avatar mood, the round number, and whether the session is finished.
- **Get report:** returns the report data for the report screen.
- **Load demo rubric:** starts a session from the hand-checked recursion rubric instead of calling the planner.

### Rubric shape (planner output)

Four rounds in fixed order. Each has a type (what, how, why, example), the kid's question, and 2-4 key points tied to that type. A "what" round checks for a definition; an "example" round checks for a concrete case. Round types are a named list, so adding a type means adding an entry, not editing the turn logic.

### Judge output per turn

- `covered_key_points`: which of this round's key points the answer covered
- `parroting`: whether the answer mirrored the notes, plus the user phrase and the matching note line when it did
- `decision`: `move_on` or `follow_up`
- `kid_reply_text`: 1-2 short sentences, either a confused question about one missing point or "oh I get it" plus a restatement in the user's words

The server, not Gemini, enforces the cap. When `decision` is `follow_up` and the round already had `MAX_FOLLOW_UPS_PER_ROUND` (2) follow-ups, the server marks the round fuzzy and replaces the reply with the named fuzzy line: "I'm still a bit fuzzy on that, but let's try the next part!"

### Kid rules (in the judge prompt)

- One fixed character with one ElevenLabs voice.
- Only two moods in speech: confused, or "oh I get it".
- Never corrects, never teaches, never adds facts from the notes, and never says the answer sounds like the notes. Parroting is only reported at the end.
- The restatement uses only the user's own words.

### Report rules

- Round status: covered (all key points, no follow-ups needed or fixed after them), partly covered (some points), fuzzy (hit the cap).
- Missed points come straight from the rubric minus what was covered.
- Parroting flags show the user's phrase next to the matching note line.
- One re-explain prompt per gap, phrased as a question to retry, never as the answer.
- No score.

### ElevenLabs API key permissions

Only two permissions are needed: **Text to Speech** and **Speech to Text**. Everything else stays at "No Access" (turn Speech to Speech off). Optional extras: Voices (Read) and Models, only if the server looks them up through the API; it's simpler to paste the voice ID and model name into config. Keep Workspace, Service Accounts, Webhooks, Workspace Members, User and Terms of Service Accept off. If a voice comes from the public library, add it to your own voices on the website first.

## Testing Decisions

Test at one seam: the server's endpoints, using **pytest** and FastAPI's test client, with Gemini and ElevenLabs swapped for fake adapters that return canned answers. The fakes implement the same small interfaces as the real adapters, which is why the turn logic can be tested without any network. This is a proposal; confirm it before building.

- **What a good test checks:** what the endpoints return for a given input (the reply, the round number, the mood, the report contents), not how the code is arranged inside.
- **Test names read like sentences:** for example, `test_moves_to_next_round_when_answer_covers_every_key_point`.
- **Why fakes:** real AI calls are slow, cost credits, and give different answers each time. A fake judge that returns fixed fields makes the turn logic testable in seconds.
- **Turn-flow tests (the most important):**
    - A `move_on` judgment advances to the next round.
    - A `follow_up` judgment stays on the round and counts the follow-up.
    - A third `follow_up` in one round marks it fuzzy, uses the fuzzy line, and advances.
    - After round 4 the session is marked finished.
- **Report tests:** missed points equal rubric points minus covered points; a parroted answer appears with its phrase and note line; a fuzzy round gets a re-explain prompt; no score field exists.
- **Typed fallback test:** a typed answer skips speech-to-text and goes through the same turn flow.
- **Prompt quality is tested by rehearsal, not code.** Run the four demo answers (good, vague, weak, parroted) against the real services and read the results. If Gemini passes a weak answer or misses parroting, fix the prompt.
- **Leak check during rehearsal:** confirm the kid never states a fact from the notes that the learner didn't say.
- **Prior art:** none; this is a new project. Keep tests to a handful; the turn-flow ones matter most.

## Build Order

Build thin slices that always run: logic first, then voice, then polish. **Every slice ends with the "could I replicate this?" check** from Code Quality Requirements before the next one starts.

- [ ] **0. Setup (both):** install Python and Node, create the FastAPI server in a virtual environment and the Vite React TypeScript app, turn on TypeScript strict mode, set up Ruff, pytest, Prettier and ESLint, get Gemini and ElevenLabs keys working with the promo code, create the env file, add it to gitignore, pick the kid's ElevenLabs voice. Paste the AI rules block into your assistant.
- [ ] **1. Hello server:** the data models (and their mirrored TypeScript file), a page with a button that calls the server and shows a reply.
- [ ] **2. Planner:** paste notes, start, Gemini returns the four rounds, the rubric is saved to a file and shown in the console.
- [ ] **3. Text-only loop:** type answers, the judge returns structured fields, the server applies move on / follow up / fuzzy at 2, the transcript fills in. Add the turn-flow tests here.
- [ ] **4. Report:** round cards, missed points, parroting flags, re-explain prompts on a scrolling page.
- [ ] **5. Kid's voice out:** every kid reply is spoken with ElevenLabs text-to-speech.
- [ ] **6. Voice in:** press-to-talk records audio, ElevenLabs speech-to-text transcribes it, the typed box stays as fallback.
- [ ] **7. Readability pass (both, short):** read the whole codebase once. Rename anything unclear, delete dead code, merge real duplicates, split anything too long.
- [ ] **8. Demo prep:** write the recursion notes, hand-check the rubric and save it as the demo rubric, rehearse the four answers, fix prompts.
- [ ] **9. Polish:** avatar moods, round tracker styling, thinking animation.

**Cut line:** only polish can be cut. If time is short, the avatar becomes one static image and styling stays basic. The planner, judge, report, voice out, voice in, and the readability pass are all required.

### Demo script (one behavior per round)

| Round | Question | Planned answer | Shows |
| --- | --- | --- | --- |
| 1 | What is recursion? | Good, original explanation | Covered on first try |
| 2 | How does it relate to loops? | Vague ("a loop that calls itself"), then a fix | One follow-up, then covered |
| 3 | What is it for? | Two weak answers | Fuzzy after the 2 follow-up cap |
| 4 | Give an example | Read close to the notes | Parroting flag in the report |

The less technical teammate is the learner on stage. Rehearse talking points (2-3 bullets per round), not scripts.

## Out of Scope

- Selectable kid levels or more than one character (stretch goal only if everything else is done).
- Adaptive difficulty.
- The kid interrupting mid-sentence, or any streaming audio. The conversation is turn-based.
- Progress tracking across sessions, accounts, or a database.
- Deployment, hosting, or a custom domain. The app runs on the demo laptop.
- An overall score or grade.
- Handling thin notes. The team controls the notes and always provides enough for 4 rounds.
- Hardware from the lab.
- A state-management library, a CSS framework, a frontend test suite, generating TypeScript types from the server, or any other tooling the spec doesn't call for.

## Further Notes

- **Latency:** each turn chains speech-to-text, Gemini, and text-to-speech, so expect a few seconds. Short kid replies and the thinking state keep it feeling alive.
- **If the kid leaks answers in rehearsal:** split the judge into two calls, where the reply-writing call never sees the notes. It's a contained change.
- **Working with AI:** let it write larger chunks if you fall behind, but the explain-back and rewrite check still apply, so both of you can explain the code to judges. If the AI produces something you can't explain, ask it to simplify rather than accepting it.
- **Learning curve:** React is the new part for a team with static-site experience. Components are just functions that return page pieces, and the AI can explain each one as it's written. The Python server stays the language the stronger teammate is most comfortable in.
- **On stage:** the technical teammate runs the laptop and takes architecture questions; the learner should still be able to say "browser, server, Gemini, ElevenLabs" in their own words.
- **Tracks this enters by default:** Best Overall, Beginner, Best Use of Gemini API, Best Use of ElevenLabs. Prizes are not the goal.
- **Open item:** the avatar style (drawn or generated), four mood images.
- **Issue tracker:** there's no repo yet, so this file is the spec. It can be split into tickets once the repo exists.