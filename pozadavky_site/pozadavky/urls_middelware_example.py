from django.urls import path
from . import views
from sqlite3.test.factory import RowFactoryTestsBackwardsCompat

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.home_page, name='home_page'),
    path('detail<int:requirement_id>/', views.detail, name='detail'),
    path('<int:requirement_id>/results/', views.results, name='results'),
    path('<int:requirement_id>/requirement/', views.requirement, name='requirement'),
]

"""
	https://docs.djangoproject.com/en/4.2/topics/http/middleware/#writing-your-own-middleware.
	V zásadě by stačil jednoduchý middleware:
"""


from app.nejaky_package import ctx

class SimpleMiddleware:
     def __init__(self, get_response):
         self.get_response = get_response
     def __call__(self, request):
        token = ctx.current_user.set(request.user)
        try:
             response = self.get_response(request)
        finally:
             ctx.current_user.reset(token)
        return response

"""
	Middleware ti aktuálního usera uloží do context proměnné current_user.
	Context proměnná je threadově i asyncio bezpečné uložení nějaké hodnoty,
	kterou v rámci procesu vidí jen to vlákno nebo coroutina, co si to
	uložila, viz https://docs.python.org/3/library/contextvars.html. V
	app/nejaky_package/ctx.py bude:
"""

from contextvars import ContextVar

current_user = ContextVar('current_user')


"""
    A tam, kde potřebuješ hodnotu přečíst, budeš mít:
"""


from app.nejaky_package import ctx

class NejakyModel(Model):
    ...
    def save(kwaqrd):
        user = ctx.current_user.get()
        if user.is_authenticated:
            self.created_by = user
        super().save(...)

"""
	Jen pozor, user může být i AnonymousUser, pokud nikdo není přihlášený,
	tak si to raději ošetřit.
"""
