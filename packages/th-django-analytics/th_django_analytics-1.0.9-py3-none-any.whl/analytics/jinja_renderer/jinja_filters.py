import re
import ast
import base64
import hashlib
import json
import logging
from copy import deepcopy
from datetime import datetime, timedelta
from enum import Enum
from io import BytesIO
from string import punctuation
from colour import Color, color_scale
import pandas as pd
import dateutil.parser
import requests
from Levenshtein import ratio
from dateparser import parse
from decouple import config
from lxml.html import fromstring
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from unidecode import unidecode

from django.db.models.manager import Manager

logger = logging.getLogger("analytics")

month_translate = {
    "january": [
        "janeiro",
        "jan",
    ],
    "february": [
        "fevereiro",
        "fev",
    ],
    "march": [
        "março",
        "mar",
    ],
    "april": [
        "abril",
        "abr",
    ],
    "may": [
        "maio",
        "mai",
    ],
    "june": [
        "junho",
        "jun",
    ],
    "july": [
        "julho",
        "jul",
    ],
    "august": [
        "agosto",
        "ago",
    ],
    "september": [
        "setembro",
        "set",
    ],
    "october": [
        "outubro",
        "out",
    ],
    "november": [
        "novembro",
        "nov",
    ],
    "december": [
        "dezembro",
        "dez",
    ],
}


def is_list(x):
    """Check if a string is a list"""

    return isinstance(x, list)


def is_dict(x):
    """Check if a string is a dictionary"""

    return isinstance(x, dict)


def is_tuple(x):
    """Check if a string is a tuple"""

    return isinstance(x, tuple)


def is_str(x):
    """Check if a string is a string"""

    return isinstance(x, str)


def is_int(x):
    """Check if a string is an integer"""

    return type(x) is int


def is_float(x):
    """Check if a string is a float"""

    return isinstance(x, float)


def is_bool(x):
    """Check if a string is a boolean"""

    return isinstance(x, bool)


def value(dictionary):
    """Get the 'value' of a dictionary"""

    if isinstance(dictionary["value"], str):
        return dictionary["value"]
    elif isinstance(dictionary["value"], list):
        return dictionary["value"][-1]


def is_base64(x):
    """Validate if a string is base64"""

    try:
        if isinstance(x, bytes):
            x = x.decode()
        elif isinstance(x, str) and x.startswith("b'"):
            x = ast.literal_eval(x).decode()
        if base64.b64encode(base64.b64decode(x)).decode() == str(x):
            return True
        return False
    except:
        return False


def to_base64(x):
    """Convert a string into base64"""

    try:
        if is_base64(x):
            if isinstance(x, bytes):
                return x.decode()
            elif isinstance(x, str) and x.startswith("b'"):
                return ast.literal_eval(x).decode()
        else:
            if isinstance(x, bytes):
                return base64.b64encode(x).decode()
            elif isinstance(x, str):
                return base64.b64encode(x.encode()).decode()
    except:
        return None


def clean_string(text):
    text = str(text)
    text = "".join([word for word in text if word not in punctuation])
    text = text.lower()
    text = " ".join([word for word in text.split() if word != ""])
    return text.strip()


def normalize_string(text):
    """Normalize a string"""

    return unidecode(clean_string(text))


def validate_email(text):
    """Validate an email"""

    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    extracted = re.findall(pattern=pattern, string=text)
    if len(extracted) > 0:
        return extracted[0]
    return None


def cosine_sim_value(original, reference):
    """Compute cosine similarity between samples in X and Y"""

    original = unidecode(clean_string(original))
    reference = unidecode(clean_string(reference))
    vectorizer = CountVectorizer().fit_transform([original, reference])
    vectors = vectorizer.toarray()
    vector_original = vectors[0].reshape(1, -1)
    vector_reference = vectors[1].reshape(1, -1)
    csim = cosine_similarity(vector_original, vector_reference)[0][0]
    return csim


def cosine_sim(original, reference, threshold):
    """Compute cosine similarity between samples in X and Y using a threshold"""

    csim = cosine_sim_value(original, reference)
    if csim >= threshold:
        return True
    return False


