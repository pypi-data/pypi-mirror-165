
def version(**kwargs): # pylint: disable=R0911
    if kwargs['engine'] in ('redshift', 'postgres'):
        from syngenta_digital_dbv.postgres.versioner import PostgresVersioner # pylint: disable=C
        redshift_versioner = PostgresVersioner(**kwargs)
        redshift_versioner.version()
    elif kwargs['engine'] == 'mongo':
        from syngenta_digital_dbv.mongo.versioner import MongoVersioner # pylint: disable=C
        mongo_versioner = MongoVersioner(**kwargs)
        mongo_versioner.version()
    else:
        raise Exception(f'engine {kwargs["engine"]} not supported; contribute to get it supported')
