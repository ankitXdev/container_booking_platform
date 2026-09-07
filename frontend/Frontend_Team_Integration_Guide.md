# Frontend Authentication Integration Guide

## 1. Purpose

This document explains how the React frontend is connected to the FastAPI backend authentication APIs.

The current authentication flow contains:

- Login
- Account type selection
- Registration
- Authentication token storage
- Protected dashboard route
- Logout
- API error handling
- CORS configuration

The goal is that another developer can clone/open the frontend, understand where each piece belongs, run it, and connect it to the backend without guessing.

---

# 2. Technologies

Frontend:

- React
- Vite
- React Router
- JavaScript
- Fetch API
- CSS

Backend:

- FastAPI
- SQLAlchemy
- PostgreSQL

Development URLs:

```text
Frontend: http://localhost:5173
Backend:  http://127.0.0.1:8000
```

If the backend is running on another port, update the API URL in:

```text
src/services/authService.js
```

---

# 3. Frontend Directory Structure

The frontend should be organized like this:

```text
frontend/
├── public/
├── src/
│   ├── assets/
│   │   └── auth.css
│   │
│   ├── components/
│   │   └── auth/
│   │       ├── AuthLayout.jsx
│   │       ├── AuthInput.jsx
│   │       └── RoleSelector.jsx
│   │
│   ├── pages/
│   │   └── auth/
│   │       ├── Login.jsx
│   │       ├── Signup.jsx
│   │       └── Registration.jsx
│   │
│   ├── layouts/
│   │   └── MainLayout.jsx
│   │
│   ├── services/
│   │   └── authService.js
│   │
│   ├── hooks/
│   │   └── useAuth.js
│   │
│   ├── context/
│   │   └── AuthContext.jsx
│   │
│   ├── utils/
│   │   └── validation.js
│   │
│   ├── routes/
│   │   ├── AppRoutes.jsx
│   │   └── ProtectedRoute.jsx
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
├── vite.config.js
└── index.html
```

---

# 4. What Each Folder Does

## `components/auth/`

Contains reusable UI components used by authentication pages.

### `AuthLayout.jsx`

Provides the common authentication page layout.

Used by:

- Login
- Signup
- Registration

### `AuthInput.jsx`

Reusable form input component.

Instead of writing the same label/input HTML repeatedly, pages use:

```jsx
<AuthInput
    label="Email address"
    name="email"
    type="email"
    ...
/>
```

### `RoleSelector.jsx`

Allows the user to choose:

```text
Exporter
Provider
```

The selected role is passed back to the page using React state.

---

# 5. Authentication Pages

## `pages/auth/Login.jsx`

Responsible for logging an existing user into the system.

Flow:

```text
User enters email/password
        ↓
Frontend validates input
        ↓
login() from AuthContext
        ↓
authService.js
        ↓
POST /auth/login
        ↓
FastAPI
        ↓
Database
        ↓
access_token returned
        ↓
Token stored in localStorage
        ↓
User goes to dashboard
```

---

## `pages/auth/Signup.jsx`

This page does NOT create the account.

It only asks:

```text
How do you want to use the platform?

Exporter
Provider
```

After selecting a role:

```text
Exporter
   ↓
/registration?role=exporter

Provider
   ↓
/registration?role=provider
```

---

## `pages/auth/Registration.jsx`

This page collects:

```text
Name
Email
Password
Confirm Password
```

The role comes from the URL:

```text
/registration?role=exporter
```

or:

```text
/registration?role=provider
```

Before sending the request, the frontend validates:

- Name has at least 2 characters
- Email format
- Password has at least 16 characters
- Password confirmation matches
- Role is either `exporter` or `provider`

Then it sends:

```text
POST /auth/register
```

---

# 6. Backend Authentication APIs

The frontend expects these endpoints.

## Register

```http
POST /auth/register
```

Request:

```json
{
    "name": "Test User",
    "email": "test@example.com",
    "password": "this-is-a-password-123",
    "role": "exporter",
    "status": "active"
}
```

Important:

```text
password >= 16 characters
role = exporter OR provider
```

---

## Login

```http
POST /auth/login
```

Request:

```json
{
    "email": "test@example.com",
    "password": "this-is-a-password-123"
}
```

Expected response contains:

```json
{
    "message": "Login successful",
    "name": "Test User",
    "access_token": "....",
    "token_type": "bearer"
}
```

The frontend stores the access token.

---

## Logout

```http
POST /auth/logout
```

The frontend sends:

