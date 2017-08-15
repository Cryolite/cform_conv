# -*- coding: utf-8 -*-

import re

conj_suffixes = {}
with open('conj_suffixes.txt') as f:
    for line in f:
        line = line.rstrip()
        columns = line.split(',')
        if len(columns) != 3:
            raise AssertionError
        ctype = columns[0]
        cform = columns[1]
        suffixes = columns[2]
        suffixes = suffixes.split('|')
        if (ctype, cform) in conj_suffixes:
            print(','.join((ctype, cform, str(suffixes))))
            raise AssertionError
        conj_suffixes[(ctype, cform)] = suffixes

if False:
    with open('mecab-naist-jdic-0.6.3b-20111013/naist-jdic.csv.utf-8') as f:
        for line in f:
            line = line.rstrip()
            columns = line.split(',')
            if len(columns) != 15:
                raise AssertionError
            surface = columns[0]
            ctype = columns[8]
            cform = columns[9]
            if ctype == '*':
                if cform != '*':
                    raise AssertionError
                continue
            if (ctype, cform) not in conj_suffixes:
                print(','.join((ctype, cform)))
                raise AssertionError
            found = False
            for suffix in conj_suffixes[(ctype, cform)]:
                if re.search('{0}$'.format(suffix), surface):
                    found = True
                    break
            if not found:
                print(','.join((surface, ctype, cform)))

def convertConjugationSuffix(surface, ctype, cform, target_cform):
    if (ctype, cform) not in conj_suffixes:
        raise AssertionError
    suffixes = conj_suffixes[(ctype, cform)]
    if (ctype, target_cform) not in conj_suffixes:
        raise AssertionError
    target_suffixes = conj_suffixes[(ctype, target_cform)]
    for suffix in suffixes:
        m = re.search('^(.*){0}$'.format(suffix), surface)
        if m:
            stem = m.group(1)
            results = []
            for target_suffix in target_suffixes:
                results.append(stem + target_suffix)
            return results
    raise AssertionError

print(convertConjugationSuffix('うれし', '形容詞・アウオ段', 'ガル接続', '連用テ接続'))
print(convertConjugationSuffix('うれしい', '形容詞・アウオ段', '基本形', '連用テ接続'))
