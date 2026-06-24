import { useNavigate } from "react-router-dom";
import { LogOut } from "lucide-react";

import { authApi } from "../api/client";
import { useAuth } from "../context/AuthContext";

const Dashboard = () => {
  const navigate = useNavigate();
  const { isAuthenticated, setIsAuthenticated } = useAuth();

  const handleLogout = async () => {
    await authApi.post("/logout");

    setIsAuthenticated(false);

    navigate("/login");
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <h1 className="text-xl font-semibold">
            CareerLedger
          </h1>

          {isAuthenticated && (
            <button
              onClick={handleLogout}
              className="
                p-2
                rounded-lg
                hover:bg-slate-100
                transition
              "
              title="Logout"
            >
              <LogOut size={20} />
            </button>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <h2 className="text-3xl font-bold">
          Welcome Back 👋
        </h2>

        <p className="text-slate-500 mt-2">
          Manage your applications, resumes and interviews.
        </p>

        <div className="grid md:grid-cols-3 gap-6 mt-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-sm text-slate-500">
              Applications
            </h3>

            <p className="text-3xl font-bold mt-2">
              0
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-sm text-slate-500">
              Interviews
            </h3>

            <p className="text-3xl font-bold mt-2">
              0
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h3 className="text-sm text-slate-500">
              Resumes
            </h3>

            <p className="text-3xl font-bold mt-2">
              0
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;