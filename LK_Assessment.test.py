import unittest
from LK_Assessment import filters_from_schema


parent = {'type': 'Sequence', 'id': 41}

conditions1 = [{'active': 'true',
                'path': 'entity.Shot.sg_sequence',
                'relation': 'is',
                'values': [{'id': 0,
                            'name': 'Current '
                            'Sequence',
                            'type': 'Sequence',
                            'valid': 'parent_entity_token'}]},
               {'active': 'true',
                'path': 'entity.Shot.sg_status_list',
                'relation': 'is_not',
                'values': ['fin']}]

conditions2 = [{'active': 'true',
                'path': 'entity.Shot.sg_status_list',
                'relation': 'is_not',
                'values': ['fin']}]

conditions3 = [{'path': 'entity.Shot.sg_sequence',
                'relation': 'is',
                'values': [{'type': 'Sequence',
                            'id': 0,
                            'name': 'Current Sequence',
                            'valid': 'parent_entity_token'}]}]


class TestFilterConversion(unittest.TestCase):

    def test_cond1(self):
        self.assertEqual(filters_from_schema(conditions1, parent),
                         [['entity.Shot.sg_sequence', 'is', parent], ['entity.Shot.sg_status_list', 'is_not', 'fin']])

    def test_cond2(self):
        self.assertEqual(filters_from_schema(conditions2, parent), [
                         ['entity.Shot.sg_status_list', 'is_not', 'fin']])

    def test_cond3(self):
        self.assertEqual(filters_from_schema(conditions3, parent), [
                         ['entity.Shot.sg_sequence', 'is', parent]])


if __name__ == '__main__':
    unittest.main()
