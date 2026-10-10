import { useState } from "react";
import NotesScreen from "./screens/NotesScreen.tsx";
import SessionScreen from "./screens/SessionScreen.tsx";

function App() {
  const [kidQuestion, setKidQuestion] = useState("");

  if (kidQuestion === "") {
    return <NotesScreen onSessionStarted={setKidQuestion} />;
  }

  return <SessionScreen firstKidQuestion={kidQuestion} />;
}

export default App;
