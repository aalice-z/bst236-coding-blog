#!/usr/bin/env python3
"""
generate_page.py - Generate HTML page from arXiv papers data

Usage:
    python generate_page.py
    
Reads papers.json and generates papers.html
"""

import json
import sys
from datetime import datetime


def load_papers(filename='papers.json'):
    """
    Load papers from JSON file.
    
    Args:
        filename: Input JSON filename
        
    Returns:
        Dictionary with papers data
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run fetch_papers.py first.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error parsing {filename}: {e}")
        sys.exit(1)


def generate_paper_card(paper):
    """
    Generate HTML for a single paper card.
    
    Args:
        paper: Dictionary with paper information
        
    Returns:
        HTML string for the paper card
    """
    # Truncate abstract if too long
    abstract = paper['abstract']
    if len(abstract) > 300:
        abstract = abstract[:297] + '...'
    
    # Format authors
    authors = paper['authors']
    if len(authors) > 3:
        authors_str = ', '.join(authors[:3]) + f', et al. ({len(authors)} authors)'
    else:
        authors_str = ', '.join(authors)
    
    return f'''
        <div class="paper-card">
            <div class="paper-header">
                <h3 class="paper-title">
                    <a href="{paper['pdf_link']}" target="_blank" rel="noopener noreferrer">
                        {paper['title']}
                    </a>
                </h3>
                <div class="paper-meta">
                    <span class="paper-date">📅 {paper['published']}</span>
                    <span class="paper-id">
                        <a href="{paper['arxiv_link']}" target="_blank" rel="noopener noreferrer">
                            arXiv:{paper['id']}
                        </a>
                    </span>
                </div>
            </div>
            <div class="paper-authors">
                <span class="authors-label">👥 Authors:</span> {authors_str}
            </div>
            <div class="paper-abstract">
                <p>{abstract}</p>
            </div>
            <div class="paper-links">
                <a href="{paper['pdf_link']}" class="paper-link pdf-link" target="_blank" rel="noopener noreferrer">
                    📄 PDF
                </a>
                <a href="{paper['arxiv_link']}" class="paper-link arxiv-link" target="_blank" rel="noopener noreferrer">
                    🔗 arXiv Page
                </a>
            </div>
        </div>
    '''


def generate_html(papers_data):
    """
    Generate complete HTML page.
    
    Args:
        papers_data: Dictionary with papers data
        
    Returns:
        Complete HTML string
    """
    papers = papers_data['papers']
    last_updated = papers_data['last_updated']
    count = papers_data['count']
    
    # Format last updated time
    try:
        dt = datetime.fromisoformat(last_updated)
        formatted_time = dt.strftime('%B %d, %Y at %I:%M %p')
    except:
        formatted_time = last_updated
    
    # Generate all paper cards
    paper_cards_html = '\n'.join(generate_paper_card(paper) for paper in papers)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest arXiv Papers - My Coding Blog</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .papers-container {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            min-height: 100vh;
            padding: 2rem 0;
        }}

        .papers-header {{
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }}

        .papers-header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }}

        .papers-header p {{
            font-size: 1.1rem;
            opacity: 0.95;
        }}

        .papers-info {{
            background: white;
            padding: 1rem 2rem;
            border-radius: 1rem;
            box-shadow: var(--shadow-lg);
            margin-bottom: 2rem;
            text-align: center;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}

        .papers-info p {{
            margin: 0.5rem 0;
            color: var(--text-light);
        }}

        .papers-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        .paper-card {{
            background: white;
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            transition: transform 0.3s, box-shadow 0.3s;
            display: flex;
            flex-direction: column;
            border: 2px solid transparent;
        }}

        .paper-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary-color);
        }}

        .paper-header {{
            margin-bottom: 1rem;
        }}

        .paper-title {{
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            line-height: 1.4;
        }}

        .paper-title a {{
            color: var(--text-color);
            text-decoration: none;
            transition: color 0.3s;
        }}

        .paper-title a:hover {{
            color: var(--primary-color);
        }}

        .paper-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-light);
        }}

        .paper-date {{
            color: var(--accent-color);
            font-weight: 600;
        }}

        .paper-id a {{
            color: var(--text-light);
            text-decoration: none;
            font-family: monospace;
        }}

        .paper-id a:hover {{
            color: var(--primary-color);
        }}

        .paper-authors {{
            margin-bottom: 1rem;
            padding: 0.75rem;
            background: var(--bg-secondary);
            border-radius: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-light);
        }}

        .authors-label {{
            font-weight: 600;
            color: var(--text-color);
        }}

        .paper-abstract {{
            flex-grow: 1;
            margin-bottom: 1rem;
            line-height: 1.6;
            color: var(--text-light);
        }}

        .paper-abstract p {{
            margin: 0;
        }}

        .paper-links {{
            display: flex;
            gap: 1rem;
            margin-top: auto;
        }}

        .paper-link {{
            flex: 1;
            text-align: center;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: transform 0.2s, opacity 0.2s;
        }}

        .paper-link:hover {{
            transform: scale(1.05);
            opacity: 0.9;
        }}

        .pdf-link {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
        }}

        .arxiv-link {{
            background: var(--bg-secondary);
            color: var(--text-color);
            border: 2px solid var(--border-color);
        }}

        .back-link {{
            display: inline-block;
            margin: 2rem auto;
            padding: 0.75rem 1.5rem;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            text-decoration: none;
            border-radius: 0.5rem;
            font-weight: 600;
            transition: background 0.3s;
            text-align: center;
        }}

        .back-link:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}

        .back-link-container {{
            text-align: center;
            margin-top: 3rem;
        }}

        @media (max-width: 768px) {{
            .papers-grid {{
                grid-template-columns: 1fr;
                padding: 0 1rem;
            }}

            .papers-header h1 {{
                font-size: 2rem;
            }}

            .paper-links {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="papers-container">
        <div class="container">
            <div class="papers-header">
                <h1>📚 Latest arXiv Papers</h1>
                <p>Curated research papers on machine learning and deep learning</p>
            </div>

            <div class="papers-info">
                <p><strong>{count} papers</strong> • Last updated: {formatted_time}</p>
                <p>🔄 Automatically updated daily at midnight</p>
            </div>

            <div class="papers-grid">
{paper_cards_html}
            </div>

            <div class="back-link-container">
                <a href="index.html" class="back-link">← Back to Home</a>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    return html


def save_html(html_content, filename='papers.html'):
    """
    Save HTML content to file.
    
    Args:
        html_content: HTML string to save
        filename: Output HTML filename
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Successfully generated {filename}")
    except IOError as e:
        print(f"Error saving {filename}: {e}")
        sys.exit(1)


def main():
    """Main function to generate papers page."""
    print("Loading papers from papers.json...")
    papers_data = load_papers()
    
    print(f"Found {papers_data['count']} papers")
    print("Generating HTML page...")
    
    html = generate_html(papers_data)
    save_html(html)
    
    print("\n" + "="*60)
    print("SUCCESS!")
    print("="*60)
    print("papers.html has been generated successfully")
    print("You can now open it in a browser or deploy to GitHub Pages")
    print("="*60)


if __name__ == '__main__':
    main()
