
# SmartSeat - Intelligent Session Allocation Platform

## 📋 Challenge Background

In large organisations, managing training programmes at scale is often complex and prone to error. Coordinators typically rely on manual tools like spreadsheets to assign employees to sessions, which leads to issues such as:
- Overbooking sessions
- Duplicate allocations
- Lack of visibility into available capacity

As organisations grow, these inefficiencies become more costly, impacting planning, fairness across departments, and overall programme success. There is a clear need for intelligent, automated systems that can enforce rules, reduce human error, and provide real-time insights.

## 🚀 Problem Statement

Design and build a Smart Seat Allocation Platform that helps assign participants to training sessions automatically, replacing the messy manual process with a system that ensures:
- No training session is overbooked
- No participant is assigned more than once
- Department limits are respected

The platform demonstrates how a basic, rule-driven system can improve accuracy and reduce human error.

## ✨ Key Features

- Assigning participants to sessions
- Preventing invalid allocations:
  - Overfilling a session
  - Assigning the same person twice
  - Exceeding department limits
- Simple feedback features:
  - Available seats per session
  - Validation of allocation actions

## 📅 Session Structure

| Session   | Time Slot      | Capacity | Duration |
|-----------|----------------|----------|----------|
| Morning   | 09:00 - 10:30  | 20       | 1.5 hours |
| Midday    | 11:00 - 12:30  | 20       | 1.5 hours |
| Afternoon | 13:00 - 14:30  | 20       | 1.5 hours |

Each session can hold a maximum of 20 participants. This limit cannot be exceeded.

## 🏢 Department Seats Allocation

Participants are divided into 3 departments, each with a fixed allocation per session.

| Department   | Total Participants | Seats Allocated | Max per Session | Total Seats |
|--------------|-------------------|-----------------|-----------------|-------------|
| Division A   | 24                | 24              | 8               | 24          |
| Division B   | 18                | 18              | 6               | 18          |
| Division C   | 18                | 18              | 6               | 18          |
| **Total**    | **60**            | **60**          | **20**          | **60**      |

The sum of department allocations per session equals 20, matching session capacity.

## 🔒 System Constraints

| # | Constraint | Type |
|---|-----------|------|
| 1 | Maximum 20 participants per session | Hard Limit |
| 2 | A participant can only be assigned to one session | Hard Limit |
| 3 | Departments cannot exceed their per-session allocation | Hard Limit |
| 4 | System should show remaining available seats per session | System Behaviour |

## 🛠️ Tech Stack

- **Python** - Backend logic and business rules
- **SQLite** - Database management
- **HTML** - User interface
- **CSS** - Styling and design

## 👥 Contributors

- Akhona Nzimande
- Asanda Shezi
- Lungelo Manci
- Sisekelo Mhlamvu
- Vidur Somaru

## 📖 Getting Started
```bash
# Clone the repo
git clone https://github.com/Vidur-S/SmartSeat.git
cd SmartSeat

# Install dependencies
pip install -r requirements.txt

# Run the system
python app.py

```

*SmartSeat: Your days of overbooking, double booking, and exceeding your session limits are over!*
