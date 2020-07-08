"""
This script sets up the 'index.html' page. Needs to be run manually and requires an internet connection. It uses
BeautifulSoup4 to parse Anchor.fm and YouTUbe to get links and populate the web page. Most content is 'static' in that
it is a pre-defined layout. 
"""
import requests
from bs4 import BeautifulSoup


# Output Options
# ----------------------------------------------------------------------
# output_html = "../index_test.html"  # Testing
output_html = "../index.html"  # Live!

# URLs
# ----------------------------------------------------------------------
anchor_fm_url = "https://anchor.fm/speaking-from-ignorance/"
youtube_url = "https://www.youtube.com/channel/UCpnEGWBnxAErZxhZqZbRgNg/videos"

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
    description_class = "styles__episodeDescription___C3oZg"

    # Keep first 10 entries
    entries = anchor_soup.findAll('div', class_=entry_class)[:10]
    anchor_links = []
    anchor_headings = []
    anchor_descriptions = []

    for entry in entries:
        anchor_links.append(f"https://anchor.fm{entry.find('a', class_=image_class)['href']}")
        
        # Get the heading
        anchor_heading = entry.find('div', class_=heading_class)
        anchor_headings.append(anchor_heading.findAll('div')[-1].contents[0])

        # Get description
        anchor_description = entry.find('div', class_=description_class)
        anchor_description = anchor_description.findAll('div')[-1].contents[0]
        anchor_descriptions.append(anchor_description)


    return anchor_links, anchor_headings, anchor_descriptions

# HTML construct functions
# ----------------------------------------------------------------------
def get_html_from_file(path):
    with open(path, 'r') as infile:
        html_text = ''.join(infile.readlines())

    return html_text


def setup_scrollbox():
    anchor_links, episode_titles, episode_descriptions = get_anchor_links()
    scrollbox = ''
    scrollbox += '        <div class="ep-scrollbox">\n'  # open scrollbox

    for i, (link, title, description) in enumerate(zip(anchor_links, episode_titles, episode_descriptions)):
        entry = ''
        
        entry += '          <div class="ep-entry">\n'  # entry header
        entry += '            <div class="ep-name">' + title + '</div>\n'  # episode name

        # Info contains, image, description, links
        entry += '            <div class="ep-info">'  # info header

        # Eventually, automatically populate images. for now, use placeholder
        entry += '              <img class="ep-img" src="images/logo/colour/Person_Colour.png">\n'  # image
        entry += '              <div class="ep-description">' + description +  '</div>\n'  # description
        entry += '              <div class="ep-links">\n'  # links header

        button_js = f'"window.open(\'{link}\', \'_blank\'); return false;"'
        entry += '                <button onclick=' + button_js + '>Audio</button>\n'  # audio link

        # Closing divs for the entries that are left open
        entry += '              </div>\n'  # close links div
        entry += '            </div>\n'  # close info div
        entry += '          </div>\n'  # close entry div

        scrollbox += entry
    
    scrollbox += '        </div>\n'  # close scrollbox

    return scrollbox


def speakers_html():
    # Setup the 'Podcast and Speakers' section
    speakers_header = get_html_from_file("setup_html/speakers_header.html")
    scrollbox = setup_scrollbox()
    speakers_footer = get_html_from_file("setup_html/speakers_footer.html")

    speakers_html = speakers_header + scrollbox + speakers_footer

    return speakers_html        


def construct_page(output_html):
    # Construct the web page and print it to 'output_html'
    page = ''.join(html_before)
    page += speakers_html()
    page += ''.join(html_after)
    with open(output_html, 'w', encoding='utf-8') as outfile:
        outfile.write(page)


if __name__ == "__main__":
    # HTML static elements
    # ----------------------------------------------------------------------
    html_dir = "setup_html/"
    static_elements_before = ['header.html', 'body_header.html', 'navbar.html', 'overview.html']
    static_elements_after = ['team.html', 'contribute.html', 'faq.html', 'doc_end.html']

    # Get the HTML before and after the 'podcast episodes and speakers' section, which will be populated in this script
    html_before = [get_html_from_file(html_dir + path) for path in static_elements_before]
    html_after = [get_html_from_file(html_dir + path) for path in static_elements_after]

    construct_page(output_html)