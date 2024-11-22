def display_results(results):
    """
    Display ranked results.

    Args:
        results (list): List of tuples (link, score).
    """
    print("Ranked Results:")
    for rank, (link, score) in enumerate(results, start=1):
        print(f"{rank}. Score: {score}, Link: {link}")
