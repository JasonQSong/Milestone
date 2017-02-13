#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Yin Yi -- yyi1
# Xiao Song -- xiaos1
# Date Created: 02/10/017
# Date Modified: 02/12/2017

'''
Filter rules:
1. noise: remove all the words in 'MilestonesA Del_YinYi_XiaoSong.txt'
2. substitution: replace words according to 'MilestonesA Sub_YinYi_XiaoSong.txt'
3. Verb-stem: all verbs end with 'ing, ed, s' will be replaced by the stem.
4. Mini-words: filter out all words contain less than two characters.
'''
import re


def main():
    noise_words_list = getDelWord()
    substitution_dic = getRepWord()
    keywords_set = filter_text(noise_words_list, substitution_dic)
    generate_index(keywords_set)


# get junk words
def getDelWord():
    noise_words_list = []
    with open('MilestonesA Del_YinYi_XiaoSong.txt', 'r') as file:
        while True:
            line = file.readline().strip()
            if line == '':
                break
            else:
                noise_words_list.append(line)
        return noise_words_list


# get word replacements
def getRepWord():
    substitution_dic = {}
    with open('MilestonesA Sub_YinYi_XiaoSong.txt', 'r') as file:
        while True:
            try:
                line = file.readline().strip()
                if line == '':
                    break
                else:
                    replace_pairs = line.strip().split(',')
                    substitution_dic[replace_pairs[0]] = replace_pairs[1]
            except UnicodeDecodeError as e:
                print(e)
        return substitution_dic


# pull out keywords from the input file
def filter_text(noise_words_list, substitution_dic):
    keywords_set = set()
    with open('MilestonesA Input_YinYi_XiaoSong.txt', 'r') as file:
        while True:
            line = file.readline()
            if line == '':
                break
            else:
                keywords_set |= separate_words(
                    line, noise_words_list, substitution_dic)
                print(len(keywords_set))
        return keywords_set


# extract words
def separate_words(line, noise_words_list, substitution_dic):
    lower_line = line.lower().strip()
    # Rule2: replace words
    for e in substitution_dic:
        if e in lower_line:
            lower_line.replace(e, substitution_dic.get(e))

    splitter = re.compile('[^a-zA-Z]')
    # Rule4: filter out mini words
    word_set = set([s for s in splitter.split(lower_line) if len(s) > 2])
    clean_word_set = set()
    for w in word_set:
        # Rule3: find out stem for verbs
        stem = getStem(w)
        # Rule1: delete junk words
        if stem not in noise_words_list and len(stem) > 2:
            clean_word_set.add(stem)
    return clean_word_set


# find stems of verbs
def getStem(verb):
    suffixes = ["ing", "ed", "s"]
    for suffix in suffixes:
        if verb.endswith(suffix):
            return verb[:-len(suffix)]
    return verb


# produce the index.html file
def generate_index(keywords_set):
    with open('index.html', 'w') as file:
        file.write('''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Index</title>
</head><body bgcolor="#faebd7"><div><h1 align="center">Welcome to U.S. patent center</h1></div><hr>
<div style="margin-left: 200px; font-size: large"><table><tr><td style="padding-right: 50px">''')
        count = 1
        for i in sorted(keywords_set):
            if count % 1000 == 0:
                file.write('''</td><td style="padding-right: 50px">''')
            file.write(
                '''<li style="margin-bottom: 5px"><a href="#">''' + i + '''</a></li>''')
            count += 1
        file.write('''</td></tr></div></body></html>''')


# Run main
main()
