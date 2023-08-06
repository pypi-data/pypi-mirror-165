#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from src.diPwm import diPWM, create_diPwm
import pandas as pd


def rounded_di(M):
	return {k : round(v,6) for k,v in M.items()}

def test_create_diPwm():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	df = pd.read_csv(pathDiPwm, delimiter='\t', skiprows=1, header=None)
	diPwm_matrix_sol = diPWM([list(row) for row in df.values])
	diPwm_matrix_new = create_diPwm(pathDiPwm)

	assert diPwm_matrix_sol == diPwm_matrix_new


def test_length():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	A = create_diPwm(pathDiPwm)

	assert A.length == 11

def test_alphabet_size():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	A = create_diPwm(pathDiPwm)

	assert A.alphabet_size == 4

def test_LAM():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	A = create_diPwm(pathDiPwm)

	assert [rounded_di(x) for x in A.LAM] == [{'A': 21.226616, 'C': 21.667164, 'G': 21.577231, 'T': 21.507651}, {'A': 19.968843, 'C': 19.202268, 'G': 20.722303, 'T': 19.079832}, {'A': 17.738444, 'C': 14.691876, 'G': 18.886448, 'T': 14.227987}, {'A': 12.835326, 'C': 12.694676, 'G': 11.714997, 'T': 16.461997}, {'A': 9.565331, 'C': 14.294562, 'G': 13.949007, 'T': 9.022864}, {'A': 12.149074, 'C': 8.471302, 'G': 8.086312, 'T': 8.231739}, {'A': 6.212374, 'C': 9.686198, 'G': 6.29654, 'T': 8.166648}, {'A': 4.26985, 'C': 2.57849, 'G': 7.23415, 'T': 3.212615}, {'A': 1.212554, 'C': 2.601378, 'G': 0.691609, 'T': 4.812501}, {'A': 1.954952, 'C': 1.707343, 'G': 2.667013, 'T': -0.030775}, {'A': 1.184121, 'C': -0.007933, 'G': 0.646425, 'T': -1.214896}, {'A': 0, 'C': 0, 'G': 0, 'T': 0}]


def test_min():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	A = create_diPwm(pathDiPwm)

	assert round(A.min,6) == -42.885822

def test_max():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	A = create_diPwm(pathDiPwm)

	assert round(A.max,6) == 21.667164
