from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAdapter(DefaultSocialAccountAdapter):
    def populate_self(self, request, sociallogin, data):
        user = super().populate_self(request, sociallogin, data)

        extra = sociallogin.account.extra_data

        user.email = extra.get("email", "")
        user.first_name = extra.get("given_name", "")
        user.last_name = extra.get("family_name", "")
        return user
