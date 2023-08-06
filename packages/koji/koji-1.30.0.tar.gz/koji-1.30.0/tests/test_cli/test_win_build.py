from __future__ import absolute_import

import mock
from six.moves import StringIO

import koji
from koji_cli.commands import handle_win_build
from . import utils


class TestWinBuild(utils.CliTestCase):
    def setUp(self):
        self.options = mock.MagicMock()
        self.options.debug = False
        self.session = mock.MagicMock()
        self.session.getAPIVersion.return_value = koji.API_VERSION
        self.target = 'test-target'
        self.dest_tag = 'destination-test_tag'
        self.target_info = {'build_tag': 4,
                       'build_tag_name': 'test_tag',
                       'dest_tag': 5,
                       'dest_tag_name': self.dest_tag,
                       'id': 2,
                       'name': self.target}
        self.scm_url = 'git://test.redhat.com/rpms/pkg-1.1.0' \
                    '?#3fab2ea42ecdc30a41daf1306154dfa04c4d64fd'
        self.vm = 'test-vm'

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_win_build_without_option(self, stderr):
        expected = "Usage: %s win-build [options] <target> <URL> <VM>\n" \
                   "(Specify the --help global option for a list of other help options)\n\n" \
                   "%s: error: Exactly three arguments (a build target, a SCM URL, " \
                   "and a VM name) are required\n" % (self.progname, self.progname)
        with self.assertRaises(SystemExit) as ex:
            handle_win_build(self.options, self.session, [])
        self.assertExitCode(ex, 2)
        self.assert_console_message(stderr, expected)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_win_build_non_exist_build_target(self, stderr):
        expected = "Usage: %s win-build [options] <target> <URL> <VM>\n" \
                   "(Specify the --help global option for a list of other help options)\n\n" \
                   "%s: error: No such build target: %s\n" % (self.progname, self.progname,
                                                              self.target)
        self.session.getBuildTarget.return_value = None
        with self.assertRaises(SystemExit) as ex:
            handle_win_build(self.options, self.session, [self.target, self.scm_url, self.vm])
        self.assertExitCode(ex, 2)
        self.assert_console_message(stderr, expected)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_win_build_non_exist_dest_tag(self, stderr):
        expected = "Usage: %s win-build [options] <target> <URL> <VM>\n" \
                   "(Specify the --help global option for a list of other help options)\n\n" \
                   "%s: error: No such destination tag: %s\n" % (self.progname, self.progname,
                                                                 self.dest_tag)
        self.session.getBuildTarget.return_value = self.target_info
        self.session.getTag.return_value = None
        with self.assertRaises(SystemExit) as ex:
            handle_win_build(self.options, self.session, [self.target, self.scm_url, self.vm])
        self.assertExitCode(ex, 2)
        self.assert_console_message(stderr, expected)

    @mock.patch('sys.stderr', new_callable=StringIO)
    def test_handle_build_dest_tag_locked(self, stderr):
        expected = "Usage: %s win-build [options] <target> <URL> <VM>\n" \
                   "(Specify the --help global option for a list of other help options)\n\n" \
                   "%s: error: Destination tag %s is locked\n" % (self.progname, self.progname,
                                                                 self.dest_tag)
        dest_tag_info = {'name': self.dest_tag, 'locked': True}

        self.session.getBuildTarget.return_value = self.target_info
        self.session.getTag.return_value = dest_tag_info
        with self.assertRaises(SystemExit) as ex:
            handle_win_build(self.options, self.session, [self.target, self.scm_url, self.vm])
        self.assertExitCode(ex, 2)
        self.assert_console_message(stderr, expected)
