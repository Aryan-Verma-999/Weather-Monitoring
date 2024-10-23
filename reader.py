from sqlalchemy import create_engine, Column, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for our ORM models
Base = declarative_base()

# Define the class that maps to the 'daily_summary' table
class DailySummary(Base):
    __tablename__ = 'daily_summary'
    
    date = Column(Date, primary_key=True)
    city = Column(String, primary_key=True)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_condition = Column(String)

# Create an SQLite engine
engine = create_engine('sqlite:///weather_data.db')

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()
# Query all rows from the 'daily_summary' table
daily_summaries = session.query(DailySummary).all()

# Print out the results
for summary in daily_summaries:
    print(f"Date: {summary.date}, City: {summary.city}, "
          f"Avg Temp: {summary.avg_temp}, Max Temp: {summary.max_temp}, "
          f"Min Temp: {summary.min_temp}, Dominant Condition: {summary.dominant_condition}")
