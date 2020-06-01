import numpy as np


class Rule:
    """Store information about cellular automata rules."""

    def __init__(self, indices, ruleset):
        """
        Parameters
        ----------
        indices : array_like
            List of relative indices that will be retrieved in rule applying process. Must be 2-D with shape of (_, 2).
        ruleset : function
            Parameters
            ----------
            cell : bool
                Value of the selected cell.
            retrieved_cells : array_like
                Array of bools, representing cell values retrieved using `indices` array. Same 1-D size as `indices`.

            Returns
            -------
            bool
                Final value of the cell after applying a rule.
        """
        self.indices = indices
        self.ruleset = ruleset

    @property
    def indices(self):
        return self._indices

    @indices.setter
    def indices(self, value):
        value = np.array(value)
        if value.ndim != 2 or value.shape[1] != 2:
            raise ValueError("Misshapen 'indices'!")

        if value.dtype != "int64":
            raise ValueError("Invalid data type for 'indices'")

        self._indices = value

    @property
    def ruleset(self):
        return self._ruleset

    @ruleset.setter
    def ruleset(self, value):
        if not callable(value):
            raise ValueError("`ruleset` is not callable!")
        try:
            value(True, [True] * len(self.indices))
        except TypeError:
            raise ValueError("Ruleset doesn't accept 2 arguments!")

        self._ruleset = value
