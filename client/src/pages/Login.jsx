import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FcGoogle } from "react-icons/fc";

import { authApi } from "../api/client";
import { useAuthForm } from "../hooks/useAuthForm";
import { useAuth } from "../context/AuthContext";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";

const Login = () => {
  const navigate = useNavigate();
  const { setIsAuthenticated } = useAuth();

  const [step, setStep] = useState("credentials");
  const [otp, setOtp] = useState("");
  const [timer, setTimer] = useState(0);
  const [resending, setResending] = useState(false);

  const { values, loading, setLoading, error, setError, handleChange } =
    useAuthForm({
      email: "",
      password: "",
    });

  useEffect(() => {
    if (timer <= 0) return;

    const intervalId = setInterval(() => {
      setTimer((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(intervalId);
  }, [timer]);

  const handleLoginSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      await authApi.post("/login", values);

      setStep("otp");
      setTimer(60);
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();

    setError("");
    setLoading(true);

    try {
      await authApi.post("/login/verify-otp", {
        email: values.email,
        otp,
      });

      setIsAuthenticated(true);
      navigate("/dashboard");
    } catch (err) {
      setError(
        err.response?.data?.detail || "OTP verification failed"
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
        email: values.email,
      });

      setTimer(60);
      setOtp("");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Failed to resend OTP"
      );
    } finally {
      setResending(false);
    }
  };

  const handleGoogleLogin = () => {
    window.location.href = `${
      import.meta.env.VITE_AUTH_API_URL
    }/oauth/google/login`;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-50 px-4">
      <Card className="w-full max-w-md shadow-lg">
        <CardHeader>
          <CardTitle className="text-2xl text-center">
            {step === "credentials" ? "Welcome back" : "Verify OTP"}
          </CardTitle>

          <p className="text-center text-sm text-muted-foreground">
            {step === "credentials"
              ? "Login to continue to CareerLedger"
              : `OTP sent to ${values.email}`}
          </p>
        </CardHeader>

        <CardContent className="space-y-5">
          {step === "credentials" ? (
            <>
              <form onSubmit={handleLoginSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    name="email"
                    type="email"
                    placeholder="you@example.com"
                    value={values.email}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    name="password"
                    type="password"
                    placeholder="Enter your password"
                    value={values.password}
                    onChange={handleChange}
                    required
                  />
                </div>

                {error && <p className="text-sm text-red-600">{error}</p>}

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? "Sending OTP..." : "Sign in"}
                </Button>
              </form>

              <div className="relative">
                <Separator />
                <span className="absolute left-1/2 -translate-x-1/2 -top-3 bg-card px-2 text-sm text-muted-foreground">
                  or 
                </span>
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={handleGoogleLogin}
              >
                <FcGoogle className="mr-2 h-5 w-5" />
                Continue with Google
              </Button>

              <p className="text-center text-sm text-muted-foreground">
                Don&apos;t have an account?{" "}
                <button
                  type="button"
                  onClick={() => navigate("/signup")}
                  className="font-medium text-primary hover:underline"
                >
                  Sign up
                </button>
              </p>
            </>
          ) : (
            <form onSubmit={handleVerifyOtp} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="otp">OTP</Label>
                <Input
                  id="otp"
                  name="otp"
                  value={otp}
                  onChange={(e) => setOtp(e.target.value)}
                  placeholder="Enter OTP"
                  required
                />
              </div>

              <p className="text-sm text-muted-foreground">
                {timer > 0
                  ? `Resend available in ${timer}s`
                  : "You can resend OTP now"}
              </p>

              {error && <p className="text-sm text-red-600">{error}</p>}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? "Verifying..." : "Verify OTP"}
              </Button>

              <Button
                type="button"
                variant="outline"
                className="w-full"
                disabled={timer > 0 || resending}
                onClick={handleResendOtp}
              >
                {resending ? "Resending..." : "Resend OTP"}
              </Button>

              <button
                type="button"
                onClick={() => {
                  setStep("credentials");
                  setOtp("");
                  setError("");
                }}
                className="w-full text-sm text-muted-foreground hover:text-primary"
              >
                Change email or password
              </button>
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Login;