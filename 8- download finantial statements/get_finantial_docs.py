import requests
from bs4 import BeautifulSoup

def get_fin_docs(CIK="1018724"):
    # base URL for the SEC EDGAR browser
    endpoint = r"https://www.sec.gov/cgi-bin/browse-edgar"

    # define our parameters dictionary
    param_dict = {'action':'getcompany',
                'CIK': CIK,
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

    # get the table that have the class tableFile2
    table = soup.find(class_="tableFile2")

    rows = table.find_all("tr")[1:] #removes the header row

    # iterates al rows of the table
    for row in rows:
        l = []
        s = "interactiveDataBtn"

        # if interactiveDataBtn text exist in the row
        if s in row.decode():
            date = row.find_all("td")[3].string # get the date
            url = row.find(id=s).get('href') # get the interactive data url
            l.append("https://www.sec.gov" + url)
            l.append(date)
            I_D_links.append(l)

    # getting the xls finantial docs
    len_docs = len(I_D_links)
    print("Gettings docs URLs... ")
    for n, l in enumerate(I_D_links):
        print(str(int(100*n/len_docs)) + "%...") # print the percentage of the process
        endpoint = l[0]
        response = requests.get(url = endpoint)
        soup = BeautifulSoup(response.content, 'lxml')
        # look for the xls docs links
        entries = soup.find("a", string="View Excel Document")
        url = entries.get('href')
        I_D_links[n].append("https://www.sec.gov" + url)
    print("done!...")
    return I_D_links
