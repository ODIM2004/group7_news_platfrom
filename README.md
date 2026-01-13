This website showcases the simplicity of consuming daily news.

---

## Project Overview
This is a **Flask-based** news aggregation platform that fetches real-time news from an API, allows users to generate personalized news summaries, and tracks user activity in a database.

---

## Architecture Components

### 1. Core Technology Stack
* **Backend Framework:** Flask (Python web framework)
* **Database:** SQLite3 (lightweight SQL database)
* **External API:** NewsAPI.org (news data source)
* **Deployment:** Optimized for Vercel (serverless platform)

### 2. Key Features
* **Real-time News Aggregation:** Pulls from multiple categories.
* **Personalized Summaries:** Generation based on user preferences.
* **Search Functionality:** Quickly find specific topics.
* **Category-Based Filtering:** Narrow down news by interest.
* **Admin Panel:** Includes activity logging for monitoring.
* **Reliability:** Includes fallback news sources.

---

## Complete User Flow Example
**Scenario:** *Executive wants business & tech news summary*

1.  **Entry:** User visits homepage → Sees general news.
2.  **Request:** Clicks **"Generate Summary"** button → Form appears.
3.  **Preferences:** User fills form:
    * **Name:** "Sarah Johnson"
    * **Checks:** ☑ Business, ☑ Technology
4.  **Submission:** Submits form → `POST` to `/generate-summary`.
5.  **Backend Processing:**
    * Logs "Sarah Johnson, business, technology, 2026-01-12 16:00:00" to database.
    * Fetches top 3 business articles and top 3 technology articles.
6.  **Display:** User sees summary page:
    * "Good day, Sarah Johnson"
    * Business and Technology sections with articles.
    * Generated timestamp.
7.  **Verification:** Admin checks `/admin` → Sees Sarah's activity logged.

---

## Educational Purpose
This project demonstrates:
* **Web application architecture**
* **API integration**
* **Database operations (CRUD)**
* **User input handling**
* **Error handling & fallbacks**
* **Deployment considerations**