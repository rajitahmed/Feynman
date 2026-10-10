import type { GapReport } from "../api/types.ts";
import KidAvatar from "../components/KidAvatar.tsx";
import RoundCard from "../components/RoundCard.tsx";
import "./ReportScreen.css";

type ReportScreenProps = {
  report: GapReport;
};

function ReportScreen({ report }: ReportScreenProps) {
  const todayText = new Date().toLocaleDateString(undefined, {
    dateStyle: "long",
  });

  return (
    <main className="report-screen">
      <header className="card report-screen__card report-screen__header">
        <KidAvatar mood="got_it" shouldPlayOnce />
        <div>
          <h1 className="report-screen__title">Thanks for teaching me!</h1>
          <p className="report-screen__muted">{todayText}</p>
        </div>
      </header>

      <section className="card report-screen__card">
        <h2 className="card-label report-screen__label">How each round went</h2>
        <div className="report-screen__round-cards">
          {report.round_cards.map((roundCard) => (
            <RoundCard key={roundCard.round_number} roundCard={roundCard} />
          ))}
        </div>
      </section>

      <section className="card report-screen__card">
        <h2 className="card-label report-screen__label">
          Ideas you didn't mention
        </h2>
        {report.missed_key_points.length === 0 ? (
          <p>You covered every idea in your notes!</p>
        ) : (
          <ul className="report-screen__missed-points">
            {report.missed_key_points.map((keyPoint) => (
              <li key={keyPoint}>{keyPoint}</li>
            ))}
          </ul>
        )}
      </section>

      {report.parroting_flags.length > 0 && (
        <section className="card report-screen__card">
          <h2 className="card-label report-screen__label">
            Sounded like your notes
          </h2>
          {report.parroting_flags.map((parroting, flagIndex) => (
            // Flags never reorder, so their position is a stable key.
            <div key={flagIndex} className="report-screen__parroting">
              <blockquote className="report-screen__you-said">
                <p className="card-label report-screen__label">You said</p>
                <q>{parroting.user_phrase}</q>
              </blockquote>
              <blockquote className="report-screen__your-notes">
                <p className="card-label report-screen__label">Your notes</p>
                <q>{parroting.note_line}</q>
              </blockquote>
            </div>
          ))}
        </section>
      )}

      {report.re_explain_prompts.length > 0 && (
        <section className="card report-screen__card">
          <h2 className="card-label report-screen__label">
            Try re-explaining this
          </h2>
          <ul className="report-screen__re-explain-prompts">
            {report.re_explain_prompts.map((reExplainPrompt) => (
              <li key={reExplainPrompt}>
                <span aria-hidden="true">🎤</span> {reExplainPrompt}
              </li>
            ))}
          </ul>
        </section>
      )}

      <p className="report-screen__muted report-screen__footer">
        No score here, just the parts to practice next.
      </p>
    </main>
  );
}

export default ReportScreen;