```http
Authorization: Bearer <access_token>
```

After logout, the frontend removes the stored token and user information.

---

# 7. API Service Layer

File:

```text
src/services/authService.js
```

This file is responsible for communicating with FastAPI.

The React pages should NOT contain raw `fetch()` calls wherever possible.

Example:

```javascript
export const loginUser = async (email, password) => {
    const response = await fetch(
        `${API_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Invalid email or password"
        );
    }

    return data;
};
```

The same pattern is used for:

```text
registerUser()
logoutUser()
```

---

# 8. Why We Have `AuthContext`

File:

```text
src/context/AuthContext.jsx
```

Authentication state is needed by multiple components.

For example:

- Login page needs to log in
- MainLayout needs the current user's name
- ProtectedRoute needs to know whether the user is authenticated
- Logout needs to clear authentication

Instead of passing authentication state through many components, we use React Context.

The context exposes:

```javascript
{
    user,
    token,
    loading,
    isAuthenticated,
    login,
    register,
    logout
}
```

---

# 9. `useAuth`

File:

```text
src/hooks/useAuth.js
```

This is a small helper around `AuthContext`.

Components can write:

```jsx
const { login } = useAuth();
```

instead of repeatedly writing:

```jsx
useContext(AuthContext)
```

---

# 10. Authentication Storage

After login, the frontend stores:

```text
access_token
user
```

in:

```javascript
localStorage
```

Example:

```javascript
localStorage.setItem(
    "access_token",
    data.access_token
);
```

User information:

```javascript
localStorage.setItem(
    "user",
    JSON.stringify(userData)
);
```

When the application starts, `AuthContext` reads these values again.

This allows a page refresh without immediately losing the frontend authentication state.

---

# 11. Protected Routes

File:

```text
src/routes/ProtectedRoute.jsx
```

The dashboard is protected.

If:

```javascript
isAuthenticated === true
```

the user can access the protected page.

If:

```javascript
isAuthenticated === false
```

the user is redirected to:

```text
/login
```

Flow:

```text
User opens /
      ↓
ProtectedRoute
      ↓
Authenticated?
   ┌──┴──┐
  YES    NO
   ↓      ↓
Dashboard /login
```

---

# 12. Application Routes

File:

```text
src/routes/AppRoutes.jsx
```

Current routes:

```text
/login
/signup
/registration
/
```

The first three are public.

The dashboard `/` is protected.

Structure:

```jsx
<Routes>

    <Route
        path="/login"
        element={<Login />}
    />

    <Route
        path="/signup"
        element={<Signup />}
    />

    <Route
        path="/registration"
        element={<Registration />}
    />

    <Route element={
        <ProtectedRoute>
            <MainLayout />
        </ProtectedRoute>
    }>
        <Route
            path="/"
            element={<Dashboard />}
        />
    </Route>

</Routes>
```

When adding future pages, determine first whether the page is:

```text
Public
```

or:

```text
Authenticated/Protected
```

Protected pages should be placed inside the protected route structure.

---

# 13. Main Layout

File:

```text
src/layouts/MainLayout.jsx
```

This is the common layout for authenticated pages.

It currently contains:

- Logo
- User name
- Logout button
- Main content area

It uses:

```jsx
<Outlet />
```

from React Router.

Future authenticated pages can therefore appear inside the same layout.

Example:

```text
MainLayout
├── Header
│   ├── Logo
│   ├── User
│   └── Logout
│
└── Outlet
    └── Current authenticated page
```

---

# 14. Validation

File:

```text
src/utils/validation.js
```

Validation functions:

```javascript
validateEmail()
validateName()
validatePassword()
validateConfirmPassword()
```

Frontend validation improves user experience.

However:

## Never rely only on frontend validation.

The backend must continue validating:

- Email
- Password
- Role
- Required fields
- Duplicate users
- Authentication

Frontend validation can be bypassed.

---

# 15. `main.jsx`

File:

```text
src/main.jsx
```

This is the entry point of the React application.

It should wrap the application in:

```jsx
<AuthProvider>
    <App />
</AuthProvider>
```

Example:

```jsx
ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <React.StrictMode>
        <AuthProvider>
            <App />
        </AuthProvider>
    </React.StrictMode>
);
```

It also imports the authentication CSS:

```javascript
import "./assets/auth.css";
```

---

# 16. `App.jsx`

`App.jsx` should remain simple.

```jsx
import AppRoutes from "./routes/AppRoutes";

