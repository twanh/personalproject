# Import the databases 
from games.models import Game, GameManager
from seller.models import seller

# Import the crawler 
from webcrawler.crawlers import *

def dbSearch(query):
    '''
    Search the database (games) from the query
    Args:
        query (str): The query to search for...
    Returns:
        True (Boolean), results (Dict -> Queryset): When search was sucsessfull
        False (Boolean), results: When search was unsucsessfull
    '''

    results = Game.objects.all().filter(name__icontains=query)
    if len(results) > 0:
        return True, [results]
    else:
        return False, []


def crawlSearch(query):
    pass