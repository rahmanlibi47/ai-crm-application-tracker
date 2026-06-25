import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const OAuthSuccess = () => {
  const navigate = useNavigate();
  const { setIsAuthenticated } = useAuth();

  useEffect(() => {
    setIsAuthenticated(true);
    navigate("/dashboard", { replace: true });
  }, []);

  return <div>Logging you in...</div>;
};

export default OAuthSuccess;