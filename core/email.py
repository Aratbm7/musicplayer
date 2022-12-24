# from djoser.email import ActivationEmail as BaseActivationEmail
# from djoser.email import ConfirmationEmail as BaseConfrimationEmail
# from django.conf import settings
# from rest_framework_simplejwt.tokens import AccessToken
# class ActivationEmail(BaseActivationEmail):

#     template_name = "email/activation.html"

#     def get_context_data(self):
#             # ActivationEmail can be deleted
#             context = super().get_context_data()

#             user = context.get("user")
            
#             # context["token"] = 'JWT' + str(AccessToken.for_user(user))
#             context["token"] = default_token_generator.make_token(user)

#             context["url"] = settings.DJOSER['ACTIVATION_URL'].format(**context)
#             return context

# class ConfirmationEmail(BaseConfrimationEmail):
#     template_name = "email/confrimation.html"

