# Extract Electricity Bill Data

A project created with FastAPI and Remix/React Router to extract key fields, such as: retailer, billing period, total cost, and total usage from electicity bill uploaded as PDF files.

## Prerequisites

The following software is required to run the application:

- Python 3.10+
- uv package manager
- node js LTS

### Start the development server

Backend server:

```bash
cd backend
uv run fastapi dev
```

Frontend:

```bash
cd frontend
npm run dev
```

## How to

- Visit http://localhost:5173/.
- Upload an energy bill PDF file. You can select across 2 different modes, simple and advanced.
- Simple mode extracts the data "synchronously" and redirects the user to the summary page.
- Advanced extracts the data "asynchronously" using a background job. The extration might take minutes depending on the server capacity and file size. The user is redirected to the summarty page and the job status is set as pending. Currently, the page does not automatically updates when the background job completes. To view the results, the user needs to refresh the page manually.

## Project Structure

Technologies:

- `backend`
  - Python
  - FastAPI
  - SQLMode
  - SQLLite
- `frontend`
  - Nodejs
  - Remix/React router
  - Tailwind CSS
  - DaisyUI
