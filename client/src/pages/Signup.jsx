import { useNavigate } from "react-router-dom";
import { authApi } from "../api/client";
import AuthCard from "../components/AuthCard";
import Input from "../components/Input";
import Button from "../components/Button";
import { useAuthForm } from "../hooks/useAuthForm";

const Signup = () => {
  const navigate = useNavigate();

  const {
    values,
    loading,
    setLoading,
    error,
    setError,
    handleChange,
  } = useAuthForm({
    full_name: "",
    email: "",
    password: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await authApi.post("/signup", values);
      navigate("/login");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Signup failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthCard title="Create Account">
      <form onSubmit={handleSubmit}>
        <Input
          label="Full Name"
          name="full_name"
          value={values.full_name}
          onChange={handleChange}
        />

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

        <Button loading={loading}>
          Sign Up
        </Button>
      </form>
    </AuthCard>
  );
};

export default Signup;