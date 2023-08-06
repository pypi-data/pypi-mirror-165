import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from termcolor import colored

ua = UserAgent()

class parser_proxy():
    def __init__(self, proxys_list):
        self.proxys_list = proxys_list
        self.parse_proxies_one()
        self.parse_proxies_two()
        self.parse_proxies_three()
        self.parse_proxies_four()
        self.parse_proxies_five()
        self.parse_proxies_six()

    def parse_proxies_one(self):
        self.r = requests.get('https://www.sslproxies.org/')
        html = BS(self.r.content, 'lxml')
        for el in html.select('.form-control'):
            ssl = el.text.split()[9:40]
            for i in ssl:
                self.proxys_list.append(i)
            
    def parse_proxies_two(self):
        self.r = requests.get('https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=500&country=all').text.split()
        for i in self.r:
            self.proxys_list.append(i)
   
    def parse_proxies_three(self):
        self.r = requests.get('https://free-proxy-list.net/anonymous-proxy.html')
        html = BS(self.r.content, 'lxml')
        for el in html.select('.form-control'):
            ssl = el.text.split()[9:40]
            for i in ssl:
                self.proxys_list.append(i)
            
    def parse_proxies_four(self):     
        self.r = requests.get('https://free-proxy-list.net/')
        html = BS(self.r.content, 'lxml')
        for el in html.select('.form-control'):
            ssl = el.text.split()[9:40]
            for i in ssl:
                self.proxys_list.append(i)

    def parse_proxies_five(self):     
        self.r = requests.get('https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt').text.split()[:40]
        for i in self.r:
            self.proxys_list.append(i)

    def parse_proxies_six(self):
        self.r = requests.get('https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt').text.split()[:40]
        for i in self.r:
            self.proxys_list.append(i)
        

    def check_ip(self,proxy_list_valid,print_error_proxy=None):
    #g = time.time()
        self.print_error_proxy = print_error_proxy
        for i in self.proxys_list:
            try:
                proxies = {
                'http': f'http://{i}',
                'https': f'http://{i}'
                }
                headers = {
                    'User-Agent': ua.random
                }
                self.url_google = 'https://www.google.com'
                google_reguest = requests.get(self.url_google,proxies=proxies,headers=headers,timeout=1)
                if google_reguest.status_code == 200:
                    print(colored(i, 'green'))
                    proxy_list_valid.append(i)
            except:
                if self.print_error_proxy == True:
                    print(colored(f'ERROR {i}', 'red'))
                else:
                    pass

proxys_list = []
parser_proxy = parser_proxy(proxys_list)
#http://icanhazip.com/  
#http://ip-api.com/json/
#http://ip-api.com/json/?fields=8217