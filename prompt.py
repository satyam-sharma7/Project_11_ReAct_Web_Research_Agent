Tools = """
there is two tools to use:

web_search : A web search tool that can search querys on web. parameters --> only a query. result --> Titles of pages, urls.\n
fetch_page :  A tools that can scrape text content of a web page. parameters --> url of the page. result --> Text content of page\n

You have to choose tool that can help to gather information for generating the answer of user query.
check your full chat history based on the history think which tool will be more appropiate.\n

final goal is to find relevent latest information. Don't specify date try to find latest information.

Expected output:

{'tool': 'web_search', 'parameters': ['which team won last IPL.']}

"""


Check_Final_Answer = """
You are a search evaluator.

Given:
- User Query
- Current Document
- Candidate Next Topics (top 5 web search titles)

If the Current Document contains enough information to answer the User Query, output exactly:
{"Final":"yes","next_topic":"not needed"}

Otherwise, choose the single best title from Candidate Next Topics to search next and output exactly:
{"Final":"no","next_topic":"<exact title>"}

Return only the JSON. Do not explain your decision or generate a new topic.
"""
