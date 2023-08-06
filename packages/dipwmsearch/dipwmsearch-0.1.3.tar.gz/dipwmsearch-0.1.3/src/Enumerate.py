#!/usr/bin/env python3
#_*_ coding:utf-8 _*_

from .diPwm import diPWM


def enumerate_words_LAM(diP, threshold):
	"""This function enumerates words of length of diPWM + 1 which scores are >= to threshold.
	To estimate score, this function uses LAM.

	Args:
		diP (diPWM): Object diPWM

		threshold (float): score of the words >= threshold will be enumerated

	Yields:
		tuple: word, score
	"""
	stack = []

	# for root, child and parent : [0]:level, [1]:score, [2]:prefix
	# one root per symbol of the alphabet
	for nt in diP.alphabet:
		root = (0,0,nt)
		stack.append(root)

	while stack:
		parent = stack.pop()

		for d in diP.alphabet:
			child = (
				parent[0] + 1,
				parent[1] + diP.value[parent[0]][parent[2][-1] + d],
				parent[2] + d
			)

			# case of the last step to create word of full length
			if parent[0] == diP.length-1:

				if child[1] >= threshold:
					yield child[2], child[1]	# generate word, score

			# other cases : inside the tree
			# create child if estimate score can reach threshold using LAM
			elif child[1] + diP.LAM[child[0]][d] >= threshold:

				#Child added as last element of the stack
				stack.append(child)

def enumerate_words_LAM_ratio(diP, ratio):
	"""This function enumerates words of length of diPWM + 1 which scores are >= to a threshold.
	Threshold is calculated from score range of the diPWM and ratio.
	To estimate score, this function uses LAM.

	Args:
		diP (diPWM): object diPWM

		ratio (float): float or int. From 0 to 1

	Yields:
		tuple: word, score
	"""
	# calculate threshold from ratio
	threshold = diP.set_threshold_from_ratio(ratio)
	for mot, score in enumerate_words_LAM(diP, threshold):
		yield mot, score



def enumerate_words_LAT(diP, threshold):
	"""This function enumerates words of length of diPWM + 1 which scores are >= to threshold.
	To estimate score, this function uses LAT.

	Args:
		diP (diPWM): Object diPWM

		threshold (float): score of the words >= threshold will be enumerated

	Yields:
		tuple: word, score
	"""

	LAT = diP.make_look_ahead_table()
	stack = []

	# for root, child and parent : [0]:level, [1]:score, [2]:prefix
	# one root per symbol of the alphabet
	for nt in diP.alphabet:
		root = (0,0,nt)
		stack.append(root)

	while stack:
		parent = stack.pop()

		for d in diP.alphabet:
			child = (
				parent[0] + 1,
				parent[1] + diP.value[parent[0]][parent[2][-1] + d],
				parent[2] + d
			)

			# case of the last step to create word of full length
			if parent[0] == diP.length-1:

				if child[1] >= threshold:
					yield child[2], child[1]	# generate word, score

			# other cases : inside the tree
			# create child if estimate score can reach threshold using LAM
			elif child[1] + LAT[0] >= threshold:

				#Child added as last element of the stack
				stack.append(child)


def enumerate_words_LAT_ratio(diP, ratio):
	"""This function enumerates words of length of diPWM + 1 which scores are >= to a threshold.
	Threshold is calculated from score range of the diPWM and ratio.
	To estimate score, this function uses LAT.

	Args:
		diP (diPWM): object diPWM

		ratio (float): float or int. From 0 to 1

	Yields:
		tuple: word, score
	"""

	# calculate threshold from ratio
	threshold = diP.set_threshold_from_ratio(ratio)
	for mot, score in enumerate_words_LAT(diP, threshold):
		yield mot, score
