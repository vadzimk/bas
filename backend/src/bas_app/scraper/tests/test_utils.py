import unittest

from bas_app.scraper.utils import normalize_company_homepage_url


class TestUtils(unittest.TestCase):

    def test_normalize_company_profile_url(self):
        in1r = "https://corporate.televisaunivision.com"
        in1e = "https://corporate.televisaunivision.com"
        self.assertEqual(
            in1e,
            normalize_company_homepage_url(in1r))
        in2r = "https://ocompany.io/"
        in2e = "https://ocompany.io"
        self.assertEqual(
            in2e,
            normalize_company_homepage_url(in2r))
        in3r = "https://www.fanduel.com/careers"
        in3e = "https://www.fanduel.com"
        in4r = "https://www.edwardjones.com/us-en/"
        in4e = "https://www.edwardjones.com"
        in5r = "http://www.judge.com?&utm_source=linkedin.com&utm_medium=social"
        in5e = "http://www.judge.com"
        in6r = "https://careers.blizzard.com/?utm_source=linkedin"
        in6e = "https://careers.blizzard.com"
        in7r = "http://www.boozallen.com?source=SNS-17780"
        in7e = "http://www.boozallen.com"
        in8r = "http://www.CyberCoders.com"
        in8e = "http://www.cybercoders.com"

if __name__ == '__main__':
    unittest.main()