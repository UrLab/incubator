import hashlib
from collections import OrderedDict
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare
from django.contrib.auth.hashers import mask_hash


class MediaWikiHasher(BasePasswordHasher):
    """
    Returns hashes as stored in a `MediaWiki <https://www.mediawiki.org>`_ user
    database. If salt is a string, the hash returned is the md5 hash of a
    concatenation of the salt, a dash ("-"), and the md5 hash of the password,
    otherwise it is identical to a plain md5 hash of the password.

    Please see the `official documentation
    <http://www.mediawiki.org/wiki/Manual:User_table#user_password>`_ for exact
    details.
    """

    algorithm = 'mediawiki'

    def salt(self):
        return get_random_string(8)

    def encode(self, password, salt=None):
        hash = self._encode(password, salt=salt)
        if salt is None:  # pragma: no cover
            return '%s$$%s' % (self.algorithm, hash)
        else:
            return '%s$%s$%s' % (self.algorithm, salt, hash)

    def _encode(self, password, salt=None):  # pragma: py3
        password = bytes(password, 'utf-8')

        if salt is None or salt == '':  # pragma: no cover
            return hashlib.md5(password).hexdigest()
        else:
            secret_hash = hashlib.md5(password).hexdigest()
            message = bytes('%s-%s' % (salt, secret_hash), 'utf-8')
            return hashlib.md5(message).hexdigest()

    def verify(self, password, encoded):
        algorithm, salt, hash = encoded.split('$', 3)
        if len(salt) == 0:  # pragma: no cover
            return constant_time_compare(encoded, self.encode(password, None))
        else:
            return constant_time_compare(encoded, self.encode(password, salt))

    def safe_summary(self, encoded):  # pragma: no cover
        algorithm, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return OrderedDict([
            ('algorithm', algorithm),
            ('salt', mask_hash(salt)),
            ('hash', mask_hash(hash)),
        ])
