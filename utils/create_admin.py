from database.connection import SessionLocal
from database.models import User
from utils.security import hash_password

password=hash_password("admin123")

session = SessionLocal()

admin = session.query(User).filter(
    User.username == "admin"
).first()

if not admin:

    admin = User(
        username="admin",
        password=hash_password("admin123"),
        role="Admin",
    )

    session.add(admin)
    session.commit()

    print("Admin user created.")

else:

    print("Admin already exists.")

session.close()