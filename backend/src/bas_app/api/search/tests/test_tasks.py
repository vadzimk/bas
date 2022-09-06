import unittest

from bas_app.api.search.tasks import convert_search_fields


class TestTasks(unittest.TestCase):
    def test_convert_search_fields_linkedin(self):
        form_values_linkedin = {'what': 'test role',
                                'where': 'test city',
                                'radius': '10mi',
                                'age': 'day',
                                'experience': ['entry level', 'mid-senior'],
                                'limit': ''}
        expected_out_linkedin = {'what': 'test role',
                                 'where': 'test city',
                                 'radius': 'distance=10',
                                 'age': '&f_TPR=r86400',
                                 'experience': ['2', '4'],
                                 'limit': ''}

        out_values_linkedin = convert_search_fields(form_values_linkedin, 'linkedin')
        self.assertEqual(expected_out_linkedin, out_values_linkedin)


    def test_convert_search_fields_indeed(self):
        form_values_indeed = {'what': 'test role',
                              'where': 'test city',
                              'radius': '100mi',
                              'age': '14 days',
                              'experience': 'entry level',
                              'education': 'school',
                              'limit': ''}
        expected_out_indeed = {'what': 'test role',
                               'where': 'test city',
                               'radius': '&radius=100',
                               'age': '14',
                               'experience': 'explvl(ENTRY_LEVEL)',
                               'education': 'attr(FCGTU%7CQJZM9%252COR)',
                               'limit': ''}
        out_values_indeed = convert_search_fields(form_values_indeed, 'indeed')
        print('expect', expected_out_indeed)
        print('actual', out_values_indeed)
        self.assertEqual(expected_out_indeed, out_values_indeed)


if __name__ == '__main__':
    unittest.main()
