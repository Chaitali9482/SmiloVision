import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path="toothcheck.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create scans table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                overall_score REAL NOT NULL,
                yellowness_score REAL NOT NULL,
                cavity_score REAL NOT NULL,
                alignment_score REAL NOT NULL,
                analysis_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create user_progress table for rewards and achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stars INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 0,
                total_scans INTEGER DEFAULT 0,
                last_scan_date TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create reminders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reminder_type TEXT NOT NULL,
                reminder_text TEXT NOT NULL,
                scheduled_date TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Initialize user progress if doesn't exist
        self.init_user_progress()
    
    def init_user_progress(self):
        """Initialize user progress record if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM user_progress")
        count = cursor.fetchone()[0]
        
        if count == 0:
            cursor.execute("""
                INSERT INTO user_progress (stars, coins, total_scans)
                VALUES (0, 0, 0)
            """)
            conn.commit()
        
        conn.close()
    
    def save_scan_results(self, results):
        """Save scan results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Prepare data
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        analysis_data = json.dumps({
            key: str(value) if not isinstance(value, (int, float, str, bool, type(None))) else value
            for key, value in results.items() 
            if key not in ['overall_score', 'yellowness_score', 'cavity_score', 'alignment_score']
        })
        
        # Insert scan record
        cursor.execute("""
            INSERT INTO scans (date, overall_score, yellowness_score, cavity_score, 
                             alignment_score, analysis_data)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            date_str,
            results['overall_score'],
            results['yellowness_score'],
            results['cavity_score'],
            results['alignment_score'],
            analysis_data
        ))
        
        # Update user progress
        cursor.execute("""
            UPDATE user_progress 
            SET total_scans = total_scans + 1,
                last_scan_date = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (date_str,))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def get_all_scans(self):
        """Get all scan results ordered by date"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, overall_score, yellowness_score, cavity_score, alignment_score
            FROM scans
            ORDER BY created_at ASC
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'date': row[0],
                'overall_score': row[1],
                'yellowness_score': row[2],
                'cavity_score': row[3],
                'alignment_score': row[4]
            })
        
        conn.close()
        return results
    
    def get_recent_scans(self, limit=5):
        """Get recent scan results"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, overall_score
            FROM scans
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        results = []
        for row in cursor.fetchall():
            # Format date for display
            date_obj = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            formatted_date = date_obj.strftime("%m/%d")
            
            results.append({
                'date': formatted_date,
                'overall_score': row[1]
            })
        
        conn.close()
        return results
    
    def get_user_progress(self):
        """Get user progress including stars and coins"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT stars, coins, total_scans, last_scan_date
            FROM user_progress
            WHERE id = 1
        """)
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'stars': row[0],
                'coins': row[1],
                'total_scans': row[2],
                'last_scan_date': row[3]
            }
        else:
            return {'stars': 0, 'coins': 0, 'total_scans': 0, 'last_scan_date': None}
    
    def update_user_rewards(self, stars_earned=0, coins_earned=0):
        """Update user rewards (stars and coins)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE user_progress 
            SET stars = stars + ?, 
                coins = coins + ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        """, (stars_earned, coins_earned))
        
        conn.commit()
        conn.close()
    
    def get_progress_trends(self, days=30):
        """Get progress trends for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, overall_score, yellowness_score, cavity_score, alignment_score
            FROM scans
            WHERE date >= date('now', '-{} days')
            ORDER BY created_at ASC
        """.format(days))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'date': row[0],
                'overall_score': row[1],
                'yellowness_score': row[2],
                'cavity_score': row[3],
                'alignment_score': row[4]
            })
        
        conn.close()
        return results
    
    def save_reminder(self, reminder_type, reminder_text, scheduled_date):
        """Save a reminder"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO reminders (reminder_type, reminder_text, scheduled_date)
            VALUES (?, ?, ?)
        """, (reminder_type, reminder_text, scheduled_date))
        
        conn.commit()
        conn.close()
        
        return cursor.lastrowid
    
    def get_active_reminders(self):
        """Get all active reminders"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, reminder_type, reminder_text, scheduled_date
            FROM reminders
            WHERE is_active = 1
            ORDER BY scheduled_date ASC
        """)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row[0],
                'type': row[1],
                'text': row[2],
                'date': row[3]
            })
        
        conn.close()
        return results
    
    def get_stats_summary(self):
        """Get summary statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total scans
        cursor.execute("SELECT COUNT(*) FROM scans")
        total_scans = cursor.fetchone()[0]
        
        # Get average scores
        cursor.execute("""
            SELECT AVG(overall_score), AVG(yellowness_score), 
                   AVG(cavity_score), AVG(alignment_score)
            FROM scans
        """)
        
        averages = cursor.fetchone()
        
        # Get latest scan
        cursor.execute("""
            SELECT overall_score, date
            FROM scans
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        latest_scan = cursor.fetchone()
        
        # Get user progress
        user_progress = self.get_user_progress()
        
        conn.close()
        
        return {
            'total_scans': total_scans,
            'avg_overall_score': averages[0] if averages[0] else 0,
            'avg_yellowness_score': averages[1] if averages[1] else 0,
            'avg_cavity_score': averages[2] if averages[2] else 0,
            'avg_alignment_score': averages[3] if averages[3] else 0,
            'latest_score': latest_scan[0] if latest_scan else 0,
            'latest_date': latest_scan[1] if latest_scan else None,
            'stars': user_progress['stars'],
            'coins': user_progress['coins']
        }
    
    def clear_all_data(self):
        """Clear all data (for testing/reset purposes)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM scans")
        cursor.execute("DELETE FROM reminders")
        cursor.execute("UPDATE user_progress SET stars=0, coins=0, total_scans=0, last_scan_date=NULL")
        
        conn.commit()
        conn.close()