def levenshtein_sim(query: str, data: str) -> float:
    """
    Matching values by levenshtein ratio in ordered parts of the querys
    query :  value to be matched against the reference value
    data  :  reference value to be matched against the query
    Warning : This filter is not commutative.
        - levenshtein(A,B) != levenshtein(B,A)
    """

    def short_query_sim(input_query: str, input_data: str) -> float:
        """
        If the query term is short (one word, few characters),
        we do a comparison with each word of the exam, focusing on the first letters,
        and choose the max value found
        """
        options = input_data.strip().split(" ")
        sim_value = max(
            [
                ratio(input_query, opt) * 3 / (3 + i)
                for i, opt in enumerate(options)
            ]
        )
        # sim_value = ratio(input_query, input_data)
        return sim_value

    def long_query_sim(input_query: str, input_data: str) -> float:
        """
        If the query is long (multiple words, more characters),
        we return the sum of matches from the words of the query to the key
        we get sum(max(ratio(query_word, key_word))) for every query/key word pair
        and normalize the value
        """
        q_options = input_query.split(" ")
        k_options = input_data.strip().split(" ")
        ls_value1 = sum(
            [max([ratio(q, k) for k in k_options]) for q in q_options]
        ) / len(q_options)
        ls_value2 = sum(
            [max([ratio(q, k) for q in q_options]) for k in k_options]
        ) / len(k_options)
        return max(ls_value1, ls_value2)

    query = normalize_string(query)
    data = normalize_string(data)
    if (len(query) < 5) or (len(query.split(" ")) == 1):
        levenshtein_value = short_query_sim(query, data)
    else:
        levenshtein_value = long_query_sim(query, data)
    return levenshtein_value


def add_day_weekday(day):
    """Add day to a date and return the weekday"""

    obj = datetime.strptime(day, "%Y-%m-%d")
    options = [obj + timedelta(days=i) for i in range(6)]
    options = [i for i in options if i.weekday() not in [5, 6]]
    return [i.strftime("%Y-%m-%d") for i in options]


def delta_time(day, interval, type):
    """This filter is used to add a arbitrary timedelta into a date object
    interval : the period to be added into the date (positive or negative)
    type     : the type of period (day, month, year)
    """
    if isinstance(day, str):
        day = datetime.strptime(day, "%Y-%m-%d")
    return (day + timedelta(**{type: interval})).strftime("%Y-%m-%d")


def subtract_day_weekday(day):
    """Subtract a arbitrary timedelta from a date object"""

    obj = datetime.strptime(day, "%Y-%m-%d")
    options = [obj - timedelta(days=7) + timedelta(days=i) for i in range(7)]
    options = [i for i in options if i.weekday() not in [5, 6]]
    return [i.strftime("%Y-%m-%d") for i in options]


def clip_day_tomorrow(day):
    """Clips a datetime objeto to be at least tomorrow
    This is used to avoid user entry to be in the past
    """

    obj = datetime.strptime(day, "%Y-%m-%d")
    if (datetime.now() + timedelta(days=1)) > obj:
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        return day


def format_date(value, output_format="%Y-%m-%d", input_format="%Y-%m-%d"):
    """Format a date object, given the specified input and output formats"""

    date = datetime.strptime(value, input_format)
    return date.strftime(output_format)


def format_time(value, output_format="%H:%M:%S", input_format="%H:%M:%S"):
    """Format a time object, given the specified input and output formats"""

    time = datetime.strptime(value, input_format)
    return time.strftime(output_format)


def format_datetime(
    value, output_format="%Y-%m-%d %H:%M:%S", input_format="%Y-%m-%d %H:%M:%S"
):
    """Format a datetime object, given the specified input and output formats"""

    time = datetime.strptime(value, input_format)
    return time.strftime(output_format)


def get_obj_by(lst, field, value_):
    """Get an object from a list of objects, given a field and a value"""

    if not is_list(lst):
        lst = json.loads(lst)
    for obj in lst:
        if obj.get(field, None) == value_:
            return obj
    return dict()


def convert_date(date_str: str, fmt: str):
    """Convert a date string to another format"""

    try:
        fmt_dict = {"br": "%d/%m/%Y", "us": "%Y-%m-%d"}
        fmt = fmt_dict.get(fmt, fmt)
        date_obj = extract_date(date_str)
        date_str = date_obj.strftime(fmt)
        return date_str
    except:
        return date_str


