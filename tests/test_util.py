# encoding: utf-8

from unittest import TestCase

from alacarte.util import Cache


class TestCommonUsage(TestCase):
    def setUp(self):
        self.cache = Cache(3)

        self.cache['A'] = 0
        self.cache['B'] = 1
        self.cache['C'] = 2

    def test_basic(self):
        self.assertEqual(repr(self.cache), "{'A': 0, 'C': 2, 'B': 1}")
        self.assertEqual(len(self.cache), 3)
        self.assertEqual(self.cache['A'], 0)

    def test_overflow(self):
        self.cache['D'] = 3

        self.assertEqual(len(self.cache), 3)
        self.assertFalse('A' in self.cache)

    def test_sort(self):
        self.cache['E'] = 4
        self.cache['B']

        self.assertEqual([i for i in self.cache], ['B', 'E', 'C'])

    def test_reassignment(self):
        self.cache['A'] = 5
        self.assertEqual(self.cache['A'], 5)
        self.assertEqual([i for i in self.cache], ['A', 'C', 'B'])

        self.cache['C'] = 6
        self.assertEqual(self.cache['C'], 6)
        self.assertEqual([i for i in self.cache], ['C', 'A', 'B'])

    def test_capacity(self):
        self.cache.capacity = 1
        self.cache._restrict()

        self.assertEqual(len(self.cache), 1)
        self.assertFalse('A' in self.cache)
        self.assertTrue('C' in self.cache)

        self.cache['A'] = 0
        self.assertEqual(len(self.cache), 1)
        self.assertTrue('A' in self.cache)
        self.assertFalse('C' in self.cache)

        self.cache.capacity = 0
        self.cache._restrict()

        self.assertEqual(len(self.cache), 0)