const App = () => {
    return <AppRoutes />;
};

export default App;
```

Routing logic belongs in:

```text
src/routes/AppRoutes.jsx
```

not directly inside `App.jsx`.

---

# 17. Backend CORS

Because the frontend and backend run on different origins, FastAPI needs CORS middleware.

Backend:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Without CORS, the browser may send:

```text
OPTIONS /auth/register
```

and the request can fail before the actual POST request reaches the backend.

---

# 18. Backend Database Setup

The backend must have the required database tables before registration is tested.

The SQLAlchemy model currently defines:

```python
class users(Base):
    __tablename__ = "user"
```

Therefore:

```text
Python class = users
PostgreSQL table = user
```

Do not confuse these two names.

The backend can create tables using:

```python
Base.metadata.create_all(bind=engine)
```

This must happen after the models have been imported so SQLAlchemy knows about the tables.

---

# 19. Running the Backend

Open a terminal:

```powershell
cd "D:\Major project\Backend"
```

Activate the virtual environment:

```powershell
..\venv\Scripts\Activate.ps1
```

Run:

```powershell
python -m uvicorn app.main:app --reload
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
Database connected successfully!
Application startup complete.
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Use Swagger to test backend APIs before testing the React frontend.

---

# 20. Running the Frontend

Open another terminal:

```powershell
cd "D:\Major project\frontend"
```

Install dependencies:

```powershell
npm install
```

Install React Router if necessary:

```powershell
npm install react-router-dom
```

Start Vite:

```powershell
npm run dev
```

Expected:

```text
Local: http://localhost:5173/
```

Open:

```text
http://localhost:5173
```

---

# 21. Recommended Testing Order

Do NOT immediately assume that a frontend failure means the frontend is broken.

Test in this order.

## Step 1 — Database

Confirm PostgreSQL is running and the database connection works.

Backend should print:

```text
Database connected successfully!
```

---

## Step 2 — Backend Startup

Run:

```powershell
python -m uvicorn app.main:app --reload
```

Confirm:

```text
Application startup complete.
```

---

## Step 3 — Swagger

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Step 4 — Register using Swagger

Test:

```text
POST /auth/register
```

If this fails, fix the backend before testing React.

---

## Step 5 — Login using Swagger

Test:

```text
POST /auth/login
```

Confirm that an:

```text
access_token
```

is returned.

---

## Step 6 — Start React

```powershell
npm run dev
```

---

## Step 7 — Test Registration from React

Go to:

```text
http://localhost:5173/signup
```

Select:

```text
Exporter
```

or:

```text
Provider
```

Complete registration.

---

## Step 8 — Test Login from React

Go to:

```text
/login
```

Enter the credentials created during registration.

---

## Step 9 — Check Browser Network

Open:

```text
F12
→ Network
→ Fetch/XHR
```

Look for:

```text
POST /auth/login
```

or:

```text
POST /auth/register
```

A successful request should return an appropriate HTTP success status.

---

# 22. Debugging Guide

## Error: `Failed to fetch`

Check:

1. Is FastAPI running?
2. Is the API URL correct?
3. Is the backend port correct?
4. Is CORS configured?
5. Is the browser sending an `OPTIONS` request that receives `405`?

---

## Error:

```text
OPTIONS /auth/register 405 Method Not Allowed
```

Usually indicates a CORS/preflight configuration problem.

Check FastAPI:

```python
CORSMiddleware
```

and make sure the frontend origin is allowed.

---

## Error:

```text
relation "user" does not exist
```

This means:

```text
Database connection works
BUT
the "user" table does not exist
```

Check:

```python
Base.metadata.create_all(bind=engine)
```

and ensure the user model was imported before table creation.

---

## Error:

```text
ImportError: cannot import name 'user'
```

Check the class name in:

```text
app/models/user_model.py
```

The current model class is:

```python
class users(Base):
```

Therefore the import is:

```python
from app.models.user_model import users
```

not:

```python
from app.models.user_model import user
```

---

## Error:

```text
401 Unauthorized
```

Usually means authentication credentials/token are invalid or missing.

Check:

```text
Authorization: Bearer <token>
```

for protected API requests.

---

## Error:

```text
422 Unprocessable Entity
```

Usually means the request body does not match the FastAPI/Pydantic schema.

Check:

- Field names
- Required fields
- Data types
- Password length
- Role value

---

# 23. How to Add a New API

When the backend team adds a new API, follow this process.

## Step 1

Backend developer provides:

