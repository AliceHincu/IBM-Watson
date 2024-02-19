class MRRCalculator:
    @staticmethod
    def compute_mrr(ranks):
        """
        Computes the Mean Reciprocal Rank (MRR) given a list of ranks.

        Args:
            ranks (list): A list of ranks where each rank represents the position of a relevant item.

        Returns:
            float: The Mean Reciprocal Rank (MRR) computed from the given ranks.

        Raises:
            ValueError: If the input list of ranks is empty.
         """

        if not ranks:
            raise ValueError("Input list of ranks is empty.")
        return sum(1.0 / rank for rank in ranks if rank) / len(ranks)