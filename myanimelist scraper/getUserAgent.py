from random import randint
import userAgents

proxies = []

with open('proxies.txt', 'r+') as proxyList:
    for proxy in proxyList.readlines():
        toString = str(proxy).removesuffix('\n')
        proxies.append(toString)

def getAgent():
    getNumber = randint(0, len(userAgents.user_agents_list) - 1)
    return userAgents.user_agents_list[getNumber]

def getProxy():
    getNumber = randint(0, len(proxies) - 1)
    return proxies[getNumber]