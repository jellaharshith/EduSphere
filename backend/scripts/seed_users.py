from app.db.session import SessionLocal
from app.models import user, opportunity
from app.models.user import User, UserType
from app.core.security import get_password_hash

# Create a new database session
session = SessionLocal()

# Create admin user (as a university type)
admin = User(
    email="admin@example.com",
    hashed_password=get_password_hash("adminpassword"),
    user_type=UserType.UNIVERSITY,
    is_active=True,
    is_verified=True
)

# Create dummy user (as a student type)
user = User(
    email="user@example.com",
    hashed_password=get_password_hash("userpassword"),
    user_type=UserType.STUDENT,
    is_active=True,
    is_verified=True
)

# Add users to the session and commit
session.add(admin)
session.add(user)
session.commit()
session.close()
print("Admin (university) and dummy (student) user created!") 