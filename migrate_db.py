#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DATABASE MIGRATION SCRIPT
Migrate data from JSON to PostgreSQL
"""

import os
import sys
from database import get_db

def main():
    """Main migration function"""
    print("🚀 Starting database migration...")

    # Initialize database
    db = get_db()

    if not db.pg_conn:
        print("❌ PostgreSQL connection failed. Please check DATABASE_URL environment variable.")
        sys.exit(1)

    # Check if migration already done
    if db.get_setting("migration_completed"):
        print("✅ Migration already completed!")
        return

    # Start migration
    print("📊 Migrating data from JSON to PostgreSQL...")

    success = db.migrate_from_json()

    if success:
        # Mark migration as completed
        db.set_setting("migration_completed", True)
        print("✅ Migration completed successfully!")

        # Show statistics
        stats = db.get_stats()
        print("\n📈 Migration Statistics:")
        print(f"• Users migrated: {stats.get('total_users', 0)}")
        print(f"• Admins migrated: {stats.get('total_admins', 0)}")
        print(f"• Logs migrated: {stats.get('total_logs', 0)}")
        print(f"• Scheduled messages: {stats.get('active_scheduled', 0)}")

        print("\n🎉 Bot is now using PostgreSQL database!")
        print("💡 You can safely delete bot_database.json if migration is successful.")

    else:
        print("❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()