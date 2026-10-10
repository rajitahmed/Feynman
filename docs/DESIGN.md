# Feynman: Design Guide

Companion to `SPEC.md`. This file says how the app should **look and feel**. The spec says what it does. If they ever disagree, the spec wins.

Suggested location: `docs/DESIGN.md`.

## The idea in one sentence

**It feels like a video call with a cartoon kid.** The layout borrows from Zoom (a big video tile, a small "you" tile, a control bar with a mic button, a chat-style transcript). The personality borrows from Duolingo (bright colors, chunky rounded buttons, bold numbers, a character who reacts to you). The gap report reads like a friendly certificate with no score on it.

## Principles

1. **The kid is the star.** On the session screen, the kid's tile is the biggest thing. You should always be able to tell its mood at a glance.
2. **One obvious action.** Each screen has one big button: **Start** on the notes screen, the **mic** on the session screen, and none on the report screen, which you just read.
3. **Playful, never judgy.** Use soft colors for gaps, write labels in friendly words, and show no score, grades or red X marks. "Fuzzy" is a status, not a failure.
4. **Always show what's happening.** Preparing, listening, thinking and speaking each get a visible state, so a slow turn never looks broken.
5. **Simple CSS.** Use plain CSS, with design tokens in one file and one CSS file per component. No framework and no animation library (see the spec).

## Look and feel references

| Borrow from | What we take | What we don't take |
| --- | --- | --- |
| **Zoom / video calls** | A big speaker tile, a small self tile, a name tag in the tile's corner, a highlighted border on whoever is talking, a bottom control bar, a side panel for chat (our transcript) | The dark, corporate chrome; extra buttons (no leave, camera, share or reactions) |
| **Duolingo** | Bright flat colors, chunky buttons with a darker bottom edge, a rounded bold font, big bold numbers with small uppercase labels, a character who reacts, speech bubbles | Their logo, owl, name or exact brand green. Our look takes its colors from the propeller beanie instead. |
| **The Duolingo English Test certificate** | The report layout: a header card, a row of four equal summary cards, then clean sections underneath | The score gauge and the numbers (we have no score) |

## Design tokens

Put all of these in **one file**, `client/src/styles/tokens.css`, and nowhere else (DRY). Components use only `var(--...)` and never raw hex values.

```css
:root {
  /* Beanie colors: the brand palette */
  --color-red: #e74c3c;
  --color-yellow: #f5c428;
  --color-blue: #3498db;
  --color-green: #2ecc71;

  /* Darker edges for chunky buttons */
  --color-red-edge: #b83a2d;
  --color-yellow-edge: #c99d14;
  --color-blue-edge: #2477ad;
  --color-green-edge: #22a259;

  /* Avatar greys (from the sprite) */
  --color-avatar-light: #d1d2d4;
  --color-avatar-dark: #a7a8ac;

  /* Surfaces and text */
  --color-page: #faf8f3;        /* warm off-white page */
  --color-card: #ffffff;
  --color-stage: #2b3044;       /* the "video" background behind the kid */
  --color-border: #e6e4de;
  --color-text: #2f3140;
  --color-text-muted: #6d6f7b;

  /* Round status colors (the report and the round tracker) */
  --color-status-covered: var(--color-green);
  --color-status-partly: var(--color-yellow);
  --color-status-fuzzy: #f08a7e;   /* soft coral, never harsh red */

  /* Type */
  --font-family: "Nunito", system-ui, sans-serif;
  --font-size-label: 0.8rem;     /* UPPERCASE labels */
  --font-size-body: 1rem;
  --font-size-large: 1.25rem;
  --font-size-title: 1.75rem;
  --font-size-display: 2.75rem;  /* big bold card text */

  /* Spacing (4px steps) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;

  /* Shape */
  --radius-card: 16px;
  --radius-button: 14px;
  --radius-pill: 999px;
  --border-width: 2px;
  --button-edge: 4px;            /* the chunky bottom edge */

  /* Motion */
  --duration-fast: 120ms;
  --duration-normal: 250ms;
  --sprite-frame-duration: 110ms;
}
```

### Typography

- **Font:** Nunito from Google Fonts, weights 400, 700 and 800. It's rounded and friendly, close to Duolingo's feel. If you're offline at the demo, the system font fallback is fine.
- **Headings and big text:** weight 800.
- **Labels:** small, UPPERCASE, weight 700, `letter-spacing: 0.06em`, muted color, like `SPEAKING` on the certificate.
- **Body:** weight 400, line height 1.5.
- Use sentence case everywhere except the uppercase labels.