def get_urls_from_html(html: str, url_prefix=None):
    """Extract all the urls from a html string"""

    tag_search = ".//a"
    if url_prefix is not None:
        if url_prefix.endswith("/"):
            url_prefix = url_prefix[:-1]
        if "google" in url_prefix:
            tag_search = './/a[contains(@href, "/url?q=")]'
        else:
            tag_search = ".//h2//a"
    links = list()

    root = fromstring(html)

    for element in root.xpath(tag_search):
        url = element.attrib["href"]
        if url.startswith("/") and url_prefix:
            links.append([element.text_content(), url_prefix + url])
        else:
            links.append([element.text_content(), url])
    return links


def validate_is_in_dict(
    user_input, dictionary, additional=None, threshold=0.9
):
    """Validate if a user input is in a dictionary"""

    if dictionary is None:
        return None
    results = dict()
    possibilities = deepcopy(dictionary)
    if additional:
        possibilities.update(additional)
    for possibility in possibilities:
        try:
            results.update(
                {
                    possibility: cosine_sim_value(
                        str(possibility), str(user_input)
                    )
                }
            )
        except Exception as exc:
            print(
                "Error while processing cosine sim value at [validate_is_in_dict]."
                f"Got error {exc} with arguments (original={possibility}, reference={user_input})"
            )
            x = normalize_string(str(possibility))
            y = normalize_string(str(user_input))
            if x in y or y in x:
                results.update({possibility: 1})
            else:
                results.update({possibility: 0})
    ordered = sorted(results, key=results.get, reverse=True)
    if len(ordered) > 0:
        if results[ordered[0]] >= threshold:
            return possibilities[ordered[0]]

    search_item = unidecode(clean_string(user_input))
    possibilities_list = [
        unidecode(clean_string(i)) for i in possibilities.keys()
    ]
    for possibility in zip(possibilities_list, possibilities.keys()):
        search_list = possibilities_list
        search_list.remove(possibility[0])
        if search_item in possibility[0] and search_item not in search_list:
            return possibilities[possibility[1]]

    dict_position = {
        "primeir": 0,
        "segund": 1,
        "treceir": 2,
        "quart": 3,
        "quint": 4,
        "ultim": -1,
        "penultim": -2,
    }
    for position, index in dict_position.items():
        if position in search_item:
            return dictionary[list(dictionary.keys())[index]]

    return None


class ListTypes(Enum):
    SUGGESTIONS = 0
    OPTIONS = 1


def validate_is_in_list(
    user_input,
    items,
    has_enumerator,
    threshold=0.7,
    list_type: ListTypes = ListTypes.SUGGESTIONS,
):
    """
    Find the best match between the "user_input" and the multiple options in "items"
    The comparison can be done in different ways, depending on the type of items given (suggestion, options)
        items : the objects to be compared with the user input.
                can be defined in the following ways
                list[str], list[dict],
    The values retrieved from the items are:
        item_index : value to use to compare the enumerator similarity
        item_name  : value to be used to compare the query similarity
        item_value : value to be returned for the option
    """
    if len(items) == 0:
        logger.error(
            f"List of options does not have any items. Could not find a match for this case."
            f"Error while processing user_input={user_input} and items={items}"
        )
        return None
    results = list()
    for i, item in enumerate(items):
        if list_type == ListTypes.SUGGESTIONS:
            item_index = i + 1
            value = item if type(items) == list else item.value
            item_name = value
            item_value = value
        elif list_type == ListTypes.OPTIONS:
            item_index = item.get("index", None)
            item_name = item.get("name")
            item_value = item.get("value")
        else:
            logger.error(
                f"Similarity type {list_type} not recognized. Could not extract item name and value"
            )
            return None

        try:
            # First we check if the user input is exactly equal to the item value (with or without enumeration)
            if has_enumerator and (
                user_input == f"{item_index} - {item_name}"
            ):
                similarity = 1
            elif not has_enumerator and (user_input == f"{item_name}"):
                similarity = 1
            else:
                similarity = levenshtein_sim(user_input, item_name)
        except Exception as exc:
            logger.error(
                "Error while processing cosine sim value at [validate_is_in_list]."
                f"Got error {exc} with arguments (original={user_input}, reference={item_name})"
            )
            x = normalize_string(item_name)
            y = normalize_string(user_input)
            if x == y:
                similarity = 1
            elif (not has_enumerator) and (x in y or y in x):
                similarity = 1
            else:
                similarity = 0

        if has_enumerator:
            if normalize_string(user_input) == str(item_index):
                enumeration_sim = 1
            else:
                enumeration_sim = 0
            similarity = max(similarity, enumeration_sim)

        results.append((similarity, item_value))

    logger.info(
        f'validate_is_in_list results with user input "{user_input}": {results}'
    )
    results.sort(reverse=True, key=lambda r: r[0])

    # If we have at least two items in the list, and they have the same score, we return a 'undecided' result
    if len(results) >= 2:
        if results[0][0] == results[1][0]:
            logger.info(
                f"User input matched two list options. Could not decide between items."
                f"Error with results={results} and user inputs={user_input}"
            )
            return None
    if results[0][0] >= threshold:
        logger.info(
            f"Similaridade {results[0][0]} >= threshold {threshold}. Retornando {results[0][1]}"
        )
        return results[0][1]
    else:
        logger.info(
            f"No results matched on validate_is_in_list."
            f" No result in {results} has a threshold greater than {threshold}"
        )
        return None


