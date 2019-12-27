import sys
import unittest
import _1_Zablokowanie
import _2_Usuniecie
import _3_OdszyfrowanieZaladowanie
import _4_Domena
import _5_NazwaSesja
import _6_RandomSesja

class Test_Suite(unittest.TestCase):
    def test_main(self):
        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(_1_Zablokowanie._1_Zablokowanie),
            unittest.defaultTestLoader.loadTestsFromTestCase(_2_Usuniecie._2_Usuniecie),
            unittest.defaultTestLoader.loadTestsFromTestCase(_3_OdszyfrowanieZaladowanie._3_OdszyfrowanieZaladowanie),
            unittest.defaultTestLoader.loadTestsFromTestCase(_4_Domena._4_Domena),
            unittest.defaultTestLoader.loadTestsFromTestCase(_5_NazwaSesja._5_NazwaSesja),
            unittest.defaultTestLoader.loadTestsFromTestCase(_6_RandomSesja._6_RandomSesja),
            ])
        runner = unittest.TextTestRunner()
        runner.run (self.suite)

import unittest

if __name__ == "__main__":
    unittest.main()
