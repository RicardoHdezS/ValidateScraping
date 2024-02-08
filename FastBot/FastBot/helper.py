import dateparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import copy
import time
import re
import random

def get_content_xpath(response, selector, web_note_content = False, web_note_attr_titles = None, web_note_remove_elements = None):
    try:
        if web_note_content:
            if ' ? ' in selector:
                xpath, css = re.split(r'\s*\?\s*', selector, maxsplit=1)

                content = get_content_css(
                    response=response.text,
                    selector=css,
                    headers=web_note_attr_titles,
                    remove_tags=web_note_remove_elements
                )

                if content == '':
                    content = get_content_xpath(response, xpath)
                    return content
                else:
                    return content
            else:
                return ' '.join(response.xpath(selector).getall())
        return ' '.join(response.xpath(selector).getall())
        # return response.xpath(selector).get(default = '').strip().encode('utf-16', 'surrogatepass').decode('utf-16')
    except Exception:
        return ''

def get_content_css(response, selector, restricted = '', headers = 'h', remove_tags = '', wraps = True, selective = True, c_print = False):
    tw_script ='<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
    # insta_script = '<script async src="//www.instagram.com/embed.js"></script>'
    soup = BeautifulSoup(response, 'lxml')
    if remove_tags:
        for remove in soup.select(remove_tags):
            remove.decompose()
    content_note, WIDGET = [], []
    if selective:
        for step_1 in soup.select(selector):
            if wraps:
                scrolling = step_1.descendants
            else:
                scrolling = step_1.next_elements
            for step_2 in scrolling:
                # print('1', step_2) input() print('2', step_2.name) input()
                if not step_2 or not step_2.name: # For None
                    continue
                elif str(step_2.name) in headers:
                    content_note.append('-' + step_2.get_text().encode('utf-16', 'surrogatepass').decode('utf-16'))
                elif str(step_2.name) == 'li':
                    content_note.append('. ' + step_2.get_text().encode('utf-16', 'surrogatepass').decode('utf-16'))
                elif step_2.name == 'p' and not step_2.select('p'):
                    # Algunas págs no estan bien parseadas (algún error en el html)
                    # hay una parte del contenido que esta dentro de un tag <p> el cual hace que se repita parte del texto
                    content_note.append(step_2.get_text().encode('utf-16', 'surrogatepass').decode('utf-16'))
    else:
        content_note = [p.get_text() for p in soup.select(selector) if p.get_text(strip=True)]
    del soup

    content_note = [p.strip() for p in content_note if p.strip() and not any(word in p.strip().lower() for word in restricted)]
    content_note = remove_duplicates(content_note)

    if c_print:
        print(*content_note, sep='\n')
    return '\n'.join(content_note)

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output

def parse_format_date(response, publish_date, modified_date, UTC, JSON, STR, str_format):

    settings = {
        'TO_TIMEZONE': 'America/Mexico_City',
        'RETURN_AS_TIMEZONE_AWARE': False
    }
    languages = ['es']
    date_formats = [str_format]

    if JSON:
        print("Proceso para que sea JSON")
    else:
        if UTC:
            settings['TIMEZONE'] = 'UTC'

        if publish_date is None:
            print("Error al obtener el contenido xpath")
            return False, publish_date, modified_date
        else:
            if STR:

                publish_parsed = parse_text_date(publish_date, str_format, settings)
                modified_parsed = parse_text_date(modified_date, str_format, settings)

                if publish_parsed:
                    return True, publish_parsed.strftime("%Y-%m-%dT%H:%M:%SZ"), modified_parsed.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    print("Error al analizar fechas en formato de texto")
                    return False, publish_date, modified_date
            else:
                publish_parsed, modified_parsed = dateparser.parse(publish_date, settings=settings), dateparser.parse(modified_date, settings=settings)
                valid = validate_date(publish_parsed)
                if valid:
                    return True, publish_parsed.strftime("%Y-%m-%dT%H:%M:%SZ"), modified_parsed.strftime("%Y-%m-%dT%H:%M:%SZ")
                else:
                    return False, publish_parsed.strftime("%Y-%m-%dT%H:%M:%SZ"), modified_parsed.strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_text_date(text_date, str_format, settings):

    parsed_date = dateparser.parse(text_date, languages=['es'])

    if parsed_date:
        return parsed_date

    regex_formats = [r'\b(\d{1,2}/\d{1,2}/\d{4})\b']

    for regex_format in regex_formats:
        match = re.search(regex_format, text_date)
        if match:
            detected_date = match.group(1)
            parsed_date = dateparser.parse(detected_date, date_formats=[str_format], settings=settings)
            if parsed_date:
                return parsed_date

    return None

def validate_date(web_note_date):

    min_available_range = datetime.now() - timedelta(days=1)
    min_available_range = min_available_range.replace(hour=0, minute=0, second=0, microsecond=0)
    max_available_range = datetime.combine(datetime.now(), datetime.max.time())

    if min_available_range <= web_note_date <= max_available_range:
        return True
    else:
        return False