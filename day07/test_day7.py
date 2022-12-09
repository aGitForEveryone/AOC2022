# Unit testing
"""
@author: Tobias Van Damme
"""

import unittest
import json
from pathlib import Path


from . import day7


TEST_FOLDER = Path(__file__).parent


class TestDay7(unittest.TestCase):
    """Test class to test functions in day07.day7"""

    def setUp(self):
        """Setup the tests"""
        pass

    def tearDown(self):
        """Clean up"""
        pass

    def test_create_file_system(self):
        """Test day7.create_file_system"""
        commands = ["$ cd /", "$ cd a", "$ cd ..", "$ cd b"]
        commands = """$ cd /
$ ls
dir brdsppd
dir dnjqmzgg
126880 fmftdzrp.fwt
173625 hhfqgzfj.qvt
dir lbbcfjl
dir mzdqcb
dir npppw
dir plmb
6337 rfgtcj.tdn
dir szfw
230140 vmc.cdf""".splitlines()
        file_system = day7.create_file_system(commands)
        day7.render_file_system(file_system[Path(day7.HOME)])


if __name__ == "__main__":
    unittest.main(module="test_day7")
