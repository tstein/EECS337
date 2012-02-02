#!/usr/bin/env python2
""" Contains functions for scraping allrecipes.com. """

import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup
from recipe import Recipe


SEARCH_URL = "http://allrecipes.com/Search/Recipes.aspx?WithTerm=%s"
RECIPE_URL = "http://allrecipes.com/recipe/%s/detail.aspx"


def scrapeSearch(query):
    """ Search for query and return a list of 2-tuples of (pretty-name, title).
    e.g., [("Frog Cupcakes", "frog-cupcakes")]
    """
    entity = urlopen(SEARCH_URL % query).read()
    soup = BeautifulSoup(entity)
    links = soup.findAll('a', id=re.compile('.*lnkRecipeTitle'))
    return [_parseSearcha(a) for a in links]


def scrapeRecipe(title):
    """ Scrape the page for the recipe with the given title. Return a recipe
    parsed from that page. """
    entity = urlopen(RECIPE_URL % title).read()
    soup = BeautifulSoup(entity)
    details = soup.find('div', attrs={'class' :
        re.compile('recipe-details-content.*')})
    recipe = Recipe()
    # Get title and image.
    recipe.title = soup.find('span', 'itemreviewed').text
    # Get prep, cook, and total times.
    recipe.preptime = _parseTime(details, 'Prep')
    recipe.cooktime = _parseTime(details, 'Cook')
    recipe.totaltime = _parseTime(details, 'Ready')
    # Get ingredients.
    pass
    # Get steps.
    pass
    return recipe


def _parseSearcha(a):
    """ Parse a pretty-name and title out of an <a> element and return them as a
    2-tuple. """
    pretty_name = a.text
    title = a.attrMap['href'].split('/')[-2]
    return (pretty_name, title)

def _parseTime(details, name):
    """ Parse {prep, cook, total} time out of the details div. """
    h5 = details.find('h5', id=re.compile('.*h5' + name))
    spans = h5.findAll('span')
    return spans[-1].text

