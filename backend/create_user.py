"""Script para crear un usuario y generar su primera API key."""

from app.auth.api_key import create_api_key
from app.db.database import SessionLocal, engine
from app.db.models import ApiKey, Base, User

Base.metadata.create_all(bind=engine)

EMAIL = "test@test.com"

with SessionLocal() as db:
    user = db.query(User).filter(User.email == EMAIL).first()
    if not user:
        user = User(email=EMAIL)
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Usuario creado: {user.email} (id={user.id})")
    else:
        print(f"Usuario ya existe: {user.email} (id={user.id})")

    created = create_api_key()
    api_key_row = ApiKey(
        user_id=user.id,
        key_prefix=created.key_prefix,
        key_hash=created.key_hash,
    )
    db.add(api_key_row)
    db.commit()

    print(f"\nAPI key generada (guardala, no se muestra de nuevo):")
    print(f"  {created.raw_key}")
    print(f"\nPoné esto en frontend/.env:")
    print(f"  VITE_API_URL=http://localhost:8000")
    print(f"  VITE_API_KEY={created.raw_key}")
