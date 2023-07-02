import math
import re
import uuid
from datetime import datetime

def generateUniqueReceiptId(receipt):
    '''
    Generates a unique receipt ID based on the provided receipt.
        Parameters:pi
            receipt (str): Receipt details used as the input for generating the unique ID.

        Returns:
            str: The unique receipt ID generated using the UUIDv3 algorithm.
    '''
    
    #uuid3 to make sure same id is generated for a particular receipt to safeguard against multiple submissions
    return uuid.uuid3(uuid.NAMESPACE_DNS, receipt)

def calculateReceiptPoints(receipt):
    '''
    Calculates the points for a given receipt based on the specified criteria.

        Parameters:
            receipt_data (dict): A dictionary containing the receipt details under 'data' key and total reward points under 'points' key.

        Returns:
            None: This function updates the by adding the calculated points to the "points" key.
    '''

    total_points = 0

    #One point for every alphanumeric character in the retailer name.
    total_points += len(re.sub(r'\W+', '', receipt.retailer))
    
    #50 points if the total is a round dollar amount with no cents.
    if receipt.total.is_integer():
        total_points+=50
    
    #25 points if the total is a multiple of 0.25.
    if receipt.total%0.25==0:
        total_points += 25
    
    #5 points for every two items on the receipt.
    total_points += len(receipt.items)//2*5
    
    #If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt.items:
        item["shortDescription"] = item["shortDescription"].strip()
        if len(item["shortDescription"])%3==0:
            total_points += math.ceil(float(item["price"])*0.2)

    #6 points if the day in the purchase date is odd.
    purchase_date = receipt.purchaseDate.split("-")
    if int(purchase_date[-1])%2!=0:
        total_points += 6
    
    #10 points if the time of purchase is after 2:00pm and before 4:00pm.
    purchase_time = datetime.strptime(receipt.purchaseTime,'%H:%M')

    if purchase_time>datetime.strptime('14:00','%H:%M') and purchase_time<datetime.strptime('16:00','%H:%M'):
        total_points += 10
    
    return total_points
