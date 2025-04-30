from app.db.session import engine
from app.models import user, opportunity

user.Base.metadata.create_all(bind=engine)
opportunity.Base.metadata.create_all(bind=engine)
print("Tables created!") 