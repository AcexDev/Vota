from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist

@receiver(post_save, sender=User)
def create_or_save_profile(sender, instance, created, **kwargs):
    #  """Automatically create a Profile when a new User is created,
    # and save the Profile whenever the User is saved."""
    if created:
        #If user is new, create profile
        Profile.objects.create(user=instance)

    else:
        try:
            #if user already exists, save the profile
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)


    


def extract_social_data(sociallogin):
    data = sociallogin.account.extra_data
    email = data.get("email")
    full_name = data.get("name") or ""
    first_name = full_name.split(" ")[0] if full_name else ""
    last_name = " ".join(full_name.split(" ")[1:]) if len(full_name.split()) > 1 else ""
    avatar = data.get("picture")

    return {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "avatar": avatar
    }

# Handling User SIGNuP
@receiver(user_signed_up)
def populate_user_data(request, user, **kwargs):
    sociallogin = kwargs.get("sociallogin")
    if not sociallogin:
        return
    
    info = extract_social_data(sociallogin)

    profile = getattr(user, "profile", None)
    if profile and info["avatar"]:
        profile.avatar = info["avatar"]
        profile.save()

# @receiver(social_account_added)
# def update_user_data_on_social_link(request, sociallogin, **kwargs):
#     user = sociallogin.user
#     info = extract_social_data(sociallogin)    

#     if not user.first_name and info["first_name"]:
#         user.first_name = info["first_name"]
#     if not user.last_name and info["last_name"]:
#         user.last_name = info["last_name"]

#     if not user.email and info["email"]:
#         user.email = info["email"]

#     user.save()

#     profile = getattr(user, 'profile', None)

#     if profile and info["avatar"]:
#         profile.avatar = info["avatar"]
#         profile.save()


