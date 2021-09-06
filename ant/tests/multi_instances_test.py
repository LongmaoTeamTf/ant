#!/usr/bin/python3
# -*- coding: utf-8 -*-

from absl.testing import parameterized, absltest

import tempfile
import numpy as np
from ant.core import TopKSearch
from ant.core import MultiInstances


class MultiInstancesTest(parameterized.TestCase):

    def test(self):
        with tempfile.TemporaryDirectory() as tmp:
            mis = MultiInstances(tmp)
            self.assertEqual(mis.list_instances(), [])
            mis.create_instance("tests", {"dim": 10})
            self.assertEqual(mis.list_instances(), ["tests"])
            instance = mis.get_instance("tests")
            self.assertEqual(type(instance), TopKSearch)
            mis.delete_instance("tests")
            self.assertEqual(mis.list_instances(), [])


if __name__ == '__main__':
    absltest.main()
