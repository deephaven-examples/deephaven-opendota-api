class D2Constant:
    def __init__(self):
        self.json = None
        self.dataframe = None
        self.table = None

class D2:
    def __init__(self):
        self.Heroes = D2Constant()
        self.GameModes = D2Constant()
        self.Items = D2Constant()

Dota2 = D2()
