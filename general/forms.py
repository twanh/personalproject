from django import forms
from django.core.mail import EmailMessage

# Contact form
class ContactForm(forms.Form):

    contact_name = forms.CharField(required=True, label='Your Name')
    contact_email = forms.EmailField(required=True, label='Your Email')
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'wid': 'True'}),
        label='Your Message'
    )
   
    def send_email(self):
        # Confirm
        msg = EmailMessage('Message has been send!',
                 'Your contact request has been send!',
                 to=self.contact_email,
                  from_email='huiskenstwan@gmail.com')
        msg.send()

        # Send req
        msg = EmailMessage('New contact req!',
                 'Request from: {}, {}\n message:{}'.format(self.contact_name,
                                             self.contact_email, 
                                             self.content),
                 to='huiskenstwan@gmail.com',
                  from_email='huiskenstwan@gmail.com')
        msg.send()

