"""Abstract Base Interface"""
interface = None

class DBInterface(object): pass

class TransactionMaker(object): pass

def instance_transaction(obj, session):
    """Context Manager"""
    pass
    
