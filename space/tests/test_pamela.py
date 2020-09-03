import pytest
import re

from space.helpers import should_keep
from django.conf import settings


def test_should_keep():
    # Test if the qemu regex is in config it should not keep it

    qemu = "52:54:00:dd:6f:15"
    regexes = settings.IGNORE_LIST_RE

    if regexes:
        if regexes[0].match(qemu):
            assert not should_keep(qemu)

    # Should keep a random address
    assert should_keep("c2:86:1d:23:0e:36")

    # Add the vmware regex to the config and verify it should not be kept
    settings.IGNORE_LIST_RE.append(re.compile(r'00:50:56(:[0-9a-f]{2}){3}'))
    assert not should_keep("00:50:56:c5:ec:19")
