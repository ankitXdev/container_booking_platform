# Development Setup

## Prerequisites

Install:

- Python 3.10+
- Node.js and npm
- PostgreSQL
- Git
- VS Code or another development environment

## Backend

From the backend directory:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install core dependencies:

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pyjwt pwdlib email-validator
```

After the dependency list is finalized:

```bash
pip freeze > requirements.txt
```

Run:

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Frontend

The planned frontend uses React.

Typical setup:

```bash
npm install
npm run dev
```

The exact command depends on whether the project uses Vite or another React setup.

## Environment Variables

Backend:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>/<database>
JWT_SECRET_KEY=<strong-secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

RAZORPAY_KEY_ID=<razorpay-key>
RAZORPAY_KEY_SECRET=<razorpay-secret>
```

Frontend should use only public/client-safe configuration. Razorpay secret credentials must remain on the backend.

## Git Safety

Add:

```text
.env
venv/
__pycache__/
node_modules/
*.pyc
```

to `.gitignore`.

Never commit real credentials.
