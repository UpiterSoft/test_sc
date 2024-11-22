from flask import Flask, render_template, request, redirect, url_for
from arxiv_search_lib import search_arxiv_papers, evaluate_papers

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        max_results = int(request.form.get("max_results", 10))
        return redirect(url_for("results", query=query, max_results=max_results))
    return render_template("search.html")

@app.route("/results", methods=["GET"])
def results():
    query = request.args.get("query")
    max_results = int(request.args.get("max_results", 10))

    # Fetch and evaluate papers
    papers = search_arxiv_papers(query, max_results=max_results)
    evaluated_results = evaluate_papers(papers, query)

    return render_template("results.html", query=query, results=evaluated_results)

if __name__ == "__main__":
    app.run(debug=True)
