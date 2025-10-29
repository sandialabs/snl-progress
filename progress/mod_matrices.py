import numpy as np
# from snl_progress.mod_sysdata import RASystemData


class RAMatrices:
    '''Creates generation, incidence, and curtailment matrices for the RA model'''

    def __init__(self, nb):
        """
        Initializes the RAMatrices class.

        Parameters:
            nb (int): Number of buses in the system.
        """
        self.nb = nb

    def genmat(self, ng, genbus, ness, essbus):
        """
        Creates a generation matrix for the optimization problem.

        Parameters:
            ng (int): Number of generators.
            genbus (list): List of generator buses.
            ness (int): Number of energy storage systems (ESS).
            essbus (list): List of ESS buses.

        Returns:
            numpy.ndarray: Generation matrix.
        """
        self.ng = ng + ness
        self.genbus = np.concatenate((genbus, essbus))
        # TODO: Add dtype validation - empty essbus arrays need dtype=int to avoid IndexError
        # when using genbus[i] as array index. Consider: self.genbus = np.concatenate((genbus, essbus)).astype(int)
        self.gen_mat = np.zeros((self.nb, self.ng))
        j_temp = 0
        for i in range(self.ng):
            self.gen_mat[self.genbus[i]-1, j_temp] = 1
            j_temp+=1

        return(self.gen_mat)
    
    def Ainc(self, nl, fb, tb):
        """
        Creates an incidence matrix for modeling the flow constraints.

        Parameters:
            nl (int): Number of lines.
            fb (list): From buses.
            tb (list): To buses.

        Returns:
            numpy.ndarray: Incidence matrix.
        """
        self.nl = nl
        self.fb = fb
        self.tb = tb
        self.A_inc = np.zeros((self.nl, self.nb))
        for i in range(self.nl):
            for j in range(self.nb + 1):
                if self.fb[i] == j:
                    self.A_inc[i,j - 1] = 1
                elif self.tb[i] == j:
                    self.A_inc[i, j - 1] = -1
        return(self.A_inc)

    def curtmat(self, nb):
        """
        Creates a curtailment matrix for the load curtailment variables in the optimizer.

        Parameters:
            nb (int): Number of buses.

        Returns:
            numpy.ndarray: Curtailment matrix.
        """
        return(np.eye(nb))

    def chmat(self, ness, essbus, nb):
        """
        Creates a matrix for ESS charging variables.

        Parameters:
            ness (int): Number of energy storage systems (ESS).
            essbus (list): List of ESS buses.
            nb (int): Number of buses.

        Returns:
            numpy.ndarray: ESS charging matrix.
        """
        self.ch_mat = np.zeros((nb, ness))
        j_temp = 0
        for i in range(ness):
            self.ch_mat[essbus[i]-1, j_temp] = 1
            j_temp+=1

        return(self.ch_mat)
    

