# Informatica Cloud CI/CD Pipeline with GitLab

This project implements a complete CI/CD pipeline for deploying Informatica Cloud assets from a development environment through to production. It is designed to be run within GitLab CI/CD and integrates with Jira for change validation and Nexus for artifact storage.

## How it Works

The pipeline is defined in the `.gitlab-ci.yml` file and consists of the following stages:

1.  **`validate`**: This stage runs automatically on every commit to the `main` branch. It inspects the commit message for a Jira ticket ID (e.g., `PROJ-123`) and calls the Jira API to verify that the ticket is in an "Approved" state. If the ticket is not found or not approved, the pipeline fails.

2.  **`build`**: If the validation stage succeeds, the `build` stage runs. It executes a script that connects to the DEV Informatica Cloud environment and exports the assets defined in `export_assets.json`. The exported assets are packaged into a `informatica_assets.zip` file, which is stored as a GitLab CI artifact.

3.  **`deploy_uat`**: This stage also runs automatically after a successful build on the `main` branch. It takes the `informatica_assets.zip` artifact and deploys it to the UAT environment. After a successful deployment, it uploads the asset package to a Nexus repository for versioning and auditing purposes.

4.  **`deploy_prd`**: This is a **manual** stage. It can only be triggered by a user with appropriate permissions in GitLab. When triggered, it takes the same artifact from the `build` stage and deploys it to the PRD environment. This manual gate ensures that production deployments are always intentional.

## Configuration

To use this pipeline, you must configure the following CI/CD variables in your GitLab project settings (`Settings > CI/CD > Variables`):

### General
*   `CI_COMMIT_MESSAGE`: The commit message. (Provided by GitLab)
*   `CI_MERGE_REQUEST_TITLE`: The merge request title. (Provided by GitLab)
*   `CI_COMMIT_SHORT_SHA`: The short commit SHA. (Provided by GitLab)
*   `CI_PROJECT_NAME`: The project name. (Provided by GitLab)

### Informatica Credentials
*   `IICS_USER`: The username for the Informatica Cloud user. You may need separate users for DEV, UAT, and PRD, in which case you would create variables like `IICS_USER_DEV`, `IICS_USER_UAT`, etc., and modify the scripts accordingly.
*   `IICS_PASSWORD`: The password for the Informatica Cloud user.

### Jira Integration
*   `JIRA_URL`: The base URL of your Jira instance (e.g., `https://your-company.atlassian.net`).
*   `JIRA_USER`: The email address of the user for Jira API access.
*   `JIRA_TOKEN`: The API token for the Jira user.

### Nexus Integration
*   `NEXUS_URL`: The base URL of your Nexus repository manager.
*   `NEXUS_USER`: The username for Nexus access.
*   `NEXUS_PASSWORD`: The password for the Nexus user.

## How to Use

1.  **Update `export_assets.json`**: Before committing, ensure the `export_assets.json` file lists all the Informatica assets you wish to deploy.
2.  **Commit with a Jira Ticket**: Make your changes and commit them with a message that includes the relevant Jira ticket ID. For example:
    ```
    feat: Update sales processing taskflow (PROJ-456)
    ```
3.  **Push to `main`**: Pushing your commit to the `main` branch will automatically trigger the pipeline, which will validate your ticket and deploy to UAT.
4.  **Deploy to Production**: To deploy to production, navigate to the pipeline's page in GitLab and manually trigger the `deploy_to_prd` job.

## Project Structure

*   `.gitlab-ci.yml`: The main configuration file for the GitLab CI/CD pipeline.
*   `requirements.txt`: A list of Python dependencies required by the scripts.
*   `export_assets.json`: A JSON file where you define the list of Informatica assets to be exported and deployed.
*   `scripts/`: A directory containing all the Python automation scripts.
    *   `iics_login.py`: Handles authentication with Informatica Cloud.
    *   `iics_export.py`: Exports assets from the source environment.
    *   `iics_import.py`: Imports assets into the target environment.
    *   `jira_validator.py`: Validates the Jira ticket status.
    *   `nexus_uploader.py`: Uploads the asset package to Nexus.
