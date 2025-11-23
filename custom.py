from app import db, create_app

from sqlalchemy import text

app = create_app()

with app.app_context():
    db.session.execute(text("DELETE FROM alembic_version;"))
    db.session.commit()