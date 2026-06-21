import os
import sqlite3
import shutil
from datetime import datetime
from contextlib import contextmanager
from kivy.app import App

DEFAULT_DB = "data.db"

# User implementation for Preview simplified
USER_ID = 1


def get_data_file(filename=DEFAULT_DB):
    app = App.get_running_app()
    target_dir = app.user_data_dir
    target_db_path = os.path.join(target_dir, filename)
    
    if not os.path.exists(target_db_path):
        print("First launch detected! Copying database to writeable storage...")
        
        bundled_db_path = os.path.join("data", filename) 
        
        if os.path.exists(bundled_db_path):
            shutil.copy(bundled_db_path, target_db_path)
            print("Database successfully copied.")
        else:
            print("Bundled template data/data.db not found. Creating a blank one.")
            os.makedirs(target_dir, exist_ok=True)
    print(target_db_path)
    return target_db_path


@contextmanager
def get_db_cursor(filename=DEFAULT_DB):
    """Manages the lifecycle of the DB connection automatically."""
    file_path = get_data_file(filename)
    conn = sqlite3.connect(file_path)
    try:
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Database error: {e}")
        raise e
    finally:
        conn.close()


@contextmanager
def get_db_read_cursor(filename=DEFAULT_DB):
    """For SELECT queries. No commit, no rollback logic needed."""
    file_path = get_data_file(filename)
    conn = sqlite3.connect(file_path)
    try:
        yield conn.cursor()
    finally:
        conn.close()


# --- TrainingsplanScreen ---
def load_plan_data(filename=DEFAULT_DB):
    with get_db_read_cursor(filename) as cursor:
        cursor.execute("""
                SELECT id, plan_name, description
                FROM plans
                WHERE profile_id = ?;
                """, (USER_ID,))
            
        plan_entries = cursor.fetchall()

        plan_list = []
        for id, name, desc in plan_entries:
            plan_list.append({"plan_id": id,
                                "plan_name": name,
                                "desc": desc,
                                "workouts": []})
        return plan_list


# --- EditPlanScreen ---
def get_days(plan_id, filename=DEFAULT_DB):
    with get_db_read_cursor(filename) as cursor:
        cursor.execute("""
            SELECT id, day_name
            FROM plan_days
            WHERE plan_id = ?
            ORDER BY day_order ASC;
            """, (plan_id,))

        day_entries = cursor.fetchall()
        days_list = []
        for id, day_name in day_entries:
            days_list.append({
                "day_id": id,
                "day": day_name})
        return days_list

def get_plan_exercises(day_id, filename=DEFAULT_DB):
    with get_db_read_cursor(filename) as cursor:
        cursor.execute("""
            SELECT 
                p.id AS plan_exercise_id,
                e.id AS exercise_id,
                e.name AS exercise_name
            FROM plan_exercises p
            INNER JOIN exercises e 
                ON p.exercise_id = e.id
            WHERE p.plan_day_id = ?
            ORDER BY p.exercise_order;
        """, (day_id,))

        plan_exercise_entries = cursor.fetchall()

        exercise_list = []
        for id, exercise_id, exercise_name in plan_exercise_entries:
            exercise_list.append({"plan_exercise_id": id,
                                  "exercise_id": exercise_id,
                                  "exercise_name": exercise_name})
        return exercise_list

def save_plan_set_entry(value, filename=DEFAULT_DB):
    with get_db_cursor(filename) as cursor:
        cursor.execute("""
            INSERT INTO plan_sets
            (plan_exercise_id, set_number, target_reps, target_weight)
            VALUES (?, COALESCE((SELECT MAX(set_number) FROM plan_sets WHERE plan_exercise_id = ?), 0) + 1, ?, ?)
            """, (
                value["plan_exercise_id"],
                value["plan_exercise_id"],
                0,
                0
            ))
        set_id = cursor.lastrowid
        print("Set added.")
        return set_id

