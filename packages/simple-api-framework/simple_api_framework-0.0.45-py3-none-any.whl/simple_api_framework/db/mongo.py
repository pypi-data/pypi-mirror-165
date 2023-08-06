from motor.motor_tornado import MotorClient


class MongoDB:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')

    def __connect(self):
        if not self.url:
            raise Exception("MongoDB: no connection url specified")
        mongo = MotorClient(self.url)
        return mongo.get_default_database()

    async def insert(self, collection, data, remove=False):
        db = self.__connect()
        db_collection = db[collection]
        await db_collection.create_index(keys='_id', name=f'{collection}Index')
        if remove:
            await db_collection.delete_many({})
        if isinstance(data, list):
            await db_collection.insert_many(data)
        else:
            await db_collection.insert_one(data)

    async def get(self, collection, many=True, parameters=None):
        db = self.__connect()
        if not parameters:
            parameters = {}
        if many:
            count = await db[collection].count_documents(parameters)
            result = await db[collection].find(parameters).to_list(length=count)
        else:
            result = await db[collection].find_one(parameters)
        return result
