# All Fake User-Agent are taken from http://useragentstring.com/pages/useragentstring.php?typ=Browser

import random,os

LATEST_CHROME_USERAGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'

class FakeUserAgent:
    def __init__(self):
        
        self.FakeUserAgentList = []
        
        with open(os.path.join(os.path.join("DS_Core",'UserAgentList'),'fake_user_agent_list.txt'),'r') as f:
            self.FakeUserAgentList = f.readlines()
        
        self.FakeUserAgentList = [link.replace('\n','') for link in self.FakeUserAgentList]

    def get_random_fake_user_agent(self):
        return random.choice(self.FakeUserAgentList) 
