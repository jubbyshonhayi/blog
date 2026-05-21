# Gazette

A modern Django blogging platform for thoughtful posts, notes, and founder-minded writing.

Live Site → https://blogging-ofno.onrender.com/

---

## ✨ Features

- User authentication system
- Profile creation and profile updates
- Default profile image support
- Password reset via email
- Create, edit, and delete posts
- Comment and reply system
- User mention notifications (`@username`)
- Dynamic sidebar with latest posts
- Read More functionality for long posts
- Pagination for cleaner browsing
- Responsive Bootstrap UI
- PostgreSQL database powered by Neon
- Production deployment on Render

---

## 🛠 Tech Stack

- Django
- PostgreSQL (Neon)
- Bootstrap
- Render
- Git & GitHub

---

## 📸 Overview

Gazette is designed as a lightweight and thoughtful writing platform focused on clean interaction, readability, and founder-minded content.

The project evolved from a simple Django blog into a more polished production-ready application with authentication, notifications, profile management, and performance optimizations.

---

## ⚡ Performance Improvements

- Database connection reuse
- Lightweight keep-alive endpoint
- Cached public pages
- Optimized query usage
- Reduced unnecessary database calls

---

## 🚀 Local Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd <project-folder>
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

### Windows
```bash
venv\Scripts\activate
```

### macOS/Linux
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_neon_database_url
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

---

## 🌍 Deployment

Gazette is deployed using Render with a Neon PostgreSQL database.

Production considerations include:

- Environment variable management
- PostgreSQL database configuration
- Static/media file handling
- Production-ready settings
- Database connection optimization

---

## 📌 Future Improvements

- Real-time notifications
- Like and bookmark system
- Rich text editor
- Trending posts section
- Search functionality
- Dark mode
- Email notifications

---

## 👤 Author

Built by founderz.zw.

---

## 📄 License

This project is open-source and available for learning and personal development.
