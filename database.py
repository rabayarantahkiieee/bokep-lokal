#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DATABASE MODULE - PostgreSQL + Redis Integration
Dibuat untuk Bot Bokep Lokal
"""

import os
import json
import psycopg2
import psycopg2.extras
import redis
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

class DatabaseManager:
    """Manajer database dengan PostgreSQL primary dan Redis cache"""

    def __init__(self):
        # Database connections
        self.pg_conn = None
        self.redis_conn = None

        # Cache settings
        self.cache_ttl = 300  # 5 minutes
        self.admin_cache_ttl = 60  # 1 minute

        # Initialize connections
        self._init_postgresql()
        self._init_redis()
        self._create_tables()

    def _init_postgresql(self):
        """Initialize PostgreSQL connection"""
        try:
            # Get database URL from environment (use provided URL if available)
            database_url = os.getenv('DATABASE_URL', 'postgres://ubrbg1abcr6305:p26111a2abf61143377ca27214204dceb1a64495b35d1faf13f56e75479a25759@c7itisjfjj8ril.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dch0m1dl2r3et8')

            if database_url:
                # Parse database URL
                parsed = urlparse(database_url)
                self.pg_conn = psycopg2.connect(
                    host=parsed.hostname,
                    port=parsed.port,
                    user=parsed.username,
                    password=parsed.password,
                    database=parsed.path.lstrip('/'),
                    sslmode='require'
                )
                print("PostgreSQL connected successfully")
            else:
                print("DATABASE_URL not found, using JSON fallback")
                self.pg_conn = None

        except Exception as e:
            print(f"PostgreSQL connection failed: {e}")
            self.pg_conn = None

    def _init_redis(self):
        """Initialize Redis connection"""
        try:
            redis_url = os.getenv('REDIS_URL', os.getenv('REDISCLOUD_URL'))

            if redis_url:
                self.redis_conn = redis.from_url(redis_url)
                # Test connection
                self.redis_conn.ping()
                print("Redis connected successfully")
            else:
                print("REDIS_URL not found, Redis disabled")
                self.redis_conn = None

        except Exception as e:
            print(f"Redis connection failed: {e}")
            self.redis_conn = None

    def _create_tables(self):
        """Create database tables if they don't exist"""
        if not self.pg_conn:
            return

        try:
            with self.pg_conn.cursor() as cursor:
                # Users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE
                    )
                """)

                # Admins table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS admins (
                        user_id BIGINT PRIMARY KEY,
                        added_by BIGINT,
                        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_main_admin BOOLEAN DEFAULT FALSE
                    )
                """)

                # Bot settings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bot_settings (
                        key TEXT PRIMARY KEY,
                        value JSONB,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_by BIGINT
                    )
                """)

                # User logs table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_logs (
                        id SERIAL PRIMARY KEY,
                        user_id BIGINT,
                        username TEXT,
                        first_name TEXT,
                        action TEXT,
                        details TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ip_address TEXT
                    )
                """)

                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_logs_user_id ON user_logs(user_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_logs_timestamp ON user_logs(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_logs_action ON user_logs(action)")

                # Scheduled messages table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scheduled_messages (
                        id SERIAL PRIMARY KEY,
                        time TEXT NOT NULL,
                        message TEXT NOT NULL,
                        created_by BIGINT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_active BOOLEAN DEFAULT TRUE
                    )
                """)

                # Anti-spam data table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS anti_spam_data (
                        key TEXT PRIMARY KEY,
                        value JSONB,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                self.pg_conn.commit()
                print("Database tables created successfully")

        except Exception as e:
            print(f"Error creating tables: {e}")
            self.pg_conn.rollback()

    # --- CACHE METHODS ---

    def _get_cache_key(self, key: str) -> str:
        """Generate cache key"""
        return f"bot_cache:{key}"

    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get data from Redis cache"""
        if not self.redis_conn:
            return None

        try:
            cached_data = self.redis_conn.get(self._get_cache_key(key))
            if cached_data:
                return json.loads(cached_data)
        except Exception as e:
            print(f"Cache get error: {e}")

        return None

    def _set_cache(self, key: str, data: Any, ttl: int = None) -> None:
        """Set data to Redis cache"""
        if not self.redis_conn:
            return

        try:
            ttl = ttl or self.cache_ttl
            self.redis_conn.setex(
                self._get_cache_key(key),
                ttl,
                json.dumps(data, default=str)
            )
        except Exception as e:
            print(f"Cache set error: {e}")

    def _clear_cache(self, key: str = None) -> None:
        """Clear cache"""
        if not self.redis_conn:
            return

        try:
            if key:
                self.redis_conn.delete(self._get_cache_key(key))
            else:
                # Clear all bot cache
                keys = self.redis_conn.keys("bot_cache:*")
                if keys:
                    self.redis_conn.delete(*keys)
        except Exception as e:
            print(f"Cache clear error: {e}")

    # --- USER METHODS ---

    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> bool:
        """Add or update user"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (user_id, username, first_name, last_name, last_active)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON CONFLICT (user_id) DO UPDATE SET
                        username = EXCLUDED.username,
                        first_name = EXCLUDED.first_name,
                        last_name = EXCLUDED.last_name,
                        last_active = CURRENT_TIMESTAMP,
                        is_active = TRUE
                """, (user_id, username, first_name, last_name))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache("users")
                self._clear_cache(f"user_{user_id}")

                return True

        except Exception as e:
            print(f"Error adding user: {e}")
            self.pg_conn.rollback()
            return False

    def get_users(self) -> List[Dict]:
        """Get all users"""
        # Try cache first
        cached_users = self._get_from_cache("users")
        if cached_users:
            return cached_users

        if not self.pg_conn:
            return []

        try:
            with self.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT user_id, username, first_name, last_name, joined_at, last_active, is_active
                    FROM users
                    WHERE is_active = TRUE
                    ORDER BY joined_at DESC
                """)

                users = [dict(row) for row in cursor.fetchall()]

                # Cache result
                self._set_cache("users", users)

                return users

        except Exception as e:
            print(f"Error getting users: {e}")
            return []

    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        # Try cache first
        cached_user = self._get_from_cache(f"user_{user_id}")
        if cached_user:
            return cached_user

        if not self.pg_conn:
            return None

        try:
            with self.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT user_id, username, first_name, last_name, joined_at, last_active, is_active
                    FROM users
                    WHERE user_id = %s AND is_active = TRUE
                """, (user_id,))

                user = cursor.fetchone()
                if user:
                    user_dict = dict(user)
                    # Cache result
                    self._set_cache(f"user_{user_id}", user_dict)
                    return user_dict

        except Exception as e:
            print(f"Error getting user: {e}")

        return None

    # --- ADMIN METHODS ---

    def add_admin(self, user_id: int, added_by: int = None) -> bool:
        """Add admin"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO admins (user_id, added_by, is_main_admin)
                    VALUES (%s, %s, FALSE)
                    ON CONFLICT (user_id) DO NOTHING
                """, (user_id, added_by))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache("admins")

                return True

        except Exception as e:
            print(f"Error adding admin: {e}")
            self.pg_conn.rollback()
            return False

    def remove_admin(self, user_id: int) -> bool:
        """Remove admin"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("DELETE FROM admins WHERE user_id = %s AND is_main_admin = FALSE", (user_id,))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache("admins")

                return True

        except Exception as e:
            print(f"Error removing admin: {e}")
            self.pg_conn.rollback()
            return False

    def get_admins(self) -> List[int]:
        """Get all admin IDs"""
        # Try cache first
        cached_admins = self._get_from_cache("admins")
        if cached_admins:
            return cached_admins

        if not self.pg_conn:
            return []

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("SELECT user_id FROM admins ORDER BY added_at DESC")
                admins = [row[0] for row in cursor.fetchall()]

                # Cache result
                self._set_cache("admins", admins, self.admin_cache_ttl)

                return admins

        except Exception as e:
            print(f"Error getting admins: {e}")
            return []

    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        admins = self.get_admins()
        return user_id in admins

    # --- SETTINGS METHODS ---

    def get_setting(self, key: str) -> Any:
        """Get bot setting"""
        # Try cache first
        cached_setting = self._get_from_cache(f"setting_{key}")
        if cached_setting is not None:
            return cached_setting

        if not self.pg_conn:
            return None

        try:
            with self.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT value FROM bot_settings WHERE key = %s", (key,))
                result = cursor.fetchone()

                if result:
                    setting_value = result['value']
                    # Cache result
                    self._set_cache(f"setting_{key}", setting_value)
                    return setting_value

        except Exception as e:
            print(f"Error getting setting: {e}")

        return None

    def set_setting(self, key: str, value: Any, updated_by: int = None) -> bool:
        """Set bot setting"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO bot_settings (key, value, updated_by)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (key) DO UPDATE SET
                        value = EXCLUDED.value,
                        updated_at = CURRENT_TIMESTAMP,
                        updated_by = EXCLUDED.updated_by
                """, (key, json.dumps(value, default=str), updated_by))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache(f"setting_{key}")

                return True

        except Exception as e:
            print(f"Error setting value: {e}")
            self.pg_conn.rollback()
            return False

    # --- LOG METHODS ---

    def add_log(self, user_id: int, username: str, first_name: str, action: str, details: str = "", ip_address: str = "") -> bool:
        """Add user activity log"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO user_logs (user_id, username, first_name, action, details, ip_address)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (user_id, username, first_name, action, details, ip_address))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache("user_logs")

                return True

        except Exception as e:
            print(f"Error adding log: {e}")
            self.pg_conn.rollback()
            return False

    def get_logs(self, limit: int = 1000) -> List[Dict]:
        """Get user activity logs"""
        # Try cache first
        cached_logs = self._get_from_cache("user_logs")
        if cached_logs:
            return cached_logs

        if not self.pg_conn:
            return []

        try:
            with self.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id, user_id, username, first_name, action, details, timestamp, ip_address
                    FROM user_logs
                    ORDER BY timestamp DESC
                    LIMIT %s
                """, (limit,))

                logs = [dict(row) for row in cursor.fetchall()]

                # Cache result
                self._set_cache("user_logs", logs)

                return logs

        except Exception as e:
            print(f"Error getting logs: {e}")
            return []

    # --- SCHEDULED MESSAGES METHODS ---

    def add_scheduled_message(self, time: str, message: str, created_by: int) -> bool:
        """Add scheduled message"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO scheduled_messages (time, message, created_by)
                    VALUES (%s, %s, %s)
                """, (time, message, created_by))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache("scheduled_messages")

                return True

        except Exception as e:
            print(f"Error adding scheduled message: {e}")
            self.pg_conn.rollback()
            return False

    def get_scheduled_messages(self) -> List[Dict]:
        """Get all scheduled messages"""
        # Try cache first
        cached_messages = self._get_from_cache("scheduled_messages")
        if cached_messages:
            return cached_messages

        if not self.pg_conn:
            return []

        try:
            with self.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("""
                    SELECT id, time, message, created_by, created_at, is_active
                    FROM scheduled_messages
                    WHERE is_active = TRUE
                    ORDER BY time ASC
                """)

                messages = [dict(row) for row in cursor.fetchall()]

                # Cache result
                self._set_cache("scheduled_messages", messages)

                return messages

        except Exception as e:
            print(f"Error getting scheduled messages: {e}")
            return []

    def remove_scheduled_message(self, message_id: int) -> bool:
        """Remove scheduled message"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("UPDATE scheduled_messages SET is_active = FALSE WHERE id = %s", (message_id,))

                self.pg_conn.commit()

                # Clear cache
                self._clear_cache("scheduled_messages")

                return True

        except Exception as e:
            print(f"Error removing scheduled message: {e}")
            self.pg_conn.rollback()
            return False

    # --- ANTI-SPAM METHODS ---

    def get_antispam_setting(self, key: str) -> Any:
        """Get anti-spam setting"""
        if not self.pg_conn:
            return None

        try:
            with self.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT value FROM anti_spam_data WHERE key = %s", (key,))
                result = cursor.fetchone()

                if result:
                    return result['value']

        except Exception as e:
            print(f"Error getting anti-spam setting: {e}")

        return None

    def set_antispam_setting(self, key: str, value: Any) -> bool:
        """Set anti-spam setting"""
        if not self.pg_conn:
            return False

        try:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO anti_spam_data (key, value)
                    VALUES (%s, %s)
                    ON CONFLICT (key) DO UPDATE SET
                        value = EXCLUDED.value,
                        updated_at = CURRENT_TIMESTAMP
                """, (key, json.dumps(value, default=str)))

                self.pg_conn.commit()

                return True

        except Exception as e:
            print(f"Error setting anti-spam value: {e}")
            self.pg_conn.rollback()
            return False

    # --- UTILITY METHODS ---

    def migrate_from_json(self, json_file: str = "bot_database.json") -> bool:
        """Migrate data from JSON file to PostgreSQL"""
        if not self.pg_conn:
            return False

        try:
            # Load JSON data
            if not os.path.exists(json_file):
                print(f"JSON file {json_file} not found")
                return False

            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # Migrate users
            if "users" in json_data:
                for user_id in json_data["users"]:
                    self.add_user(user_id)

            # Migrate admins
            if "admins" in json_data:
                for admin_id in json_data["admins"]:
                    self.add_admin(admin_id)

            # Migrate settings
            settings_to_migrate = [
                "welcome_message", "broadcast_message", "auto_broadcast",
                "custom_commands", "anti_spam", "group_welcome"
            ]

            for setting_key in settings_to_migrate:
                if setting_key in json_data:
                    self.set_setting(setting_key, json_data[setting_key])

            # Migrate user logs
            if "user_logs" in json_data:
                for log in json_data["user_logs"]:
                    self.add_log(
                        log.get("user_id", 0),
                        log.get("username", ""),
                        log.get("first_name", ""),
                        log.get("action", ""),
                        log.get("details", ""),
                        log.get("ip_address", "")
                    )

            # Migrate scheduled messages
            if "scheduled_messages" in json_data:
                for msg in json_data["scheduled_messages"]:
                    self.add_scheduled_message(
                        msg.get("time", ""),
                        msg.get("message", ""),
                        msg.get("created_by", 0)
                    )

            print("Migration from JSON to PostgreSQL completed successfully")
            return True

        except Exception as e:
            print(f"Migration failed: {e}")
            return False

    def get_stats(self) -> Dict:
        """Get database statistics"""
        if not self.pg_conn:
            return {}

        try:
            stats = {}

            with self.pg_conn.cursor() as cursor:
                # User stats
                cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
                stats["total_users"] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM admins")
                stats["total_admins"] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM user_logs")
                stats["total_logs"] = cursor.fetchone()[0]

                cursor.execute("SELECT COUNT(*) FROM scheduled_messages WHERE is_active = TRUE")
                stats["active_scheduled"] = cursor.fetchone()[0]

                # Recent activity
                cursor.execute("""
                    SELECT COUNT(*) FROM user_logs
                    WHERE timestamp > CURRENT_TIMESTAMP - INTERVAL '24 hours'
                """)
                stats["logs_last_24h"] = cursor.fetchone()[0]

                cursor.execute("""
                    SELECT COUNT(*) FROM users
                    WHERE last_active > CURRENT_TIMESTAMP - INTERVAL '7 days'
                """)
                stats["active_users_7d"] = cursor.fetchone()[0]

            return stats

        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}

    def close(self):
        """Close database connections"""
        if self.pg_conn:
            self.pg_conn.close()
            print("PostgreSQL connection closed")

        if self.redis_conn:
            self.redis_conn.close()
            print("Redis connection closed")

# Global database instance
db_manager = None

def get_db() -> DatabaseManager:
    """Get database manager instance"""
    global db_manager
    if db_manager is None:
        db_manager = DatabaseManager()
    return db_manager

def init_db():
    """Initialize database"""
    global db_manager
    db_manager = DatabaseManager()
    return db_manager