import numpy as np
# from snl_progress.mod_sysdata import RASystemData


class RAMatrices:
    """
    Creates generation, incidence, and curtailment matrices for the RA model.

    :param nb: Number of buses in the system.
    :type nb: int
    """
    def __init__(self, nb):
        """
        Initializes the RAMatrices class.

        :param nb: Number of buses in the system.
        :type nb: int
        """
        self.nb = nb

    def genmat(self, ng, genbus, ness, essbus):
        """
        Creates a generation matrix for the optimization problem.

        :param ng: Number of generators.
        :type ng: int
        :param genbus: List of generator bus indices.
        :type genbus: list[int]
        :param ness: Number of energy storage systems (ESS).
        :type ness: int
        :param essbus: List of ESS bus indices.
        :type essbus: list[int]

        :return:
            A 2D NumPy array with shape ``(nb, ng + ness)`` where each column
            corresponds to one generator (or ESS) and the row index indicates
            the bus to which that generator/ESS is connected.

        :rtype: numpy.ndarray
        """
        self.ng = ng + ness
        self.genbus = np.concatenate((genbus, essbus))
        self.gen_mat = np.zeros((self.nb, self.ng))
        j_temp = 0
        for i in range(self.ng):
            self.gen_mat[self.genbus[i]-1, j_temp] = 1
            j_temp+=1

        return(self.gen_mat)
    
    def Ainc(self, nl, fb, tb):
        """
        Creates an incidence matrix for modeling flow constraints.

        :param nl: Number of lines.
        :type nl: int
        :param fb: List of "from bus" indices for each line.
        :type fb: list[int]
        :param tb: List of "to bus" indices for each line.
        :type tb: list[int]

        :return:
            A 2D NumPy array with shape ``(nl, nb)`` where each row
            represents one line. Entries of ``+1`` and ``-1`` indicate
            the sending and receiving buses, respectively.

        :rtype: numpy.ndarray
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
        Creates a curtailment matrix for load curtailment variables.

        :param nb: Number of buses.
        :type nb: int

        :return:
            A 2D identity matrix of shape ``(nb, nb)``. This matrix is often used
            to represent a direct mapping of curtailment variables to each bus.

        :rtype: numpy.ndarray
        """
        return(np.eye(nb))

    def chmat(self, ness, essbus, nb):
        """
        Creates a matrix for ESS charging variables.

        :param ness: Number of energy storage systems (ESS).
        :type ness: int
        :param essbus: List of ESS bus indices.
        :type essbus: list[int]
        :param nb: Number of buses.
        :type nb: int

        :return:
            A 2D NumPy array with shape ``(nb, ness)`` where each column
            corresponds to an ESS unit and the row index indicates the bus
            at which that ESS is located.

        :rtype: numpy.ndarray
        """
        self.ch_mat = np.zeros((nb, ness))
        j_temp = 0
        for i in range(ness):
            self.ch_mat[essbus[i]-1, j_temp] = 1
            j_temp+=1

        return(self.ch_mat)
    

