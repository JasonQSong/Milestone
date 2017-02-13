#!/usr/bin/env python
# Author: Jason Song

'''
Filter rules:
1. noise: remove all the words in 'MilestonesA_noise_words.txt'
2. substitution: replace words according to 'MilestonesA_replacement_words.txt'
3. Verb-stem: all verbs end with 'ing, ed, s' will be replaced by the stem.
4. Mini-words: filter out all words contain less than two characters.
'''
import logging
import re

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


NOISE_WORDS_FILEPATH = 'MilestoneA_noise_words.txt'
REPLACEMENT_WORDS_FILEPATH = 'MilestoneA_replacement_words.txt'
INPUT_FILEPATH = 'MilestoneA_input.txt'
REPORT_FILEPATH = 'index.html'


def read_noise_words(noise_words_filepath=NOISE_WORDS_FILEPATH):
    '''Get junk words.'''
    noise_words = []
    with open(noise_words_filepath, 'r') as noise_words_file:
        noise_words = noise_words_file.readlines()
    return [l.strip() for l in noise_words if l.strip()]


def read_replacement_words(replacement_words_filepath=REPLACEMENT_WORDS_FILEPATH):
    '''Get word replacements'''
    replacement_words_lines = []
    with open(replacement_words_filepath, 'r') as replacement_words_file:
        replacement_words_lines = replacement_words_file.readlines()
    replacement_words_lines = [l.strip()
                               for l in replacement_words_lines if l.strip()]
    replacement_words = {
        l.split(',')[0]: l.split(',')[1]
        for l in replacement_words_lines if l.find(',') >= 0
    }
    return replacement_words


def parse_stem(verb):
    '''Find stems of verbs.'''
    suffixes = ["ing", "ed", "s"]
    for suffix in suffixes:
        if verb.endswith(suffix):
            return verb[:-len(suffix)]
    return verb


def parse_keywords(article, replacement_words, noise_words):
    '''Parse the keywords from article with replacement words exclude noise words.

    Return a list of sorted unique tokens.
    '''
    article = article.lower()
    LOG.debug('Lower article: %s', article)
    # Rule2: replace words
    for key, value in replacement_words.items():
        article = article.replace(key, value)
    LOG.debug('Replaced article: %s', article)
    tokens = re.findall('[a-z]+', article)
    LOG.debug('Tokens: %s', tokens)
    # Rule3: find out stem for verbs
    # Rule4: filter out mini words
    keywords = [parse_stem(verb=w) for w in tokens if len(w) > 2]
    LOG.debug('Parsed keywords: %s', keywords)
    # Rule1: delete noise words
    return list(sorted(set(keywords) - set(noise_words)))

REPORT_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Index</title>
</head>
<body bgcolor="#faebd7">
    <div>
        <h1 align="center">Welcome to U.S. patent center</h1>
    </div>
    <hr/>
    <div style="margin-left: 200px; font-size: large">
        <table>
            <tr>
                <td style="padding-right: 50px">
                %s
                </td>
            </tr>
        </table>
    </div>
</body>
</html>
'''
REPORT_LINESEP_TEMPLATE = '''</td>
<td style="padding-right: 50px">'''
REPORT_KEYWORD_TEMPLATE = '''<li style="margin-bottom: 5px"><a href="#">%s</a></li>
'''


def generate_report(keywords, report_filepath=REPORT_FILEPATH):
    '''Produce the report index.html file.'''
    content = ''
    for i, keyword in enumerate(keywords):
        if i and i % 1000 == 0:
            content += REPORT_LINESEP_TEMPLATE
        content += REPORT_KEYWORD_TEMPLATE % keyword
    with open(report_filepath, 'w') as report_file:
        report_file.write(REPORT_TEMPLATE % content)
        LOG.info('Report generated at %s', report_filepath)


def main():
    '''Main function.'''
    noise_words = read_noise_words()
    LOG.debug('Noise words: %s', noise_words)
    replacement_words = read_replacement_words()
    LOG.debug('Replacement words: %s', replacement_words)
    with open(INPUT_FILEPATH, 'r') as input_file:
        article = input_file.read()
    LOG.debug('Article : %s', article)
    keywords = parse_keywords(
        article=article, noise_words=noise_words, replacement_words=replacement_words)
    LOG.info('Keywords (%s): %s', len(keywords), keywords)
    generate_report(keywords=keywords)

if __name__ == '__main__':
    main()
