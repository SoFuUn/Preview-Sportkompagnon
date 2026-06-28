# SoFuUn Sportkompagnon Preview

Welcome to the **SoFuUn Sportkompagnon Preview** repository!

> **⚠️ Note for Reviewers & Recruiters:**
> This repository serves as a functional **Interactive Public Preview** of a comprehensive fitness management ecosystem currently in active development. To protect proprietary logic while still demonstrating production-level architecture and code quality, several advanced features have been intentionally streamlined or scoped out of this public build. Restricted functionality is represented through informative UI dialogs.

The complete application combines a polished Kivy/KivyMD frontend with a robust, data-driven Python backend to create a modern desktop fitness management experience.

---

# 🚀 Vision & Feature Roadmap

The production version of **SoFuUn Sportkompagnon** is designed as a complete training management platform featuring:

* **Dynamic Workout Plan Creation**

  * Flexible routine builder
  * Custom workout days
  * Split planning
  * Multi-level exercise organization

* **Live Workout Tracking**

  * Interactive workout sessions
  * Set-by-set tracking
  * Weight and repetition logging
  * Automatic workout persistence

* **1RM Calculator & Analytics**

  * Instant estimated One-Rep Max calculations
  * Long-term strength progression charts
  * Historical performance analysis

* **Background Rest Timer**

  * Automatic recovery timer
  * Structured pacing between sets
  * Optimized workout flow

* **Biometric Tracking**

  * Bodyweight history
  * Timeline visualization
  * Progress graphs

* **Exercise Library**

  * Searchable exercise database
  * Categories and documentation
  * Media guides
  * Individual PR tracking

* **Workout History**

  * Historical workout archive
  * Volume analysis
  * Performance consistency tracking

---

# 📱 Feature Showcase

Since this repository contains a curated preview build, the images below demonstrate the complete production workflow.

|                     🏋️ Workout Tracker & History                     |                  📊 Analytics & Exercise Database                  |
| :-------------------------------------------------------------------: | :----------------------------------------------------------------: |
|            ![Workout Demo](docs/images/weight_tracker.gif)            |        ![Exercise Library](docs/images/exercise_library.gif)       |
| *Real-time workout tracking with automatic One-Rep Max calculations.* | *Searchable relational exercise database with normalized storage.* |

---

# 🛠️ Running the Interactive Preview

## Prerequisites

* Python **3.11.9**

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

Create and activate a virtual environment.

### Windows

```bash
py -3.11 -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Launch the Application

Run the application with:

```bash
python main.py
```

---

# 💡 Exploring the Preview

### Available Interactions

* Expand preloaded workout exercises
* Edit repetitions and weight values
* Add additional workout sets dynamically
* Delete individual exercise sets
* Observe immediate SQLite database commits after changes

### Simulated Feature Boundaries

Features intentionally omitted from the public preview (such as creating new workout plans, browsing the complete exercise library, or accessing analytics dashboards) display embedded informational dialogs explaining that they are unavailable in the preview version.

---

# 📊 Database Architecture (Preview)

The application utilizes a normalized SQLite relational database with foreign key constraints and generated columns to ensure excellent performance and data integrity.

The production database consists of **nine interconnected tables**. The examples below showcase three of the more advanced table designs.

## User Personal Records

Tracks lifetime personal records and automatically calculates estimated One-Rep Max values.

```sql
CREATE TABLE user_prs (
    profile_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    pr_weight REAL NOT NULL,
    pr_reps INTEGER NOT NULL,
    pr_date TEXT NOT NULL,

    pr_orm REAL GENERATED ALWAYS AS (
        pr_weight * (1 + (pr_reps / 30.0))
    ) STORED,

    PRIMARY KEY (profile_id, exercise_id),

    FOREIGN KEY (profile_id)
        REFERENCES profiles(id)
        ON DELETE CASCADE,

    FOREIGN KEY (exercise_id)
        REFERENCES exercises(id)
        ON DELETE CASCADE
);
```

---

## Plan Exercises

Junction table connecting workout plans with assigned exercises.

```sql
CREATE TABLE plan_exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    plan_day_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,

    exercise_order INTEGER,

    FOREIGN KEY (plan_day_id)
        REFERENCES plan_days(id)
        ON DELETE CASCADE,

    FOREIGN KEY (exercise_id)
        REFERENCES exercises(id)
        ON DELETE CASCADE
);
```

---

## History Sets

Stores historical workout performance while generating estimated One-Rep Max values automatically.

```sql
CREATE TABLE history_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    history_exercises_id INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight REAL NOT NULL,

    orm REAL GENERATED ALWAYS AS (
        weight * (1 + (reps / 30.0))
    ) STORED,

    FOREIGN KEY (history_exercises_id)
        REFERENCES history_exercises(id)
        ON DELETE CASCADE
);
```

---

# Database Design Highlights

### Automated Data Lifecycle

Using **ON DELETE CASCADE** ensures complete relational integrity. Deleting a user profile or workout plan automatically removes all associated exercises, sets, and historical records without leaving orphaned data.

### Optimized Query Performance

Computed values such as estimated One-Rep Max are stored directly using **GENERATED ALWAYS AS ... STORED**, eliminating expensive runtime calculations and enabling instant analytics rendering.

---

# 🛠️ Technology Stack

| Component          | Technology                        |
| ------------------ | --------------------------------- |
| **Frontend**       | Kivy & KivyMD                     |
| **Backend**        | Python 3.11                       |
| **Database**       | SQLite3                           |
| **Architecture**   | Model–View–Controller (MVC)       |
| **Design Pattern** | Object-Oriented Programming (OOP) |

---

## Architecture

The project follows a clean **Model–View–Controller (MVC)** architecture, separating business logic, data persistence, and user interface components into independent layers for improved maintainability, scalability, and long-term development.
