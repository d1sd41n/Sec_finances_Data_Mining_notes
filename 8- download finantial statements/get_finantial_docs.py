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
    table = soup.find(class_="tableFile2")

    rows = table.find_all("tr")[1:]
    for row in rows:
        l = []
        s = "interactiveDataBtn"
        if s in row.decode():
            date = row.find_all("td")[3].string
            url = row.find(id=s).get('href')
            l.append("https://www.sec.gov" + url)
            l.append(date)
            I_D_links.append(l)
    print(I_D_links)

    F_S_links = []
    len_docs = len(I_D_links)
    print("Gettings docs URLs... ")
    for n, l in enumerate(I_D_links):
        print(str(int(100*n/len_docs)) + "%...")
        endpoint = l[0]
        l2 = []
        response = requests.get(url = endpoint)
        soup = BeautifulSoup(response.content, 'lxml')
        entries = soup.find("a", string="View Excel Document")
        url = entries.get('href')
        l2.append("https://www.sec.gov" + url)
        l2.append(l[1])
        F_S_links.append(l2)
    return F_S_links

get_fin_docs()
d = get_fin_docs()

print(d)
