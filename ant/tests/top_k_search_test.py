#!/usr/bin/python3
# -*- coding: utf-8 -*-

from absl.testing import parameterized, absltest

import tempfile
import numpy as np
from recommends.recall.faiss.top_k_search import TopKSearch


class TopKSearchTest(parameterized.TestCase):

    d = 64  # dimension
    nb = 100000  # database size
    nq = 10000  # nb of queries
    np.random.seed(1234)  # make reproducible
    xb = np.random.random((nb, d)).astype('float32')
    xb[:, 0] += np.arange(nb) / 1000.
    xq = np.random.random((nq, d)).astype('float32')
    xq[:, 0] += np.arange(nq) / 1000.
    xb_ids = np.arange(0, nb)
    xq_ids = np.arange(nb, nb + nq)
    version = "1"

    def test_not_exists_dir(self):

        not_exists_dir = "/abc/def"

        self.assertRaisesRegex(FileNotFoundError,
                               not_exists_dir,
                               TopKSearch, not_exists_dir, self.version, self.d)

    def test_not_build_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)

            self.assertRaisesRegex(ValueError,
                                   "Exec insert method, must run `build` method before.",
                                   tks.insert, self.xq, self.xq_ids)

    def test_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            self.assertEqual(tks.num_total, self.nb)

    def test_insert(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            tks.insert(self.xq, self.xq_ids)
            self.assertEqual(tks.num_total, self.nb + self.nq)

    def test_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            tks.insert(self.xq, self.xq_ids)
            tks.update(self.xq, self.xq_ids)
            self.assertEqual(tks.num_total, self.nb + self.nq)

    def test_remove(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            tks.insert(self.xq, self.xq_ids)
            self.assertEqual(tks.num_total, self.nb + self.nq)
            self.assertIn(100001, tks.ids)
            tks.remove(self.xq_ids)
            self.assertEqual(tks.num_total, self.nb)
            self.assertNotIn(100001, tks.ids)

    def test_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            distances, ids = tks.search(self.xq[:2], top_k=10)
            self.assertEqual(len(ids), 2)
            self.assertEqual(len(ids[0]), 10)

    def test_write_aof(self):

        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            tks.memory_lock = True
            tks.insert(self.xq, self.xq_ids)
            self.assertEqual(tks.num_total, self.nb)
            tks.update(self.xq, self.xq_ids)
            self.assertEqual(tks.num_total, self.nb)
            tks.remove(self.xq_ids)
            self.assertEqual(tks.num_total, self.nb)

    def test_restore_from_aof(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.memory_lock = True
            tks.build(self.xb, self.xb_ids)

            tks.memory_lock = False
            tks.aof_lock = True
            self.assertRaisesRegex(ValueError,
                                   "Exec num_total method, must run `build` method before.",
                                   lambda: tks.num_total)
            tks.restore_from_aof()
            self.assertEqual(tks.num_total, self.nb)

    def test_restore_from_fif(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            tks.save()
            new_tks = TopKSearch(tmp, self.version, self.d)
            new_tks.restore_from_fif()
            self.assertEqual(new_tks.num_total, self.nb)

    def test_restore_from_buffer(self):
        with tempfile.TemporaryDirectory() as tmp:
            tks = TopKSearch(tmp, self.version, self.d)
            tks.build(self.xb, self.xb_ids)
            tks.memory_lock = True
            tks.aof_lock = True
            tks.insert(self.xq, self.xq_ids)
            self.assertEqual(tks.num_total, self.nb)
            tks.memory_lock = False
            tks.aof_lock = True
            tks.restore_from_aof(buffer=True)
            self.assertEqual(tks.num_total, self.nb + self.nq)


if __name__ == '__main__':
    absltest.main()
