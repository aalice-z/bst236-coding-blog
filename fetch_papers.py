#!/usr/bin/env python3
"""
fetch_papers.py - Fetch latest papers from arXiv API

Usage:
    python fetch_papers.py keyword1 keyword2 ...
    python fetch_papers.py "machine learning" "deep learning"
    python fetch_papers.py cat:cs.AI  # Search by category
"""

import sys
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import quote
import requests


# arXiv API configuration
ARXIV_API_URL = "http://export.arxiv.org/api/query"
MAX_RESULTS = 20


def build_query(keywords):
    """
    Build arXiv API query from keywords.
    
    Args:
        keywords: List of search keywords
        
    Returns:
        Query string for arXiv API
    """
    if not keywords:
        # Default to recent machine learning papers
        return "cat:cs.LG OR cat:cs.AI OR cat:stat.ML"
    
    # Check if using category search (e.g., cat:cs.AI)
    if any(kw.startswith("cat:") for kw in keywords):
        # Join categories with OR
        return " OR ".join(keywords)
    
    # Otherwise, do full-text search
    # Join keywords with AND for more specific results
    query_terms = [f'all:"{kw}"' for kw in keywords]
    return " AND ".join(query_terms)


def fetch_arxiv_papers(keywords, max_results=MAX_RESULTS):
    """
    Fetch papers from arXiv API based on keywords.
    
    Args:
        keywords: List of search keywords
        max_results: Maximum number of papers to fetch
        
    Returns:
        XML response text from arXiv API
    """
    query = build_query(keywords)
    
    params = {
        'search_query': query,
        'start': 0,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    print(f"Querying arXiv API with: {query}")
    print(f"Fetching up to {max_results} papers...")
    
    try:
        response = requests.get(ARXIV_API_URL, params=params, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching from arXiv API: {e}")
        sys.exit(1)


def parse_arxiv_response(xml_text):
    """
    Parse arXiv API XML response and extract paper information.
    
    Args:
        xml_text: XML response from arXiv API
        
    Returns:
        List of paper dictionaries
    """
    # Define XML namespaces
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        sys.exit(1)
    
    papers = []
    entries = root.findall('atom:entry', namespaces)
    
    print(f"Found {len(entries)} papers")
    
    for entry in entries:
        # Extract paper ID from the entry ID URL
        entry_id = entry.find('atom:id', namespaces).text
        paper_id = entry_id.split('/abs/')[-1]
        
        # Extract title (clean up whitespace)
        title_elem = entry.find('atom:title', namespaces)
        title = ' '.join(title_elem.text.split()) if title_elem is not None else "No title"
        
        # Extract authors
        authors = []
        for author in entry.findall('atom:author', namespaces):
            name_elem = author.find('atom:name', namespaces)
            if name_elem is not None:
                authors.append(name_elem.text)
        
        # Extract abstract (clean up whitespace)
        summary_elem = entry.find('atom:summary', namespaces)
        abstract = ' '.join(summary_elem.text.split()) if summary_elem is not None else "No abstract"
        
        # Extract published date
        published_elem = entry.find('atom:published', namespaces)
        published_date = published_elem.text if published_elem is not None else "Unknown"
        
        # Format date to be more readable
        try:
            dt = datetime.fromisoformat(published_date.replace('Z', '+00:00'))
            formatted_date = dt.strftime('%B %d, %Y')
        except:
            formatted_date = published_date
        
        # Construct PDF link
        pdf_link = f"http://arxiv.org/pdf/{paper_id}.pdf"
        
        # Construct arXiv page link
        arxiv_link = f"http://arxiv.org/abs/{paper_id}"
        
        paper = {
            'id': paper_id,
            'title': title,
            'authors': authors,
            'abstract': abstract,
            'published': formatted_date,
            'published_raw': published_date,
            'pdf_link': pdf_link,
            'arxiv_link': arxiv_link
        }
        
        papers.append(paper)
    
    return papers


def save_papers_to_json(papers, filename='papers.json'):
    """
    Save papers to JSON file.
    
    Args:
        papers: List of paper dictionaries
        filename: Output JSON filename
    """
    output = {
        'last_updated': datetime.now().isoformat(),
        'count': len(papers),
        'papers': papers
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nSuccessfully saved {len(papers)} papers to {filename}")
    except IOError as e:
        print(f"Error saving to {filename}: {e}")
        sys.exit(1)


def main():
    """Main function to fetch and save arXiv papers."""
    # Get keywords from command-line arguments
    keywords = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if not keywords:
        print("No keywords provided. Using default: machine learning, AI, and statistics papers")
        print("\nUsage: python fetch_papers.py keyword1 keyword2 ...")
        print("Example: python fetch_papers.py 'machine learning' 'neural networks'")
        print("Example: python fetch_papers.py cat:cs.AI cat:cs.LG\n")
    
    # Fetch papers from arXiv
    xml_response = fetch_arxiv_papers(keywords, MAX_RESULTS)
    
    # Parse the XML response
    papers = parse_arxiv_response(xml_response)
    
    if not papers:
        print("No papers found!")
        sys.exit(1)
    
    # Save to JSON
    save_papers_to_json(papers)
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total papers fetched: {len(papers)}")
    print(f"First paper: {papers[0]['title'][:60]}...")
    print(f"Latest published: {papers[0]['published']}")
    print("="*60)


if __name__ == '__main__':
    main()
