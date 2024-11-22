from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

def evaluate_papers(papers, query, llm_model="gpt-4"):
    """
    Evaluate papers' relevance to the query using a language model.

    Args:
        papers (list): List of dictionaries with keys 'title', 'abstract', and 'link'.
        query (str): The search query.
        llm_model (str): The LLM model to use for evaluation.

    Returns:
        list: List of tuples (link, score).
    """
    llm = ChatOpenAI(model=llm_model)
    prompt_template = PromptTemplate(
        input_variables=["abstract", "query"],
        template=(
            "Does the paper described with abstract ```{abstract}``` correspond to the search topic of `{query}`? "
            "Respond with a number from 1 to 5, where 1 means not related and 5 means highly related."
        )
    )

    evaluated_papers = []

    for paper in papers:
        prompt = prompt_template.format(abstract=paper["abstract"], query=query)
        response = llm([HumanMessage(content=prompt)])
        try:
            score = int(response.content.strip())
        except ValueError:
            score = 0  # Handle unexpected response format

        evaluated_papers.append((paper["link"], score))

    # Sort papers by score in descending order
    return sorted(evaluated_papers, key=lambda x: x[1], reverse=True)
