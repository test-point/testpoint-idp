from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class OurAllauthSocialAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super(OurAllauthSocialAdapter, self).populate_user(
            request, sociallogin, data
        )
        # set username like github_3278237 or facebook_4737347347
        # it's unique and formal
        user.username = u"{}_{}".format(
            sociallogin.account.provider,
            sociallogin.account.uid,
        )
        return user


def user_email_display(user):
    if user.socialaccount_set.exists():
        acc1 = user.socialaccount_set.all()[0]
        if 'login' in acc1.extra_data:
            return u'{}@{}'.format(acc1.extra_data.get('login'), acc1.provider)
    return user.email or (user.first_name + ' ' + user.last_name).strip() or user.username
