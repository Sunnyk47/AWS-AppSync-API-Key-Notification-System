# AWS-AppSync-API-Key-Notification-System
Our current implementation involves an AWS AppSync API key that is hardcoded within our codebase. This approach presents a risk of service disruption as the key is subject to expiration. To avoid this issue, we have established an automated alert system to proactively notify us before the API key reaches its expiration date. This will enable us to extend the key's validity in a timely manner, ensuring uninterrupted functionality of our system.


# Resolution
We implemented a serverless system using AWS Lambda, Amazon EventBridge, and Amazon SNS to monitor the expiry of an AppSync API key and send notifications before the key expires.
