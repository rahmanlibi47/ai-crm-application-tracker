import { useNavigate } from "react-router-dom";
import { authApi } from "../api/client";
import AuthCard from "../components/AuthCard";
import Input from "../components/Input";
import Button from "../components/Button";
import { useAuthForm } from "../hooks/useAuthForm";

const Login = () => {
  const navigate = useNavigate();

  const { values, loading, setLoading, error, setError, handleChange } =
    useAuthForm({
      email: "",
      password: "",
    });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await authApi.post("/login", values);

      navigate("/verify-otp", {
        state: {
          email: response.data.email,
        },
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = `${
      import.meta.env.VITE_AUTH_API_URL
    }/oauth/google/login`;
  };

  return (
    <AuthCard title="Login">
      <form onSubmit={handleSubmit}>
        <Input
          label="Email"
          name="email"
          type="email"
          value={values.email}
          onChange={handleChange}
        />

        <Input
          label="Password"
          name="password"
          type="password"
          value={values.password}
          onChange={handleChange}
        />

        {error && <p style={{ color: "red" }}>{error}</p>}

        <Button loading={loading}>Send OTP</Button>
      </form>
      <Button type="button" onClick={handleGoogleLogin}>
        Continue with Google
      </Button>
    </AuthCard>
  );
};

export default Login;
