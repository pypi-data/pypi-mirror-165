#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from src.diPwm import diPWM, create_diPwm
from src.Enumerate import enumerate_words_LAM, enumerate_words_LAT, enumerate_words_LAM_ratio, enumerate_words_LAT_ratio
import pandas as pd

def test_enumerate_words_LAM():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	threshold = 20
	i=0
	for x in enumerate_words_LAM(diP,threshold):
		i+=1

	assert i == 41

def test_enumerate_words_LAT():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	threshold = 20
	i=0
	for x in enumerate_words_LAT(diP,threshold):
		i+=1

	assert i == 41

def test_enumerate_words_LAM_ratio():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	ratio = 0.95
	i=0
	for x in enumerate_words_LAM_ratio(diP,ratio):
		i+=1

	assert i == 158

def test_enumerate_words_LAT_ratio():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	ratio = 0.95
	i=0
	for x in enumerate_words_LAT_ratio(diP,ratio):
		i+=1

	assert i == 158