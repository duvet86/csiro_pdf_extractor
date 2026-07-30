# Extract Electricity Bill Data

A project created with FastAPI and Remix/React Router to extract key fields, such as: retailer, billing period, total cost, and total usage from electicity bills uploaded as PDF files.

## Prerequisites

The following software is required to run the application:

- Python 3.10+
- uv package manager
- node js LTS

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

## How to use the app

- Visit http://localhost:5173/.
- Upload an energy bill PDF file. You can select across 2 different modes, simple and advanced.
- Simple mode extracts the data "synchronously" and redirects the user to the summary page.
- Advanced extracts the data "asynchronously" using a background job. The extration might take minutes depending on the server capacity and file size. The user is redirected to the summarty page and the job status is set as pending. Currently, the page does not automatically updates when the background job completes. To view the results, the user needs to refresh the page manually.
- You can click on "Job Sumamry" to view two example extraction jobs demonstrating the two processing methods.

## Running at Scale for Real Participants

The current setup (local SQLite, no auth, single-process FastAPI dev server) is fine for prototyping but would need the following changes before deploying to real users:

### Cloud Hosting

- **Backend** – containerise the FastAPI app (Docker) and deploy to a managed container service (e.g Azure Container Apps). Use a ASGI production server (Uvicorn workers) behind a load balancer so multiple upload requests can be handled concurrently. Or an API management if APIs are to be made public.
- **Frontend** – containerise the Remix/React Router app and deploy to a managed container service (e.g Azure Container Apps).
- **Database** – replace SQLite with a managed relational database (e.g. Azure SQL Server, Azure Database for PostgreSQL) so state is shared across all backend instances and survives container restarts.
- **File storage** – store uploaded PDFs in object storage (Azure Blob) rather than the local filesystem, and pass object URLs to the extraction worker.
- **Background jobs** – replace the in-process background task with a proper task queue (e.g. Celery + Redis) so slow extraction jobs do not block the API and survive server restarts.
- **Private Network** - For maximum security.

### Infrastructure as Code (IaC)

Define all cloud resources (container services, database, queue, object storage, networking, IAM roles) in a declarative IaC tool such as **Bicep**. This makes environments reproducible, version-controlled, and easy to tear down.

### Authentication & Authorisation

- Add an identity provider (e.g. **Auth0**, **Azure Entra**) so only enrolled study participants can upload bills using SSO.
- Issue short-lived JWTs; the FastAPI or Azure Api Management backend validates the token on every request.
- Scope participant data with a `user_id` on every database row so individuals can only view their own results.

### Rough Architecture

```
Participant browser
       │  HTTPS
       ▼
CDN / Load Balancer
  ├─► React Router SSR (container, auto-scaled)
  └─► FastAPI API (container, auto-scaled)
           │
           ├─► PostgreSQL (managed DB)
           ├─► Object Storage (PDFs)
           └─► Task Queue ──► Extraction Worker (container)
```

All resources provisioned via Bicep files in a Virual Private network; participant identity managed by an OIDC provider, with JWT validation middleware on the FastAPI layer.
