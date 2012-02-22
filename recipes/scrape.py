#!/usr/bin/env python
""" Contains functions for scraping allrecipes.com. """

import re
from urllib2 import urlopen

from BeautifulSoup import BeautifulSoup
from recipe import Recipe, understandDirections, understandIngredients


SEARCH_URL = "http://allrecipes.com/Search/Recipes.aspx?WithTerm=%s"
RECIPE_URL = "http://allrecipes.com/recipe/%s/detail.aspx"


def scrapeSearch(query):
    """ Search for query and return a list of 2-tuples of (pretty-name, title).
    e.g., [("Frog Cupcakes", "frog-cupcakes")]
    """
    entity = urlopen(SEARCH_URL % (query.replace(" ", "%20"))).read()
    soup = BeautifulSoup(entity, convertEntities=BeautifulSoup.HTML_ENTITIES)
    links = soup.findAll('a', id=re.compile('.*lnkRecipeTitle'))
    return [_parseSearcha(a) for a in links]


def scrapeRecipe(title):
    """ Scrape the page for the recipe with the given title. Return a recipe
    parsed from that page. """
    entity = urlopen(RECIPE_URL % title).read()
    soup = BeautifulSoup(entity)
    details = soup.find('div', attrs={'class':
        re.compile('recipe-details-content.*')})
    recipe = Recipe()
    # Get title and image.
    recipe.title = soup.find('span', 'itemreviewed').text
    # Get prep, cook, and total times.
    recipe.preptime = _parseTime(details, 'Prep')
    recipe.cooktime = _parseTime(details, 'Cook')
    recipe.totaltime = _parseTime(details, 'Ready')
    # Get ingredients.
    ingredient_strings = _parseIngredients(details.find('div', 'ingredients'))
    recipe.ingredients = understandIngredients(ingredient_strings)
    # Get steps.
    direction_strings = _parseDirections(details.find('div', 'directions'))
    recipe.directions = understandDirections(direction_strings,
            recipe.ingredients)
    recipe.makeCategories()
    recipe.makeEthnicities()
    return recipe


def _parseSearcha(a):
    """ Parse a pretty-name and title out of an <a> element and return them as
    a 2-tuple. """
    pretty_name = a.text
    title = a.attrMap['href'].split('/')[-2]
    return (pretty_name, title)


def _parseTime(details, name):
    """ Parse {prep, cook, total} time out of the details div. """
    h5 = details.find('h5', id=re.compile('.*h5' + name))
    if h5 is None:
        return None
    spans = h5.findAll('span')
    return spans[-1].text


def _parseIngredients(div):
    """ Parse a list of strings out of the div.ingredients. """
    return [li.text.replace("&#174;", "") for li in div.findAll('li',
        'ingredient') if li.text != "&nbsp;"]


def _parseDirections(div):
    """ Parse a list of strings out of the div.directions. """
    return [span.text for span in div.findAll('span', 'break')]

