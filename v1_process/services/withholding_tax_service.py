"""
Define if these are methods or functions (instance related or not) to define a class
"""
def project(value, procedureType, workedDays):
    if procedureType == "T":
        return (value / workedDays) * 30
    return value

def get_table_value(base, table, uvtValue):
    for rank in table:
        if rank["min"] * uvtValue < base and base < rank["max"] * uvtValue:
            return (base - rank["subsValue"] * uvtValue) * rank["percentage"] + \
                rank["addValue"] * uvtValue
    lastRank = table[len(table) - 1]
    return (base - lastRank["subsValue"] * uvtValue) * lastRank["percentage"] + \
            lastRank["addValue"] * uvtValue
            
"""
Service to access namespace 
Fill this service with a list of WithholdingTax objects 
"""
class WithholdingTaxService:

    def __init__(self, is_foreigner, percentage_foreigner):
        self.is_foreigner = is_foreigner
        self.percentage_foreigner = percentage_foreigner

    def _internal_method(self, attr):
        return attr

    def public_method(self, attr: int) -> int:
        return attr
    
    def _save_to_database():
        #Logic to connect to Model class and persist data
        return