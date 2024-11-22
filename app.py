from flask import Flask, render_template, request, redirect, url_for
from arxiv_search_lib import search_arxiv_papers, evaluate_papers
from database import initialize_db, save_query, get_cached_results, get_recent_queries

app = Flask(__name__)

# Initialize the database
initialize_db()

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        max_results = int(request.form.get("max_results", 10))
        return redirect(url_for("results", query=query, max_results=max_results))

    # Fetch recent queries
    recent_queries = get_recent_queries(limit=100)
    return render_template("search.html", recent_queries=recent_queries)

@app.route("/results", methods=["GET"])
def results():
    query = request.args.get("query")
    max_results = int(request.args.get("max_results", 10))

    # Check for cached results
    cached_results = get_cached_results(query, max_results)
    if cached_results:
        results = cached_results
    else:
        # Fetch and evaluate papers
        papers = search_arxiv_papers(query, max_results=max_results)
        results = evaluate_papers(papers, query)

        # Save the query and results to the database
        save_query(query, max_results, results)

    return render_template("results.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)
