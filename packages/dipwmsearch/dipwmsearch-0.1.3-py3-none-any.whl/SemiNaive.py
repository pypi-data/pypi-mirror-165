#!/usr/bin/env python3
#_*_ coding:utf-8 _*_


from .diPwm import diPWM, create_diPwm
import math


def search_semi_naive_LAM_window(diP, start_position, text, threshold):
    lengthSeqRef = len(text)
    score=0
    position_in_window = 0

    #Check for character IUPAC
    if text[start_position] not in diP.alphabet:
        return None
    # Check at each position of the window
    for j in range(start_position, start_position + diP.length):
        d = text[j]
        b = text[j + 1]

        #Check for character IUPAC
        if b not in diP.alphabet:
            return None

        score = score + diP.value[position_in_window][d + b]
        # print(j,score,score + diP.LAM[position_in_window + 1][b],diP.LAM[position_in_window + 1])
        # if partial score + estimate max score suffixe doesn't reach threshold : break
        if (score + diP.LAM[position_in_window + 1][b]) < threshold:

            return None
        # otherwise computation of partial score
        position_in_window += 1
    return score

def search_semi_naive_LAM(diP, text, threshold):
    """ Search of the diPWM through a text by sliding window for a given threshold.
    This function uses the LookAheadMatrix to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        threshold (float): threshold given to select the windows

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    lengthSeqRef = len(text)

    # Computation for every position of the text - size of diPWM
    for i in range(0, lengthSeqRef - 1 - diP.length):
        score=0
        complete = False

        #Check for character IUPAC
        if text[i] not in diP.alphabet:
            return None
        # Check at each position of the window
        for j in range(0, diP.length):
            d = text[i + j]
            b = text[i + j + 1]

            #Check for character IUPAC
            if b not in diP.alphabet:
                return None

            # if partial score + estimate max score suffixe doesn't reach threshold : break
            if (j<diP.length - 1) and ((score + diP.value[j][d + b] + diP.LAM[j + 1][b]) < threshold):
                score=(-math.inf)
                break
            # otherwise computation of partial score
            else:
                score = score + diP.value[j][d + b]
                if (j == diP.length - 1):
                    complete=True

        # if whole window score is >= threshold : yield starting position, sub-string, score
        if ((score >= threshold) and complete==True):
            yield i, text[i:i+diP.length+1], score


def search_semi_naive_LAM_ratio(diP, text, ratio):
    """Search of the diPWM through a text by sliding window for a given ratio.
    From the ratio is calculated the threshold.
    This function uses the LookAheadMatrix to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        ratio (float): float or int. From 0 to 1

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    threshold = diP.set_threshold_from_ratio(ratio)
    for position, mot, score in search_semi_naive_LAM(diP, text, threshold):
        yield position, mot, score


def search_semi_naive_LAT(diP, text, threshold):
    """ Search of the diPWM through a text by sliding window for a given threshold.
    This function uses the LookAheadTable to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        threshold (float): threshold given to select the windows

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    lengthSeqRef = len(text)
    LAT = diP.make_look_ahead_table()

    # Computation for every position of the text - size of diPWM
    for i in range(0,lengthSeqRef-1-diP.length):
        score=0
        complete = False

        #Check for character IUPAC
        if text[i] not in diP.alphabet:
            return None

        # Check at each position of the window
        for j in range(0,diP.length):
            d=text[i+j]
            b=text[i+j+1]

            #Check for character IUPAC
            if b not in diP.alphabet:
                return None

            # if partial score + estimate max score suffixe doesn't reach threshold : break
            if (j<diP.length-1) and ((score + diP.value[j][d + b] + LAT[j+1]) < threshold):
                score=(-math.inf)
                break
            # otherwise computation of partial score
            else:
                score = score + diP.value[j][d + b]
                if (j==diP.length-1):
                    complete=True

        # if whole window score is >= threshold : yield starting position, sub-string, score
        if ((score >= threshold) and complete==True):
            yield i, text[i:i+diP.length+1], score


def search_semi_naive_LAT_ratio(diP, text, ratio):
    """Search of the diPWM through a text by sliding window for a given ratio.
    From the ratio is calculated the threshold.
    This function uses the LookAheadTable to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        ratio (float): float or int. From 0 to 1

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    threshold = diP.set_threshold_from_ratio(ratio)
    for position, mot, score in search_semi_naive_LAT(diP, text, threshold):
        yield position, mot, score


