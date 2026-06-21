import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { authApi } from "../api/client";
import AuthCard from "../components/AuthCard";
import Input from "../components/Input";
import Button from "../components/Button";
import { useAuth } from "../context/AuthContext";

const VerifyOtp = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const { setIsAuthenticated } = useAuth();

  const email = location.state?.email;

  const [otp, setOtp] = useState("");
  const [timer, setTimer] = useState(30);
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (timer <= 0) return;

    const intervalId = setInterval(() => {
      setTimer((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(intervalId);
  }, [timer]);

  const handleVerifyOtp = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      await authApi.post("/login/verify-otp", {
        email,
        otp,
      });

      setIsAuthenticated(true);
      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "OTP verification failed"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleResendOtp = async () => {
    setError("");
    setResending(true);

    try {
      await authApi.post("/login/resend-otp", {
        email,
      });

      setTimer(60);
      setOtp("");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Failed to resend OTP"
      );
    } finally {
      setResending(false);
    }
  };

  if (!email) {
    return (
      <AuthCard title="Verify OTP">
        <p>No email found. Please login again.</p>

        <Button onClick={() => navigate("/login")}>
          Go to Login
        </Button>
      </AuthCard>
    );
  }

  return (
    <AuthCard title="Verify OTP">
      <p>OTP sent to {email}</p>

      <form onSubmit={handleVerifyOtp}>
        <Input
          label="OTP"
          name="otp"
          value={otp}
          onChange={(e) => setOtp(e.target.value)}
        />

        <p>
          {timer > 0
            ? `Resend available in ${timer}s`
            : "You can resend OTP now"}
        </p>

        <Button
          type="button"
          disabled={timer > 0 || resending}
          loading={resending}
          onClick={handleResendOtp}
        >
          Resend OTP
        </Button>

        {error && <p style={{ color: "red" }}>{error}</p>}

        <Button loading={loading}>
          Verify OTP
        </Button>
      </form>
    </AuthCard>
  );
};

export default VerifyOtp;