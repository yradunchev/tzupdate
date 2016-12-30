#!/usr/bin/env python2

import httpretty
import tzupdate
import mock
from nose.tools import assert_false
from tests._test_utils import (FAKE_SERVICES, FAKE_TIMEZONE,
                               setup_basic_api_response)


@httpretty.activate
@mock.patch('tzupdate.link_localtime')
def test_end_to_end_no_args(link_localtime_mock):
    setup_basic_api_response()
    args = []
    tzupdate.main(args, services=FAKE_SERVICES)
    link_localtime_mock.assert_called_once_with(
        FAKE_TIMEZONE, tzupdate.DEFAULT_ZONEINFO_PATH,
        tzupdate.DEFAULT_LOCALTIME_PATH,
    )


@httpretty.activate
@mock.patch('tzupdate.link_localtime')
def test_print_only_no_link(link_localtime_mock):
    setup_basic_api_response()
    args = ['-p']
    tzupdate.main(args, services=FAKE_SERVICES)
    assert_false(link_localtime_mock.called)


@httpretty.activate
@mock.patch('tzupdate.link_localtime')
def test_explicit_paths(link_localtime_mock):
    setup_basic_api_response()
    localtime_path = '/l'
    zoneinfo_path = '/z'
    args = ['-l', localtime_path, '-z', zoneinfo_path]
    tzupdate.main(args, services=FAKE_SERVICES)
    link_localtime_mock.assert_called_once_with(
        FAKE_TIMEZONE, zoneinfo_path, localtime_path,
    )


@httpretty.activate
@mock.patch('tzupdate.link_localtime')
def test_explicit_ip(_):
    setup_basic_api_response()
    ip_addr = '1.2.3.4'
    args = ['-a', ip_addr]
    tzupdate.main(args, services=FAKE_SERVICES)

    # TODO (#16): httpretty.last_request() and
    # get_timezone_for_ip.assert_called_once_with don't work for testing here
    # because of the threading we use. We need to work out a good solution for
    # this in


@mock.patch('tzupdate.link_localtime')
def test_explicit_timezone(link_localtime_mock):
    timezone = 'Foo/Bar'
    args = ['-t', timezone]
    tzupdate.main(args)
    link_localtime_mock.assert_called_once_with(
        timezone,
        tzupdate.DEFAULT_ZONEINFO_PATH, tzupdate.DEFAULT_LOCALTIME_PATH,
    )
