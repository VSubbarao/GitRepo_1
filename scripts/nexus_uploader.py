import os
import requests
import sys

def upload_to_nexus():
    """
    Uploads an artifact to a Nexus repository.
    """
    print("Starting Nexus upload process...")

    nexus_url = os.environ.get("NEXUS_URL")
    nexus_user = os.environ.get("NEXUS_USER")
    nexus_password = os.environ.get("NEXUS_PASSWORD")
    # This is a GitLab CI/CD predefined variable
    commit_sha = os.environ.get("CI_COMMIT_SHORT_SHA", "local-dev")

    if not all([nexus_url, nexus_user, nexus_password]):
        print("Error: NEXUS_URL, NEXUS_USER, and NEXUS_PASSWORD environment variables must be set.")
        sys.exit(1)

    artifact_file = "informatica_assets.zip"
    if not os.path.exists(artifact_file):
        print(f"Error: Artifact file '{artifact_file}' not found.")
        sys.exit(1)

    # This assumes a 'raw' Nexus repository named 'informatica-artifacts'.
    # The path will be /<repo_name>/<group>/<artifact_name>/<version>/<file_name>
    # We can use the GitLab project name for the group.
    project_name = os.environ.get("CI_PROJECT_NAME", "local-project")
    repo_name = "informatica-artifacts"
    version = commit_sha

    # Example URL: http://nexus.example.com/repository/informatica-artifacts/my-project/informatica_assets/a1b2c3d4/informatica_assets.zip
    upload_url = f"{nexus_url}/repository/{repo_name}/{project_name}/informatica_assets/{version}/{artifact_file}"

    print(f"Uploading '{artifact_file}' to Nexus at: {upload_url}")

    try:
        with open(artifact_file, "rb") as f:
            response = requests.put(
                upload_url,
                auth=(nexus_user, nexus_password),
                data=f
            )
            response.raise_for_status()

        print("Artifact uploaded successfully to Nexus.")
        print(f"You can find the artifact at: {upload_url}")

    except requests.exceptions.RequestException as e:
        print(f"Error uploading to Nexus: {e}")
        if e.response:
            print(f"Response: {e.response.text}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Could not open artifact file '{artifact_file}'.")
        sys.exit(1)

if __name__ == "__main__":
    # For local testing, you would need to set the environment variables:
    # NEXUS_URL, NEXUS_USER, NEXUS_PASSWORD
    # And also create a dummy 'informatica_assets.zip' file.
    print("--- SIMULATION MODE ---")
    if not os.path.exists("informatica_assets.zip"):
        print("Creating dummy artifact 'informatica_assets.zip' for local testing.")
        with open("informatica_assets.zip", "w") as f:
            f.write("This is a dummy zip file.")

    print("Would upload 'informatica_assets.zip' to Nexus.")
    # upload_to_nexus()
    print("Simulation complete.")
    sys.exit(0)
