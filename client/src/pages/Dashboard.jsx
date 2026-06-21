import { useNavigate } from "react-router-dom";
import Button from "../components/Button";
import { authApi } from "../api/client";
import { useAuth } from "../context/AuthContext";

const Dashboard = () => {
  const navigate = useNavigate();
  const { isAuthenticated, setIsAuthenticated } = useAuth();
  const handleLogout = async () => {
    await authApi.post("/logout");
    setIsAuthenticated(false)
    navigate("/login");
  };

  return (
    <div>
      <h1>CareerLedger Dashboard</h1>

      {isAuthenticated && <Button onClick={handleLogout}>Logout</Button>}
    </div>
  );
};

export default Dashboard;
