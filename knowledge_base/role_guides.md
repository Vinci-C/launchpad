# Role-Specific Onboarding Guides

## Software Engineer
1. **Local Development Setup:** Install `uv` and Docker, clone the `core-api` repository, and spin up your local PostgreSQL database.
2. **Architecture Review:** Understanding our system design is critical before writing any code. Follow these steps:
   - **Service Map:** We run a microservices architecture. The three core services are `core-api` (REST backend), `data-pipeline` (async event processing via Pub/Sub), and `auth-service` (JWT + OAuth2). Each service has its own PostgreSQL schema.
   - **How requests flow:** A client request hits our API Gateway, which routes to `core-api`. Heavy workloads (e.g. report generation) are offloaded to the `data-pipeline` service via a Pub/Sub topic. Understand this path before touching any endpoint code.
   - **Codebase conventions:** We follow Domain-Driven Design (DDD). Each service has a `domain/`, `application/`, and `infrastructure/` layer. Business logic lives only in `domain/`. Read `CONTRIBUTING.md` in the repo root for the full coding standards.
   - **Your task:** Sketch a quick diagram (even on paper) of how a user login request travels from the browser through to the database. Share it with your engineering buddy for a quick sanity check.
3. **First Commits:** Pick up a "good first issue" from the Jira backlog to get familiar with our CI/CD pipeline.
4. **AWS IAM Setup - MFA:** Multi-factor authentication is mandatory for all AWS accounts. Follow these steps:
   - **Root account:** Go to the AWS Console → your account name (top right) → Security Credentials. Under "Multi-factor authentication (MFA)", click "Assign MFA device". Use a virtual authenticator app (e.g. Google Authenticator or Authy). Never use the root account for day-to-day work.
   - **IAM user MFA:** Navigate to IAM → Users → your username → Security credentials tab → "Assign MFA device". Follow the same virtual MFA setup. You must scan the QR code with your authenticator app and enter two consecutive OTP codes to confirm.
   - **Verify:** Log out and log back in. You should be prompted for your MFA code after entering your password. If not, contact the DevOps team.
   - **Your task:** Confirm MFA is active by checking your user's Security Credentials tab shows a green "Assigned" status next to MFA.

5. **AWS IAM Setup - Federation:** We use federated identity so you never need long-term IAM user credentials for AWS access. Here's how to get set up:
   - **How it works:** Our company uses Google Workspace as the Identity Provider (IdP). AWS is configured to trust it via IAM Identity Center (SSO). You log in with your Google account and receive temporary AWS credentials automatically — no access keys stored on your machine.
   - **Accessing AWS:** Go to our internal SSO portal (ask your manager for the URL). Log in with your `@company.com` Google account. You will see a list of AWS accounts and roles you have permission to assume. Click the role to launch the console or copy temporary CLI credentials.
   - **CLI setup:** Run `aws configure sso` in your terminal. When prompted, enter the SSO start URL and region provided by DevOps. After authenticating in your browser, your `~/.aws/config` will be updated automatically.
   - **Your task:** Successfully log into AWS via the SSO portal and confirm you can see the `dev` account listed. Run `aws sts get-caller-identity` in your terminal to verify your temporary credentials are working.

6. **AWS IAM Setup - Workload Roles:** Your local services and scripts must never use your personal credentials. Follow this process:
   - **Why roles?** Hardcoding access keys in code or `.env` files is a critical security violation. If a key leaks, it can expose the entire AWS account. IAM roles issue short-lived credentials that rotate automatically.
   - **Local development:** For local dev, use the temporary credentials from your SSO session (see federation step). Set the `AWS_PROFILE` environment variable in your `.env` file to the profile name created by `aws configure sso` (e.g. `AWS_PROFILE=dev-developer`). The AWS SDK will automatically pick this up.
   - **CI/CD pipelines:** Do not add AWS keys to GitHub secrets. Instead, our GitHub Actions workflows use OIDC federation to assume a deployment IAM role directly. This is already configured — do not alter the workflow YAML files without DevOps approval.
   - **Your task:** Open your local `.env` and confirm you are using `AWS_PROFILE` rather than `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. If you see hardcoded keys, remove them immediately and switch to the profile method.

7. **AWS IAM Setup - Least Privilege:** You should only have the permissions you absolutely need. Follow these guidelines:
   - **Check your permissions:** In the AWS Console, go to IAM → Users (or the role you assumed) → Permissions tab. Review what policies are attached. If you see `AdministratorAccess` or `*` wildcards on sensitive resources and they don't match your job role, flag this to the DevOps team.
   - **Requesting new permissions:** If you need access to a service not currently in your role (e.g. S3 bucket access for a new feature), open a Jira ticket in the `INFRA` project using the "IAM Access Request" template. Do NOT attempt to grant yourself permissions.
   - **Temporary elevated access:** For one-off tasks requiring higher privileges, use the "break-glass" process: request a time-boxed role assumption via the `#devops-access` Slack channel. All break-glass sessions are logged and audited.
   - **Your task:** Review your current IAM permissions and confirm with the DevOps team that they match the least-privilege principle for a Software Engineer on your team.

## Product Manager
1. **Product Roadmap:** Review the Q3/Q4 product roadmap and strategic objectives on Notion.
2. **Jira Access:** Request access to the primary Jira boards and review the current sprint backlog.
3. **Stakeholder Meet & Greet:** Schedule 15-minute 1:1s with the Engineering Manager, Design Lead, and Marketing Director.
4. **Analytics Dashboard:** Get access to Mixpanel to review our core user retention metrics.

## Data Scientist
1. **Data Warehouse Access:** Request read access to the BigQuery staging and production environments.
2. **Jupyter Setup:** Install the company-approved Anaconda distribution and set up your local Jupyter environment.
3. **Model Registry:** Review our MLflow dashboard to understand our currently deployed predictive models.
4. **Data Privacy Training:** Complete the strict data privacy and compliance training.

## HR Specialist
1. **Workday Admin Setup:** Complete the Workday administrative onboarding to manage employee records.
2. **Benefits Provider Sync:** Review the contact sheets for our healthcare, 401(k), and wellness vendors.
3. **Interview Training:** Complete our inclusive hiring and interview best practices module.
4. **Onboarding Buddy:** Familiarize yourself with the Launchpad system to assist other new hires!

## Sales Representative
1. **Salesforce Setup:** Log into Salesforce and complete your profile setup.
2. **Product Demo Training:** Watch the top 3 recorded product demos from last quarter.
3. **Territory Assignment:** Meet with the Regional Director to receive your account list.
4. **Pitch Deck Review:** Study the Q3 master pitch deck and prepare to deliver a mock pitch by the end of week 2.
