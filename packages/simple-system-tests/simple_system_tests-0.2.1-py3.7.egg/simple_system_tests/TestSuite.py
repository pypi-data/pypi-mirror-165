import sys
from io import StringIO
import argparse
import json
import datetime

from simple_system_tests.ReportHtml import ReportHtml
from simple_system_tests.CachedLogger import CachedLogger
from simple_system_tests.TestCase import TestCase

OVERLINE="---------------------------------------------------------------------\n"

global Suite

class TestSuite:
    def __init__(self):
        self._report = ReportHtml()
        self.__testcases = []
        self.__pass_counter = 0
        self.__fail_counter = 0
        self.__cmd_options = ["no", "h", "p", "o"]
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument('-no','--no-suite-setup', help='No Suite Prepare and Teardown', action="store_true")
        self.__parser.add_argument('-p','--json-system-params', help='Path to JSON params file.', default="system_params.json")
        self.__parser.add_argument('-o','--report-output', help='Path to report html file.', default="index.html")
        self.params = {}
        self.__old_stdout = None
        self.__stdout = None

    def __add_cmd_option(self, desc):
        for cmd_len in range(len(desc)):
            if self.__cmd_options == []:
                cmd_opt = desc[0:1].lower()
                self.__cmd_options.append(cmd_opt)
                return cmd_opt

            duplicate=False
            cmd_opt = desc[0:cmd_len + 1].lower()
            for c in self.__cmd_options:
                if cmd_opt == c:
                    duplicate = True
                    break
            if not duplicate:
                self.__cmd_options.append(cmd_opt)
                return cmd_opt

        raise Exception(desc + " has duplicate description")

    def __fail(self):
        self.__fail_counter = self.__fail_counter + 1
        print("\n\n----\nFAIL\n----\n")

    def __pass(self):
        self.__pass_counter = self.__pass_counter + 1
        print("\n\n----\nPASS\n----\n")

    def __suite(self, no_suite_setup, desc):
        start = datetime.datetime.now().timestamp()
        if not no_suite_setup:
            try:
                print(OVERLINE)
                print(desc + " of Suite\n")
                self.logger = self.__cached_logger.start_logging()
                if desc == "Setup":
                    self.prepare()
                else:
                    self.teardown()
            except Exception as ec:
                self.logger.error("ABORT: Suite " + desc + " failed with " + str(ec))
                self._report.add_result("Suite " + desc, self.__cached_logger.stop_logging(), False, datetime.datetime.now().timestamp() - start, [0,0])
                self._report.finish_results(self.__report_file)
                sys.exit(1)

            self._report.add_result("Suite " + desc, self.__cached_logger.stop_logging(), True, datetime.datetime.now().timestamp() - start, [0,0])

    def __run_testcase(self, tc):
        def __execute():
            tc_failed = False
            start = datetime.datetime.now().timestamp()
            try:
                tc.execute()
            except Exception as ec:
                self.logger.error("Testcase execution failed with: " + str(ec))
                tc_failed = True
            duration = datetime.datetime.now().timestamp() - start

            if tc.timeout > 0:
                if tc.timeout < duration:
                    self.logger.error("Testcase execution timeout (" + str(tc.timeout) + " s) exceeded taking " + '{:.5f}'.format(duration) + " s instead.")
                    tc_failed = True

            return [tc_failed, duration]

        tc.set_params(self.params)

        print(OVERLINE)
        print("TEST " + tc.get_description() + ":\n\n")
        tc_failed = True
        self.logger = self.__cached_logger.start_logging()
        tc.logger = self.logger
        try:
            tc.prepare()
        except Exception as ec:
            self.logger.error("Preparation of testcase failed with: " + str(ec))
            self._report.add_result(tc.get_description(), self.__cached_logger.stop_logging(), False, [0, 0])
            self.__fail()
            return

        retries = -1
        while retries < tc.retry and tc_failed:
            retries = retries + 1
            if retries > 0:
                self.logger.info(str(retries) + ". Retry of testcase now.")
            tc_failed, duration = __execute()

        try:
            tc.teardown()
        except Exception as ec:
            self.logger.error("Testcase teardown failed with: " + str(ec))
            tc_failed = True

        log = self.__cached_logger.stop_logging()
        if not tc_failed:
            self.__pass()
        else:
            self.__fail()

        self._report.add_result(tc.get_description(), log, not tc_failed, duration, [retries, tc.retry])

    def prepare(self):
        pass

    def teardown(self):
        pass

    def add_test_case(self, test_case, sub_params=[]):
        desc = test_case.get_description()
        test_case.set_sub_params(sub_params)
        desc_cmd = desc.replace(" ", "_").replace("-","_").lower()
        self.__parser.add_argument('-' + self.__add_cmd_option(desc),'--' + desc_cmd, help='Test ' + desc, action="store_true")
        self.__testcases.append(test_case)

    def execute_tests(self):
        self.__cached_logger = CachedLogger()
        args = self.__parser.parse_args()
        no_suite_setup = vars(args)["no_suite_setup"]
        params_env = vars(args)["json_system_params"]
        self.__report_file = vars(args)["report_output"]

        try:
            self.params = json.loads(open(params_env).read())
        except Exception as ec:
            print(str(ec) + ". So no parameters will be passed!")
            self.params = {}

        all_inactive = True
        for tc in self.__testcases:
            if tc.is_active(args):
                all_inactive = False
                break

        self.__suite(no_suite_setup, "Setup")

        for tc in self.__testcases:
            if not all_inactive and not tc.is_active(args):
                continue

            sub_params = tc.get_sub_params()
            if sub_params != []:
                for i in range(len(sub_params)):
                    tc.set_sub(i)
                    self.__run_testcase(tc)
            else:
                self.__run_testcase(tc)

        self.__suite(no_suite_setup, "Teardown")
        self._report.finish_results(self.__report_file)

        print(OVERLINE)
        print("Total pass: " + str(self.__pass_counter))
        print("Total fail: " + str(self.__fail_counter))

        if self.__fail_counter != 0:
            sys.exit(1)

Suite = TestSuite()

def prepare_suite(func):
    TestSuite.prepare = func

def teardown_suite(func):
    TestSuite.teardown = func

def testcase(desc, sub_params=[], retry=0, timeout=-1, prepare_func=None, teardown_func=None):
    def testcase_(func):
        global Suite
        T=TestCase(desc)
        T.retry=retry
        T.timeout=timeout
        T.execute_func = func
        T.prepare_func = prepare_func
        T.teardown_func = teardown_func
        Suite.add_test_case(T, sub_params)
    return testcase_

def run_tests():
    Suite.execute_tests()
