from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User, UserType
from app.core.security import get_password_hash

def create_admin_user():
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@edusphere.com").first()
        if admin:
            print("Admin user already exists!")
            return

        # Create admin user
        admin_user = User(
            email="admin@edusphere.com",
            hashed_password=get_password_hash("Admin@123"),  # You should change this password
            user_type=UserType.UNIVERSITY,  # Admin is a type of university user
            is_active=True,
            is_verified=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        print("Admin user created successfully!")
        print("Email: admin@edusphere.com")
        print("Password: Admin@123")
        print("\nIMPORTANT: Please change this password immediately after first login!")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 