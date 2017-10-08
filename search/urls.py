from django.conf.urls import url

from search.views import ListSearch

urlpatterns = [

    # Send Proposal Email
    # proposal_email - sharing:proposal_email
    # /sharing/proposal/
    url(r'^$', ListSearch.as_view(), name='main')
]
