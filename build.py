#!/usr/bin/env python3
"""
RepairEstimator.co Build Script

Processes all article JSON files and generates the static website.
Run this locally before git push, or let Vercel/Netlify run it automatically.

Usage:
    python3 build.py
"""

import os
import json
from pathlib import Path
from repairestimator_automation_system import ArticlePublisher

def main():
    print("=" * 60)
    print("RepairEstimator.co Build System")
    print("=" * 60)

    # Initialize publisher with your actual domain
    publisher = ArticlePublisher(
        base_url="https://repairestimator.co",
        output_dir="./build"
    )

    # Find and process all articles
    articles_dir = Path("./articles")

    if not articles_dir.exists():
        print("ERROR: articles/ directory not found!")
        print("Create articles/ directory and add article JSON files.")
        return

    article_files = sorted(articles_dir.glob("*.json"))

    if not article_files:
        print("WARNING: No article JSON files found in articles/")
        return

    print(f"\nFound {len(article_files)} article(s)\n")

    # Process each article
    for json_file in article_files:
        try:
            print(f"→ Processing: {json_file.name}")
            publisher.publish(str(json_file))
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print()

    # Generate supporting files
    try:
        publisher.generate_sitemap()
        publisher.generate_robots_txt()
        publisher.generate_index_page()
    except Exception as e:
        print(f"ERROR generating supporting files: {e}")
        return

    print("\n" + "=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print(f"✓ Total articles published: {len(publisher.articles)}")
    print(f"✓ Output directory: ./build/")
    print()
    print("Generated files:")
    print(f"  • ./build/index.html (Homepage)")
    print(f"  • ./build/blog/*.html ({len(publisher.articles)} articles)")
    print(f"  • ./build/sitemap.xml (For Google crawling)")
    print(f"  • ./build/robots.txt (Crawler directives)")
    print()
    print("Next steps:")
    print("  1. Test locally: python3 -m http.server 8000")
    print("  2. Visit: http://localhost:8000")
    print("  3. git push to deploy automatically to Vercel/Netlify")
    print()

if __name__ == "__main__":
    main()
