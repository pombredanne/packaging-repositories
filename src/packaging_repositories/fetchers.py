#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from .utils import package_names_match


def _is_match(entry, requirement, environment):
    if not package_names_match(entry.name, requirement.name):
        return False
    specifier = requirement.specifier
    if specifier and not specifier.contains(entry.version):
        return False
    marker = requirement.marker
    if marker and not marker.evaluate(environment):
        return False
    return True


class Fetcher(object):
    """Base fetch implementation to apply requirement filtering.
    """
    def __init__(self, repository, requirement, environment=None):
        self.repository = repository
        self.requirement = requirement
        self.environment = environment

    def __repr__(self):
        parts = [
            repr(self.repository.endpoint.value),
            repr(str(self.requirement)),
        ]
        if self.environment:
            parts.append(repr(self.environment))
        return "Fetcher({0})".format(", ".join(parts))

    def __iter__(self):
        return self

    def __aiter__(self):
        return self

    if sys.version_info < (3,):
        def next(self):
            return self.__next__()

    def iter_entries(self, endpoint, source):
        for entry in self.repository.get_entries(endpoint, source):
            if _is_match(entry, self.requirement, self.environment):
                yield entry
