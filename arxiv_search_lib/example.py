from arxiv_search_lib import search_arxiv_papers, evaluate_papers
from arxiv_search_lib.utils import display_results

if __name__ == "__main__":
    query = "solar powered refrigerators"
    max_results = 5

    print("Searching arXiv...")
    papers = search_arxiv_papers(query, max_results=max_results)

    print("Evaluating relevance...")
    results = evaluate_papers(papers, query)

    display_results(results)
