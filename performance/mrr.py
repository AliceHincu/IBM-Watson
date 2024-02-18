class MRRCalculator:
    @staticmethod
    def compute_mrr(ranks):
        """
        For evaluating your Jeopardy system, Mean Reciprocal Rank (MRR) is a suitable metric because it's designed for
        systems where the goal is to retrieve a list of items and the relevance is binary (relevant/not relevant).
        MRR is especially relevant when you are interested in the rank of the first correct answer in the list of
        returned answers. It's calculated as the average of the reciprocal ranks of the first correct answer for each
        query. This metric effectively measures the system's ability to return relevant results as close to the top
        position as possible, which aligns well with the Jeopardy system's objective where typically only one answer is
        correct, and finding it quickly is valuable.
        """
        if not ranks:
            raise ValueError("Input list of ranks is empty.")
        return sum(1.0 / rank for rank in ranks if rank) / len(ranks)