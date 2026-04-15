from rest_framework import viewsets, status
from rest_framework.response import Response
from django.conf import settings
from azure.cosmos import CosmosClient
# Keep your serializer if you want to use it for validation later
from .serializers import PostSerializer 

# Initialize Cosmos Client
client = CosmosClient(settings.COSMOS_ENDPOINT, settings.COSMOS_KEY)
database = client.get_database_client(settings.COSMOS_DATABASE_NAME)
container = database.get_container_client(settings.COSMOS_CONTAINER_NAME)

class PostViewSet(viewsets.ViewSet): # Changed from ModelViewSet to ViewSet
    lookup_field = 'id'
    def list(self, request):
        query = "SELECT * FROM c ORDER BY c.created_at DESC"
        # Cosmos returns a proxy object, list() converts it to a real list
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return Response(items)
    
    def retrieve(self, request, id=None):
        """Handle GET /api/posts/{id}/"""
        author = request.query_params.get('author')
        if not author:
            return Response(
                {"error": "Partition key 'author' is required as a query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            item = container.read_item(item=id, partition_key=author)
            return Response(item)
        except Exception:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, id=None):
        """Handle DELETE /api/posts/{id}/"""
        author = request.query_params.get('author')
        if not author:
            return Response(
                {"error": "Partition key 'author' is required as a query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            container.delete_item(item=id, partition_key=author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response({"error": "Failed to delete"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        data = request.data
        # Ensure the item has an 'id' (Cosmos NoSQL requires a string id)
        if 'id' not in data:
            import uuid
            data['id'] = str(uuid.uuid4())
            
        container.create_item(body=data)
        return Response(data, status=status.HTTP_201_CREATED)