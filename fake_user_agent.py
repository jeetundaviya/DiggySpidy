# All Fake User-Agent are taken from http://useragentstring.com/pages/useragentstring.php?typ=Browser

import random

class FakeUserAgent:
    def __init__(self):
        
        self.FakeUserAgentList = []
        
        with open('./UserAgentList/fake_user_agent_list.txt','r') as f:
            self.FakeUserAgentList = f.readlines()
        
        self.FakeUserAgentList = [link.replace('\n','') for link in self.FakeUserAgentList]

    def get_random_fake_user_agent(self):
        return random.choice(self.FakeUserAgentList) 
