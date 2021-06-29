from extract_courses import engine, Base
Base.metadata.create_all(bind=engine)