from database.connection import SessionLocal
from database.models import User
from utils.security import hash_password


session = SessionLocal()

admin = session.query(User).filter(
    User.username == "admin"
).first()

new_password = hash_password("admin123")

if not admin:

    admin = User(
        username="admin",
        password=new_password,
        role="Admin",
    )

    session.add(admin)

    print("Admin user created.")

else:

    admin.password = new_password
    admin.role = "Admin"

    print("Admin password reset successfully.")

session.commit()
session.close()