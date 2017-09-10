from django.conf.urls import url

from sharing.views import proposal_email

urlpatterns = [

    # Send Proposal Email
    # proposal_email - sharing:proposal_email
    # /sharing/proposal/
    url(r'^proposal$', proposal_email, name='proposal_email')
]
