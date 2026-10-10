import "./ThinkingDots.css";

// Decorative: the visible "Thinking…" or "Preparing…" text next to it says the same thing.
function ThinkingDots() {
  return (
    <span className="thinking-dots" aria-hidden="true">
      <span className="thinking-dots__dot" />
      <span className="thinking-dots__dot" />
      <span className="thinking-dots__dot" />
    </span>
  );
}

export default ThinkingDots;
