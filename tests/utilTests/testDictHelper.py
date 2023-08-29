from unittest import TestCase

from configTemplate.util import dictHelper

class testDictHelper(TestCase):

    def testJoinXpath(self):

        parent = '$["parent"]'
        childPropertyStr = 'child'

        expectedResult = parent + '["%s"]' % (childPropertyStr)

        result = dictHelper.joinChildToXpath(parent, childPropertyStr)
        self.assertTrue(result == expectedResult, 'Join xpath with child str property returned unexpected result: %s' % result)

        childPropertyNum = 0
        expectedResult = parent + '[%d]' % (childPropertyNum)

        result = dictHelper.joinChildToXpath(parent, childPropertyNum)
        self.assertTrue(result == expectedResult, 'Join xpath with child num property returned unexpected result: %s' % result)

    def testGetChildKeyFromXpath(self):

        xpath = '$["parent"]["foo"][0]["blah"]'
        expectedResult = 'blah'

        result = dictHelper.getChildKeyFromXpath(xpath)
        self.assertTrue(result == expectedResult, 'Get child key returned unexpected result: %s' % (result))

        xpath += '[1]' 
        expectedResult = 1

        result = dictHelper.getChildKeyFromXpath(xpath)
        self.assertTrue(result == expectedResult, 'Get child key returned unexpected result: %s' % (str(result)))

    def testGetParentFromXpath(self):

        xpath = '$["parent"]["foo"][0]["blah"]'
        expectedResult = '$["parent"]["foo"][0]'

        result = dictHelper.getParentXpath(xpath)
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

        xpath = '$["parent"]'
        expectedResult = '$'

        result = dictHelper.getParentXpath(xpath)
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

        xpath = '$'
        expectedResult = None

        result = dictHelper.getParentXpath(xpath)
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

    def testGetParentXpathForKey(self):

        xpath = None
        expectedResult = None
        result = dictHelper.getParentXpathForKey(xpath, 'foo')
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

        xpath = '$'
        expectedResult = None
        result = dictHelper.getParentXpathForKey(xpath, 'foo')
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

        xpath = '$["root"]["foo"]["bar"]["var1"]'
        expectedResult = '$["root"]["foo"]'
        result = dictHelper.getParentXpathForKey(xpath, 'foo')
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

        xpath = '$["root"]["foo"]["bar"]["var1"]'
        expectedResult = None
        result = dictHelper.getParentXpathForKey(xpath, 'var1')
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

        xpath = '$["root"]["foo"]["bar"]["var1"]'
        expectedResult = '$'
        result = dictHelper.getParentXpathForKey(xpath, '$')
        self.assertTrue(result == expectedResult, 'Returned result was %s' % (result))

    def testGetDictFromFlatternedDict(self):

        flatDict = {
            '$["parent"]["foo"]' : 'bar',
            '$["parent"]["list"][0]' : 'a',
            '$["parent"]["list"][1]' : 'b',
            '$["parent"]["list"][2]' : 'c',
            '$["parent"]["blah"]["setting1"]' : 1,
            '$["parent"]["blah"]["setting2"]' : 'x'
        }

        expectedResult = {
            'setting1' : 1,
            'setting2' : 'x'
        }

        result = dictHelper.getDictFromFlatternedDict(flatDict, '$["parent"]["blah"]')
        self.assertDictEqual(result, expectedResult)

        expectedResult = {
            0 : 'a',
            1 : 'b',
            2 : 'c'
        }

        result = dictHelper.getDictFromFlatternedDict(flatDict, '$["parent"]["list"]')
        self.assertDictEqual(result, expectedResult)

        with self.assertRaises(Exception):
            dictHelper.getDictFromFlatternedDict(flatDict, '$["parent"]["foo"]')

        result = dictHelper.getDictFromFlatternedDict(flatDict, '$["parent"]["notexist"]')
        self.assertDictEqual(result, {})

        # expectedResult = {
        #     'parent' : {
        #         'foo' : 'bar',
        #         'list' : {
        #             0 : 'a',
        #             1 : 'b',
        #             2 : 'c',
        #         },
        #         'blah' : {
        #             'setting1' : 1,
        #             'setting2' : 'x'
        #         }
        #     }
        # }
        expectedResult = {            
            'foo' : 'bar',            
            0 : 'a',
            1 : 'b',
            2 : 'c',            
            'setting1' : 1,
            'setting2' : 'x'        
        }

        result = dictHelper.getDictFromFlatternedDict(flatDict, '$')
        self.assertDictEqual(result, expectedResult)