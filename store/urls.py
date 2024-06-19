from django.urls import path, include
from rest_framework_nested import routers
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet, CartViewSet, CartItemViewSet

# Create a router for the main API endpoints
router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet, basename='carts')

# Create a nested router for CartItemViewSet under carts/<cart_pk>/items/
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

# Create a nested router for ReviewViewSet under products/<product_pk>/reviews/
products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', ReviewViewSet, basename='product-reviews')

# Combine all the URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(cart_router.urls)),
]
