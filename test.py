from scriptV2 import Shipment, SupplyDemand, calculate_order_amount
from datetime import date, timedelta
from typing import List

shipments = [
    Shipment("F600", date(2023, 9, 1), 15),   # Sell-by: 2024-04-28 — expired early x
    Shipment("H800", date(2024, 8, 20), 35),  # Sell-by: 2025-04-17 x
    Shipment("C300", date(2024, 10, 1), 30),  # Sell-by: 2025-06-28 20 x
    Shipment("A100", date(2024, 12, 1), 40),  # Sell-by: 2025-07-29 10 x
    Shipment("B200", date(2025, 1, 15), 20),  # Sell-by: 2025-09-12 x
    Shipment("D400", date(2025, 2, 1), 10),   # Sell-by: 2025-09-29 x
    Shipment("E500", date(2025, 3, 15), 25),  # Sell-by: 2025-11-10 x
    Shipment("G700", date(2025, 5, 1), 50),   # Sell-by: 2026-01-27
]

forecast = [
    SupplyDemand(45, date(2024, 11, 15)), # Tests pre-2025 inventory x
    SupplyDemand(50, date(2025, 3, 1)),   # Solid coverage from first few shipments x
    SupplyDemand(40, date(2025, 5, 1)),   # Might consume mid-expiration inventory x
    SupplyDemand(25, date(2025, 8, 1)),   # Some early shipments may expire x
    SupplyDemand(60, date(2025, 10, 1)),  # Likely needs newer inventory
    SupplyDemand(35, date(2026, 1, 1)),   # Will test long shelf life
]

def test1():
    return calculate_order_amount(shipments, forecast)

print(test1())