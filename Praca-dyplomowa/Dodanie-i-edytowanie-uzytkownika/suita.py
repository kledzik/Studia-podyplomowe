import sys
import unittest
import dodanieUzytkownika
import edycjaUzytkownika

class Test_Suite(unittest.TestCase):
    def test_main(self):
        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(DodanieUzytkownika.DodanieUzytkownika),
            unittest.defaultTestLoader.loadTestsFromTestCase(EdycjaUzytkownika.EdycjaUzytkownika),
            ])
        runner = unittest.TextTestRunner()
        runner.run (self.suite)

import unittest

if __name__ == "__main__":
    unittest.main()
