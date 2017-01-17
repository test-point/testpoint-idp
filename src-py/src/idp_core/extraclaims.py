import logging

from oidc_provider.lib.claims import ScopeClaims


class AbnScopeClaims(ScopeClaims):
    """
    Just pass whole extra_data (with abn and other random stuff).
    self.user is accessible here.
    for you custom application claim may have custom namespace prefix, it's okay.
    """

    def create_response_dic(self):
        try:
            extra_data = self.user.business.get_extra_data()
            return extra_data
        except Exception as e:
            logging.exception(e)
            return {}
