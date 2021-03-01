import unittest
from LK_Assessment import filters_from_schema, order_from_schema


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

order1 = {'default_value': {''},
          'query': {''},
          'summary_default': {'editable': False,
                              'value': 'single_record'},
          'summary_field': {'editable': False,
                            'value': 'code'},
          'summary_value': {'editable': False,
                            'value': {'column': 'TEST_COL',
                                      'detail_link': True,
                                      'direction': 'desc'}}}

order2 = {'default_value': {''},
          'query': {''},
          'summary_default': {'editable': False,
                              'value': 'single_record'},
          'summary_field': {'editable': False,
                            'value': 'code'},
          'summary_value': {'editable': False,
                            'value': {'column': 'TEST_COL_2',
                                      'detail_link': True,
                                      'direction': 'asc'}}}


class TestFilterConversion(unittest.TestCase):

    # test filters
    def test_cond1(self):
        self.assertEqual(filters_from_schema(conditions1, parent),
                         [['entity.Shot.sg_sequence', 'is', parent], ['entity.Shot.sg_status_list', 'is_not', 'fin']])

    def test_cond2(self):
        self.assertEqual(filters_from_schema(conditions2, parent), [
                         ['entity.Shot.sg_status_list', 'is_not', 'fin']])

    def test_cond3(self):
        self.assertEqual(filters_from_schema(conditions3, parent), [
                         ['entity.Shot.sg_sequence', 'is', parent]])

    # test ordering
    def test_order1(self):
        self.assertEqual(order_from_schema(order1), [
                         {'field_name': 'TEST_COL', 'direction': 'desc'}])

    def test_order2(self):
        self.assertEqual(order_from_schema(order2), [
                         {'field_name': 'TEST_COL_2', 'direction': 'asc'}])


if __name__ == '__main__':
    unittest.main()
