import { useState } from "react";
import { applicationApi } from "../api/client";

const Jobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(false);

  const [what, setWhat] = useState("");
  const [where, setWhere] = useState("");
  const [page, setPage] = useState(1);

  async function searchJobs(newPage = 1) {
    if (!what.trim()) return;

    setLoading(true);

    try {
      const res = await applicationApi.get("/jobs/search", {
        params: {
          what,
          where,
          page: newPage,
        },
      });

      setJobs(Array.isArray(res.data) ? res.data : []);
      setPage(newPage);
    } catch (err) {
      console.error(err);
      setJobs([]);
    } finally {
      setLoading(false);
    }
  }

  function formatSalary(job) {
    return job.salary || "Salary not disclosed";
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-6 md:px-8">
      <div className="mx-auto max-w-6xl">

        <h1 className="text-3xl font-bold">
          Jobs
        </h1>

        <p className="mt-1 text-slate-500">
          Find your next opportunity
        </p>

        <div className="mt-8 flex flex-col gap-4 rounded-2xl border bg-white p-4 shadow-sm md:flex-row">

          <input
            type="text"
            placeholder="Job title (e.g. Python Developer)"
            value={what}
            onChange={(e) => setWhat(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") searchJobs(1);
            }}
            className="flex-1 rounded-xl border px-4 py-3 outline-none focus:border-blue-600"
          />

          <input
            type="text"
            placeholder="Location (optional)"
            value={where}
            onChange={(e) => setWhere(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") searchJobs(1);
            }}
            className="flex-1 rounded-xl border px-4 py-3 outline-none focus:border-blue-600"
          />

          <button
            onClick={() => searchJobs(1)}
            disabled={loading}
            className="rounded-xl bg-blue-700 px-8 py-3 font-semibold text-white hover:bg-blue-800 disabled:opacity-50"
          >
            {loading ? "Searching..." : "Search"}
          </button>

        </div>

        {jobs.length > 0 && (
          <>
            <div className="mt-6 space-y-4">

              {jobs.map((job) => (
                <div
                  key={`${job.source}-${job.id}`}
                  className="flex flex-col gap-4 rounded-2xl border bg-white p-5 shadow-sm md:flex-row md:items-center md:justify-between"
                >
                  <div>

                    <div className="flex items-center gap-2">

                      <h2 className="text-xl font-bold">
                        {job.title}
                      </h2>

                      <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-600 capitalize">
                        {job.source}
                      </span>

                    </div>

                    <p className="mt-2 font-medium text-slate-700">
                      {job.company}
                    </p>

                    <p className="mt-2 text-slate-600">
                      📍 {job.location || "Remote"}
                    </p>

                    <p className="mt-2">
                      💼 {formatSalary(job)}
                    </p>

                  </div>

                  <a
                    href={job.apply_url}
                    target="_blank"
                    rel="noreferrer"
                    className="w-full rounded-xl bg-blue-700 px-8 py-3 text-center font-semibold text-white hover:bg-blue-800 md:w-auto"
                  >
                    Apply
                  </a>

                </div>
              ))}

            </div>

            <div className="mt-8 flex items-center justify-center gap-4">

              <button
                disabled={page === 1 || loading}
                onClick={() => searchJobs(page - 1)}
                className="rounded-xl border bg-white px-5 py-2 disabled:opacity-50"
              >
                Previous
              </button>

              <span className="font-semibold">
                Page {page}
              </span>

              <button
                disabled={loading}
                onClick={() => searchJobs(page + 1)}
                className="rounded-xl bg-blue-700 px-5 py-2 text-white disabled:opacity-50"
              >
                Next
              </button>

            </div>
          </>
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