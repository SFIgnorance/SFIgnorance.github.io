"""
This script sets up the 'index.html' page. Needs to be run manually and requires an internet connection. It uses
BeautifulSoup4 to parse Anchor.fm and YouTUbe to get links and populate the web page. Most content is 'static' in that
it is a pre-defined layout. 
"""
import requests
from bs4 import BeautifulSoup


# URLs
# ----------------------------------------------------------------------
anchor_fm_url = "https://anchor.fm/speaking-from-ignorance/"
youtube_url = "https://www.youtube.com/channel/UCpnEGWBnxAErZxhZqZbRgNg/videos"

# HTML static elements
# ----------------------------------------------------------------------
html_dir = "setup_html/"
static_elements_before = ['header.html', 'body_header.html', 'navbar.html', 'overview.html']
static_elements_after = ['team.html', 'contribute.html', 'faq.html', 'doc_end.html']

# Get the HTML before and after the 'podcast episodes and speakers' section, which will be populated in this script
html_before = [get_html_from_file(html_dir + path) for path in static_elements_before]
html_after = [get_html_from_file(html_dir + path) for path in static_elements_after]

# Web scraping functions
# ----------------------------------------------------------------------
def scrape_page(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def get_anchor_links():
    anchor_soup = scrape_page(anchor_fm_url)
    entry_class = "styles__episodeFeedItem___1U6E2"
    image_class = "styles__episodeImage___tMifW"
    heading_class = "styles__episodeHeading___29q7v"

    # Keep first 10 entries
    entries = anchor_soup.findAll('div', class_=entry_class)[:10]
    anchor_links = []
    anchor_headings = []

    for entry in entries:
        anchor_links.append(f"https://anchor.fm{entry.find('a', class_=image_class)['href']}")
        
        # Get the heading
        anchor_heading = entry.find('div', class_=heading_class)
        anchor_headings.append(anchor_heading.findAll('div')[-1].contents[0])


    return anchor_links, anchor_headings

# HTML construct functions
# ----------------------------------------------------------------------
def get_html_from_file(path):
    with open(path, 'r') as infile:
        html_text = ''.join(infile.readlines())

    return html_text


def setup_scrollbox():
    anchor_links, episode_titles = get_anchor_links()

    scrollbox_header = '<div class="ep-scrollbox">\n' + \
                       '\t\t<div class="ep-entry">\n' + \
                       '\t\t<div class="ep-head">\n'

    scrollbox_foo


if __name__ == "__main__":
    anchor_links, titles = get_anchor_links()