import type { Route } from "./+types/job-details";

interface Job {
  id: string;
  file_name: string;
  num_pages: number;
  status: string;
  extraction_mode: string;
  created_datetime: string;
  updated_datetime: string;
  extracted_data: {
    id: string;
    page_number: string;
    key: string;
    value: string;
    created_datetime: string;
    updated_datetime: string;
  }[];
}

export async function loader({ params }: Route.LoaderArgs) {
  const resp = await fetch(`http://127.0.0.1:8000/jobs/${params.jobId}`);

  if (!resp.ok) {
    const text = await resp.text();
    console.error("Error response from backend:", text);

    throw new Response("Failed to upload file", { status: 500 });
  }

  const data = (await resp.json()) as Job;

  return {
    job: data,
  };
}

export default function Index({ loaderData: { job } }: Route.ComponentProps) {
  return (
    <main className="p-4">
      <h1>{job.file_name}</h1>
      <p>Number of Pages: {job.num_pages}</p>
      <p>Extraction Mode: {job.extraction_mode}</p>
      <p>Status: {job.status}</p>
      <p>Created At: {job.created_datetime}</p>
      <div className="overflow-x-auto rounded-box border border-base-content/5 bg-base-100 p-4 mt-2">
        <table className="table">
          {/* head */}
          <thead>
            <tr>
              <th></th>
              <th>Page Number</th>
              <th>Key</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            {job.extracted_data.map((data, index) => (
              <tr key={job.id}>
                <th>{index + 1}</th>
                <td>{data.page_number}</td>
                <td>{data.key}</td>
                <td>{data.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
