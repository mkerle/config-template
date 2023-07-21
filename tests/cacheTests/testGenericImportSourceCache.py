from unittest import TestCase

from configTemplate.importSource.genericTemplateSourceCache import GenericTemplateSourceCache

from tests.baseTest import EXAMPLE_TEMPLATE_DIR
import pathlib


class testGenericImportSourceCache(TestCase):

    def testCreateCache(self):

        cache = GenericTemplateSourceCache()

        self.assertIsInstance(cache, GenericTemplateSourceCache)

    def testCache(self):        

        cache = GenericTemplateSourceCache()

        p = pathlib.Path(EXAMPLE_TEMPLATE_DIR)
        self.assertTrue(p.is_dir(), 'Test Path is not a directory [%s]' % (p.as_posix()))

        lastCacheKey = ''
        expectedCacheCount = 0
        for f in p.iterdir():

            if (f.is_file()):
                
                cache.add(f.name, f)
                expectedCacheCount += 1

                cacheVal = cache.get(f.name)
                self.assertTrue(cacheVal == f, 'Get object from cache did not match')

                lastCacheKey = f.name

        numCacheItems = len(cache.cache)
        self.assertTrue(numCacheItems == expectedCacheCount, 'Number of items in cache is different.  Expected [%d], got [%d]' % (expectedCacheCount, numCacheItems))

        cache.clearCache()
        self.assertIsNone(cache.get(lastCacheKey), 'Clear Cache failed - Item [%s] still found in cache' % (lastCacheKey))


        