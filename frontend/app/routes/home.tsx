import type { Route } from "./+types/home";

import { Form } from "react-router";

interface ResponseData {
  filename: string;
  total_pages: number;
  content: string;
}

export function meta({}: Route.MetaArgs) {
  return [
    { title: "New React Router App" },
    { name: "description", content: "Welcome to React Router!" },
  ];
}

export async function action({ request }: Route.ActionArgs) {
  const resp = await fetch("http://127.0.0.1:8000/advanced-extraction", {
    method: "POST",
    body: await request.formData(),
  });

  if (!resp.ok) {
    const text = await resp.text();
    console.error("Error response from backend:", text);

    throw new Response("Failed to upload file", { status: 500 });
  }

  const data = (await resp.json()) as ResponseData;

  console.log("Response data:", data);

  return {
    data,
  };
}

export default function Index({ actionData }: Route.ComponentProps) {
  return (
    <main>
      <Form method="post" encType="multipart/form-data">
        <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
          <legend className="fieldset-legend">Page details</legend>

          <label className="label">Title</label>
          <input type="file" name="file" className="file-input" />

          <button className="btn" type="submit">
            Submit
          </button>
        </fieldset>
      </Form>

      {actionData?.data && (
        <div>
          <p>Filename: {actionData.data.filename}</p>
          <p>Total Pages: {actionData.data.total_pages}</p>
        </div>
      )}
    </main>
  );
}
