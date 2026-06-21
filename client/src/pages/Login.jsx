import { useState } from "react";
import { authApi } from "../api/client";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin(e) {
    e.preventDefault();

    const response = await authApi.post("/login", {
      email,
      password,
    });

    console.log("token", response.data.access_token)

    alert("Login successful");
  }

  return (
    <form onSubmit={handleLogin}>
      <h1>Login</h1>

      <input
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <input
        placeholder="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button type="submit">Login</button>
    </form>
  );
}

export default Login;