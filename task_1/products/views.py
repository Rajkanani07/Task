from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import ProductSerializer
from .models import Product_Details
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    # POST Method
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Product created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # GET Method
    def get(self, request):
    # Get query parameters for filtering
        product_name = request.query_params.get('product_name', None)
        category = request.query_params.get('category', None)
        colour = request.query_params.get('colour', None)

        # Start with all products
        products = Product_Details.objects.all()

        # Apply filters if provided
        if product_name:
            products = products.filter(product_name__icontains=product_name)
        if category:
            products = products.filter(category__icontains=category)
        if colour:
            products = products.filter(colour__icontains=colour)


        # Serialize the filtered product data
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #PUT Method
    def put(self, request, *args, **kwargs):
        product_name = request.query_params.get('product_name')
        if product_name:
            try:
                product = Product_Details.objects.get(product_name=product_name)
                serializer = ProductSerializer(product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message": "product updated successfully"}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Product_Details.DoesNotExist:
                return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Please provide a product_name query parameter"}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE Method
    def delete(self, request, *args, **kwargs):
            product_name = request.query_params.get('product_name')
            if product_name:
                try:
                    product = Product_Details.objects.get(product_name=product_name)
                    product.delete()
                    return Response({"message": "product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
                except Product_Details.DoesNotExist:
                    return Response({"error": "product not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Please provide a product_name query parameter"}, status=status.HTTP_400_BAD_REQUEST)
            