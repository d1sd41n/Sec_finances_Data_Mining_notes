import requests
from bs4 import BeautifulSoup

def get_fin_docs(CIK="1018724"):
    # base URL for the SEC EDGAR browser
    endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

    # define our parameters dictionary
    param_dict = {'action':'getcompany',
                'CIK':'1018724',
                'type':'10-Q',
                'dateb':'',
                'owner':'exclude',
                'start':'',
                'output':'',
                'count':'100'}

    # request the url, and then parse the response.
    response = requests.get(url = endpoint, params = param_dict)
    soup = BeautifulSoup(response.content, 'lxml')

    # print status code
    print("Search page URL: " + response.url)

    # this list will save all interative data links
    I_D_links = []

    # get all interactive data financial statements
    print("Getting interactive Data...")
    entries = soup.find_all(id="interactiveDataBtn")

    for e in entries:
        I_D_links.append("https://www.sec.gov" + e.get('href'))

    F_S_links = []
    len_docs = len(I_D_links)
    print("Gettings docs URLs... ")
    for n, l in enumerate(I_D_links):
        print(str(int(100*n/len_docs)) + "%...")
        endpoint = l
        response = requests.get(url = endpoint)
        soup = BeautifulSoup(response.content, 'lxml')
        entries = soup.find("a", string="View Excel Document")
        F_S_links.append("https://www.sec.gov" + entries.get('href'))
    return F_S_links

d = get_fin_docs()

print(d)
