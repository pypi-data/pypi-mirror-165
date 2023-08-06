#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from src.diPwm import diPWM, create_diPwm
from src.AhoCorasick import search_aho

def test_search_aho():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diP=create_diPwm(pathDiPwm)
    text = open("./data/sequence.txt").readlines()[0]
    threshold = 5
    nb = 0
    for starting_position, word, score in search_aho(diP, text, threshold):
        nb += 1

    assert nb == 12
