from datetime import datetime, timedelta
from unittest.mock import Mock


def mock_get_paste(id):
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
    return None


def mock_delete_paste(id):
    ret = Mock()

    if id == 'abcd':
        ret.deleted_count = 1
    else:
        ret.deleted_count = 0

    return ret


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


def mock_upsert(d):
    return 'zyxw'
