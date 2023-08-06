#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from src.diPwm import diPWM, create_diPwm
from src.SemiNaive import *

def test_search_semi_naive_LAM():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	threshold = 5
	result = list(search_semi_naive_LAM(diP, text, threshold))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2568, 'CTGTGATCTGAG', 6.094157), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (6031, 'CAGTGATGAAAT', 8.17258), (6673, 'CAGGCATGTGCC', 5.080133)]


def test_search_semi_naive_LAM_ratio():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	ratio = 0.7
	result = list(search_semi_naive_LAM_ratio(diP, text, ratio))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (750, 'AAATGACATATG', 3.24126), (1218, 'AAGTGTAGTCAA', 4.155629), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1405, 'AAATCAAGTCCT', 3.214787), (1483, 'CCAAGATGCAAC', 2.660579), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2274, 'AGATGGAGTGAA', 2.353807), (2471, 'TGAACATGCAAA', 3.028363), (2568, 'CTGTGATCTGAG', 6.094157), (2778, 'TAGCCACATGAT', 4.869034), (2796, 'TGATGACTTTGA', 2.512363), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (3924, 'TAGTCATATAAA', 3.581544), (5216, 'AAATCACTAAAT', 2.624222), (5627, 'CAGTTATGCAAG', 2.774249), (6031, 'CAGTGATGAAAT', 8.17258), (6045, 'TGATGCCTTGGC', 2.452469), (6252, 'GAGTGGAGTGGC', 4.357664), (6404, 'GGGTCTCGCTAT', 2.560015), (6594, 'CAATGGCGCGGT', 4.006457), (6673, 'CAGGCATGTGCC', 5.080133)]



def test_search_semi_naive_LAT():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	threshold = 5
	result = list(search_semi_naive_LAT(diP, text, threshold))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2568, 'CTGTGATCTGAG', 6.094157), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (6031, 'CAGTGATGAAAT', 8.17258), (6673, 'CAGGCATGTGCC', 5.080133)]


def test_search_semi_naive_LAT_ratio():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	ratio = 0.7
	result = list(search_semi_naive_LAT_ratio(diP, text, ratio))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (750, 'AAATGACATATG', 3.24126), (1218, 'AAGTGTAGTCAA', 4.155629), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1405, 'AAATCAAGTCCT', 3.214787), (1483, 'CCAAGATGCAAC', 2.660579), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2274, 'AGATGGAGTGAA', 2.353807), (2471, 'TGAACATGCAAA', 3.028363), (2568, 'CTGTGATCTGAG', 6.094157), (2778, 'TAGCCACATGAT', 4.869034), (2796, 'TGATGACTTTGA', 2.512363), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (3924, 'TAGTCATATAAA', 3.581544), (5216, 'AAATCACTAAAT', 2.624222), (5627, 'CAGTTATGCAAG', 2.774249), (6031, 'CAGTGATGAAAT', 8.17258), (6045, 'TGATGCCTTGGC', 2.452469), (6252, 'GAGTGGAGTGGC', 4.357664), (6404, 'GGGTCTCGCTAT', 2.560015), (6594, 'CAATGGCGCGGT', 4.006457), (6673, 'CAGGCATGTGCC', 5.080133)]

def test_search_semi_naive_back_LBM():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	threshold = 5
	result = list(search_semi_naive_back_LBM(diP, text, threshold))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2568, 'CTGTGATCTGAG', 6.094157), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (6031, 'CAGTGATGAAAT', 8.17258), (6673, 'CAGGCATGTGCC', 5.080133)]


def test_search_semi_naive_back_LBM_ratio():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	ratio = 0.7
	result = list(search_semi_naive_back_LBM_ratio(diP, text, ratio))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (750, 'AAATGACATATG', 3.24126), (1218, 'AAGTGTAGTCAA', 4.155629), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1405, 'AAATCAAGTCCT', 3.214787), (1483, 'CCAAGATGCAAC', 2.660579), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2274, 'AGATGGAGTGAA', 2.353807), (2471, 'TGAACATGCAAA', 3.028363), (2568, 'CTGTGATCTGAG', 6.094157), (2778, 'TAGCCACATGAT', 4.869034), (2796, 'TGATGACTTTGA', 2.512363), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (3924, 'TAGTCATATAAA', 3.581544), (5216, 'AAATCACTAAAT', 2.624222), (5627, 'CAGTTATGCAAG', 2.774249), (6031, 'CAGTGATGAAAT', 8.17258), (6045, 'TGATGCCTTGGC', 2.452469), (6252, 'GAGTGGAGTGGC', 4.357664), (6404, 'GGGTCTCGCTAT', 2.560015), (6594, 'CAATGGCGCGGT', 4.006457), (6673, 'CAGGCATGTGCC', 5.080133)]


def test_search_semi_naive_back_LBT():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	threshold = 5
	result = list(search_semi_naive_back_LBT(diP, text, threshold))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2568, 'CTGTGATCTGAG', 6.094157), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (6031, 'CAGTGATGAAAT', 8.17258), (6673, 'CAGGCATGTGCC', 5.080133)]


def test_search_semi_naive_back_LBT_ratio():
	pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
	diP=create_diPwm(pathDiPwm)
	text = open("./data/sequence.txt").readlines()[0]
	ratio = 0.7
	result = list(search_semi_naive_back_LBT_ratio(diP, text, ratio))

	assert [(x,y,round(z,6)) for x,y,z in result] == [(226, 'AAATCAGGTCAT', 7.563292), (231, 'AGGTCATTTCAG', 7.817307), (750, 'AAATGACATATG', 3.24126), (1218, 'AAGTGTAGTCAA', 4.155629), (1223, 'TAGTCAAATGGC', 5.140737), (1356, 'AGGTCCAGTGGC', 6.409125), (1405, 'AAATCAAGTCCT', 3.214787), (1483, 'CCAAGATGCAAC', 2.660579), (1619, 'AAGTCAAGTAAT', 9.554417), (1875, 'TCATCACCTGAT', 5.391612), (2274, 'AGATGGAGTGAA', 2.353807), (2471, 'TGAACATGCAAA', 3.028363), (2568, 'CTGTGATCTGAG', 6.094157), (2778, 'TAGCCACATGAT', 4.869034), (2796, 'TGATGACTTTGA', 2.512363), (3282, 'CAATCATGTCTA', 5.175347), (3656, 'TGGTGATGAGAA', 9.224684), (3864, 'AAGTCACTGGGC', 5.198311), (3924, 'TAGTCATATAAA', 3.581544), (5216, 'AAATCACTAAAT', 2.624222), (5627, 'CAGTTATGCAAG', 2.774249), (6031, 'CAGTGATGAAAT', 8.17258), (6045, 'TGATGCCTTGGC', 2.452469), (6252, 'GAGTGGAGTGGC', 4.357664), (6404, 'GGGTCTCGCTAT', 2.560015), (6594, 'CAATGGCGCGGT', 4.006457), (6673, 'CAGGCATGTGCC', 5.080133)]
