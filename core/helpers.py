import requests
import json
import uuid
from core.metascore import score_generator

razerId = str(uuid.uuid4())
baseUrl = 'http://razerhackathon2app.eba-3mgtrpdc.ap-southeast-1.elasticbeanstalk.com'



def create_client(**payload):
    url = "https://razerhackathon.sandbox.mambu.com/api/clients"
    defaults = {
        "client": {
            "firstName": "Celeste",
            "lastName": "Goh",
            "preferredLanguage": "ENGLISH",
            "notes": "Enjoys playing RPG",
            "assignedBranchKey": "8a8e878e71c7a4d70171ca62fe0f1244"
        },
        "idDocuments": [
            {
                "identificationDocumentTemplateKey": "8a8e867271bd280c0171bf7e4ec71b01",
                "issuingAuthority": "Immigration Authority of Singapore",
                "documentType": "NRIC/Passport Number",
                "validUntil": "2021-09-12",
                "documentId": "S9812345A"
            }
        ],
        "addresses": [],
        "customInformation": [
            {
                "value": "Singapore",
                "customFieldID": "countryOfBirth"

            },
            {
                "value": razerId,
                "customFieldID": "razerID"

            }
        ]
    }
    payload.update(defaults)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic VGVhbTU5OnBhc3M3MUE5OTUxQkY=',
        'Content-Type': 'application/json',
        'Cookie': 'AWSALB=IMovU10rhtsnJ3BqG8lzoXH2YpdvmMrZqMkfTnEO1EA7eQMaU9vtYQn+iU4OlZHAYFqXazbJnZvktB3Sy1lvqNjQwatki107KJT2WaNEDTW+QTkHU6HWcAS5pqG8; AWSALBCORS=IMovU10rhtsnJ3BqG8lzoXH2YpdvmMrZqMkfTnEO1EA7eQMaU9vtYQn+iU4OlZHAYFqXazbJnZvktB3Sy1lvqNjQwatki107KJT2WaNEDTW+QTkHU6HWcAS5pqG8'
    }
    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))
    clientID = json.loads(response.text.encode('utf8'))['client']['encodedKey']
    assigned_branchkey = json.loads(response.text.encode('utf8'))[
        'client']['assignedBranchKey']
    return {'clientID': str(clientID), 'assigned_branchkey': str(assigned_branchkey)}


def create_current_account(clientID,**payload):
    url = "https://razerhackathon.sandbox.mambu.com/api/savings"

    defaults = {
    "savingsAccount": {
        "name": "Digital Account",
        "accountHolderType": "CLIENT",
        "accountHolderKey": clientID,
        "accountState": "APPROVED",
        "productTypeKey": "8a8e878471bf59cf0171bf6979700440",
        "accountType": "CURRENT_ACCOUNT",
        "currencyCode": "SGD",
        "allowOverdraft": "true",
        "overdraftLimit": "100",
        "overdraftInterestSettings": {
            "interestRate": 5
        },
            "interestSettings": {
        "interestRate": "1.25"
    }
    }

    }
    payload.update(defaults)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic VGVhbTU5OnBhc3M3MUE5OTUxQkY=',
        'Content-Type': 'application/json',
        'Cookie': 'AWSALB=YbPVsMDHAgy8HV7v2UOolZqQ5lcYDp/0+UwF5SXf7HOfHGICkom4FvlnjFWbBqGOGNvTyWxfmFGzrEu2U6giJ+1O+mlZtifa8DifgzY8VwFxQqXk5wJ8ZitgJMkc; AWSALBCORS=YbPVsMDHAgy8HV7v2UOolZqQ5lcYDp/0+UwF5SXf7HOfHGICkom4FvlnjFWbBqGOGNvTyWxfmFGzrEu2U6giJ+1O+mlZtifa8DifgzY8VwFxQqXk5wJ8ZitgJMkc'
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))
    accountID = json.loads(response.text.encode('utf8'))['savingsAccount']['encodedKey']
    return {'accountID':str(accountID)}

def create_loan_account(clientID,assigned_branchkey,**payload):
    url = "https://razerhackathon.sandbox.mambu.com/api/loans"

    defaults= {
    "loanAccount": {
        "accountHolderType": "CLIENT",
        "accountHolderKey": clientID,
        "productTypeKey": "8a8e867271bd280c0171bf768cc31a89",
        "assignedBranchKey": assigned_branchkey,
        "loanName": "Student Loan",
        "loanAmount": 1010,
        "interestRate": "2",
        "arrearsTolerancePeriod": "0",
        "gracePeriod": "0",
        "repaymentInstallments": "10",
        "repaymentPeriodCount": "1",
        "periodicPayment": "0",
        "repaymentPeriodUnit": "WEEKS",
        "disbursementDetails": {
            "customInformation": [
                {
                    "value": "unique identifier for this transaction",
                    "customFieldID": "IDENTIFIER_TRANSACTION_CHANNEL_I"
                }
            ]
        }
    }
    }
    payload.update(defaults)
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic VGVhbTU5OnBhc3M3MUE5OTUxQkY=',
    'Content-Type': 'application/json',
    'Cookie': 'AWSALB=8DazNFoO0HhPkvVwOuTzvMb7J4JzRN8kirpabPQakt8FCzziG4FwAZbPDaxkB7wRJ7c1AT4fyvV0JlNy3AE5iHB1WC/5M+5R5tgy9UyqnOisMUUP8RCEQSk1WcF4; AWSALBCORS=8DazNFoO0HhPkvVwOuTzvMb7J4JzRN8kirpabPQakt8FCzziG4FwAZbPDaxkB7wRJ7c1AT4fyvV0JlNy3AE5iHB1WC/5M+5R5tgy9UyqnOisMUUP8RCEQSk1WcF4'
    }

    response = requests.request(
        "POST", url, headers=headers, data=json.dumps(payload))

    loanID = json.loads(response.text.encode('utf8'))['loanAccount']['encodedKey']
    return {'loanID':str(loanID)}

def get_meta_score():
    jackie = {"dota2": "122272960",
          "pubg": "WackyJacky101",
          "lol": "XofAEbbZ2in_MtKIeX-mvDj1HjG4QG8US6t7jF_PqtXBxWg"
          }
    return score_generator(jackie)['metascore']



