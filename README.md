# Duo-Phishing-Script
A python script designed to mimic a push spray attack, allowing administrators to conduct MFA phishing campaigns.

Usage:
1. Create a Duo Auth API application (https://duo.com/docs/authapi#first-steps) and copy the API credentials to config.json.
2. Download a CSV list of users from your Duo Admin Panel > Users > Export, modify the list as necessary, and save the list in the same folder as the rest of the script files.
3. Run the script by using the below command:
   ```python phishingCampaign.py users.csv```
4. While the script generates a basic log as well as a raw API log, it's best to view the users' responses from the Admin Panel's reporting tab. 
