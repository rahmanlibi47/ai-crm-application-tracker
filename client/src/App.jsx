import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import { useAuth } from "./context/AuthContext";
import { useEffect } from "react";
import OAuthSuccess from "./components/OAuthSuccess";

const App = () => {
  const { isAuthenticated, setIsAuthenticated, authChecked, setAuthChecked } = useAuth();

  useEffect(() => {
    async function checkAuth() {
      const res = await fetch(`${import.meta.env.VITE_AUTH_API_URL}/me`, {
        credentials: "include",
      });

      setIsAuthenticated(res.ok);
      setAuthChecked(true);
    }

    checkAuth();
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            !authChecked ? null : isAuthenticated ? (
              <Navigate to="/dashboard" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/oauth/success" element={<OAuthSuccess />} />

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