def validate_is_in_suggestions(
    user_input, suggestions, has_enumerator, threshold=0.7
):
    """Validate if the user input is in the list of suggestions."""
    return validate_is_in_list(
        user_input,
        suggestions,
        has_enumerator,
        threshold,
        list_type=ListTypes.SUGGESTIONS,
    )


def validate_is_in_options(
    user_input, options, has_enumerator, threshold=0.7
):
    """Validate if the user input is in the list of options."""
    return validate_is_in_list(
        user_input,
        options,
        has_enumerator,
        threshold,
        list_type=ListTypes.OPTIONS,
    )


def extract_date(user_input: str):
    """Extracts the date from a string."""

    d = re.sub(r"\sd[e|o|a]\s", " ", user_input).strip()
    d = re.sub(r"^.*?(\d)", r"\1", d)
    year_month_day = validate_regex(d, r"\d{4}.\d{2}.\d{2}")
    if year_month_day is not None:
        return dateutil.parser.parse(year_month_day)
    return parse(d, settings={"STRICT_PARSING": True, "DATE_ORDER": "DMY"})


def find_date_input(user_input: str, dates: list, optionals=None):
    """Finds the date in the list of dates."""

    user_input = user_input.strip()
    opt_lst = None
    if isinstance(optionals, list):
        opt_lst = validate_is_in_suggestions(
            user_input, optionals, False, 0.5
        )
    elif isinstance(optionals, dict):
        opt_lst = validate_is_in_dict(user_input, optionals, {}, 0.5)
    if opt_lst:
        return opt_lst

    dates_obj = [extract_date(i) for i in dates]

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if "depois" in normalize_string(
        user_input
    ) and "amanha" in normalize_string(user_input):
        date_obj = today + timedelta(days=2)
        if date_obj in dates_obj:
            return date_obj
        return None
    elif "amanha" in normalize_string(user_input):
        date_obj = today + timedelta(days=1)
        if date_obj in dates_obj:
            return date_obj
        return None
    elif "hoje" in normalize_string(user_input):
        date_obj = today
        if date_obj in dates_obj:
            return date_obj
        return None

    date_obj = extract_date(user_input)
    if date_obj in dates_obj:
        return date_obj

    day = re.findall(r"\d{1,2}", user_input)
    if len(day) > 0:
        for date_obj in dates_obj:
            if int(date_obj.day) == int(day[0]):
                return date_obj
    return None


def regex(user_input, pattern):
    """Returns the first match of the regex pattern in the user input"""

    result = re.findall(user_input, pattern)
    return result


def validate_regex(user_input, pattern):
    """Validates if the user input matches the regex pattern."""

    result = re.findall(pattern, user_input)
    if len(result):
        return result[0]
    return None


def findall_regex(user_input, pattern):
    """Find all matches in a string using regex."""

    return re.findall(pattern, user_input)


def join(items: list, separator: str):
    """Join a list of items with a separator."""

    return separator.join(items)


def split(string: str, separator: str = " "):
    """Splits a string into a list of strings, using the separator as a delimiter."""

    return string.split(separator)


def validate_cpf(cpf: str):
    """Validate CPF number length and digits"""

    cpf = "".join(re.findall(r"\d+", cpf))
    if len(cpf) == 11:
        return cpf
    return None


