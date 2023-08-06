import unittest

import numpy as np

from osaft.core.warnings import AssumptionWarning, raise_assumption_warning


class TestCustomWarnings(unittest.TestCase):

    def test_AssumptionWarning(self) -> None:
        for _ in np.arange(5):
            val = np.random.randint(0, 100) * np.random.random_sample()

            with self.assertWarns(AssumptionWarning) as _:
                raise_assumption_warning(val >= 0.9 * val)
            with self.assertWarns(AssumptionWarning) as _:
                raise_assumption_warning(val <= 1.1 * val)


if __name__ == '__main__':
    unittest.main()
