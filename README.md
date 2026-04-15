# Django REST Blog API (Azure Cosmos DB)
A robust RESTful API built with Django REST Framework and Azure Cosmos DB (NoSQL), deployed via Azure App Service.

## 🚀 Features
- Full CRUD: Create, Read, Update, and Delete blog posts.

- Cloud Native: Powered by Azure Cosmos DB using the azure-cosmos Python SDK.

- Production Ready: Configured for Azure App Service with Gunicorn and environment variable management.

## 🛠️ Prerequisites
- Python 3.11+

- Azure CLI

- An active Azure Subscription

- An Azure Cosmos DB (NoSQL) account

## 💻 Local Setup
### 1. Clone the repository:
```Bash
git clone <your-repo-url>
cd django-blog-api
```
### 2. Create a Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 3. Install Dependencies:
```
Bash
pip install -r requirements.txt
```
### 4. Environment Variables:
```bash
COSMOS_URI="https://<your-account>.documents.azure.com:443/"
COSMOS_KEY="<your-primary-key>"
COSMOS_DATABASE="blogdb"
COSMOS_CONTAINER="posts"
DJANGO_SECRET_KEY="your-local-secret"
```
### 5. Run Locally:
   ```bash
   python manage.py runserver
   ```

## ☁️ Azure Deployment

#### 1. Configure the Web App
Ensure your Azure App Service has the following Application Settings (Configuration) set in the Azure Portal:

- COSMOS_URI, COSMOS_KEY, COSMOS_DATABASE, COSMOS_CONTAINER

- DJANGO_SECRET_KEY

- SCM_DO_BUILD_DURING_DEPLOYMENT = true

#### 2. Deploy via Azure CLI
Use the Zip deployment method to avoid Windows file-locking issues:

```Bash
# Create a deployment zip (excluding venv)
Compress-Archive -Path * -Exclude venv -DestinationPath deploy.zip

# Deploy
az webapp deploy --resource-group <YourRG> --name <YourAppName> --src-path deploy.zip --type zip
```
## 📡 API Endpoints
| Method| Endpoint| Description|
| --------| --------| -------------|
| GET| /posts| Retrieve all Blog posts|
| POST| /posts| Create a new Blog post|
| GET| /posts/id/?author=authorname| Retrieve a specific post|
| DELETE| /posts/id/?author=authorname| Remove a specific Blog post|

### Example POST Body:
```JSON
{
    "title": "Azure Deployment",
    "content": "Deploying Django to App Service.",
    "author": "CloudDev"
}
```

## 📖 License
MIT License. 
