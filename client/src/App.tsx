import { useState } from "react";
import NotesScreen from "./screens/NotesScreen.tsx";

function App() {
  const [kidQuestion, setKidQuestion] = useState("");

  if (kidQuestion === "") {
    return <NotesScreen onSessionStarted={setKidQuestion} />;
  }

  // ponytail: placeholder until the session screen lands (#4).
  return (
    <main>
      <p>{kidQuestion}</p>
    </main>
  );
}

export default App;
