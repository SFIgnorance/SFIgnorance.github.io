"""
This script sets up the 'index.html' page. Needs to be run manually and requires an internet connection. It uses
BeautifulSoup4 to parse Anchor.fm and YouTUbe to get links and populate the web page. Most content is 'static' in that
it is a pre-defined layout. 
"""
import requests
import bs4
from bs4 import BeautifulSoup
import podcastparser
import urllib
import os.path


# Output Options
# ----------------------------------------------------------------------
# output_html = "../index_test.html"  # Testing
output_html = "../index.html"  # Live!

# URLs
# ----------------------------------------------------------------------
anchor_fm_url = "https://anchor.fm/speaking-from-ignorance/"
anchor_fm_rss = "https://anchor.fm/s/1f3b1374/podcast/rss"
youtube_url = "https://www.youtube.com/channel/UCpnEGWBnxAErZxhZqZbRgNg/videos"

# String formatting functions
# ----------------------------------------------------------------------
def format_description(description_html):
    # Remove newline 'p'
    soup = BeautifulSoup(description_html, 'html.parser')
    paragraphs = soup.findAll('p')
    descriptions = []

    for paragraph in paragraphs:
        try:
            # print(paragraph.contents)
            if (paragraph.contents[0].startswith("Music")):
                break
        except TypeError:
            print("Skipping newline character")
            continue

        description = [str(content) for content in paragraph.contents]
        descriptions.append(''.join(description))

    return '<br>'.join(descriptions)

# Local file functions
# ----------------------------------------------------------------------
def get_speaker_image(episode_index, total_episodes):
    images_directory = "images/speakers/"
    # Naming scheme is 'ep_EpisodeNumber'
    # Episode index is index counting backwards from ten latest episodes
    episode_number = total_episodes - episode_index
    episode_image = f'\"{images_directory}ep{episode_number}.png\"'
    python_path = '../' + episode_image.replace('"', '')

    # We have to check if the path exists from Python script location
    # but return path from
    if os.path.exists(python_path):
        return episode_image
    else:
        return f'\"images/logo/colour/Person_Colour.png\"'

    return episode_image
    
# Web scraping functions
# ----------------------------------------------------------------------

# BeautifulSoup version (HTML) (UNUSED)
def scrape_page(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, 'html.parser')


def get_anchor_links_html():
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


# Podcast parser version (RSS)
def get_anchor_links_rss(newest=False):
    parsed = podcastparser.parse(anchor_fm_rss, urllib.request.urlopen(anchor_fm_rss))
    total_episodes = len(parsed['episodes'])

    if newest:  # just get the newest episode
        return parsed['episodes'][0], total_episodes

    episodes = parsed['episodes'][:10]
    anchor_links = []
    anchor_titles = []
    anchor_descriptions = []

    for episode in episodes:
        anchor_links.append(episode['link'])
        anchor_titles.append(episode['title'])
        anchor_descriptions.append(format_description(episode['description_html']))
   
    return anchor_links, anchor_titles, anchor_descriptions, total_episodes

# HTML construct functions
# ----------------------------------------------------------------------
def get_html_from_file(path):
    with open(path, 'r') as infile:
        html_text = ''.join(infile.readlines())

    return html_text


def setup_scrollbox():
    anchor_links, episode_titles, episode_descriptions, num_episodes = get_anchor_links_rss()
    scrollbox = ''
    scrollbox += '        <div class="ep-scrollbox">\n'  # open scrollbox

    for i, (link, title, description) in enumerate(zip(anchor_links, episode_titles, episode_descriptions)):
        entry = ''
        
        entry += '          <div class="ep-entry">\n'  # entry header
        entry += '            <div class="ep-name">' + title + '</div>\n'  # episode name

        # Info contains, image, description, links
        entry += '            <div class="ep-info">\n'  # info header

        # Eventually, automatically populate images. for now, use placeholder
        entry += f'              <img class="ep-img" src={get_speaker_image(i, num_episodes)}>\n'  # image
        entry += '              <div class="ep-description"><p>' + description +  '</p></div>\n'  # description
        entry += '              <div class="ep-links">\n'  # links header

        button_js = f'"openLink(\'{link}\');"'
        entry += '                <button onclick=' + button_js + '>Audio</button>\n'  # audio link
        entry += '                <button onclick=' + button_js + '>Video</button>\n'  # video link

        # Closing divs for the entries that are left open
        entry += '              </div>\n'  # close links div
        entry += '            </div>\n'  # close info div
        entry += '          </div>\n'  # close entry div

        scrollbox += entry
    
    scrollbox += '        </div>\n'  # close scrollbox

    return scrollbox


def newest_episode_html():
    episode, num_episodes = get_anchor_links_rss(newest=True)
    title, description, link = episode['title'], episode['description_html'], episode['link']

    episode_html = '\n'
    episode_html += f'          <div class="ep-newest">\n'
    episode_html += f'            <div class="ep-name">{title}</div>\n'
    episode_html += f'            <div class="ep-info">\n'
    episode_html += f'              <img class="ep-img" src={get_speaker_image(0, num_episodes)}>\n'
    episode_html += f'              <div class="ep-description"><p>{format_description(description)}</p></div>\n'
    episode_html += f'              <div class="ep-links">\n'
    button_js = f'"openLink(\'{link}\');"'
    episode_html += f'                <button onclick={button_js}>Audio</button>\n'
    episode_html += f'                <button onclick={button_js}>Video</button>\n'
    episode_html += f'              </div>\n'
    episode_html += f'            </div>\n'
    episode_html += f'          </div>\n'

    return episode_html


def overview_html():
    # Setup 'overview' section
    overview_html = ''
    overview_html += get_html_from_file("setup_html/overview_header.html")

    # Add newest episode
    overview_html += newest_episode_html()

    overview_html += get_html_from_file("setup_html/overview_footer.html")

    return overview_html

def speakers_html():
    # Setup the 'Podcast and Speakers' section
    speakers_html = ''
    speakers_html += get_html_from_file("setup_html/speakers_header.html")  # left side header
    speakers_html += setup_scrollbox()  # scrollbox of episode
    speakers_html += get_html_from_file("setup_html/speakers_footer.html")  # footer

    return speakers_html        


def construct_page(output_html):
    # Construct the web page and print it to 'output_html'
    page = ''.join(html_before)
    page += overview_html()
    page += speakers_html()
    page += ''.join(html_after)
    with open(output_html, 'w', encoding='utf-8') as outfile:
        outfile.write(page)


if __name__ == "__main__":
    # HTML static elements
    # ----------------------------------------------------------------------
    html_dir = "setup_html/"
    static_elements_before = ['header.html', 'body_header.html']
    static_elements_after = ['team.html', 'doc_end.html']

    # Get the HTML before and after the 'podcast episodes and speakers' section, which will be populated in this script
    html_before = [get_html_from_file(html_dir + path) for path in static_elements_before]
    html_after = [get_html_from_file(html_dir + path) for path in static_elements_after]

    construct_page(output_html)
