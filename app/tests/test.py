import unittest
from ..utils.helper import generateUniqueReceiptId, calculateReceiptPoints
from ..models.receiptModel import Receipt

class TestReceiptProcessor(unittest.TestCase):

    def test_unique_id_different_reeceipts(self):
        '''Check if application returns unique id for different request'''
        
        mock_request_1 = str({
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        })

        mock_request_2 = str({
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:13",
            "total": "1.25",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"}
            ]
        })

        id_one = generateUniqueReceiptId(mock_request_1)
        id_two = generateUniqueReceiptId(mock_request_2)

        self.assertNotEqual(id_one, id_two, "Application returns same id for different request")


    def test_unique_id_same_receipts(self):
        '''Check if application returns same unique id even when same request is submitted multiple times. This will help ensure correct error message is raised if the user tries to submit same receipt multiple times'''
        
        mock_request = str({
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        })

        id_1 = generateUniqueReceiptId(mock_request)
        id_2 = generateUniqueReceiptId(mock_request)

        self.assertEqual(id_1,id_2, "System accepts duplicate receipts")

    def test_reward_points(self):
        '''Check if the total rewards calculation function works fine'''

        mock_request_data = Receipt.parse_obj({
            "retailer": "Walgreens",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Pepsi - 12-oz", "price": "1.25"},
                {"shortDescription": "Dasani", "price": "1.40"}
            ]
        })

        points = calculateReceiptPoints(mock_request_data)

        self.assertEqual(points, 15, "Reward points not calculated correctly")

    def test_reward_points_retailer(self):
        '''Check if the retailer contribution to reward points is calculated correctly'''

        mock_request_data = Receipt.parse_obj({
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "08:13",
            "total": "2.65",
            "items": [
                {"shortDescription": "Dasani wat", "price": "1.40"}
            ]
        })

        points = calculateReceiptPoints(mock_request_data)

        self.assertEqual(points, 14, "Incorrect calculaiton of alphanumeric characters in retailer")

    def test_reward_points_purhaseTime(self):
        '''Check if the retailer contribution to reward points is calculated correctly'''

        mock_request_1 = Receipt.parse_obj({
            "retailer": "",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "14:00",
            "total": "2.65",
            "items": [
                {"shortDescription": "Dasani wat", "price": "1.40"}
            ]
        })
        
        mock_request_2 = Receipt.parse_obj({
            "retailer": "",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "14:01",
            "total": "2.65",
            "items": [
                {"shortDescription": "Dasani wat", "price": "1.40"}
            ]
        })
        
        points_1 = calculateReceiptPoints(mock_request_1)
        points_2 = calculateReceiptPoints(mock_request_2)

        self.assertEqual(points_1, 0, "Incorrect calculaiton of alphanumeric characters in retailer")
        self.assertEqual(points_2, 10, "Incorrect calculaiton of alphanumeric characters in retailer")


if __name__=="__main__":
    unittest.main()