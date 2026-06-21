import { useEffect, useState } from "react";
import { applicationApi } from "../api/client";

function Dashboard() {
  const [applications, setApplications] = useState([]);

  async function fetchApplications() {
    const response = await applicationApi.get("/applications");
    setApplications(response.data);
  }

  useEffect(() => {
    fetchApplications();
  }, []);

  function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "/login";
  }

  return (
    <div>
      <h1>Dashboard</h1>

      <button onClick={logout}>Logout</button>

      <h2>Applications</h2>

      {applications.length === 0 && <p>No applications found.</p>}

      {applications.map((app) => (
        <div key={app.id}>
          <h3>{app.company_name}</h3>
          <p>{app.job_title}</p>
          <p>Status: {app.status}</p>
          {app.job_url && <a href={app.job_url}>Job Link</a>}
          {app.notes && <p>{app.notes}</p>}
        </div>
      ))}
    </div>
  );
}

export default Dashboard;