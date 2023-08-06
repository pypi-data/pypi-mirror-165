from kbbi_scraper import constants, utils

from functools import cached_property
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--headless")

import chromedriver_autoinstaller
chromedriver_autoinstaller.install()

class Word:
    def __init__(self, word, cache: bool=True):
        self.input_word = word
        self.url = f'{constants.SOURCE_URL}/{word}'
        self.cache = cache

    def __repr__(self):
        return self.input_word
    
    @cached_property
    def soup(self):
        bowl = utils.load_soup_bowl()
        
        if self.input_word in bowl and self.cache:
            return BeautifulSoup(bowl[self.input_word], 'html.parser')
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get(self.url)
            try:
                element = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "content")))
                soup = BeautifulSoup(element.get_attribute('innerHTML'), 'html.parser')
                self.driver.close()

                # Clean and store fetched html locally, excluding unnecessary google ads script
                if self.cache:    
                    for ads in soup.find_all('script'): ads.decompose()
                    for ads in soup.find_all('ins'): ads.decompose()
                    bowl[self.input_word] = soup.decode()
                    utils.dump_soup_bowl(bowl)

                return soup
            except TimeoutException:
                print("Failed to load web source")

    @cached_property
    def desc_section(self):
        return self.soup.find('div', {'id': 'desc'})

    @cached_property
    def word_section(self):
        return self.soup.find('div', {'id': 'desc'})

    @cached_property
    def d1_section(self):
        return self.soup.find('div', {'id': 'd1'})   

    @cached_property
    def base_word(self) -> str:
        return ''.join(self.syllables)

    @cached_property
    def word(self) -> str:
        composite_word = self.d1_section.select_one('b.mjk')
        if (composite_word and composite_word.parent == self.d1_section):
            return composite_word.next_element.text.replace('--', self.base_word).title()
        else:
            return ''.join(self.syllables)

    @cached_property
    def syllables(self) -> list:
        """
        Return a list of the word's syllable
        """

        per_suku = self.d1_section.select_one('span.per-suku')
        if per_suku and per_suku.parent == self.d1_section:
            syllable = per_suku.text.strip('/').strip('\\')
        else:
            syllable = self.d1_section.select_one('b.highlight').text.strip('/').strip('\\')

        word_number = self.d1_section.find('b').find('sup')
        if word_number and word_number.parent == self.d1_section:
            return syllable.replace(word_number, '').split('·')
        else:
            return syllable.split('·')

    @cached_property
    def meanings(self) -> list:
        """
        Return a list of meaning -> a dictionary containing
            {
                meaning: one of (if many) word's meaning,
                category: part of speech or any other category that the source decided to put,
                example: if any
            }
        """
        meanings = []
        # get all words multiple meaning if any, excluding any that are not direct child of d1_section and not in peribahasa_section
        numbers = [number for number in self.d1_section.select('b.num') if number.parent == self.d1_section and not number.find_previous('em', {'class': 'pb'})]

        def extract_meaning_and_example(meaning):
            cleaned_meaning = self._format_string(meaning.text)
            if (',' in cleaned_meaning and meaning.next_sibling == meaning.find_next_sibling('em') and meaning.next_sibling != meaning.find_next_sibling('em', {'class': 'pb'})):
                cleaned_meaning = cleaned_meaning.replace(',', '')
                cleaned_meaning += f"({meaning.find_next_sibling('em').text})"

            # Check if meaning has an example 
            if meaning.text.strip().endswith(':'):
                example = meaning.find_next('em').text.replace('--', cleaned_meaning).strip().strip(';').capitalize()
            else:
                example = None 

            return cleaned_meaning, example

        if numbers:
            for number in numbers:
                categories_symbol = self.d1_section.find_next('em', {'class': 'jk'}).text.lower().split(' ')
                default_category = [constants.CATEGORY[category] for category in categories_symbol]

                if number.text == "1":
                    categories = default_category
                    meaning = number.next_element.next_element
                else:
                    categories_symbol = number.find_next('em', {'class': 'jk'}).text.lower().split(' ')
                    categories = [constants.CATEGORY[category] for category in categories_symbol] or default_category
                    meaning = number.next_element.next_element if categories == default_category else number.find_next('em', {'class': 'jk'}).next_element.next_element

                meaning, example = extract_meaning_and_example(meaning)

                meanings.append({
                    'meaning': meaning,
                    'category': categories,
                    'example': example
                })
        else:
            categories_symbol = self.d1_section.find_next('em', {'class': 'jk'}).text.lower().split(' ')
            composite_word = self.d1_section.select_one('b.mjk')
            if (composite_word and composite_word.parent == self.d1_section):
                meaning = composite_word.next_element.next_element
            else:
                meaning = self.d1_section.select_one('em.jk').next_element.next_element

            meaning, example = extract_meaning_and_example(meaning)
                
            meanings.append({
                'meaning': meaning,
                'categories': [constants.CATEGORY[category] for category in categories_symbol],
                'example': example
            })

        return meanings
    
    # Kata turunan, kata dasar yang diberi imbuhan dll
    @cached_property
    def derived_words(self):
        derives = []
        for word in self.d1_section.select('b.tur'):
            numbers = word.find_next_siblings('b', {'class': 'num'}) or []
            syllables = word.find_next_sibling('span', {'class': 'per-suku'})

            # filter only derived word that have syllable, exclude any that doesn't have any
            if syllables.find_previous_sibling('b', {'class': 'tur'}) != word:
                continue
            
            if numbers:
                meanings = []
                for number in numbers:
                    categories_symbol = self.d1_section.find_next('em', {'class': 'jk'}).text.lower().split(' ')
                    default_category = [constants.CATEGORY[category] for category in categories_symbol]
                    
                    if number.find_previous('b', {'class': 'tur'}) != word:
                        continue

                    if number.text == "1":
                        categories = default_category
                        meaning = number.next_element.next_element
                    else:
                        categories_symbol = number.find_next('em', {'class': 'jk'}).text.lower().split(' ')
                        categories = [constants.CATEGORY[category] for category in categories_symbol] or default_category
                        meaning = number.next_element.next_element if categories == default_category else number.find_next('em', {'class': 'jk'}).next_element.next_element

                    if meaning.text.strip().endswith(':'):
                        example = meaning.next_element.next_element.text.replace('~', word.text).strip().strip(';').capitalize()
                    else:
                        example = None

                    meanings.append({
                        'meaning': self._format_string(meaning.text),
                        'categories': categories,
                        'example': example
                    })
                
                derives.append({
                    'word': word.text.title(),
                    'syllables': syllables.text.strip('\\').strip('/').split('·'),
                    'meanings': meanings
                })
            else:
                categories_symbol = word.find_next_sibling('em', {'class': 'jk'}).text.lower().split(' ')
                meaning = word.find_next_sibling('em', {'class': 'jk'}).next_element.next_element

                if meaning.text.strip().endswith(':'):
                    example = meaning.next_element.next_element.text.replace('~', word.text).strip().strip(';').capitalize()
                else:
                    example = None

                derives.append({
                    'word': word.text.title(),
                    'syllables': syllables.text.strip('\\').strip('/').split('·'),
                    'meanings': [{
                        'meaning': self._format_string(meaning.text),
                        'categories': [constants.CATEGORY[category] for category in categories_symbol],
                        'example': example
                    }]
                })
        return derives
    
    @cached_property
    def related_words(self):
        related_words = []

        for related_word in self.soup.select_one('div#word div#w1 ul#u1').find_all('li'):
            link = related_word.find_next('a')
            if 'cur' in link['class']:
                continue

            related_words.append(Word(link.get('href').lstrip('./')))

        for related_word in self.soup.select_one('div#word div#w2 ul#u2').find_all('li'):
            related_words.append(Word(related_word.find_next('a').get('href').lstrip('./')))

        return related_words

    @cached_property
    def proverbs(self) -> list:
        proverbs = []
        # Cari tag em dengan class pb untuk pribahasa
        for pb in self.d1_section.select("em.pb"):
            mean = []
            pb_text = ''
            # looping jika next element adalah tag b dengan class num, itu berarti pribahasa memiliki lebih dari 1 arti
            if 'class' in pb.next_sibling.next_sibling.attrs and 'num' in pb.next_sibling.next_sibling['class']:
                for num in pb.find_all_next('b', {'class': 'num'}):
                    mean.append(self._format_string(num.next_sibling))
            
            if not len(mean):
                mean.append(self._format_string(pb.next_sibling).split(';')[0])

            if '--' in pb.previous_sibling:
                previous_pb = [ex for ex in (pb.previous_sibling.split(';') if ':' not in pb.previous_sibling else pb.previous_sibling.split(':')) if '--' in ex][0]
                pb_text = f'{previous_pb} {pb.text}'

            if not pb_text:
                pb_text = pb.text

            proverbs.append(
                {
                    'meaning': mean,
                    'proverb': [ex for ex in self._format_proverb(pb_text).split(';') if self.word in ex ][0]
                }
            )

        return proverbs

    def _format_proverb(self, string) -> str:
        return string.strip().replace('--', self.word).replace('  ', ' ').replace(', pb', '')

    def _format_string(self, string) -> str:
        return string.strip().strip(';').strip(':').strip(': --').capitalize()
            
    def _is_already_in_bowl(self) -> bool:
        return self.input_word in utils.load_soup_bowl()