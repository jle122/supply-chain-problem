
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
    
    def sell_by_date(self): # the expiration date (calculated as 8 months from date_made)
        return self.date_made + timedelta(days=240)

class SupplyDemand:
    '''attributes of a forecast'''
    '''at this current date, what is the demand needed?'''
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

    for i in shipments: # going through current stock
        # if the expiration date is later than input date and the date it was made is less than the input date
        # add it to available shipments
        if i.sell_by_date() >= date and i.date_made < date:
            available_shipments.append(i)
        else: # otherwise, add it to expired shipments
            expired_shipments.append(i)

    return (available_shipments, expired_shipments)

def calculate_order_amount(shipments: List[Shipment], forecast: List[SupplyDemand]):
    '''input the dictionary outputted by the previous algorithm'''
    '''Given this input, this function will output a dictionary telling how much needs to be ordered at each date'''

    output_dict = {} # output value
    shipments1 = shipments

    # sort the chart by earliest date
    forecast = sorted(forecast, key=lambda s: s.current_date)

    # go through the forecast
    for i in forecast:
        demand = i.demand 
        # call the previous function to find all available shipments at the date
        (available_shipments, expired_shipments) = find_available_and_expired_at_single_date(shipments1, i.current_date)

        if available_shipments == []: # if there are no available shipments, set output to be demand
            output_dict[i.current_date] = demand
        else: # otherwise...
            # sort the available shipments by earliest expiration date
            available_shipments = sorted(available_shipments, key=lambda s: s.sell_by_date())

            stock = 0 # initialize a counter variable to track current stock
            while stock < demand:
                if available_shipments != []: # if available shipments is not empty
                    current = available_shipments[0]

                    if stock + current.amount <= demand: # if the counter is under demand, completely sell the shipment
                        stock += current.amount
                        # remove this shipment (consider it completely shipped out)
                        available_shipments.pop(0)
                        shipments1.remove(current)
                    else: # otherwise, partially sell the shipment based on whatever is needed to meet demand
                        current.amount = current.amount - (demand - stock)
                        stock = demand # demand is met with part of a shipment

                else: # if there are no more available shipments, end the prematurely end the loop
                    break

            # set the number at the current date to be either 0 (demand is met) or demand - stock
            # if the number is not 0, the amount shown is the amount needed to meet demand based on current supply
            output_dict[i.current_date] = max(0,demand - stock)

    # Sort keys in descending order and rebuild the dictionary
    output_dict = dict(sorted(output_dict.items()))
    return output_dict
