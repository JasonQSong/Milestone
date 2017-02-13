'''Unittests for MilestoneA.'''
import unittest
import MilestoneA


class TestMilestoneA(unittest.TestCase):

    def test_read_noise_words(self):
        noise_words = MilestoneA.read_noise_words(
            noise_words_filepath='test_MilestoneA_noise_words.txt')
        self.assertListEqual(noise_words, [
            'add', 'are', 'and', 'book'
        ])

    def test_read_replacement_words(self):
        replacement_words = MilestoneA.read_replacement_words(
            replacement_words_filepath='test_MilestoneA_replacement_words.txt')
        self.assertDictEqual(replacement_words, {
            'com': 'company',
            'gmail': 'google',
            'dummy': ''
        })

    def test_parse_stem(self):
        self.assertEqual(MilestoneA.parse_stem(verb='test'), 'test')
        self.assertEqual(MilestoneA.parse_stem(verb='tested'), 'test')
        self.assertEqual(MilestoneA.parse_stem(verb='testing'), 'test')
        self.assertEqual(MilestoneA.parse_stem(verb='tests'), 'test')

    def test_parse_keywords(self):
        article = 'This is an long article. I am testing these filters working status'
        replacement_words = {'this': 'that', 'dummy': 'none'}
        noise_words = ['these', 'null']
        keywords = MilestoneA.parse_keywords(
            article=article, replacement_words=replacement_words, noise_words=noise_words)
        self.assertListEqual(keywords, [
            'article', 'filter', 'long', 'statu', 'test', 'that', 'work'
        ])

    def test_integration(self):
        # Cannot test integration w/o mocking file write
        pass
