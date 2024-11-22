import arxiv

def search_arxiv_papers(query, max_results=10):
    """
    Search for papers on arXiv using a query.

    Args:
        query (str): The search query.
        max_results (int): Maximum number of results to fetch.

    Returns:
        list: List of dictionaries containing title, abstract, and link.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    results = []
    for result in search.results():
        results.append({
            "title": result.title,
            "abstract": result.summary,
            "link": result.pdf_url
        })

    return results
