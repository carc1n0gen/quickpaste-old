from datetime import datetime, timedelta
from unittest.mock import Mock


def mock_get_paste_factory(id, content_list):
    ret = Mock()
    ret.side_effect = [
        {
            '_id': id,
            'created_at': datetime.utcnow(),
            'delete_at': datetime.utcnow(),
            'text': content
        } for content in content_list
    ]
    return ret


class MockMongoCollection:
    def find_one(self, query):
        id = query['_id']
        if id == 'abcd':
            return {
                '_id': id,
                'created_at': datetime.utcnow(),
                'delete_at': datetime.utcnow() + timedelta(days=2),
                'text': 'The cow goes mooooooo.'
            }
        elif id == 'about':
            return {
                '_id': id,
                'created_at': datetime.utcnow(),
                'delete_at': None,
                'text': 'The about page.'
            }

    def update_one(self, query, updates, upsert=False):
        ret = Mock()
        ret.modified_count = 1
        ret.raw_result = {
            '_id': 'zyxw',
            'created_at': datetime.utcnow(),
            'delete_at': datetime.utcnow() + timedelta(days=2),
            'text': 'peep peep peep peep, I\'m a baby chicken.'
        }

        if upsert:
            ret.upserted_id = 'zyxw'

        return ret

    def delete_one(self, query):
        ret = Mock()
        id = query['_id']

        if id == 'abcd':
            ret.deleted_count = 1
        else:
            ret.deleted_count = 0

        return ret


class MockMongoDatabase:
    def __getitem__(self, name):
        if name == 'pastes':
            return MockMongoCollection()


class MockMongoClient:
    def __init__(self, *args, **kwargs):
        pass

    def __getitem__(self, name):
        if name == 'quickpaste':
            return MockMongoDatabase()

    def close(self):
        pass
