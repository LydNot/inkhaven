#!/usr/bin/env python3
"""
Convert inkhaven_updated.xml (RSS format) to inkhaven_feed.json (JSON Feed format)
"""

import xml.etree.ElementTree as ET
import json
from datetime import datetime
from urllib.parse import urlparse
import re

def extract_author_from_url(url):
    """Extract author name and blog URL from post URL"""
    parsed = urlparse(url)
    domain = parsed.netloc
    
    # Comprehensive author mapping from existing JSON feed
    author_mapping = {
        'aelerinya.substack.com': ('Lucie Philippon', 'https://aelerinya.substack.com'),
        'agarriga.substack.com': ('Adrià Garriga Alonso', 'https://substack.com/@columnspace'),
        'agifriday.substack.com': ('Daniel Reeves', 'https://blog.beeminder.com/'),
        'alignmentforum.org': ('Alignment Forum', 'https://www.alignmentforum.org/'),
        'www.alignmentforum.org': ('Alignment Forum', 'https://www.alignmentforum.org/'),
        'angadh.com': ('Angadh Nanjangud', 'https://angadh.com/'),
        'anthropic.ml': ('Anthropic', 'https://anthropic.ml/'),
        'archiveofourown.org': ('Justin Kuiper', 'https://justinkuiper.substack.com/'),
        'asourdays.substack.com': ('William Friedman', 'https://asourdays.substack.com/'),
        'befriendjamin.substack.com': ('Ben Steinhorn', 'https://befriendjamin.substack.com/'),
        'bengoldhaber.substack.com': ('Ben Goldhaber', 'https://bengoldhaber.substack.com/'),
        'bestjelly.substack.com': ('Harri Besceli', 'https://bestjelly.substack.com/'),
        'blog.beeminder.com': ('Daniel Reeves', 'https://blog.beeminder.com/'),
        'boardgamegeek.com': ('Vaniver', 'https://www.lesswrong.com/users/vaniver'),
        'camilleberger.substack.com': ('Camille Berger', 'https://camilleberger.substack.com/?sort=top'),
        'collisteru.net': ('Sean Carter', 'https://collisteru.substack.com/'),
        'collisteru.substack.com': ('Sean Carter', 'https://collisteru.substack.com/'),
        'comments.ustr.gov': ('Jenn', 'https://jenn.site/'),
        'complexityzoo.net': ('Harri Besceli', 'https://bestjelly.substack.com/'),
        'croissanthology.com': ('Croissanthology', 'http://croissanthology.com/'),
        'croissanthology.substack.com': ('Croissanthology', 'http://croissanthology.com/'),
        'dactile.net': ('David Gros', 'https://dactile.net'),
        'danielpaleka.com': ('Daniel Paleka', 'https://danielpaleka.com/inkhaven'),
        'daystareld.com': ('Damon Sasi', 'https://daystareld.com/'),
        'deathisbad.substack.com': ('Eneasz Brodski', 'https://deathisbad.substack.com/'),
        'futuring.substack.com': ('Raye', 'https://futuring.substack.com/'),
        'hauke.substack.com': ('Hauke Hillebrandt', 'https://hauke.substack.com/'),
        'hfh.pw': ('Hauke Hillebrandt', 'https://hauke.substack.com/'),
        'www.hfh.pw': ('Hauke Hillebrandt', 'https://hauke.substack.com/'),
        'huggingface.co': ('Daniel Paleka', 'https://danielpaleka.com/inkhaven'),
        'humaninvariant.substack.com': ('Human Invariant', 'https://www.humaninvariant.com/'),
        'www.humaninvariant.com': ('Human Invariant', 'https://www.humaninvariant.com/'),
        'inchpin.substack.com': ('Linch Zhang', 'https://linch.substack.com/'),
        'inkhavenspotlight.substack.com': ('Ben Pace', 'https://www.lesswrong.com/users/benito'),
        'jenn.site': ('Jenn', 'https://jenn.site/'),
        'www.jenn.site': ('Jenn', 'https://jenn.site/'),
        'joannabregan.medium.com': ('Joanna Bregan', 'https://joannabregan.substack.com/'),
        'joannabregan.substack.com': ('Joanna Bregan', 'https://joannabregan.substack.com/'),
        'justinkuiper.substack.com': ('Justin Kuiper', 'https://justinkuiper.substack.com/'),
        'justismills.substack.com': ('Justis Mills', 'https://justismills.substack.com/'),
        'kaverennedy.substack.com': ('Kave Rennedy', 'https://kaverennedy.substack.com'),
        'kuiperblog.tumblr.com': ('Justin Kuiper', 'https://justinkuiper.substack.com/'),
        'letterboxd.com': ('Justin Kuiper', 'https://justinkuiper.substack.com/'),
        'lettersfrombethlehem.substack.com': ('Amanda Luce', 'https://lettersfrombethlehem.substack.com/'),
        'life-in-a-monospace-typeface.tumblr.com': ('Rob Miles', 'https://life-in-a-monospace-typeface.tumblr.com/'),
        'linch.substack.com': ('Linch Zhang', 'https://linch.substack.com/'),
        'lucent.substack.com': ('Michael Dayah', 'https://lucent.substack.com/'),
        'lucent.vision': ('Michael Dayah', 'https://lucent.substack.com/'),
        'lydia.ml': ('Lydia Nottingham', 'https://lydianottingham.substack.com/'),
        'lydianottingham.substack.com': ('Lydia Nottingham', 'https://lydianottingham.substack.com/'),
        'markusstrasser.org': ('Markus Strasser', 'https://markusstrasser.org/'),
        'mdickens.me': ('Michael Dickens', 'https://mdickens.me/'),
        'mikhailsamin.substack.com': ('Mikhail Samin', 'https://mikhailsamin.substack.com/'),
        'mingyuan.substack.com': ('Claire Wang', 'https://mingyuan.substack.com/'),
        'mynamelowercase.com': ('Mahmoud Ghanem', 'https://mynamelowercase.com/'),
        'mynamelowercase.mataroa.blog': ('Mahmoud Ghanem', 'https://mynamelowercase.com/'),
        'namelessvirtue.com': ('Alex Altair', 'https://namelessvirtue.com/'),
        'newsletter.danielpaleka.com': ('Daniel Paleka', 'https://danielpaleka.com/inkhaven'),
        'nikolajurkovic.substack.com': ('Nikola Jurkovic', 'https://substack.com/@nikolajurkovic'),
        'nomadsvagabonds.substack.com': ('Nomads and Vagabonds', 'https://nomadsvagabonds.substack.com/'),
        'old.reddit.com': ('Oliver Habryka', 'https://www.lesswrong.com/users/habryka4'),
        'open.substack.com': ('Substack Open', 'https://open.substack.com/'),
        'psychotechnology.substack.com': ('Psychotechnology', 'https://psychotechnology.substack.com/'),
        'radimentary.wordpress.com': ('alkjash', 'https://radimentary.wordpress.com/'),
        'reddit.com': ('Oliver Habryka', 'https://www.lesswrong.com/users/habryka4'),
        'www.reddit.com': ('Oliver Habryka', 'https://www.lesswrong.com/users/habryka4'),
        'rivalvoices.substack.com': ('Rival Voices', 'https://rivalvoices.substack.com/'),
        'sexmoneyart.com': ('Sacha Witt', 'https://www.sexmoneyart.com/'),
        'www.sexmoneyart.com': ('Sacha Witt', 'https://www.sexmoneyart.com/'),
        'signoregalilei.com': ('Signore Galilei', 'https://signoregalilei.com/'),
        'simonlermen.substack.com': ('Simon Lermen', 'https://simonlermen.substack.com/'),
        'thought37.com': ('Ruben Bloom', 'https://www.thought37.com/'),
        'www.thought37.com': ('Ruben Bloom', 'https://www.thought37.com/'),
        'tomasbjartur.bearblog.dev': ('Tomás Bjartur', 'https://tomasbjartur.bearblog.dev/'),
        'tsvibt.blogspot.com': ('Tsvi Benson-Tilsen', 'https://tsvibt.blogspot.com/'),
        'tsvibt.github.io': ('Tsvi Benson-Tilsen', 'https://tsvibt.blogspot.com/'),
        'vishalblog.substack.com': ('Vishal', 'https://vishalblog.substack.com/'),
        'www.lesswrong.com': ('LessWrong', 'https://www.lesswrong.com/'),
        'www.mutuallyassuredseduction.com': ('Mutually Assured Seduction', 'https://www.mutuallyassuredseduction.com/'),
        'x.com': ('X Post', 'https://x.com/'),
    }
    
    # Check if domain is in mapping
    if domain in author_mapping:
        return {
            'name': author_mapping[domain][0],
            'url': author_mapping[domain][1]
        }
    
    # For LessWrong and other sites, extract from domain
    if 'lesswrong.com' in domain:
        return {
            'name': 'LessWrong',
            'url': 'https://www.lesswrong.com/'
        }
    
    # For Substack blogs, extract author from subdomain
    if 'substack.com' in domain:
        subdomain = domain.split('.')[0]
        author_name = subdomain.replace('-', ' ').title()
        return {
            'name': author_name,
            'url': f'https://{domain}/'
        }
    
    # Default: use domain as author
    clean_domain = domain.replace('www.', '')
    return {
        'name': clean_domain,
        'url': f'https://{domain}/'
    }

