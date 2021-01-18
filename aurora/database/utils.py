def recreate_db(base, engine):
    base.metadata.drop_all(engine)
    base.metadata.create_all(engine)
