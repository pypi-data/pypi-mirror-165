#!/usr/bin/env python
# coding: utf-8

# In[8]:


# -*- coding: utf-8 -*-
#
# Natural Language Toolkit: ARLSTem Stemmer
#
# Author: Kheireddine Abainia (x-programer) <k.abainia@gmail.com>
# Algorithms: Kheireddine Abainia <k.abainia@gmail.com>
#                         Siham Ouamour
#                         Halim Sayoud


"""
ARLSTem Arabic Stemmer
The details about the implementation of this algorithm are described in:
K. Abainia, S. Ouamour and H. Sayoud, A Novel Robust Arabic Light Stemmer ,
Journal of Experimental & Theoretical Artificial Intelligence (JETAI'17),
Vol. 29, No. 3, 2017, pp. 557-573.
The ARLSTem is a light Arabic stemmer that is based on removing the affixes
from the word (i.e. prefixes, suffixes and infixes). It was evaluated and
compared to several other stemmers using Paice's parameters (under-stemming
index, over-stemming index and stemming weight), and the results showed that
ARLSTem is promising and producing high performances. This stemmer is not
based on any dictionary and can be used on-line effectively.
"""
from __future__ import unicode_literals
import re


class Normalization:
    '''
    ARLSTem stemmer : a light Arabic Stemming algorithm without any dictionary.
    Department of Telecommunication & Information Processing. USTHB University,
    Algiers, Algeria.
    ARLSTem.stem(token) returns the Arabic stem for the input token.
    The ARLSTem Stemmer requires that all tokens are encoded using Unicode
    encoding.
    '''

    def __init__(self):
        # different Alif with hamza
        self.re_hamzated_alif = re.compile(r'[\u0622\u0623\u0625]')
        self.re_alifMaqsura = re.compile(r'[\u0649]')
        self.re_diacritics = re.compile(r'[\u064B-\u065F]')

        # Alif Laam, Laam Laam, Fa Laam, Fa Ba
        self.pr2 = [
            '\u0627\u0644', '\u0644\u0644',
            '\u0641\u0644', '\u0641\u0628'
            ]
        # Ba Alif Laam, Kaaf Alif Laam, Waaw Alif Laam
        self.pr3 = [
            '\u0628\u0627\u0644',
            '\u0643\u0627\u0644',
            '\u0648\u0627\u0644'
            ]
        # Fa Laam Laam, Waaw Laam Laam
        self.pr32 = ['\u0641\u0644\u0644', '\u0648\u0644\u0644']
        # Fa Ba Alif Laam, Waaw Ba Alif Laam, Fa Kaaf Alif Laam
        self.pr4 = [
            '\u0641\u0628\u0627\u0644',
            '\u0648\u0628\u0627\u0644',
            '\u0641\u0643\u0627\u0644'
            ]

        # Kaf Yaa, Kaf Miim
        self.su2 = [
            '\u0643\u064A',
            '\u0643\u0645'
            ]
        # Ha Alif, Ha Miim
        self.su22 = ['\u0647\u0627', '\u0647\u0645']
        # Kaf Miim Alif, Kaf Noon Shadda
        self.su3 = ['\u0643\u0645\u0627', '\u0643\u0646\u0651']
        # Ha Miim Alif, Ha Noon Shadda
        self.su32 = ['\u0647\u0645\u0627', '\u0647\u0646\u0651']

        # Alif Noon, Ya Noon, Waaw Noon
        self.pl_si2 = ['\u0627\u0646', '\u064A\u0646', '\u0648\u0646']
        # Taa Alif Noon, Taa Ya Noon
        self.pl_si3 = ['\u062A\u0627\u0646', '\u062A\u064A\u0646']

        # Alif Noon, Waaw Noon
        self.verb_su2 = ['\u0627\u0646', '\u0648\u0646']
        # Siin Taa, Siin Yaa
        self.verb_pr2 = ['\u0633\u062A', '\u0633\u064A']
        # Siin Alif, Siin Noon
        self.verb_pr22 = ['\u0633\u0627', '\u0633\u0646']

        # Taa Miim Alif, Taa Noon Shadda
        self.verb_suf3 = ['\u062A\u0645\u0627', '\u062A\u0646\u0651']
        # Noon Alif, Taa Miim, Taa Alif, Waaw Alif
        self.verb_suf2 = [
            '\u0646\u0627', '\u062A\u0645',
            '\u062A\u0627', '\u0648\u0627'
            ]
        # Taa, Alif, Noon
        self.verb_suf1 = ['\u062A', '\u0627', '\u0646']

   
    def norm(self, token):
        """
            normalize the word by removing diacritics, replacing hamzated Alif
            with Alif replacing AlifMaqsura with Yaa and removing Waaw at the
            beginning.
        """
        # strip Arabic diacritics
        token = self.re_diacritics.sub('', token)
        # replace Hamzated Alif with Alif bare
        token = self.re_hamzated_alif.sub('\u0627', token)
        # replace alifMaqsura with Yaa
        token = self.re_alifMaqsura.sub('\u064A', token)
        # strip the Waaw from the word beginning if the remaining is 3 letters
        # at least
        if token.startswith('\u0648') and len(token) > 3:
            token = token[1:]
        return token

   


