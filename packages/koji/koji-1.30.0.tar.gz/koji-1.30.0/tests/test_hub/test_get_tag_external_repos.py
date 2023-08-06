import unittest

import mock

import kojihub

QP = kojihub.QueryProcessor


class TestGetTagExternalRepos(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.get_tag = mock.patch('kojihub.get_tag').start()
        self.get_external_repo = mock.patch('kojihub.get_external_repo').start()
        self.exports = kojihub.RootExports()
        self.context = mock.patch('kojihub.context').start()
        self.cursor = mock.MagicMock()
        self.QueryProcessor = mock.patch('kojihub.QueryProcessor',
                                         side_effect=self.getQuery).start()
        self.queries = []
        self.build_tag = 'tag'
        self.repo = 'repo_name'
        self.build_tag_info = {'id': 111, 'name': self.build_tag}
        self.repo_info = {'id': 123, 'name': self.repo}

    def tearDown(self):
        mock.patch.stopall()

    def getQuery(self, *args, **kwargs):
        query = QP(*args, **kwargs)
        query.execute = mock.MagicMock()
        query.executeOne = mock.MagicMock()
        self.queries.append(query)
        return query

    def test_valid(self):
        self.get_tag.return_value = self.build_tag_info
        self.get_external_repo.return_value = self.repo_info
        kojihub.get_tag_external_repos(tag_info=self.build_tag, repo_info=self.repo)
        self.assertEqual(len(self.queries), 1)
        query = self.queries[0]
        self.assertEqual(query.tables, ['tag_external_repos'])
        self.assertEqual(query.joins, [
            'tag ON tag_external_repos.tag_id = tag.id',
            'external_repo ON tag_external_repos.external_repo_id = external_repo.id',
            'external_repo_config ON external_repo.id = external_repo_config.external_repo_id'])
        self.assertEqual(query.clauses,
                         ['(external_repo_config.active = TRUE)',
                          '(tag_external_repos.active = TRUE)',
                          'external_repo.id = %(repo_id)i', 'tag.id = %(tag_id)i'])
