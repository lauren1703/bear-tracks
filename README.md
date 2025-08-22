# BearTracks 🐻  
A backend system for scraping, storing, and serving university events, with calendar integration.  

## 🎯 Project Summary  
BearTracks is a **Flask-based backend** that automates event aggregation and management. The system **scrapes live event data** from Cornell’s CampusGroups platform, normalizes it, and persists it in a **relational database** (SQLite via SQLAlchemy ORM). It exposes a suite of **RESTful APIs** for querying, creating, and managing events, users, and organizations, and integrates with the **Google Calendar API** to sync events into personal calendars.  

This project highlights skills in **API design, database modeling, data ingestion pipelines, and third-party API integration**.  

---

## 💡 Key Contributions  
- **Built a data ingestion pipeline** with `requests` + `BeautifulSoup` to scrape 40+ live event entries per fetch, clean HTML, and standardize inconsistent datetime formats.  
- **Designed relational schemas** for users, events, and organizations with SQLAlchemy, implementing many-to-many relationships for user attendance.  
- **Developed REST APIs** in Flask for event management (`GET /events`, `POST /events`, `DELETE /events/<id>`), user registration, and organization management.  
- **Integrated Google Calendar API (OAuth2)** to automatically add/remove events from users’ calendars.  
- **Implemented error handling & validation**, ensuring robustness against malformed data and invalid API requests.  

---

## 🛠️ Tech Stack  
- **Python** (Flask, Requests, BeautifulSoup, SQLAlchemy)  
- **Database:** SQLite  
- **APIs:** Google Calendar API (OAuth2)  
- **Architecture:** RESTful backend, JSON-based responses 
