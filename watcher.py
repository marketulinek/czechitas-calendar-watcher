from bs4 import BeautifulSoup
import requests


TARGET_URL = 'https://www.czechitas.cz/kalendar'

TABLE_HEAD = ' '.join('CZECHITAS KALENDÁŘ')
TABLE_WIDTH = 98
HORIZONTAL_BORDER = '-' * TABLE_WIDTH


def get_event_title(event):
    try:
        return event.find('a', {'class': 'event-title'}).get_text()
    except AttributeError:
        return '?'


def get_event_city(event):
    try:
        return event.find('h2', {'class': 'm-sto'}).get_text()
    except AttributeError:
        return '?'


def get_event_date(event):
    event_date = ''
    date_tags = event.find_all('div', {'class': 'event-date-title'})
    for date in date_tags:
        if 'w-condition-invisible' not in date.attrs['class']:
            event_date += date.get_text()
    return event_date.replace('a', ', ')


def get_events(event_tags):
    events = []
    for tag in event_tags:
        events.append({
            'title': get_event_title(tag),
            'city': get_event_city(tag),
            'date': get_event_date(tag)
        })
    return events


def get_next_page_url(content):
    try:
        return TARGET_URL + content.find('a',
                                         {'aria-label': 'Next Page'}
                                         ).attrs['href']
    except AttributeError:
        # Next page does not exist.
        return None
    except KeyError:
        # Attribute "href" of next page element was not found
        print('Nastala chyba při přechodu na další stránku.')
        return None


def show_data(events):

    print(HORIZONTAL_BORDER)
    print(f"|{TABLE_HEAD.center(TABLE_WIDTH-2)}|")
    print(HORIZONTAL_BORDER)

    if len(events) > 1:
        for event in events:
            print(
                f"| {event['date']:>17} ",
                f"| {event['city']:>16} ",
                f"| {event['title']:<55} |",
                sep=''
            )
    else:
        print(f"|{''.center(TABLE_WIDTH-2)}|")
        print(f"|{'Nenalezeny žádné události :-('.center(TABLE_WIDTH-2)}|")
        print(f"|{''.center(TABLE_WIDTH-2)}|")

    print(HORIZONTAL_BORDER)


def watch():

    url = TARGET_URL
    events = []

    # Scrape the first 15 pages
    for i in range(1, 15):

        response = requests.get(url)
        response.raise_for_status()

        content = BeautifulSoup(response.content, 'html.parser')

        event_tags = content.find_all('div', {'class': 'collection-item'})
        if len(event_tags) < 1:
            break

        events = events + get_events(event_tags)

        url = get_next_page_url(content)
        if url is None:
            break
    else:
        print('Nalezeno více než 15 stránek.'
              ' Je to nepravděpodobné, může se jednat o chybu.')

    show_data(events)


if __name__ == "__main__":
    watch()
    input('Dej enter pro ukončení...')
