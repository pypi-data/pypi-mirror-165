#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

import ahocorasick
from .diPwm import diPWM
from .Enumerate import enumerate_words_LAM, enumerate_words_LAM_ratio


def search_aho(diP, text, threshold):
	""" Search of a set of words through a text using Aho-Corasick algorithm for a given threshold.

	Args:
		diP (diPWM): object diPWM

		text (string): text to search on the motif (first position = 0)

		threshold (float): threshold given to select the windows

	Yields:
		tuple: starting_position, word, score
	"""

	# create empty automaton
	autom = ahocorasick.Automaton()

	# fill automaton with words and scores
	for word, score in enumerate_words_LAM(diP, threshold):
		autom.add_word(word, (word,score))
	autom.make_automaton()

	# search with the automaton through the text : yields starting position in the text, word, score
	for (position, (word, score)) in autom.iter(text):
		yield position-diP.length, word, score


def search_aho_ratio(diP, text, ratio):
	""" Search of a set of words through a text using Aho-Corasick algorithm for a given ratio.
    From the ratio is calculated the threshold.


	Args:
 		diP (diPWM): object diPWM

		text (string): text to search on the motif (first position = 0)

		ratio (float): float or int. From 0 to 1

	Yields:
		tuple: starting_position, word, score
	"""
	threshold = diP.set_threshold_from_ratio(ratio)
	for position, word, score in search_aho(diP, text, threshold):
		yield position, word, score
