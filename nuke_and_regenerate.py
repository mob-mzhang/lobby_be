import uuid
from faker import Faker
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from random import choice, randint, sample
from src.database import SessionLocal, engine
from src.models import Base, User, Friend, Event, user_event

#L6X3U5R68EPRUXYGT4R8VP24

# Recreate all tables
fake = Faker()

# Create all tables
Base.metadata.create_all(bind=engine)

# List of common Chinese surnames
chinese_surnames = ['Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou']

# List of event names and their descriptions
event_descriptions = {
    'House Party': "Join us for a fun-filled house party! Bring your favorite snacks and drinks.",
    'Golf': "Let's hit the greens for a relaxing day of golf. All skill levels welcome!",
    'Ski Trip': "Get ready for an exciting ski trip in the mountains. Don't forget your warm clothes!",
    'Cooking Potluck': "Bring your signature dish and let's enjoy a delicious potluck together.",
    'Games Night': "It's game on! We'll have a variety of board games and video games.",
    'Karaoke': "Sing your heart out at our karaoke night. No talent required, just enthusiasm!"
}

event_names = list(event_descriptions.keys())

def generate_chinese_american_name():
    return f"{choice(chinese_surnames)} {fake.first_name()}"

def generate_phone_number():
    return fake.numerify(text="(###) ###-####")

def create_fake_users(db: Session, num_users=50):
    users = []
    for _ in range(num_users):
        user = User(
            id=str(uuid.uuid4()),
            username=generate_chinese_american_name(),
            phone_number=generate_phone_number(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year()
        )
        users.append(user)
    db.add_all(users)
    db.commit()
    return users

def create_fake_friends(db: Session, users, num_friendships=100):
    for _ in range(num_friendships):
        user1, user2 = sample(users, 2)
        friendship = Friend(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            friend_id=user2.id
        )
        db.add(friendship)
    db.commit()

def create_fake_events(db: Session, users, num_events=30):
    events = []
    for _ in range(num_events):
        host = choice(users)
        event_name = choice(event_names)
        event = Event(
            id=str(uuid.uuid4()),
            name=event_name,
            description=event_descriptions[event_name],
            date=fake.future_datetime(end_date="+30d"),
            host_id=host.id
        )
        events.append(event)
    db.add_all(events)
    db.commit()
    return events

def add_users_to_events(db: Session, users, events):
    for event in events:
        num_participants = randint(1, 10)
        participants = sample(users, num_participants)
        for user in participants:
            db.execute(user_event.insert().values(user_id=user.id, event_id=event.id))
    db.commit()

def main():
    db = SessionLocal()
    try:
        # Create fake users
        users = create_fake_users(db)
        print(f"Created {len(users)} fake users.")

        # Create fake friendships
        create_fake_friends(db, users)
        print("Created fake friendships.")

        # Create fake events
        events = create_fake_events(db, users)
        print(f"Created {len(events)} fake events.")

        # Add users to events
        add_users_to_events(db, users, events)
        print("Added users to events.")

        print("Fake data has been generated and pushed to the database.")
    finally:
        db.close()

if __name__ == "__main__":
    main()