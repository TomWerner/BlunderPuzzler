from django.conf.urls import url

from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

from puzzler import views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', views.home),
    url(r'^admin/', admin.site.urls),
    url(r'^add/', views.add_annotated_pgn),

    # Default django stuff
    url(r'^(?i)accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^(?i)accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^(?i)accounts/$', RedirectView.as_view(url='/')),

]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
