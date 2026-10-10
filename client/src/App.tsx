import { useState } from "react";
import { checkHealth } from "./api/server.ts";

function App() {
  const [serverReply, setServerReply] = useState("");

  async function askServer() {
    try {
      const healthCheck = await checkHealth();
      setServerReply(`Server says: ${healthCheck.status}`);
    } catch (error) {
      setServerReply(`Could not reach the server: ${String(error)}`);
    }
  }

  return (
    <main>
      <h1>Feynman</h1>
      <button type="button" onClick={askServer}>
        Ask the server
      </button>
      <p>{serverReply}</p>
    </main>
  );
}

export default App;
