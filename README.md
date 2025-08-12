# Employee Time Scheduler

**Overview:** This application allows small businesses to create and share employee schedules. The application supports two user roles: managers and non-managers, each with different levels of access and functionality. Manager users can create an account, create, update and delete positions and employees, and view all shifts within the company, create new shifts, update all shift details, and delete shifts. Meanwhile, other users can view only their own assigned shifts, view shift details, and update the status of their assigned shifts.

This is the backend service for the application. It provides a RESTful API to manage scheduling. 

## Tech Stack
- Django REST Framework
- PostgreSQL 

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <project-directory>

2. **Create and activate a virtual environment**

   ```bash
   git clone <repository-url>
   cd <project-directory>

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt

4. **Run migrations**

   ```bash
   python manage.py migrate

4. **Start the development server**

   ```bash
   python manage.py runserver