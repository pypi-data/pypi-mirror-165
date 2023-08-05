__all__ = ('OA2Access', )

import warnings
from datetime import datetime, timedelta
from time import time as time_now

from scarletio import RichAttributeErrorBaseType

from .helpers import OAUTH2_SCOPES


class OA2Access(RichAttributeErrorBaseType):
    """
    Represents a Discord oauth2 access object, what is returned by ``Client.activate_authorization_code`` if
    activating the authorization code went successfully.
    
    Attributes
    ----------
    access_token : `str`
        Token used for `Bearer` authorizations, when requesting OAuth2 data about the respective user.
    created_at : `datetime`
        The time when the access was last created or renewed.
    expires_after : `int`
        The time in seconds after this access expires.
    redirect_url : `str`
        The redirect url with what the user granted the authorization code for the oauth2 scopes for the application.
        
        Can be empty string if application's owner's access was requested.
    refresh_token : `str`
        The token used to renew the access token.
        
        Can be empty string if application's owner's access was requested.
    scopes : `set` of `str`
        A set of the scopes, what the user granted with the access token.
    
    Class Attributes
    ----------------
    TOKEN_TYPE : `str` = `'Bearer'`
        The access token's type.
    """
    TOKEN_TYPE = 'Bearer'
    
    __slots__ = ('access_token', 'created_at', 'expires_after', 'redirect_url', 'refresh_token', 'scopes',)
    
    def __init__(self, data, redirect_url):
        """
        Creates an ``OA2Access``.
        
        Parameters
        ----------
        data : `dict` of (`str`, `Any`) items
            Received access data.
        redirect_url : `str`
            The redirect url with what the user granted the authorization code for the oauth2 scopes for the
            application.
        """
        self.redirect_url = redirect_url
        self.access_token = data['access_token']
        self.refresh_token = data.get('refresh_token', '')
        self.expires_after = data['expires_in'] # default is 604800 (s) (1 week)
        self.scopes = scopes = set()
        for scope in data['scope'].split():
            scope = OAUTH2_SCOPES.get(scope, scope)
            scopes.add(scope)
        
        self.created_at = datetime.utcnow() # important for renewing
    
    
    def _renew(self, data):
        """
        Renews the access with the given data.
        
        Parameters
        ----------
        data : `None` or (`dict` of (`str`, `Any`))
            Requested access data.
        """
        self.created_at = datetime.utcnow()
        if data is None:
            return
        
        self.access_token = data['access_token']
        self.refresh_token = data.get('refresh_token', '')
        self.expires_after = data['expires_in']
        scopes = self.scopes
        scopes.clear()
        for scope in data['scope'].split():
            try:
                scopes.add(OAUTH2_SCOPES[scope])
            except KeyError:
                pass
    
    
    @property
    def expires_in(self):
        """
        `.expires_in` is deprecated and will be removed in 2022 Jul. Please use ``.expires
        """
        warnings.warn(
            (
                f'`{self.__class__.__name__}.expires_in` is deprecated, and '
                f'will be removed in 2022 Jul. Please use `.expires_after` instead.'
            ),
            FutureWarning,
            stacklevel = 2,
        )
        return self.expires_after
    
    
    @property
    def expires_at(self):
        """
        Returns when the access expires.
        
        Returns
        -------
        expires_at : `datetime`
        """
        return self.created_at + timedelta(seconds=self.expires_after)
    
    
    def __repr__(self):
        """Returns the representation of the achievement."""
        repr_parts = ['<', self.__class__.__name__]
        
        if self.created_at.timestamp() + self.expires_after > time_now():
            state = 'active'
        else:
            state = 'expired'
        
        repr_parts.append(' ')
        repr_parts.append(state)
        
        repr_parts.append('scope count=')
        repr_parts.append(str(len(self.scopes)))
        
        repr_parts.append('>')
        
        return ''.join(repr_parts)
