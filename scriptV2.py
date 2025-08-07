
from datetime import date, timedelta
from typing import List

class Shipment:
    '''shipment definition with attributes'''

    product_id: str # or some other identifier
    date_made: date # some date we can calculate the age from
    amount: int # amount in the shipment

    def __init__(self, product_id: str, date_made: date, amount: int):
        self.product_id = product_id
        self.date_made = date_made
        self.amount = amount
    
    def sell_by_date(self):
        return self.date_made + timedelta(days=240)

class SupplyDemand:
    '''attributes of a forecast'''

    demand: int # projected quota
    current_date: date

    def __init__(self, demand: int, current_date: date):
        self.demand = demand
        self.current_date = current_date
    
def find_available_and_expired_at_single_date(shipments: List[Shipment], date: date):
    '''Inputs: a list of shipments, and some date'''
    '''Given a single date, and a list of a shipments available, give all available and expired shipments
    for at some date'''

    available_shipments = []
    expired_shipments = []

    for i in shipments:
        if i.sell_by_date() >= date and i.date_made < date:
            available_shipments.append(i)
        else:
            expired_shipments.append(i)

    return (available_shipments, expired_shipments)

def find_available(shipments: List[Shipment], forecast: List[SupplyDemand]):
    '''Input: List of shipments and a list of dates (probably following a 12 month forecast)'''
    '''Given a supply-demand chart of a date forecast, and available stock, find how much available based on the forecast.'''

    projected_stock = {}

    for i in forecast:
        (available_shipments, expired_shipments) = find_available_and_expired_at_single_date(shipments, i.date)
        total_stock = 0

        for j in available_shipments:
            total_stock += j.amount
            
        projected_stock[i.date] = (total_stock, available_shipments, expired_shipments)

    return projected_stock

def calculate_order_amount(shipments: List[Shipment], forecast: List[SupplyDemand]):
    '''input the dictionary outputted by the previous algorithm'''
    '''Given this input, this function will output a dictionary telling how much needs to be ordered at each date'''

    output_dict = {} # output value
    shipments1 = shipments
    forecast = sorted(forecast, key=lambda s: s.current_date)
    for i in forecast:
        demand = i.demand 
        (available_shipments, expired_shipments) = find_available_and_expired_at_single_date(shipments1, i.current_date)

        if available_shipments == []:
            output_dict[i.current_date] = demand
        else: 
            available_shipments = sorted(available_shipments, key=lambda s: s.sell_by_date())
            stock = 0
            while stock < demand:
                if available_shipments != []:
                    current = available_shipments[0]
                    if stock + current.amount <= demand:
                        stock += current.amount
                        available_shipments.pop(0)
                        shipments1.pop(0)
                    else:
                        for j in shipments1:
                            if j == current:
                                current.amount = current.amount - (demand - stock)
                                j = current
                                break
                        stock = demand

                else:
                    break
            output_dict[i.current_date] = max(0,demand - stock)
    # Sort keys in descending order and rebuild the dictionary
    output_dict = dict(sorted(output_dict.items()))
    return output_dict

# test cases
shipments = [
    Shipment("A100", date(2024, 12, 1), 40),  # Sell-by: 2025-07-29
    Shipment("B200", date(2025, 1, 15), 20),  # Sell-by: 2025-09-12
    Shipment("C300", date(2024, 10, 1), 30),  # Sell-by: 2025-06-28
    Shipment("D400", date(2025, 2, 1), 10),   # Sell-by: 2025-09-29
    Shipment("E500", date(2025, 3, 15), 25),  # Sell-by: 2025-11-10
    Shipment("F600", date(2023, 9, 1), 15),   # Sell-by: 2024-04-28 — expired early
    Shipment("G700", date(2025, 5, 1), 50),   # Sell-by: 2026-01-27
    Shipment("H800", date(2024, 8, 20), 35),  # Sell-by: 2025-04-17
]

forecast = [
    SupplyDemand(50, date(2025, 3, 1)),   # Solid coverage from first few shipments
    SupplyDemand(40, date(2025, 5, 1)),   # Might consume mid-expiration inventory
    SupplyDemand(25, date(2025, 8, 1)),   # Some early shipments may expire
    SupplyDemand(60, date(2025, 10, 1)),  # Likely needs newer inventory
    SupplyDemand(35, date(2026, 1, 1)),   # Will test long shelf life
    SupplyDemand(45, date(2024, 11, 15)), # Tests pre-2025 inventory
]
def test1():
    return calculate_order_amount(shipments, forecast)

print(test1())