def search_semi_naive_back_LBM(diP, text, threshold):
    """ Search of the diPWM through a text by sliding window for a given threshold.
    Each window is computed backward from right to left.
    This function uses the LookBackMatrix to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        threshold (float): threshold given to select the windows

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    lengthSeqRef = len(text)
    LBM= diP.make_look_back_matrix()

    # Computation for every position of the text starting at the length of the diPWM
    for i in range(diP.length, lengthSeqRef):
        score=0
        complete = False


        #Check for character IUPAC
        if text[i] not in diP.alphabet:
            return None

        # Check at each position of the window, starting from the end of the window
        # moving backward
        for j in range(diP.length-2,-2,-1):
            d=text[i-(diP.length-1-j)]
            b=text[i-(diP.length-1-j)+1]

            #Check for character IUPAC
            if b not in diP.alphabet:
                return None

            # if partial score + estimate max score prefix doesn't reach threshold : break
            if (j>0) and ((score + diP.value[j+1][d + b] + LBM[j][d]) < threshold):
                score=(-math.inf)
                break
            # otherwise computation of partial score
            else:
                score = score + diP.value[j+1][d + b]
                if (j==0):
                    complete=True

        # if whole window score is >= threshold : yield starting position, sub-string, score
        if ((score >= threshold) and complete==True):
            yield i-diP.length, text[i-(diP.length):i+1], score


def search_semi_naive_back_LBM_ratio(diP, text, ratio):
    """Search of the diPWM through a text by sliding window for a given ratio.
    From the ratio is calculated the threshold.
    Each window is computed backward from right to left.
    This function uses the LookBackMatrix to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        ratio (float): float or int. From 0 to 1

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    threshold = diP.set_threshold_from_ratio(ratio)
    for position, mot, score in search_semi_naive_back_LBM(diP, text, threshold):
        yield position, mot, score


def search_semi_naive_back_LBT(diP, text, threshold):
    """ Search of the diPWM through a text by sliding window for a given threshold.
    Each window is computed backward from right to left.
    This function uses the LookBackTable to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        threshold (float): threshold given to select the windows

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    lengthSeqRef = len(text)
    LBT = diP.make_look_back_table()

    # Computation for every position of the text starting at the length of the diPWM
    for i in range(diP.length, lengthSeqRef):
        score=0
        complete = False

        #Check for character IUPAC
        if text[i] not in diP.alphabet:
            return None

        # Check at each position of the window, starting from the end of the window
        # moving backward
        for j in range(diP.length-2,-2,-1):
            d=text[i-(diP.length-1-j)]
            b=text[i-(diP.length-1-j)+1]

            #Check for character IUPAC
            if b not in diP.alphabet:
                return None

            # if partial score + estimate max score prefix doesn't reach threshold : break
            if (j>0) and ((score + diP.value[j+1][d + b] + LBT[j]) < threshold):
                score=(-math.inf)
                break
            # otherwise computation of partial score
            else:
                score = score + diP.value[j+1][d + b]
                if (j==0):
                    complete=True

        # if whole window score is >= threshold : yield starting position, sub-string, score
        if ((score >= threshold) and complete==True):
            yield i-diP.length, text[i-(diP.length):i+1], score


def search_semi_naive_back_LBT_ratio(diP, text, ratio):
    """Search of the diPWM through a text by sliding window for a given ratio.
    From the ratio is calculated the threshold.
    Each window is computed backward from right to left.
    This function uses the LookBackTable to shorten computations.

    Args:
        diP (diPWM): object diPWM

        text (string): text to search on the motif (first position = 0)

        ratio (float): float or int. From 0 to 1

    Yields:
        tuple: starting position in the text, sub-string, score
    """
    threshold = diP.set_threshold_from_ratio(ratio)
    for position, mot, score in search_semi_naive_back_LBT(diP, text, threshold):
        yield position, mot, score
