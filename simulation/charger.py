


class Charger():

    def __init__(self, maxOutputPerConnector, decisionMaker):
        self.connectors = []
        self.maxOutputPerConnector = maxOutputPerConnector
        self.chargerSchedule = []
        self.decisionMaker = decisionMaker

