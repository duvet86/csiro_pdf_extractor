import type { Route } from "./+types/job-summary";

interface Job {
  id: string;
  file_name: string;
  num_pages: number;
  status: string;
}

export async function loader({ params }: Route.LoaderArgs) {
  const resp = await fetch(`http://127.0.0.1:8000/jobs`);

  if (!resp.ok) {
    const text = await resp.text();
    console.error("Error response from backend:", text);

    throw new Response("Failed to upload file", { status: 500 });
  }

  const data = (await resp.json()) as Job[];

  return {
    jobs: data,
  };
}

export default function Index({ loaderData: { jobs } }: Route.ComponentProps) {
  return (
    <main className="p-4">
      <h1>Job Summary</h1>
      <div className="overflow-x-auto rounded-box border border-base-content/5 bg-base-100 p-4 mt-2">
        <table className="table">
          {/* head */}
          <thead>
            <tr>
              <th></th>
              <th>File Name</th>
              <th>Number of Pages</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job, index) => (
              <tr key={job.id}>
                <th>{index + 1}</th>
                <td>{job.file_name}</td>
                <td>{job.num_pages}</td>
                <td>{job.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
