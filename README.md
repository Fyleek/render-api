# Render Api

Wanting to set up the Render deployment status on GitHub for one of my projects, I noticed that render did not have a solution yet available...
So here we are!

Render-API is an innovative solution designed to seamlessly integrate GitHub's webhook functionality with Render's deployment status updates.
This non-official API acts as a bridge, automatically updating the deployment status in a GitHub repository's
main branch based on the deployment status from Render. It enhances the continuous integration and deployment
(CI/CD) process by providing real-time synchronization between these two critical platforms.

## Features
- **GitHub Webhook Integration**: Listens for events from GitHub's webhook, triggering actions in response to repository events,
particularly focusing on deployment-related activities.
- **Deployment Status Sync**: Retrieves deployment status from Render and updates the corresponding status in the GitHub repository
on the main branch. This ensures that the deployment status in GitHub is always in sync with Render's actual deployment state.
- **Automatic Updates**: The API automatically handles the update process without manual intervention, streamlining the deployment workflow.
- **Easy Configuration**: Simple setup for connecting with GitHub and Render services, with minimal configuration required.

## Tech Stack

Backend:
- [Python](https://www.python.org/)
- [pipenv](https://github.com/pypa/pipenv)

Packages:
- [pytest](https://docs.pytest.org) (Test)
- [request](https://fr.python-requests.org) (HTTP lib)
- [fastapi](https://fastapi.tiangolo.com/) (Framework)

GitHub Action:
- [Lint and Format](https://github.com/Fyleek/render-api/blob/main/.github/workflows/lint_format.yml) (flake8 and black)
- [Tests](https://github.com/Fyleek/render-api/blob/main/.github/workflows/sonar_cloud.yml) (pytest)
- [Sonar Cloud](https://github.com/Fyleek/render-api/blob/main/.github/workflows/tests.yml) (Scan for Bugs, Code Smells, Security Hotspots or Vulnerabilities)

GitHub App:
- [Your Render App [UNOFFICIAL]](#installation-and-creation-of-the-github-app)


## Installation and Setup

Make sure you have Python v3.12.0+ installed on your machine.

1. **Clone the Repository**:   
```git clone https://github.com/Fyleek/render-api.git```  
```cd render-api```
2. **Configure Environment variables**:  
Don't forget to rename your ```tokensExample.json``` to ```token.json```
   - GitHub Token: [Manage access token](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)  
    **⚠️Warning⚠️:** You need to select the following scopes
     - repo
     - workflow
   - Render Token: [Authentication](https://api-docs.render.com/reference/authentication#:~:text=To%20create%20and%20view%20your,or%20team%20directly%20owns%20them)
   - Webhook: [Validating webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
3. **Install Dependencies**:  
```pip install -r requirements.txt```
4. **Start the API**:  
```uvicorn render_api.main:app --host 127.0.0.1 --port 8000```
5. **Configure GitHub Webhook**:
   - [Production](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/using-webhooks-with-github-apps)
   - [Local](https://docs.github.com/en/webhooks/using-webhooks/handling-webhook-deliveries)

## Installation and creation of the GitHub App
| Follow the GitHub [documentation](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app) to create your own App | ![Render-API [UNOFFICIAL]](icon.png) |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------|

## Installating the Postman Collection
To understand or add new features to the API and test its functionalities, I provide a preconfigured Postman request collection.
Follow these simple steps to install and import the collection into your Postman environment:

1.  Download the Collection JSON File:
    -   First, download the JSON file of the collection from the GitHub repository: ```render-api.postman_collection.json```.
2.  Open Postman:
    -   If you haven't already installed Postman, download it from the [official Postman website](https://www.postman.com/downloads/).
    -   Open Postman on your computer.
3.  Import the Collection:
    -   In the left-hand sidebar of Postman, click on the **"Collections"** tab.
    -   Click the **"Import"** button located in the top right corner of the window.
    -   Select the **"Import From File"** option.
    -   Browse and select the JSON file of the collection you downloaded in step 1.
    -   Click the **"Open"** button to import the collection.
4.  Verify the Collection:
    -   Once imported, you should see the new collection in the left-hand sidebar under the **"Collections"** tab. Click on it to open.
5.  Set Up the Environment:
    -   When you click on **"render-api"** folder, then click on **"Variables"**
    -   Then setup **"user"** and **"repo"** value
6.  Set Up the bearer:
    -   When you click on **"GitHub"** folder, then click on **"Authorization"** and past your [GitHub Token](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) inside Token input
    -   When you click on **"Render"** folder, then click on **"Authorization"** and past your [Render Token](https://api-docs.render.com/reference/authentication#:~:text=To%20create%20and%20view%20your,or%20team%20directly%20owns%20them) inside Token input
7.  Execute the Requests:
    -   You can now browse through the different requests within the collection and execute them as needed.
    -   Remember to customize settings such as environment variable values, bearer tokens, ..., according to your configuration.

## Deployment

This project can be easily deployed to [Render](https://render.com/). Simply connect your Render account to your GitHub repository,
and Render will automatically build and deploy your application with each new push to the main branch.

Add the content of `tokens.json` variables to your Render project settings as environment variable.

## Usage
Once the API is running and the webhook is configured, it will automatically respond to deployment-related events from the GitHub repository.
The API fetches the latest deployment status from Render and updates the status in the GitHub repository accordingly.

## Contributing
Contributions to Render-API are welcome!
Please refer to the contributing guidelines for more information on how to submit pull requests, report issues, or request features.

## License
Render-API is licensed under [MIT License](https://mit-license.org/). Feel free to use, modify, and distribute the code as per the license terms.


*Note: This is a non-official API and is not endorsed by GitHub or Render. It is developed and maintained by independent contributors.*