import os
import random
import re
import sys
from typing import Dict

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus: Dict[str, set], page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus.get(page, [])
    numberOfPages = len(corpus)
    pageLinks = {}
    allPages = list(corpus.keys())
    
    uniform_probability = (1-damping_factor)/numberOfPages
    link_probability = (damping_factor * (1/len(links))) if links else 0
    
    for eachPage in allPages:
        if eachPage in links:
            pageLinks[eachPage] = link_probability + uniform_probability
        else:
            pageLinks[eachPage] = uniform_probability
        
    
    return pageLinks


def sample_pagerank(corpus:Dict[str, set], damping_factor:float, n:int):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    allPages = list(corpus.keys())
    page = random.choice(allPages)
  
    pageFrequency = {page: 1}

    for i in range(1,n):
        models = transition_model(corpus, page, damping_factor)
        page = random.choices(list(models.keys()), weights=list(models.values()))[0]
        if page in pageFrequency:
            pageFrequency[page] += 1
        else:
            pageFrequency[page] = 1
    
    
    # pageRank = {}
    # for key, value in pageFrequency.items():
    #     keyProb = value/n
    #     pageRank[key] = keyProb
    pageRank = {key: value/n for key, value in pageFrequency.items()}
    
        
    return pageRank


def iterate_pagerank(corpus:Dict[str,set], damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    allPages = list(corpus.keys())
    numberOfPages = len(allPages)
    pageRank = {page: 1/numberOfPages for page in allPages}
    
    #handle pages with no links
    for page, links in corpus.items():
        if not links:
            corpus[page] = set(allPages)
    
    while True:
        newRank = {}
        
        for page in allPages:
            uniform_probability = (1-damping_factor)/numberOfPages
            link_probability = 0 
            for other_page, links in corpus.items():
                if page in links:
                    link_probability += pageRank[other_page]/len(links)
            
            
            newRank[page] = uniform_probability + damping_factor * link_probability
        
        #check convergence
        if all(abs(newRank[page] - pageRank[page]) < 0.001 for page in allPages):
            break
        
        # Update pageRank for the next iteration
        pageRank = newRank
    
        
    return pageRank


if __name__ == "__main__":
    main()

