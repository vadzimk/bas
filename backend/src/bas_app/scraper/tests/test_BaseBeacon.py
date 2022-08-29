import unittest
from ..LinkedinBeacon import LinkedinBeacon


class TestBaseBeacon(unittest.TestCase):
    def setUp(self):
        self.beacon = LinkedinBeacon.__new__(LinkedinBeacon)
        self.beacon._job_post = {"company": {}}

    def test_make_attribute_helper(self):
        attr = "description"
        value = "test-result"
        self.beacon.make_attribute_helper(
            self.beacon._job_post,
            attr,
            lambda: value,
            lambda: None)
        self.assertEqual(value, self.beacon._job_post[attr])

    def test_make_attribute(self):
        attr1 = "description1"
        value1 = "test-result1"
        self.beacon.make_attribute(
            attr1,
            lambda: value1,
            lambda: None)
        self.assertEqual(value1, self.beacon._job_post[attr1])

        attr2 = "description2"
        value2 = "test-result2"
        self.beacon.make_attribute(
            attr2,
            lambda: None,
            lambda: value2,
        )

        self.assertEqual(value2, self.beacon._job_post[attr2])

        def raises():
            raise Exception('not Found')

        attr3 = "description3"
        value3 = "test-result3"
        self.beacon.make_attribute(
            attr3,
            raises,
            lambda: value3,
        )
        self.assertEqual(value3, self.beacon._job_post[attr3])

        attr4 = "description4"
        value4 = "test-result4"
        self.beacon.make_attribute(
            attr4,
            lambda: value4,
            raises,
        )
        self.assertEqual(value4, self.beacon._job_post[attr4])
        print(self.beacon._job_post)