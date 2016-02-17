from app.app import app


class Place:
    @staticmethod
    def get(_id, projections):
        return app.data.driver.db['places'].find_one({'_id': _id}, projections)