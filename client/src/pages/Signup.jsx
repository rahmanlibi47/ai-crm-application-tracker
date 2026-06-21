import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "../api/client";

function Signup() {
  const navigate = useNavigate();

  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSignup(e) {
    e.preventDefault();

    await authApi.post("/signup", {
      full_name: fullName,
      email,
      password,
    });

    alert("Signup successful. Please verify your email");
    navigate("/login");
  }

  return (
    <form onSubmit={handleSignup}>
      <h1>Signup</h1>

      <input
        placeholder="Full name"
        value={fullName}
        onChange={(e) => setFullName(e.target.value)}
      />

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

      <button type="submit">Create Account</button>
    </form>
  );
}

export default Signup;
