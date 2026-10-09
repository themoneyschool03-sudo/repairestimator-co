#!/usr/bin/env python3
"""
RepairEstimator.co Article Publishing Automation System

Converts article JSON to HTML pages with proper SEO, AdSense, and Google Search Console compliance.
Generates dynamic sitemap and robots.txt.

Usage:
    python3 repairestimator_automation_system.py --input article.json --output ./build
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
import re

class ArticlePublisher:
    def __init__(self, base_url="https://repairestimator.co", output_dir="./build"):
        self.base_url = base_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.articles = []

    def load_article(self, json_file):
        """Load article from JSON file."""
        with open(json_file, 'r') as f:
            article = json.load(f)
        self.articles.append(article)
        return article

    def generate_html(self, article):
        """Convert article JSON to HTML with SEO and AdSense compliance."""

        # Create safe filename from slug
        filename = f"{article['slug']}.html"

        # Parse markdown body to HTML (basic conversion)
        html_body = self._markdown_to_html(article['article_body'])

        # Build internal links HTML
        internal_links_html = ""
        if article.get('internal_links'):
            internal_links_html = '<div class="internal-links" style="background: #f5f5f5; padding: 20px; margin: 30px 0; border-radius: 8px;"><h3>Related Articles</h3><ul style="list-style: none; padding: 0;">'
            for link in article['internal_links']:
                internal_links_html += f'<li style="margin: 10px 0;"><a href="{link["url"]}" style="color: #0066cc; text-decoration: none;">{link["anchor_text"]}</a></li>'
            internal_links_html += '</ul></div>'

        # Build FAQ HTML
        faq_html = ""
        if article.get('faq'):
            faq_html = '<section class="faq-section" style="margin: 40px 0;"><h2>Frequently Asked Questions</h2>'
            for i, item in enumerate(article['faq'], 1):
                faq_html += f'''
<div class="faq-item" itemscope itemtype="https://schema.org/FAQPage" style="margin: 20px 0; padding: 15px; border-left: 4px solid #0066cc;">
    <h3 itemprop="name" style="margin: 0 0 10px 0;">{item['question']}</h3>
    <p itemprop="text">{item['answer']}</p>
</div>
'''
            faq_html += '</section>'

        # Build structured data for Article schema
        article_schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article['seo_title'],
            "description": article['meta_description'],
            "image": article.get('featured_image_url', ''),
            "author": {
                "@type": "Organization",
                "name": "RepairEstimator.co"
            },
            "publisher": {
                "@type": "Organization",
                "name": "RepairEstimator.co"
            },
            "datePublished": article.get('created_date', datetime.now().isoformat()),
            "dateModified": article.get('last_updated', datetime.now().isoformat())
        }

        schema_json = json.dumps(article_schema)

        # Generate complete HTML
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['seo_title']}</title>
    <meta name="description" content="{article['meta_description']}">
    <meta name="keywords" content="{article['meta_keywords']}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="RepairEstimator.co">
    <meta property="og:title" content="{article['seo_title']}">
    <meta property="og:description" content="{article['meta_description']}">
    <meta property="og:image" content="{article.get('featured_image_url', '')}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="{self.base_url}/blog/{article['slug']}.html">
    <link rel="canonical" href="{self.base_url}/blog/{article['slug']}.html">

    <!-- Google Search Console verification tag -->
    <meta name="google-site-verification" content="YOUR_GSC_VERIFICATION_CODE">

    <!-- AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-YOUR_ADSENSE_ID"
        crossorigin="anonymous"></script>

    <!-- Schema.org structured data -->
    <script type="application/ld+json">
{schema_json}
    </script>

    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }}

        header {{
            background: #2c3e50;
            color: white;
            padding: 20px 0;
            border-bottom: 3px solid #3498db;
        }}

        .header-content {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }}

        .header-content h1 {{
            font-size: 28px;
            margin-bottom: 10px;
        }}

        .header-content p {{
            font-size: 16px;
            color: #ecf0f1;
        }}

        main {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        article {{
            background: #fff;
            padding: 30px;
        }}

        h2 {{
            margin: 30px 0 15px 0;
            color: #2c3e50;
            font-size: 22px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }}

        h3 {{
            margin: 20px 0 10px 0;
            color: #34495e;
            font-size: 18px;
        }}

        p {{
            margin: 15px 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 15px 0 15px 30px;
        }}

        li {{
            margin: 8px 0;
        }}

        a {{
            color: #0066cc;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        strong {{
            color: #2c3e50;
        }}

        /* AdSense compliance - ad spacing */
        .ad-space {{
            margin: 30px 0;
            min-height: 250px;
            background: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 12px;
        }}

        .cta-box {{
            background: #e8f4f8;
            border-left: 4px solid #0066cc;
            padding: 20px;
            margin: 30px 0;
            border-radius: 4px;
        }}

        .cta-box p {{
            margin: 0;
            font-weight: 500;
        }}

        .cta-box a {{
            font-weight: bold;
            color: #0066cc;
        }}

        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 50px;
        }}

        .breadcrumb {{
            margin: 20px 0;
            font-size: 14px;
            color: #666;
        }}

        .breadcrumb a {{
            margin: 0 5px;
        }}

        .meta-info {{
            color: #666;
            font-size: 14px;
            margin: 15px 0;
            border-bottom: 1px solid #ecf0f1;
            padding-bottom: 15px;
        }}

        /* Mobile responsiveness */
        @media (max-width: 768px) {{
            main {{
                padding: 20px 10px;
            }}

            article {{
                padding: 20px;
            }}

            h2 {{
                font-size: 18px;
            }}

            .header-content h1 {{
                font-size: 22px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <h1>RepairEstimator.co</h1>
            <p>Your Guide to Fair Repair Pricing</p>
        </div>
    </header>

    <main>
        <div class="breadcrumb">
            <a href="/">Home</a> / <a href="/blog">Blog</a> / {article['title']}
        </div>

        <article>
            <h1 style="margin: 0 0 20px 0; font-size: 28px; color: #2c3e50;">{article['title']}</h1>

            <div class="meta-info">
                <strong>Last Updated:</strong> {article.get('last_updated', 'Oct 3, 2026')} |
                <strong>Reading Time:</strong> {max(1, article.get('word_count', 1000) // 250)} min read
            </div>

            <!-- Ad space - top of article -->
            <div class="ad-space">
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-YOUR_ADSENSE_ID"
                     data-ad-slot="YOUR_AD_SLOT_1"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({{}});
                </script>
            </div>

            {html_body}

            <!-- Ad space - middle of article -->
            <div class="ad-space">
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-YOUR_ADSENSE_ID"
                     data-ad-slot="YOUR_AD_SLOT_2"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({{}});
                </script>
            </div>

            {faq_html}

            {internal_links_html}

            <!-- CTA Box -->
            <div class="cta-box">
                <p>{article.get('call_to_action', "Want to know if your repair quote is fair? Use RepairEstimator.co to compare prices and get a second opinion on your mechanic's quote.")}</p>
            </div>

            <!-- Ad space - bottom of article -->
            <div class="ad-space">
                <ins class="adsbygoogle"
                     style="display:block"
                     data-ad-client="ca-pub-YOUR_ADSENSE_ID"
                     data-ad-slot="YOUR_AD_SLOT_3"
                     data-ad-format="auto"
                     data-full-width-responsive="true"></ins>
                <script>
                     (adsbygoogle = window.adsbygoogle || []).push({{}});
                </script>
            </div>
        </article>
    </main>

    <footer>
        <p>&copy; 2026 RepairEstimator.co. All rights reserved.</p>
    </footer>
</body>
</html>
'''

        return html, filename

    def _markdown_to_html(self, markdown_text):
        """Basic markdown to HTML conversion."""
        html = markdown_text

        # Convert markdown headers
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

        # Convert bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Convert line breaks to paragraphs
        paragraphs = html.split('\n\n')
        html = ''.join(f'<p>{p.strip()}</p>' if p.strip() and not p.strip().startswith('<') else p for p in paragraphs)

        return html

    def publish(self, json_file):
        """Load and publish article."""
        article = self.load_article(json_file)
        html, filename = self.generate_html(article)

        # Create blog directory
        blog_dir = self.output_dir / "blog"
        blog_dir.mkdir(exist_ok=True)

        # Write HTML file
        output_path = blog_dir / filename
        with open(output_path, 'w') as f:
            f.write(html)

        print(f"✓ Published: {filename}")
        return str(output_path), article

    def generate_sitemap(self):
        """Generate XML sitemap from all articles."""
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        # Add home page
        sitemap += f'''  <url>
    <loc>{self.base_url}/</loc>
    <lastmod>{datetime.now().isoformat()}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
'''

        # Add all articles
        for article in self.articles:
            sitemap += f'''  <url>
    <loc>{self.base_url}/blog/{article['slug']}.html</loc>
    <lastmod>{article.get('last_updated', datetime.now().isoformat())}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
'''

        sitemap += '</urlset>'

        # Write sitemap
        sitemap_path = self.output_dir / "sitemap.xml"
        with open(sitemap_path, 'w') as f:
            f.write(sitemap)

        print(f"✓ Generated sitemap with {len(self.articles)} articles")
        return str(sitemap_path)

    def generate_robots_txt(self):
        """Generate robots.txt for Google crawling."""
        robots = '''User-agent: *
Allow: /
Disallow: /admin/
Disallow: /private/

Sitemap: https://repairestimator.co/sitemap.xml

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

# Crawl delay
Crawl-delay: 1
'''

        robots_path = self.output_dir / "robots.txt"
        with open(robots_path, 'w') as f:
            f.write(robots)

        print(f"✓ Generated robots.txt")
        return str(robots_path)

    def generate_index_page(self):
        """Generate homepage listing all articles."""
        articles_html = '<div class="articles-list">'

        for article in self.articles:
            articles_html += f'''
<div class="article-card" style="margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px;">
    <h2><a href="/blog/{article['slug']}.html">{article['title']}</a></h2>
    <p>{article.get('excerpt', article['meta_description'])}</p>
    <a href="/blog/{article['slug']}.html" style="color: #0066cc; font-weight: bold;">Read more →</a>
</div>
'''

        articles_html += '</div>'

        index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RepairEstimator.co - Fair Repair Pricing Guide</title>
    <meta name="description" content="Learn about repair costs, common issues, and fair pricing for car repairs. Get expert guides on everything from power steering to fuel pumps.">
    <link rel="canonical" href="https://repairestimator.co/">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        header {{
            background: #2c3e50;
            color: white;
            padding: 60px 20px;
            text-align: center;
        }}
        header h1 {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        main {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        .article-card {{
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            transition: box-shadow 0.3s;
        }}
        .article-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 50px;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <header>
        <h1>RepairEstimator.co</h1>
        <p>Your Guide to Fair Auto Repair Pricing</p>
    </header>

    <main>
        <h2>Latest Articles</h2>
        {articles_html}
    </main>

    <footer>
        <p>&copy; 2026 RepairEstimator.co. All rights reserved.</p>
    </footer>
</body>
</html>
'''

        index_path = self.output_dir / "index.html"
        with open(index_path, 'w') as f:
            f.write(index_html)

        print(f"✓ Generated homepage")
        return str(index_path)

def main():
    # Initialize publisher
    publisher = ArticlePublisher(
        base_url="https://repairestimator.co",
        output_dir="./build"
    )

    # Publish article
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        if os.path.exists(json_file):
            publisher.publish(json_file)

    # Generate supporting files
    publisher.generate_sitemap()
    publisher.generate_robots_txt()
    publisher.generate_index_page()

    print("\n✓ Build complete! Site ready in ./build/")
    print(f"  - Articles: ./build/blog/")
    print(f"  - Sitemap: ./build/sitemap.xml")
    print(f"  - Robots: ./build/robots.txt")
    print(f"  - Homepage: ./build/index.html")

if __name__ == "__main__":
    main()
