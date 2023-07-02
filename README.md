

# Receipt Processing API

This API allows you to process receipts and calculate the rewards points associated with them.

## Running the API

To run the API, run the following command:

* Clone the repository on to your local machine
```
    git clone https://github.com/bhansaliyash/fetch-challenge
```

* Run the command - 
```
    docker compose up -d receipt_processor
```

This will start the API on port 8000. You can access the API documentation at http://localhost:8000/docs.

### API Endpoints
do
The API has two endpoints:
```
/receipts/process
```
This endpoint accepts a receipt as input and returns a unique id for the receipt. It also calculates the rewards points associated with the receipt and stores it in a dictionary.

```
/receipts/{id}/points
```

This endpoint returns the rewards points for the receipt with the given id.

Example -  

To process a receipt, you can use the following curl command:
```
curl -X POST -H "Content-Type: application/json" -d '{
            "retailer": "Target",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "14:01",
            "total": "2.65",
            "items": [
                {"shortDescription": "Dasani wat", "price": "1.40"}
            ]
        }' http://localhost:8000/receipts/process
```

This will return the following response:

```
{ "id": "a1661952-15b9-31a3-ae44-e27b992cd7ad", "message": "Receipt processed successfully" }
```

To get the rewards points for the above receipt, you can use the following curl command:

```
curl http://localhost:8000/receipts/a1661952-15b9-31a3-ae44-e27b992cd7ad/points
```

This will return the following response:
```
{ "reward points": 16 }
```

## Running the test cases

* Once the docker container is running use the below command to run the associated test cases written in test.py- 

```
docker exec fetch-receipt_processor-1 python -m unittest test.py
``` 

fetch-receipt_processor-1 is the container name. You can replace it with your container name or container id if that is different for you

## Production 

Some ideas on how I would extend the implementation in production -

* Functions can be defined as async and implemetation can be done accordingly in the calling systems so that apis can be called in asynchronous manner by implementing message brokers which will help in managing load.

* Running multiple images and implement a load balancer to handle huge amount of requests. Optionally as the application is dockerized its easy to deploy it on cloud and also setup a kubernetes cluser.

* A CI/CD pipeline can be implemented that will first run the test cases to ensure if all checks are passed and deploy the applicaion on the server.

* Implementing caching and persistent storage solutions.

* Implement Static security scans for the code to check for vulnerabilities before it is deployed.

* Setup access management so that acess to APIs can be controlled