### Surfaces

- **Cards:** white, `--border-width` solid `--color-border`, `--radius-card`, and no drop shadow. Flat and outlined, Duolingo style.
- **Page:** `--color-page`.
- **The kid's video tile** is the only dark surface (`--color-stage`), so the grey avatar and the colorful beanie stand out like a person on camera.

### Buttons

One chunky button style, with color variants:

```css
.button {
  font: 800 var(--font-size-large) var(--font-family);
  color: white;
  border: none;
  border-radius: var(--radius-button);
  padding: var(--space-3) var(--space-8);
  box-shadow: 0 var(--button-edge) 0 var(--button-edge-color);
  transition: transform var(--duration-fast), box-shadow var(--duration-fast);
}
.button:active {
  transform: translateY(var(--button-edge));
  box-shadow: 0 0 0 var(--button-edge-color);
}
.button:disabled {
  background: var(--color-avatar-light);
  --button-edge-color: var(--color-avatar-dark);
}
```

- **Primary (Start):** green background, green edge.
- **Mic:** blue when idle and red while recording (see below).
- **Secondary (Use demo rubric, Send typed answer):** white background, `--color-border` outline, text-colored label, and a grey edge.

## The kid sprite

**Asset:** `sprite_sheet.png` goes in `client/public/sprites/kid.png`. It has 6 columns and 3 rows, each frame 256×256, on a transparent background.

| Row | Animation | Used for these moods |
| --- | --- | --- |
| 0 | Generic (bobbing, slow propeller) | `listening`, `thinking`, and idle |
| 1 | Confused (head tilt, ? marks, sweat drop) | `confused` |
| 2 | Looks good (bounce, sparkles, smile) | `got_it` |

The spec lists four moods (user story 19), but the sprite has three rows. **Don't draw a fourth row.** `listening` and `thinking` both reuse the generic row and differ by an overlay on the tile:

- **listening:** the generic row, plus a pulsing blue ring around the tile and a small "Listening…" tag.
- **thinking:** the generic row, plus a speech bubble with three bouncing dots and a small "Thinking…" tag.

Map mood to row in **one constant**:

```ts
// client/src/components/kidSpriteRows.ts
export const KID_SPRITE_ROW_BY_MOOD: Record<KidMood, number> = {
  listening: 0,
  thinking: 0,
  confused: 1,
  got_it: 2,
};
```

Play the sprite with CSS only:

```css
.kid-sprite {
  --frame-size: 320px;           /* display size; the source is 256px */
  width: var(--frame-size);
  height: var(--frame-size);
  background-image: url("/sprites/kid.png");
  background-size: calc(var(--frame-size) * 6) calc(var(--frame-size) * 3);
  background-position-y: calc(var(--frame-size) * var(--sprite-row) * -1);
  animation: play-sprite-row calc(var(--sprite-frame-duration) * 6) steps(6) infinite;
}
@keyframes play-sprite-row {
  from { background-position-x: 0; }
  to   { background-position-x: calc(var(--frame-size) * -6); }
}
@media (prefers-reduced-motion: reduce) {
  .kid-sprite { animation: none; }
}
```

The component sets `style={{ "--sprite-row": row }}` and nothing else.

**Cut line:** if polish gets cut, the sprite still works as is: show frame 0 of the right row, with no animation.

## Screen 1: Notes

