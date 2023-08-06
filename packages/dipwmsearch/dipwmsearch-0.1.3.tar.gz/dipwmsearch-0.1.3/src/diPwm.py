#!/usr/bin/env python3
#_*_ coding:utf-8 _*_
import math
from itertools import product

# Class diPwm
class diPWM:
    """ A class to represent a diPWM

    Attributes :
        value : list of dictionaries
            values of the diPWM for each position and di-symbol
        alphabet : list of char
            symbols of the alphabet
        alphabet_size : int
            size of the alphabet
        length : int
            size of the diPWM
        LAM : list of dictionaries
            LookAheadMatrix : to estimate maximum full score from a prefix
        min : float
            score minimum of the diPWM
        max : float
            score maximum of the diPWM

    Methods :
        __len__():
            returns length of the diPWM object, ie length lenght of diPWM.value
        __str__():
            returns string to print the diPWM object
        __eq__(diP_other):
            returns boolean to compare if 2 diPWM object have same values
        make_look_ahead_matrix():
            returns the lookAheadMatrix of the diPWM object
        find_min_diPwm():
            returns the score min of the diPWM object
        find_max_diPwm():
            returns  the score max of the diPWM object
        make_look_back_matrix():
            returns the lookBackMatrix of the diPWM object
        make_look_ahead_table():
            returns lookAheadTable of the diPWM object
        make_look_back_table():
            returns the lookBackTable of the diPWM object
        set_threshold_from_ratio(ratio):
            returns the threshold calculated from the given ratio        
    """    
    def __init__(self, diPwm_list, alphabet_choice = 'DNA'):
        """ Constructs all the necessary attributes for the diPWM object.

        Args:
            diPwm_list (list of lists): list of list of values at each position for each di-symbol in lexicographic order

            alphabet_choice (str, optional): choice of alpahbet between 'DNA, 'RNA' and 'Protein'. Defaults to 'DNA'.

        Raises:
            NameError: wrong alphabet choice

            NameError: length of diPwm is zero

            NameError: numbers of values at a position doesn't match the number of di-symbols
        """        
        if alphabet_choice == 'DNA':
            self.alphabet = ['A', 'C', 'G', 'T']
        elif alphabet_choice == 'RNA':
            self.alphabet = ['A', 'C', 'G', 'U']
        elif alphabet_choice == "Protein":
            self.alphabet = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
        else:
            raise NameError(f'The alphabet "{alphabet_choice}" is not known, please use "DNA", "RNA" or "Protein"!')

        self.alphabet_size = len(self.alphabet)

        list_diNT = ["".join(x) for x in product(self.alphabet, repeat =2)]
        self.value = [ {list_diNT[i] : x for i,x in enumerate(liste)} for liste in diPwm_list]

        # Check that the list is not empty
        if len(self.value) == 0:
            raise NameError('Length of diPwm is zero')

        self.length = len(self.value)

        # Check and update the alphabet_size
        for (i,diP_column) in enumerate(self.value):
            if self.alphabet_size != math.sqrt(len(diP_column)):
                raise NameError(f'Number of lines of the column {i} of the diPwm is not good.')

        self.LAM = self.make_look_ahead_matrix()

        self.min = self.find_min_diPwm()

        self.max = self.find_max_diPwm()


    # Others operators
    # use len(diP)
    def __len__(self):
        """ Defines length of diPWM object as length of diPWM.value

        Returns:
            int: length of diPWM
        """        
        return self.length

    # use print(diP)
    def __str__(self):
        """ Defines string to print for a diPWM object

        Returns:
            str: print the diPWM.value in a matrix format
        """        
        output_string = 'diPwm:'  + '\n'
        output_string += '\t' + '\t'.join([str(x) for x in self.value[0].keys()]) + '\n'
        for (i,lines) in enumerate(self.value):
            output_string += str(i) + ':\t' + '\t'.join([str(round(x,2)) for x in lines.values()]) + '\n'
        return output_string

    # use diP1 == diP2
    def __eq__(self,diP_other):
        """ Check if deux different objects diPWM have same values

        Args:
            diP_other (diPWM): other object diPWM we want to compare to

        Returns:
            boolean: True if values are equal
        """        
        return [{k : round(v,6) for k,v in diP.items()} for diP in self.value] == [{k : round(v,6) for k,v in diP.items()} for diP in diP_other.value]

    # Auxiliary functions
    # use make_look_ahead_matrix(diP)
    def make_look_ahead_matrix(self):
        """ Builds LookAheadMatrix for a diPWM object.
        Values are estimate of the max reachable score of a suffix starting at a position with a specific symbol

        Returns:
            list of dictionaries: a list of values of size of the alphabet per position
        """

        # initialize matrix of size : lines = length of diPWM , columns = alphabet size        
        matrix = [{j:-math.inf for j in self.alphabet} for i in range(self.length)]

        # case of the last position
        for d in self.alphabet:
            maxi = (-math.inf)
            for b in self.alphabet:
                score = self.value[self.length - 1][d+b]
                if (score > maxi):
                    maxi  =  score
            matrix[self.length-1][d] = maxi

        # fill matrix recursively from end to start
        for i in range(self.length-2,-1,-1):
            for d in self.alphabet:
                maxi = (-math.inf)
                for b in self.alphabet:
                    score = self.value[i][d+b] + matrix[i+1][b]
                    if score > maxi:
                        maxi = score
                matrix[i][d] = maxi

        return matrix + [{i:0 for i in self.alphabet}]

    def find_min_diPwm(self):
        """ Computes minimum score of the diPWM object

        Returns:
            float: minimum score that can be reached for a word with the diPWM object
        """        
        # initialize matrix of size : lines = length of diPWM , columns = alphabet size        
        matrix = [{j:-math.inf for j in self.alphabet} for i in range(self.length)]

        # case of the last position
        for d in self.alphabet:
            mini = (math.inf)
            for b in self.alphabet:
                score = self.value[self.length-1][d+b]
                if (score < mini):
                    mini = score
            matrix[self.length-1][d] = mini

        # fill matrix recursively from end to start
        # values are min score of suffix starting with symbol
        for i in range(self.length-2,-1,-1):
            for d in self.alphabet:
                mini=(math.inf)
                for b in self.alphabet:
                    score = self.value[i][d+b] + matrix[i+1][b]
                    if score < mini:
                        mini = score
                matrix[i][d] = mini


        min_diPwm = min(matrix[0].values())
        return min_diPwm

    def find_max_diPwm(self):
        """ Computes minimum score of the diPWM object

        Returns:
            float: maximum score that can be reached for a word with the diPWM object
        """        
        matrix = self.LAM
        max_diPwm = max(matrix[0].values())
        return max_diPwm

    def make_look_back_matrix(self):
        """Builds LookBackMatrix for a diPWM object
        Values are estimate of the max reachable score of a prefix ending at a position with a specific symbol

        Returns:
            list of dictionaries: a list of values of size of the alphabet per position
        """        
        # initialize matrix of size : lines = length of diPWM , columns = alphabet size        
        matrix = [{j:-math.inf for j in self.alphabet} for i in range(self.length)]

        # case of the first position
        for b in self.alphabet:
            maxi = (-math.inf)
            for d in self.alphabet:
                score = self.value[0][d + b]
                if (score > maxi):
                    maxi = score
            matrix[0][b] = maxi

        # fill matrix recursively
        # values are max score of prefix ending with symbol
        for i in range(1,self.length):
            for b in self.alphabet:
                maxi = (-math.inf)
                for d in self.alphabet:
                    score = self.value[i][d + b] + matrix[i-1][d]
                    if score > maxi:
                        maxi = score
                matrix[i][b] = maxi

        return matrix

    def make_look_ahead_table(self):
        """ Builds LookAheadTable for a diPWM object.
        Values are estimate of the max reachable score of a suffix starting at a position

        Returns:
            list: a value for each position
        """        
        # intialize table of length of diPWM with -infinite value
        table = [(-math.inf)]*self.length

        # case of the last element of the table = max of values at the last position
        table[-1] =  max(self.value[self.length-1].values())

        # computes recursively elements of the table
        for i in range((self.length-2),-1,-1):
            table[i] = max(self.value[i].values()) + table[i+1]

        return table

    def make_look_back_table(self):
        """ Builds LookBackTable for a diPWM object
        Values are estimate of the max reachable score of a prefix ending at a position

        Returns:
            list: a value for each position
        """        
        # intialize table of length of diPWM with -infinite value
        table = [(-math.inf)]*self.length

        # case of the first element of the table = max of values at the first position
        table[0] =  max(self.value[0].values())

        # computes recursively elements of the table
        for i in range(1,self.length):
            table[i] = max(self.value[i].values()) + table[i-1]

        return table

    def set_threshold_from_ratio(self, ratio):
        """Computes the threshold from the given ratio and the diPWM

        Args:
            ratio (float): float or int. From 0 to 1

        Returns:
            float: value of the threshold for the diPWM
        """        
        threshold = self.min + (self.max-self.min)*ratio
        return threshold


def create_diPwm(pathDiPwm, alphabet_choice = 'DNA'):
    """ Build a diPWM object from a file.

    Args:
        pathDiPwm (string): path of the diPwm file

    Returns:
        diPWM object
    """    
    #Read diPWM in a tabulated format
    with open(pathDiPwm) as file:
        # User list comprehension to create a diPWM object
        diPwm_matrix = diPWM([[float(y) for y in x.strip().split('\t')] for x in file.readlines() if x[0] != '>'], alphabet_choice)
        return diPwm_matrix
