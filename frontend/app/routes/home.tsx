import type { Route } from "./+types/home";

import { Form, redirect } from "react-router";

interface ResponseData {
  filename: string;
  total_pages: number;
  content: string;
}

export async function action({ request }: Route.ActionArgs) {
  const formData = await request.formData();

  const extractionType = formData.get("extractionType");
  const url = !extractionType ? "simple-extraction" : "advanced-extraction";

  console.log("Has file:");

  if (!formData.get("file") || (formData.get("file") as File).size === 0) {
    return {
      message: "File is required",
    };
  }

  const resp = await fetch(`http://127.0.0.1:8000/${url}`, {
    method: "POST",
    body: formData,
  });

  if (!resp.ok) {
    const text = await resp.text();
    console.error("Error response from backend:", text);

    throw new Response("Failed to upload file", { status: 500 });
  }

  const data = (await resp.json()) as ResponseData;

  console.log("Response data:", data);

  return redirect("/summary");
}

export default function Index() {
  return (
    <main>
      <Form method="post" encType="multipart/form-data">
        <fieldset className="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
          <legend className="fieldset-legend">Extract Data</legend>

          <label className="label mb-4">
            <input type="checkbox" className="toggle" name="extractionType" />
            Advanced Extraction
          </label>

          <label className="label">Upload a Bill</label>
          <input type="file" name="file" className="file-input" required />

          <button className="btn btn-primary mt-4" type="submit">
            Submit
          </button>
        </fieldset>
      </Form>
    </main>
  );
}