def get_sets(plan_exercise_id, filename=DEFAULT_DB):
    with get_db_read_cursor(filename) as cursor:
        cursor.execute("""
            SELECT id, target_reps, target_weight
            FROM plan_sets p
            WHERE p.plan_exercise_id = ?
            ORDER BY set_number ASC;
        """, (plan_exercise_id,))

        plan_set_entries = cursor.fetchall()

        sets_list = []
        for id, target_reps, target_weight in plan_set_entries:
            sets_list.append({"set_id": id,
                              "reps": target_reps,
                              "weight": target_weight})
        return sets_list

def delete_set(plan_exercise_id, filename=DEFAULT_DB):
    with get_db_cursor(filename) as cursor:
        cursor.execute("DELETE FROM plan_sets WHERE id = ?", (plan_exercise_id,))

def update_set(value, filename=DEFAULT_DB):
    with get_db_cursor(filename) as cursor:
        cursor.execute("""
            UPDATE plan_sets
            SET target_reps = ?, target_weight = ?
            WHERE id = ?
        """, (value["reps"], 
              value["weight"], 
              value["set_id"]))

def get_exercises_with_sets(day_id, filename=DEFAULT_DB):
    with get_db_read_cursor(filename) as cursor:
        cursor.execute("""
            SELECT 
                p.id AS plan_exercise_id,
                e.id AS exercise_id,
                e.name AS exercise_name,
                s.id AS set_id,
                s.target_reps,
                s.target_weight
            FROM plan_exercises p
            INNER JOIN exercises e 
                ON p.exercise_id = e.id
            LEFT JOIN plan_sets s 
                ON p.id = s.plan_exercise_id
            WHERE p.plan_day_id = ?
            ORDER BY p.exercise_order, s.set_number ASC;
        """, (day_id,))

        rows = cursor.fetchall()

        exercises_dict = {}
        for p_ex_id, ex_id, ex_name, set_id, reps, weight in rows:
            if p_ex_id not in exercises_dict:
                exercises_dict[p_ex_id] = {
                    "plan_exercise_id": p_ex_id,
                    "exercise_id": ex_id,
                    "exercise_name": ex_name,
                    "sets": []
                }
            
            if set_id is not None:
                exercises_dict[p_ex_id]["sets"].append({
                    "set_id": set_id,
                    "reps": reps,
                    "weight": weight
                })
                
        return list(exercises_dict.values())


# --- HistoryScreen ---
def save_history_entry(plan_id, day_id, filename=DEFAULT_DB):
    with get_db_cursor(filename) as cursor:
        cursor.execute('''
            SELECT p.plan_name, d.day_name 
            FROM plan_days d
            INNER JOIN plans p ON d.plan_id = p.id
            WHERE p.id = ? AND d.id = ?
        ''', (plan_id, day_id))

        result = cursor.fetchone()
        if result:
            history_name = f'{datetime.now().strftime("%d.%m.%y")}: {result[0]} - {result[1]}'
            cursor.execute("""
                INSERT INTO history
                (profile_id, name, datum)
                VALUES (?, ?, ?)
                """, (
                    USER_ID,
                    history_name,
                    datetime.now().strftime("%d.%m.%y")
                ))
            history_id = cursor.lastrowid
            return history_id

def load_history_data(filename=DEFAULT_DB):
    with get_db_read_cursor(filename) as cursor:
        cursor.execute('''
            SELECT 
                h.id,
                h.name AS workout_name,
                he.exercise_id,
                e.name AS exercise_name,
                hs.reps,
                hs.weight,
                hs.orm
            FROM history h
            JOIN history_exercises he ON he.history_id = h.id
            JOIN exercises e          ON e.id = he.exercise_id
            JOIN history_sets hs      ON hs.history_exercises_id = he.id
        ''')

        history_entries = cursor.fetchall()

        workout_log = {}
        for history in history_entries:
            h_id, h_name, ex_id, ex_name, reps, weight, orm = history
            
            if h_id not in workout_log:
                workout_log[h_id] = {}
                workout_log[h_id]["name"] = h_name
                
            if ex_name not in workout_log[h_id]:
                workout_log[h_id][ex_name] = []
                
            workout_log[h_id][ex_name].append({
                'reps': reps,
                'weight': weight,
                'orm': round(orm, 1)
            })

        return workout_log