import json
import logging

class CatalogEntry:
    def __init__(self, password):
        self.password = password
        self.ip = None

    def updateIp(self, ip):
        self.ip = ip

    def getIp(self):
        return self.ip

    def getPassword(self):
        return self.password

class Catalog:
    def __init__(self, data, cacheFile):
        self.catalog = {}
        self.cacheFile = cacheFile
        
        for domain, password in data.iteritems():
            self.catalog[domain] = CatalogEntry(password)

        cacheData = {}
        try:
            with open(self.cacheFile, "r") as f:
                cacheData = json.load(f)
        except:
            pass

        for domain, ip in cacheData.iteritems():
            self.updateIp(domain, ip)

    def updateIp(self, domain, ip):
        domain = domain.lower()

        entry = self.catalog.get(domain)
        if entry and entry.getIp() != ip:
            entry.updateIp(ip)
            logging.info("Updated '%s' with '%s'" % (domain, ip))

            try:
                with open(self.cacheFile, "w") as f:
                    json.dump(dict((domain, entry.getIp()) for domain, entry in self.catalog.iteritems()), f)
            except:
                logging.exception("Unhandled exception while writing cache file")

    def getIp(self, domain):
        entry = self.catalog.get(domain.lower())
        if entry:
            return entry.getIp()
        return None

    def getPassword(self, domain):
        entry = self.catalog.get(domain.lower())
        if entry:
            return entry.getPassword()
        return None