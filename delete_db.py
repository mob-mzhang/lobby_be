from sqlalchemy import create_engine, MetaData

# Replace with your actual database URL
DATABASE_URL = "postgresql://postgres.icwupqucbnxynldgqxaq:Baibao0120!@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Create an engine connected to your database
engine = create_engine(DATABASE_URL)

# Reflect the existing database schema
metadata = MetaData()
metadata.reflect(bind=engine)

# Drop all tables
metadata.drop_all(bind=engine)

print("All tables have been dropped.")