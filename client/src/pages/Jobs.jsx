import { useState } from "react";
import { applicationApi } from "../api/client";

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const [what, setWhat] = useState("");
  const [where, setWhere] = useState("");

  async function searchJobs() {
    if (!what.trim()) return;

    setLoading(true);

    try {
      const res = await applicationApi.get("/jobs/search", {
        params: {
          what,
          where,
        },
      });

      setJobs(res.data.results || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function formatSalary(job) {
    if (!job.salary_min && !job.salary_max)
      return "Salary not disclosed";

    if (job.salary_min && job.salary_max) {
      return `₹${Math.round(job.salary_min).toLocaleString()} - ₹${Math.round(
        job.salary_max
      ).toLocaleString()} a year`;
    }

    if (job.salary_min)
      return `From ₹${Math.round(job.salary_min).toLocaleString()} a year`;

    return `Up to ₹${Math.round(job.salary_max).toLocaleString()} a year`;
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-6 md:px-8">
      <div className="mx-auto max-w-6xl">

        <h1 className="text-3xl font-bold">Jobs</h1>
        <p className="mt-1 text-slate-500">
          Find your next opportunity
        </p>

        {/* Search */}

        <div className="mt-8 rounded-2xl bg-white p-4 shadow-sm border flex flex-col gap-4 md:flex-row">

          <input
            type="text"
            placeholder="Job title (e.g. Python Developer)"
            value={what}
            onChange={(e) => setWhat(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") searchJobs();
            }}
            className="flex-1 rounded-xl border px-4 py-3 outline-none focus:border-blue-600"
          />

          <input
            type="text"
            placeholder="Location (optional)"
            value={where}
            onChange={(e) => setWhere(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") searchJobs();
            }}
            className="flex-1 rounded-xl border px-4 py-3 outline-none focus:border-blue-600"
          />

          <button
            onClick={searchJobs}
            disabled={loading}
            className="rounded-xl bg-blue-700 px-8 py-3 font-semibold text-white hover:bg-blue-800 disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search"}
          </button>

        </div>

        {/* Results */}

        {jobs.length > 0 && (
          <div className="mt-6 space-y-4">

            {jobs.map((job) => (
              <div
                key={job.id}
                className="flex flex-col gap-4 rounded-2xl border bg-white p-5 shadow-sm md:flex-row md:items-center md:justify-between"
              >
                <div>
                  <h2 className="text-xl font-bold">
                    {job.title}
                  </h2>

                  <p className="mt-2 font-medium text-slate-700">
                    {job.company?.display_name}
                  </p>

                  <p className="mt-2 text-slate-600">
                    📍 {job.location?.display_name}
                  </p>

                  <p className="mt-2">
                    💼 {formatSalary(job)}
                  </p>
                </div>

                <a
                  href={job.redirect_url}
                  target="_blank"
                  rel="noreferrer"
                  className="w-full rounded-xl bg-blue-700 px-8 py-3 text-center font-semibold text-white hover:bg-blue-800 md:w-auto"
                >
                  Apply
                </a>
              </div>
            ))}

          </div>
        )}

        {!loading && jobs.length === 0 && (
          <div className="mt-16 text-center text-slate-500">
            Search for a job to get started.
          </div>
        )}

      </div>
    </div>
  );
};

export default Jobs;