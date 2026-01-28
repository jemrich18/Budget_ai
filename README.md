# Smart Expense Tracker

An AI-powered expense tracking application that helps you manage your finances with intelligent categorization and natural language insights.

## Features

- **User Authentication** - Secure JWT-based registration and login
- **Expense Management** - Add, edit, delete, and filter expenses
- **AI Categorization** - Automatically suggests categories for expenses using Claude AI
- **AI Chat Assistant** - Ask natural language questions about your spending patterns
- **Dashboard** - View expense summaries and category breakdowns
- **Responsive UI** - Modern React frontend with Tailwind CSS

## Tech Stack

### Backend
- Python 3.12+
- Django 6.0
- Django REST Framework
- SimpleJWT for authentication
- Anthropic Claude API for AI features
- SQLite (development) / PostgreSQL (production)

### Frontend
- React 18 with TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Anthropic API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/smart-expense-tracker.git
   cd smart-expense-tracker
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

3. **Install backend dependencies**
   ```bash
   uv sync
   ```

4. **Run database migrations**
   ```bash
   cd backend
   uv run python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   uv run python manage.py runserver 8000
   ```

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000/api/
   - Admin panel: http://localhost:8000/admin/

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and get JWT tokens |
| POST | `/api/auth/logout/` | Logout and blacklist token |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| GET | `/api/auth/profile/` | Get current user profile |
| PUT | `/api/auth/profile/` | Update user profile |
| POST | `/api/auth/change-password/` | Change password |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses/` | List all expenses |
| POST | `/api/expenses/` | Create a new expense |
| GET | `/api/expenses/{id}/` | Get expense details |
| PUT | `/api/expenses/{id}/` | Update an expense |
| DELETE | `/api/expenses/{id}/` | Delete an expense |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all categories |
| POST | `/api/categories/` | Create a new category |
| GET | `/api/categories/{id}/` | Get category details |
| PUT | `/api/categories/{id}/` | Update a category |
| DELETE | `/api/categories/{id}/` | Delete a category |

### AI Query
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/query/` | Ask AI about your expenses |

## Environment Variables

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

## Project Structure

```
smart-expense-tracker/
├── backend/
│   ├── apps/
│   │   ├── expenses/      # Expense and category management
│   │   ├── users/         # User authentication
│   │   └── ai_services/   # AI integration (Claude)
│   └── config/            # Django settings
├── frontend/
│   ├── src/
│   │   ├── api/           # API client and types
│   │   ├── components/    # Reusable components
│   │   ├── contexts/      # React contexts (auth)
│   │   └── pages/         # Page components
│   └── ...
├── .env                   # Environment variables
└── pyproject.toml         # Python dependencies
```

## License

MIT