```
┌───────────────────────────────────────────────────────────┐
│                     [kid sprite, generic]                  │
│              "Hi! What are you teaching me today?"         │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ YOUR NOTES                                            │  │
│  │ ┌──────────────────────────────────────────────────┐ │  │
│  │ │ Paste your study notes here...                    │ │  │
│  │ │                                                   │ │  │
│  │ └──────────────────────────────────────────────────┘ │  │
│  │                [   START   ]  (big green)             │  │
│  │                Use demo rubric  (small text link)     │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

- One centered card, max width about 720px. The sprite sits above it at about 160px, in a speech-bubble greeting.
- The textarea is about 12 lines tall, with a 2px border that turns blue on focus.
- **Preparing state (story 3):** the card is replaced by the generic sprite, three bouncing dots and "Preparing your session…". There's no progress bar, because we don't know how long it will take.

## Screen 2: Session (the "call")

```
┌──────────────────────────────────────────────────────────────────────┐
│  ● ● ○ ○   Round 2 of 4: How does it work?                           │  ← round tracker bar
├───────────────────────────────────────────────┬──────────────────────┤
│ ┌───────────────────────────────────────────┐ │ TRANSCRIPT           │
│ │                                           │ │                      │
│ │        ┌──────────────────────────┐       │ │  Kid                 │
│ │        │ "So is it like a loop?"  │       │ │  So is it like...    │
│ │        └────────────┬─────────────┘       │ │                      │
│ │              [ KID SPRITE ]               │ │            You       │
│ │                                           │ │   It calls itself... │
│ │  ▌Pip · Confused                ┌───────┐ │ │                      │
│ │                                 │  You  │ │ │                      │
│ │                                 └───────┘ │ │                      │
│ └───────────────────────────────────────────┘ │                      │
├───────────────────────────────────────────────┴──────────────────────┤
│          [ 🎤  Tap to talk ]        or  Type your answer instead      │  ← control bar
└──────────────────────────────────────────────────────────────────────┘
```

### Round tracker (top bar, like a meeting title)

- Four dots, one per round, in beanie colors (red, yellow, blue, green). The current dot is larger and the future dots are hollow. Finished dots are filled; they don't show the round's status, because the rubric stays hidden (story 20).
- The text reads "Round 2 of 4: How does it work?", weight 800.

### Kid tile (the speaker view)

- A rounded rectangle (`--radius-card`) on `--color-stage`, filling most of the left area at about a 16:10 ratio, with the sprite centered at about 320px.
- **Name tag** in the bottom-left corner, Zoom style: a semi-transparent dark pill with white text, "Pip · Confused". The kid's name is a placeholder; pick one and keep it in one constant.
- **Speech bubble:** the kid's latest line in a white rounded bubble with a tail pointing at the kid, weight 700, at most 2 lines (the spec keeps replies to 1-2 sentences). It appears when the kid starts speaking and stays until your next answer.
- **Active speaker border:** a 4px yellow border around the tile while the kid's audio plays, like Zoom's active speaker highlight.
- Mood overlays (the listening ring and the thinking dots) are described in the kid sprite section.

### You tile (self view)

- A small tile in the bottom-right corner of the kid tile, about 160×100, `--color-avatar-dark`, with "You" in the middle. There's no camera.
- While recording, it gets a 4px blue border that pulses gently, so you're the active speaker.

### Control bar

- A white bar across the bottom with a top border, holding the big mic button in the center.
- **Mic button states:**

| State | Look | Label |
| --- | --- | --- |
| Ready | Blue chunky button with a mic icon | "Tap to talk" |
| Recording | Red, with a pulsing ring around it | "Tap to send" |
| Waiting (kid thinking or speaking) | Disabled grey | "Pip is thinking…" or "Pip is talking…" |

- Next to it is a small text button, "Type your answer instead", which swaps the mic for a single-line text field and a **Send** button. A "Use mic" link swaps it back. Both stay visible, so typing is never hidden (story 9).
- The mic button has `aria-pressed` set to whether you're recording.

### Transcript panel (like Zoom chat)

- About 320px wide on the right, with a white card background and a `TRANSCRIPT` label at the top.
- Messages are chat bubbles: **kid lines on the left** in a light grey bubble, labeled with the kid's name; **your lines on the right** in a light blue bubble, labeled "You".
- It auto-scrolls to the newest message and uses `aria-live="polite"`.
- On narrow screens (under 900px), the panel moves below the tile. We design for the demo laptop and don't polish anything smaller.

## Screen 3: Gap report

It's laid out like the certificate: one long scrolling page (story 27) in a single centered column, about 880px wide.

```
┌───────────────────────────────────────────────────────────┐
│ [sprite: looks good]  Thanks for teaching me!              │  ← header card
│                       October 10, 2026                     │
├───────────────────────────────────────────────────────────┤
│ HOW EACH ROUND WENT                                        │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│ │ ROUND 1  │ │ ROUND 2  │ │ ROUND 3  │ │ ROUND 4  │        │  ← like the four subscores
│ │ What     │ │ How      │ │ Why      │ │ Example  │        │
│ │[Covered] │ │[Covered] │ │ [Fuzzy]  │ │ [Partly] │        │
│ │ • bullet │ │ • bullet │ │ • bullet │ │ • bullet │        │
│ └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
├───────────────────────────────────────────────────────────┤
│ IDEAS YOU DIDN'T MENTION                                   │
│  ○ Every recursive function needs a base case              │
│  ○ ...                                                     │
├───────────────────────────────────────────────────────────┤
│ SOUNDED LIKE YOUR NOTES                                    │
│  ┌─ You said ───────────┐  ┌─ Your notes ──────────────┐  │
│  │ "a function that..." │  │ "A function that calls..." │  │
│  └──────────────────────┘  └───────────────────────────┘  │
├───────────────────────────────────────────────────────────┤
│ TRY RE-EXPLAINING THIS                                     │
│  🎤 How would you explain why recursion needs a stop?      │
│  🎤 ...                                                    │
├───────────────────────────────────────────────────────────┤
│        No score here, just the parts to practice next.    │
└───────────────────────────────────────────────────────────┘
```

### Header card

- The "looks good" sprite (row 2) at about 120px, playing once and then holding its last frame, next to "Thanks for teaching me!" in the title size.
- Today's date below in muted body text, taken from the browser. There's no topic line, because the report data doesn't include a topic (YAGNI).

### Round cards (four in a row)

- Equal width, white, outlined, like the certificate's subscore boxes.
- `ROUND 1` label, then the round type in large weight-800 text ("What", "How", "Why", "Example").
- A **status pill** with a colored background and a dark label. It always has both text and an icon, so color is never the only signal:
  - **Covered:** green, ✓
  - **Partly covered:** yellow, ◐
  - **Fuzzy:** coral, ?
- 1-2 short bullets below.
- They wrap to 2×2 below 900px.

### Ideas you didn't mention

- A plain list in one card. Each item has a hollow circle (not an X) and the key point text.
- If there's nothing missed, show the sentence "You covered every idea in your notes!" instead of an empty list.

### Sounded like your notes (parroting)

- For each flag, two side-by-side boxes: **You said** in a blue-tinted box and **Your notes** in a yellow-tinted box. Quotes are in italic.
- The section title is neutral. Say "sounded like", never "copied".
- Hide the section entirely when there are no flags.

### Try re-explaining this

- One row per gap: a small blue mic icon plus the prompt, written as a question in weight 700.
- These are reading prompts only; there's no record button here (YAGNI).

### Footer

- A muted, centered line: "No score here, just the parts to practice next." (story 26).

## Motion

Keep motion small and purposeful. Everything is plain CSS transitions or keyframes.

| Thing | Motion |
| --- | --- |
| Sprite | Its own 6-frame loop at `--sprite-frame-duration` |
| Mood change | The sprite crossfades over `--duration-normal` |
| Speech bubble | Pops in: scales from 0.9 to 1 and fades in over `--duration-normal` |
| Thinking dots | Three dots bounce one after another |
| Listening ring and recording mic | A gentle 1.2s pulse |
| Buttons | Press down by the edge height on `:active` |
| Report cards | No entrance animation, so the report is readable right away |

Wrap every non-essential animation in `prefers-reduced-motion: reduce` and turn it off there.

## Writing in the UI

- **Voice:** friendly, short and second person ("Paste your study notes here"). One idea per line.
- **The kid's lines** come from the server; the UI never writes kid dialogue. The fuzzy line is the named constant from the spec.
- **Words to avoid:** score, grade, wrong, failed, copied, incorrect.
- **Words to use:** covered, partly covered, fuzzy, try again, sounded like your notes.

## Accessibility basics

- Text contrast is at least 4.5:1. Don't put white text on yellow; yellow pills use dark text.
- Status always has text and an icon, never color alone.
- Every button and field can be reached with the keyboard, with a visible 3px blue focus outline.
- The transcript is an `aria-live="polite"` region, so new lines are announced.
- The sprite `div` has `role="img"` and an `aria-label` such as "Pip looks confused".

## Component checklist

These match the names in the spec. Each has one job and one CSS file.

| Component | Job |
| --- | --- |
| `KidAvatar` | Shows the sprite row for a mood |
| `KidTile` | The video-style tile: the avatar, name tag, speech bubble, mood overlay and speaker border |
| `SpeechBubble` | One line of kid text in a bubble |
| `SelfTile` | The small "You" tile and its recording border |
| `RoundTracker` | Four dots and the round title |
| `MicButton` | Tap to talk and tap to send, with its three states |
| `TypedAnswerBox` | The text field and Send button |
| `Transcript` | The chat-style list of lines |
| `RoundCard` | One report card with its status pill and bullets |
| `StatusPill` | Covered, partly covered or fuzzy |
| `Button` | The chunky button with color variants |

## Rules to paste into your AI assistant for styling

The styling block lives in [AI_RULES.md](AI_RULES.md), next to the spec's block.
