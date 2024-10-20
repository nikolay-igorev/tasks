from rest_framework.routers import DefaultRouter

from books.views import AuthorViewSet, BookViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, 'author')
router.register(r'books', BookViewSet, 'book')

urlpatterns = router.urls