```text
HTTP method
Endpoint
Request body
Response body
Authentication requirement
Possible error responses
```

Example:

```text
GET /providers
Authorization required
```

---

## Step 2

Create/update a service file.

For example:

```text
src/services/providerService.js
```

Example:

```javascript
const API_URL = "http://127.0.0.1:8000";

export const getProviders = async () => {
    const token = localStorage.getItem("access_token");

    const response = await fetch(
        `${API_URL}/providers`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.detail || "Failed to fetch providers"
        );
    }

    return data;
};
```

---

## Step 3

Create a page/component.

For example:

```text
src/pages/providers/ProviderList.jsx
```

The page calls:

```javascript
getProviders()
```

rather than putting the API URL directly into the component.

---

## Step 4

Add the route.

If authentication is required, put the route inside the protected route structure.

---

# 24. Development Responsibility Split

Recommended separation:

## Backend developer

Responsible for:

```text
FastAPI routes
Controllers
Services
Models
Database
Authentication logic
Validation
API responses
CORS
```

## Frontend developer

Responsible for:

```text
React pages
Components
Forms
Routing
UI
Frontend validation
API service functions
Authentication state
Error display
```

## Both

Need to agree on:

```text
Endpoint names
HTTP methods
Request JSON
Response JSON
Authentication requirements
Error format
```

---

# 25. Important Rule for Team Development

Do not randomly change backend API responses just to make the frontend work.

If an API changes, communicate:

```text
Old endpoint:
POST /auth/login

New endpoint:
POST /authentication/login
```

or:

```text
Old field:
access_token

New field:
token
```

The frontend service layer can then be updated deliberately.

Likewise, frontend developers should communicate when the UI requires a field that the backend does not currently return.

---

# 26. Complete Authentication Flow

The entire system currently works conceptually like this:

```text
                    FRONTEND
                       │
                       ▼
              ┌─────────────────┐
              │ React Router    │
              └────────┬────────┘
                       │
             ┌─────────┴─────────┐
             │                   │
          /signup             /login
             │                   │
             ▼                   ▼
       Role selection       Login form
             │                   │
             ▼                   ▼
      Registration form     useAuth()
             │                   │
             └─────────┬─────────┘
                       ▼
                AuthContext
                       │
                       ▼
              authService.js
                       │
                       │ HTTP
                       ▼
                    FASTAPI
                       │
               ┌───────┴────────┐
               │                │
          /auth/register   /auth/login
               │                │
               └───────┬────────┘
                       ▼
                  SQLAlchemy
                       │
                       ▼
                   PostgreSQL
                       │
                       ▼
                  Authentication
                       │
                       ▼
                  access_token
                       │
                       ▼
                  localStorage
                       │
                       ▼
                ProtectedRoute
                       │
                       ▼
                   Dashboard
```

---

# 27. Checklist for a New Developer

Before starting development:

- [ ] Node.js installed
- [ ] `npm` works
- [ ] Frontend dependencies installed
- [ ] React Router installed
- [ ] Backend virtual environment works
- [ ] PostgreSQL is running
- [ ] Backend database connection works
- [ ] Backend tables exist
- [ ] FastAPI starts successfully
- [ ] Swagger `/docs` opens
- [ ] Registration works in Swagger
- [ ] Login works in Swagger
- [ ] React starts with `npm run dev`
- [ ] Frontend can call backend
- [ ] CORS works
- [ ] Login stores token
- [ ] Protected route redirects unauthenticated users
- [ ] Logout clears authentication

---

# 28. Current API Base URL

The frontend service layer currently uses:

```javascript
const API_URL = "http://127.0.0.1:8000";
```

If the backend changes port, update this in:

```text
src/services/authService.js
```

Do not update the URL separately in every React component.

For a production deployment, this should eventually be moved to an environment variable, for example:

```text
VITE_API_URL=https://api.example.com
```

and accessed with:

```javascript
const API_URL = import.meta.env.VITE_API_URL;
```

---

# 29. Summary

The main architectural rule is:

```text
React Component
      ↓
Context/Hook (when needed)
      ↓
Service
      ↓
FastAPI API
      ↓
Database
```

Keep responsibilities separated.

Components should handle UI.

Pages should handle page-level state and user interaction.

Contexts should handle global state such as authentication.

Services should handle API communication.

Validation utilities should handle reusable frontend validation.

Routes should handle navigation and protected access.

This structure makes it easier for multiple developers to work on different parts of the frontend without putting all logic into one file.
