Group 7 News Platform
📌 Introduction
The Group 7 News Platform is a web-based news aggregation application developed as a team software engineering project.
The system demonstrates practical backend development, API integration, database management, and cloud deployment using modern software engineering principles.
The application allows users to access current news articles, filter content by category or keyword, generate summarized news selections based on preferences, and records user activity for monitoring and evaluation purposes.
👥 Team Composition and Roles
This project was developed collaboratively with roles distributed across:
Backend development
Frontend integration
API integration
Database management
Deployment and configuration
Testing and documentation
Each role contributed to the design, implementation, deployment, and defense of the system.
🧠 Project Overview
Problem Statement
Accessing and organizing relevant news content from multiple sources can be inefficient and time-consuming.
Objectives
Provide a centralized platform for consuming up-to-date news
Enable filtering by category and keyword
Generate summarized news content based on user preferences
Track user activity for evaluation purposes
Deploy a functional backend application to the cloud
🔄 Development Methodology
The project followed a lightweight Agile approach, with iterative development and incremental feature implementation.
Tasks were handled in modular stages including feature development, testing, integration, and deployment, enabling collaborative development and system stability.
🧩 Software Engineering Domain
This project applies core software engineering principles, including:
Modularity and separation of concerns
API-driven architecture
Error handling and fault tolerance
Database abstraction
Deployment awareness and environment configuration
⚙️ Technologies and Tools Used
Programming Language: Python
Backend Framework: Flask
Database: SQLite3
External API: NewsAPI (with fallback mirror API)
HTTP Requests: Requests library
Frontend: HTML & CSS (Flask templates)
Version Control: Git & GitHub
Deployment Platform: Vercel
🗄️ Database Management System
The system uses SQLite, a lightweight relational database suitable for small to medium-scale applications.
Database Table: history
Column
Description
id
Primary key
name
User name
preferences
Selected news categories
timestamp
Date and time of request
The database supports activity logging and administrative monitoring.
🏗️ System Design and Implementation Overview
High-Level Architecture
Frontend: HTML templates rendered via Flask
Backend: Flask routes handle logic and API communication
External API: NewsAPI provides real-time news data
Database: SQLite stores user activity
Deployment: Serverless deployment on Vercel
System Flow
User → Flask Route → News API → Processing → HTML Template → User
🚀 Deployment Considerations
Vercel operates on a read-only file system
SQLite database is dynamically stored in /tmp during deployment
Sensitive data such as API keys are managed using environment variables
Application runs locally in debug mode and in production via Vercel’s serverless environment
🔐 Environment Variables
The following environment variable is required:
Copy code
Bash
NEWS_API_KEY=your_api_key_here
If not provided, a fallback key is used for development and testing.
📂 Project Structure
Copy code

group7_news_platform/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── summary.html
│   └── about.html
│
├── static/
│   └── styles.css
│
├── vercel.json
├── requirements.txt
└── README.md
⚠️ Challenges and Solutions
Challenge 1: API Reliability
Solution: Implemented a fallback mirror API to ensure continued service availability.
Challenge 2: Deployment File System Restrictions
Solution: Dynamically configured the SQLite database path to use /tmp during deployment.
Challenge 3: Large Team Coordination
Solution: Modular system design and role-based task allocation enabled effective collaboration and project defense.
📈 Results
Successfully deployed functional web application
Real-time news fetching and filtering implemented
User preference logging operational
Admin activity monitoring available
🔮 Future Directions
User authentication and login system
Personalized news recommendations
Multi-country news support
Improved UI/UX design
Migration to a persistent cloud database (PostgreSQL or MySQL)
🎓 Educational Purpose
This project demonstrates:
Web application architecture
API integration
Database operations (CRUD)
User input handling
Error handling and fault tolerance
Cloud deployment considerations
📜 License
This project was developed strictly for academic purposes.