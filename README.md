# Elevator Simulator

## Overview

This project implements an elevator simulator web app using Python/Django as the backend and the default Django template (utilizing Vue) as the frontend. The `ElevatorService` class controls multiple elevators, each of which can move between floors, open/close doors, and respond to passenger requests. The system is designed to use **WebSockets** for real-time updates and **asynchronous processing** for moving elevators and handling requests.

---

## Features

- **Multiple Elevators**: Simulates multiple elevators working independently.
- **Real-time Communication**: WebSocket integration to update the UI with elevator status (position, direction, open/close status).
- **Request Handling**: The system processes requests for elevator rides based on direction and current floor.
- **Elevator Movement**: Elevators move between floors, adjusting their state (moving, idle, door open/close).

---

## Steps

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

2. **Start redis**:

```bash
service redis-server start
```

2. **Start server**:

```bash
python manage.py runserver
```