def validate_cpf_number(numbers: str):
    """Validates a CPF number."""

    cpf = [int(char) for char in numbers if char.isdigit()]
    # Length validation
    if len(cpf) != 11:
        return False
    # Validation to CPF that has all the same numbers, ex: 111.111.111-11
    if cpf == cpf[::-1]:
        return False
    # Validates the two check digits
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return None
    return "".join([str(int) for int in cpf])


def extract_phone(string: str):
    """Extracts a phone number from a string."""

    string = "".join(re.findall(r"\d+", string)).lstrip("0")

    if len(string) == 10:
        return [string[:2], "9" + string[2:]]
    if len(string) == 11:
        return [string[:2], string[2:]]
    if len(string) == 12:
        return [string[2:4], "9" + string[4:]]
    if len(string) == 13:
        return [string[2:4], string[4:]]

    return None


def synonymous(user_input):
    """Returns a list of synonymous words for a given word."""

    return user_input


def shorten_url(url):
    """Shortens a URL."""

    if isinstance(url, str):
        try:
            resp = requests.post(
                config("PRIMESERVICE_URL") + "/utils/urlShortener/",
                json={"urls": [url]},
            )
            try:
                list_urls = resp.json()
            except:
                list_urls = json.loads(resp.content)
            return list_urls[0]
        except:
            return url
    else:
        try:
            resp = requests.post(
                config("PRIMESERVICE_URL") + "/utils/urlShortener/",
                json={"urls": url},
            )
            try:
                list_urls = resp.json()
            except:
                list_urls = json.loads(resp.content)
            return list_urls
        except:
            return url


# deprecated
def image_to_base64(data: str) -> str:
    """Convert a image to base64 by checking its signature."""

    try:
        data: dict = eval(data)
        response = requests.get(data["file"])
        buffer = BytesIO(response.content)
        sha256 = hashlib.sha256()
        for block in iter(lambda: buffer.read(4096), b""):
            sha256.update(block)
        if sha256.hexdigest() == data["sha256"]:
            return base64.b64encode(response.content).decode("utf-8")
        return ""
    except BaseException as e:
        return ""


# deprecated
def image_from_url_to_base64(url: str) -> str:
    """Convert a image to base64."""

    try:
        response = requests.get(url)
        return base64.b64encode(response.content).decode("utf-8")
    except BaseException as e:
        return ""


def protect_email(email: str):
    """protects an email address by hiding information."""

    username, domain = email.split("@")
    username = username[:3] + "".join(map(lambda c: "_", username[3:]))

    domain = domain.split(".")
    domain = (
        domain[0][:2]
        + "".join(map(lambda c: "_", domain[0][2:]))
        + "."
        + domain[1]
    )

    return username + "@" + domain


def check_substrings(string: str, *args):
    """Check if a string contains any of the substrings."""

    for sub in args:
        if not re.search(sub, string):
            return False
    return True


def get_gradient_color_pallete(
    color_a: str, color_b: str, range: int = 1
) -> list:
    """responsável por retornar uma paleta de cores baseado em 2 cores iniciais"""
    try:
        color_from = Color(color_a)
        color_to = Color(color_b)
        return [
            color.get_hex() for color in color_from.range_to(color_to, range)
        ]
    except BaseException:
        return False


def get_pandas_distinct_count(data: list, key: str, sort=False) -> list:
    """responsável retornar uma contagem distinta de uma lista"""
    try:
        df = pd.DataFrame(data)
        result = df[key].value_counts(sort=sort)
        headers = [x for x in result.keys()]
        values = [int(x) for x in result]
        return {"labels": headers, "values": values, "length": len(headers)}
    except BaseException as exc:
        return f"{exc}"
    
def get_pandas_sum_value_per_group(data:list,field1:str,field2:str,):
    try:
        #  criando dataframe
        dt = pd.DataFrame(data)
        keys = dt.keys().to_list()
        
        # validando se existem os campos passados como parâmetro
        if not field1 in keys: raise BaseException("invalid index")
        if not field2 in keys: raise BaseException("invalid index")
        
        uniq = [x for x in dt[field1].value_counts().to_dict()]
        
        return [
            {
                "name":x,
                "value":dt.loc[dt[field1] == x,field2].sum()
            }
            for x in uniq
        ]
    except BaseException as exc: 
        return f"{exc}"
    
    