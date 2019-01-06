import unittest,sys,json,os
sys.path.append("../")
from function.func import *
from function.ela_log import MyLog

import read_conf

a = read_conf.ReadConfig()
ipfs_master_api_baseurl = a.get_ipfs_cluster("ipfs_master_api_baseurl")
ipfs_master_api_port = a.get_ipfs_cluster("ipfs_master_api_port")

b = read_conf.ReadData()
api = b.get_version("api")
normal_response_code = b.get_version("normal_response_code")
abnormal_response_code = b.get_version("abnormal_response_code")
not_found_code = b.get_version("not_found_code")
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


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def wrap_ela(func):
        def run(*argv):
            logger.info("-" * 25)
            logger.info("[%s] TEST CASE: [%s]" % (os.path.basename(__file__), func.__name__))
            logger.info("-" * 25)
            if argv:
                ret = func(*argv)
            else:
                ret = func()
            return ret
        return run

    @wrap_ela
    def test_normal_get(self):
        f = ConfigHttp()

        o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":"\
                           + ipfs_master_api_port + api)
        logger.info(o)
        logger.info(e)
        self.assertEqual(e, normal_response_code)

        o, e = f.curl_cmd("curl "+ipfs_master_api_baseurl + ":"\
                           + ipfs_master_api_port + api)
        logger.info(o)
        logger.info(e)
        res_dict = json.loads(e)
        expect_dict = json.loads(normal_response_body)
        res = f.check_body(res_dict, expect_dict)
        self.assertEqual(res, 0)

    @wrap_ela
    def test_normal_post_404(self):
        f = ConfigHttp()

        o, e = f.curl_cmd("curl -X POST -m 10 -o /dev/null -s -w %{http_code} "+ ipfs_master_api_baseurl + ":"\
                           + ipfs_master_api_port + api)
        logger.info(o)
        logger.info(e)
        self.assertIn(not_found_code, e)

        #{"Version":"0.4.14","Commit":"","Repo":"6","System":"386/linux","Golang":"go1.10"}
        # o, e = f.curl_cmd("curl -X POST "+ipfs_master_api_baseurl + ":"\
        #                    + ipfs_master_api_port + api)
        # logger.info(o)
        # logger.info(e)
        # res_dict = json.loads(e)
        # expect_dict = json.loads(normal_response_body)
        # res = f.check_body(res_dict, expect_dict)

    @wrap_ela
    def test_with_number_get(self):
        f = ConfigHttp()
        number_cases_r = number_param_r.split(",")
        for num in number_cases_r:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + num)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, normal_response_code)

            o, e = f.curl_cmd("curl "+ipfs_master_api_baseurl + ":"\
                              + ipfs_master_api_port + api + "?" + num)
            logger.info(o)
            logger.info(e)
            res_dict = json.loads(e)
            expect_dict = json.loads(normal_response_body)
            res = f.check_body(res_dict, expect_dict)
            self.assertEqual(res, 0)

        number_cases_e = number_param_e.split(",")
        for num in number_cases_e:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + num)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, abnormal_response_code)

    @wrap_ela
    def test_with_number_post_404(self):
        f = ConfigHttp()
        number_cases_r = number_param_r.split(",")
        for num in number_cases_r:
            parm = f.curl_post_str(num)
            o, e = f.curl_cmd("curl -X POST " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + " -d '%s'" % parm)
            logger.info(o)
            logger.info(e)
            self.assertIn(not_found_code, e)
            # res_dict = json.loads(e)
            # expect_dict = json.loads(normal_response_body)
            # res = f.check_body(res_dict, expect_dict)

    @wrap_ela
    def test_with_commit_get(self):
        f = ConfigHttp()
        commit_cases_r = number_param_r.split(",")
        for commit in commit_cases_r:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + commit)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, normal_response_code)

            o, e = f.curl_cmd("curl "+ipfs_master_api_baseurl + ":"\
                              + ipfs_master_api_port + api + "?" + commit)
            logger.info(o)
            logger.info(e)
            res_dict = json.loads(e)
            expect_dict = json.loads(normal_response_body)
            res = f.check_body(res_dict, expect_dict)
            self.assertEqual(res, 0)

        commit_cases_e = commit_param_e.split(",")
        for commit in commit_cases_e:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + commit)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, abnormal_response_code)

    @wrap_ela
    def test_with_commit_post_404(self):
        f = ConfigHttp()
        commit_cases_r = commit_param_r.split(",")
        for commit in commit_cases_r:
            parm = f.curl_post_str(commit)
            o, e = f.curl_cmd("curl -X POST " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + " -d '%s'" % parm)
            logger.info(o)
            logger.info(e)
            self.assertIn(not_found_code, e)
            # res_dict = json.loads(e)
            # expect_dict = json.loads(normal_response_body)
            # res = f.check_body(res_dict, expect_dict)

    @wrap_ela
    def test_with_repo_get(self):
        f = ConfigHttp()
        repo_cases_r = number_param_r.split(",")
        for repo in repo_cases_r:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + repo)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, normal_response_code)

            o, e = f.curl_cmd("curl "+ipfs_master_api_baseurl + ":"\
                              + ipfs_master_api_port + api + "?" + repo)
            logger.info(o)
            logger.info(e)
            res_dict = json.loads(e)
            expect_dict = json.loads(normal_response_body)
            res = f.check_body(res_dict, expect_dict)
            self.assertEqual(res, 0)

        repo_cases_e = repo_param_e.split(",")
        for repo in repo_cases_e:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + repo)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, abnormal_response_code)

    @wrap_ela
    def test_with_repo_post_404(self):
        f = ConfigHttp()
        repo_cases_r = repo_param_r.split(",")
        for repo in repo_cases_r:
            parm = f.curl_post_str(repo)
            o, e = f.curl_cmd("curl -X POST " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + " -d '%s'" % parm)
            logger.info(o)
            logger.info(e)
            self.assertIn(not_found_code, e)
            # res_dict = json.loads(e)
            # expect_dict = json.loads(normal_response_body)
            # res = f.check_body(res_dict, expect_dict)

    @wrap_ela
    def test_with_all_get(self):
        f = ConfigHttp()
        all_cases_r = number_param_r.split(",")
        for all in all_cases_r:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + all)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, normal_response_code)

            o, e = f.curl_cmd("curl "+ipfs_master_api_baseurl + ":"\
                              + ipfs_master_api_port + api + "?" + all)
            logger.info(o)
            logger.info(e)
            res_dict = json.loads(e)
            expect_dict = json.loads(normal_response_body)
            res = f.check_body(res_dict, expect_dict)
            self.assertEqual(res, 0)

        all_cases_e = all_param_e.split(",")
        for all in all_cases_e:
            o, e = f.curl_cmd("curl -m 10 -o /dev/null -s -w %{http_code} " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + "?" + all)
            logger.info(o)
            logger.info(e)
            self.assertEqual(e, abnormal_response_code)

    @wrap_ela
    def test_with_all_post_404(self):
        f = ConfigHttp()
        all_cases_r = all_param_r.split(",")
        for all in all_cases_r:
            parm = f.curl_post_str(all)
            o, e = f.curl_cmd("curl -X POST " + ipfs_master_api_baseurl + ":" \
                              + ipfs_master_api_port + api + " -d '%s'" % parm)
            logger.info(o)
            logger.info(e)
            self.assertIn(not_found_code, e)
            # res_dict = json.loads(e)
            # expect_dict = json.loads(normal_response_body)
            # res = f.check_body(res_dict, expect_dict)

    @wrap_ela
    def test_with_combined_parameters_get(self):
        parm=combined_parameters.replace(",", "&")
        f = ConfigHttp()

        o, e = f.curl_cmd("curl " + ipfs_master_api_baseurl + ":" \
                          + ipfs_master_api_port + api + "?" + parm)
        logger.info(o)
        logger.info(e)
        res_dict = json.loads(e)
        expect_dict = json.loads(normal_response_body)
        res = f.check_body(res_dict, expect_dict)
        self.assertEqual(res, 0)

    @wrap_ela
    def test_with_combined_parameters_post_404(self):
        f = ConfigHttp()
        parm = f.curl_post_str(combined_parameters)

        o, e = f.curl_cmd("curl -X POST " + ipfs_master_api_baseurl + ":" \
                          + ipfs_master_api_port + api + " -d '%s'" % parm)
        logger.info(o)
        logger.info(e)
        self.assertIn(not_found_code, e)
        # res_dict = json.loads(e)
        # expect_dict = json.loads(normal_response_body)
        # res = f.check_body(res_dict, expect_dict)


# if __name__ == '__main__':
#     suite = unittest.TestSuite()
#     suite.addTest(Version("test_with_repo_post"))
#     runner = unittest.TextTestRunner()
#     runner.run(suite)
