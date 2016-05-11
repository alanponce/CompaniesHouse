"""
Test the API functionality
"""
import requests
import csv
import json
import time

from requests.auth import HTTPBasicAuth

URL  = requests.get('https://api.companieshouse.gov.uk/company/', 
                    auth=HTTPBasicAuth('VeBXX0FG5pgfK63Khy2TTbKKOU3qzKWReXKhUXMJ', ''))
URL.status_code
URL.json()

""" This is the code that works with the other API
"""

TIME_SLEEP = 0
INFILE = './CompaniesHouse.csv'
OUTFILE = './result.json'

def get_list_company(infile):
    """ yield the company number from the txt file
    """
    # outlist = list()
    with open(infile, 'r') as f:
        csvreader = csv.reader(f)
        next(csvreader)  # to skip the header
        for l in csvreader:
            yield l[0]  # csv reader return a list, just yield the unique element of the list to return un str
            # outlist.append(l)
    # return outlist


def create_url(*args):
    """ Return an URL from the element, add them in order
    """
    url = args[0] + args[1]
    return url


def parse_company(url, api_key=API_KEY):
    """ Get the URL, api_key and company number
        Return result if receive a 200 and that the response
        is a json format otherwise print error and return empty dict otherwise
    """
    response = requests.get(url, data=api_key)
    resp = dict()
    if response.status_code == 200:
        if response.headers['content-type'] == 'application/json':
            resp = response.json()['response']
        else:
            print('Error in the type of answer received: {} with the URL: {}'.format(response.headers['content-type'], url))
    else:
        print('Error {} in accessing service with the URL: {}'.format(response.status_code, url))
    return response.status_code, resp


def company_result():
    for company in get_list_company(INFILE):
        time.sleep(TIME_SLEEP)
        url = create_url(URL, company, API_KEY)
        status, response = parse_company(url)
        print(company)
        yield company, response


def main():
    # to reinitialise the file, comment if you don't want that behaviour
    with open(OUTFILE, 'w') as out: pass
    for company, response in company_result():
        response.update({'company_name': company})  # add our own field in the response dict
        with open(OUTFILE, 'a') as out:
            json.dump(response, out)


if __name__ == '__main__':
    main()
