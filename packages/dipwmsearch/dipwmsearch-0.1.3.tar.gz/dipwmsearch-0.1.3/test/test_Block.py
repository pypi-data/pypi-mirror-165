#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
from src.diPwm import diPWM, create_diPwm
from src.Block import compute_positions_kept, make_blocks, get_longest_block, enumerate_block, search_block, get_block_optimized, search_block_optimized

def test_compute_positions_kept():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    list_positions_kept = compute_positions_kept(diPwm_matrix_new, 2)

    assert list_positions_kept == [1, 2, 3, 4, 6, 7]


def test_make_blocks():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    list_positions_kept = compute_positions_kept(diPwm_matrix_new, 2)
    list_blocks = make_blocks(list_positions_kept)

    assert list_blocks == [[1, 2, 3, 4], [6, 7]]


def test_get_longest_block():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    list_positions_kept = compute_positions_kept(diPwm_matrix_new, 2)
    list_blocks = make_blocks(list_positions_kept)
    block = get_longest_block(list_blocks)

    assert block == [1, 2, 3, 4]


def test_enumerate_block():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diPwm_matrix_new = create_diPwm(pathDiPwm)
    list_positions_kept = compute_positions_kept(diPwm_matrix_new, 2)
    list_blocks = make_blocks(list_positions_kept)
    block = get_longest_block(list_blocks)
    nb = 0
    for word, score in enumerate_block(diPwm_matrix_new, block, 10):
        nb += 1

    assert nb == 84


def test_search_block():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diP=create_diPwm(pathDiPwm)
    text = open("./data/sequence.txt").readlines()[0]
    threshold = 5
    nb = 0
    for starting_position, word, score in search_block(diP, text, threshold):
        nb += 1

    assert nb == 12


def test_get_block_optimized():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diP=create_diPwm(pathDiPwm)
    block = get_block_optimized(diP)

    assert block == [1, 2, 3, 4, 5, 6, 7, 8]


def test_search_block_optimized():
    pathDiPwm = "./data/ATF3_HUMAN.H11DI.0.A.dpwm"
    diP=create_diPwm(pathDiPwm)
    text = open("./data/sequence.txt").readlines()[0]
    threshold = 5
    nb = 0
    for starting_position, word, score in search_block_optimized(diP, text, threshold):
        nb += 1

    assert nb == 12
