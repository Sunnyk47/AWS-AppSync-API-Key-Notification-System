# AWS-AppSync-API-Key-Notification-System
Our current implementation involves an AWS AppSync API key that is hardcoded within our codebase. This approach presents a risk of service disruption as the key is subject to expiration. To avoid this issue, we have established an automated alert system to proactively notify us before the API key reaches its expiration date. This will enable us to extend the key's validity in a timely manner, ensuring uninterrupted functionality of our system.


# Resolution
We implemented a serverless system using AWS Lambda, Amazon EventBridge, and Amazon SNS to monitor the expiry of an AppSync API key and send notifications before the key expires.

# Steps to Resolution:

**Step 01** Identify the API KEY
Identify the API KEY that you want to monitor (eg: da2-bnpchjhesffrfjleqdxknk87yd).

**Step 02** Step Up the SNS topic
Create a SNS topic and add the subscriptions to the topic for the intended recipients.

**Step 03** Set Up Lambda function 
1. Create a Lambda function to interact with the AppSync service using list_api_keys API to fetch API key details.
2. Provide the IAM permission to the lambda function. (SNS publish & AppsyncApilist)
3. Write the Python code (Provided in the code file), deploy it and then test it.

**Step 04** Configure the Event Bridge to trigger the lambda function
Create an EventBridge rule to set to trigger the Lambda function periodically (e.g., Once in a week) to monitor the API key status. If the key is going to expire in given parameter then it will send you an alert. 

**Steo 05** Test the system
Test the Event bridge on a short time duration (e.g, Every 1 minute) to trigger lambda function to ensure it can detect the API key, calculate days to expiry, and send notifications via SNS.

In case of Error you can check Lambda logs and verify the configuration and IAM permission attached to lambda function. 

# Key Outcomes
This automated system ensures proactive monitoring of the AppSync API key's expiration status. It reduces the risk of service interruptions, eliminates manual monitoring, and provides a reliable alert mechanism using serverless AWS components.
