from app.db.models import ApiKey, UsageLog, User


# Test de nombres de tablas
def test_model_tablenames() -> None:
    assert User.__tablename__ == "users"
    assert ApiKey.__tablename__ == "api_keys"
    assert UsageLog.__tablename__ == "usage_logs"