def convert_rss_to_json_feed(xml_file, json_file):
    """Convert RSS XML feed to JSON Feed format"""
    
    # Parse XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Find channel
    channel = root.find('channel')
    
    # Create JSON Feed structure
    feed = {
        "version": "https://jsonfeed.org/version/1",
        "title": channel.find('title').text if channel.find('title') is not None else "Inkhaven Residency Publications",
        "home_page_url": channel.find('link').text if channel.find('link') is not None else "https://inkhaven.com/",
        "feed_url": "https://inkhaven.com/feed.json",
        "description": channel.find('description').text if channel.find('description') is not None else "Latest publications from Inkhaven Residency writers",
        "items": []
    }
    
    # Process each item
    items = channel.findall('item')
    print(f"Converting {len(items)} items from XML to JSON...")
    
    for item in items:
        title_elem = item.find('title')
        link_elem = item.find('link')
        guid_elem = item.find('guid')
        pub_date_elem = item.find('pubDate')
        
        # Extract data
        title = title_elem.text if title_elem is not None else "Untitled"
        url = link_elem.text if link_elem is not None else ""
        guid = guid_elem.text if guid_elem is not None else url
        pub_date = pub_date_elem.text if pub_date_elem is not None else ""
        
        # Convert pub_date to ISO format
        date_modified = pub_date  # Keep as-is for now, could parse if needed
        if pub_date:
            try:
                # Parse RSS date format: "Mon, 01 Dec 2025 00:00:00 GMT"
                dt = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
                date_modified = dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")
            except:
                pass
        
        # Extract author from URL
        author = extract_author_from_url(url)
        
        # Create item
        json_item = {
            "id": guid,
            "content_html": "",
            "url": url,
            "title": title,
            "date_modified": date_modified,
            "author": author
        }
        
        feed["items"].append(json_item)
    
    # Write JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(feed, f, indent=4, ensure_ascii=False)
    
    print(f"✓ Converted {len(feed['items'])} items")
    print(f"✓ Saved to {json_file}")

if __name__ == "__main__":
    convert_rss_to_json_feed("inkhaven_updated.xml", "inkhaven_feed.json")
    print("\n✓ Conversion complete! The database now uses inkhaven_updated.xml data.")

