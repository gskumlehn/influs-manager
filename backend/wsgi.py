from app import create_app
from app.infra.database import Base, engine

app = create_app()

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(host="0.0.0.0", port=5000, debug=True)
