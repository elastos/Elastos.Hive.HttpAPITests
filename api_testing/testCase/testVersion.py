import unittest,sys,json
sys.path.append("../")
from function.func import *
from function.ela_log import MyLog

import read_conf

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

b = read_conf.ReadData()
api = b.get_version("api")
normal_response_body = b.get_version("normal_response_body")

number_param_r = b.get_version("number_param_r")
number_param_e = b.get_version("number_param_e")
commit_param_r = b.get_version("commit_param_r")
commit_param_e = b.get_version("commit_param_e")
repo_param_r = b.get_version("repo_param_r")
repo_param_e = b.get_version("repo_param_e")
all_param_r = b.get_version("all_param_r")
all_param_e = b.get_version("all_param_e")
combined_parameters = b.get_version("combined_parameters")

log = MyLog.get_log()
logger = log.get_logger()


class Version(unittest.TestCase):
    '''
    # 2019-01-02
    Show cluster version information.

    Arguments

    Arguments	Type	Required	Description
    number	bool	no	Only show the version number.
    commit	bool	no	Only show the commit version number.
    repo	bool	no	Only show the repo version number.
    all	bool	no	Only show all version strings.
    HTTP Response

    Argument	Type	Required	Description
    http error	integer	yes	error code.
    http body	Json	no	Json string is following
    On success, the call to this endpoint will return with 200 and the following body:

    {
        "data": {
            "Version": "<string>",
            "Commit": "<string>",
            "Repo": "<string>",
            "System": "<string>",
        },
        "desciption": "<string>"
    }

    '''

    def __init__(self, methodName='runTest'):
        self.f = ConfigHttp()
        self.c = CaseMethod(api, normal_response_body)
        unittest.TestCase.__init__(self, methodName)

    @ConfigHttp.wrap_case
    def test_normal_get(self):
        a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(b1)
        self.assertEqual(b1, "200")

    @ConfigHttp.wrap_case
    def test_normal_post_405(self):
        o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api)
        logger.info(o)
        logger.info(e)
        self.assertEqual(e, "405")

    @ConfigHttp.wrap_case
    def test_with_number_get(self):
        number_cases_r = number_param_r.split(",")
        for num in number_cases_r:
            temp_api = "%s?%s" % (api, num)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

        number_cases_e = number_param_e.split(",")
        for num in number_cases_e:
            for num in number_cases_e:
                temp_api = "%s?%s" % (api, num)
                a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
                logger.info(b1)
                self.assertEqual(b1, "200")

    @ConfigHttp.wrap_case
    def test_with_number_post_405(self):
        number_cases_r = number_param_r.split(",")
        for num in number_cases_r:
            parm = self.f.curl_post_str(num)
            o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api, parm)
            logger.info(o)
            logger.info(e)
            self.assertIn("405", e)

    @ConfigHttp.wrap_case
    def test_with_commit_get(self):
        commit_cases_r = commit_param_r.split(",")
        for commit in commit_cases_r:
            temp_api = "%s?%s" % (api, commit)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

        commit_cases_e = commit_param_e.split(",")
        for commit in commit_cases_e:
            temp_api = "%s?%s" % (api, commit)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

    @ConfigHttp.wrap_case
    def test_with_commit_post_405(self):
        commit_cases_r = commit_param_r.split(",")
        for commit in commit_cases_r:
            parm = self.f.curl_post_str(commit)
            o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api, parm)
            logger.info(o)
            logger.info(e)
            self.assertIn("405", e)

    @ConfigHttp.wrap_case
    def test_with_repo_get(self):
        repo_cases_r = repo_param_r.split(",")
        for repo in repo_cases_r:
            temp_api = "%s?%s" % (api, repo)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

        repo_cases_e = repo_param_e.split(",")
        for repo in repo_cases_e:
            temp_api = "%s?%s" % (api, repo)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

    @ConfigHttp.wrap_case
    def test_with_repo_post_405(self):
        repo_cases_r = repo_param_r.split(",")
        for repo in repo_cases_r:
            parm = self.f.curl_post_str(repo)
            o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api, parm)
            logger.info(o)
            logger.info(e)
            self.assertIn("405", e)

    @ConfigHttp.wrap_case
    def test_with_all_get(self):
        all_cases_r = all_param_r.split(",")
        for all in all_cases_r:
            temp_api = "%s?%s" % (api, all)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

        all_cases_e = all_param_e.split(",")
        for all in all_cases_e:
            temp_api = "%s?%s" % (api, all)
            a1, b1 = self.f.curl_get_code(ipfs_master_api_baseurl, ipfs_master_api_port, temp_api)
            logger.info(b1)
            self.assertEqual(b1, "200")

    @ConfigHttp.wrap_case
    def test_with_all_post_405(self):
        all_cases_r = all_param_r.split(",")
        for all in all_cases_r:
            parm = self.f.curl_post_str(all)
            o, e = self.f.curl_post_code(ipfs_master_api_baseurl, ipfs_master_api_port, api, parm)
            logger.info(o)
            logger.info(e)
            self.assertIn("405", e)

    @ConfigHttp.wrap_case
    def test_with_combined_parameters_get(self):
        parm = combined_parameters.replace(",", "&")
        o, e = self.f.run_cmd("curl " + ipfs_master_api_baseurl + ":" \
                          + ipfs_master_api_port + api + "?" + parm)
        logger.info(o)
        logger.info(e)
        res_dict = json.loads(e)
        expect_dict = json.loads(normal_response_body)
        res = self.f.check_body(res_dict, expect_dict)
        self.assertEqual(res, 0)

    @ConfigHttp.wrap_case
    def test_with_combined_parameters_post_405(self):
        parm = self.f.curl_post_str(combined_parameters)

        o, e = self.f.run_cmd("curl -v -X POST " + ipfs_master_api_baseurl + ":"
                              + ipfs_master_api_port + api + " -d '%s'" % parm)
        logger.info(o)
        logger.info(e)
        self.assertIn("405", o)
