# simple-system-tests
Simple Python library for writing test cases for System and components tests including automatic reports via html. The intention is to have an easy framework for developers without the need to learn a separate coding language.
## Installation
The module is not yet published on pypi, therefore you have to build it manually:
```
pip3 install setuptools wheel
python3 setup.py sdist bdist_wheel
(sudo) python3 setup.py install
```
## Quick-Start
Go to `examples` and run:
```
python3 main.py
```
which will execute two testcases (defined under `examples/HttpGetTestCase.py` and `examples/TimeTestCase.py`). After that open the created `examples/index.html` for an overview of the results in a web browser.
## Testsuite
The Testsuite is defined under `simple_system_tests/TestSuite.py`:
- holds and executes testcases
- prepare and teardown of Testsuite, which can be implemented by deriving a new class from it and overwriting the `prepare` and `teardown` functions, eg:
```
import simple_system_tests as sst
class CustomTestSuite(sst.TestSuite):
    def prepare(self):
        subprocess.run("ip link set dev eth0 up", shell=True)
```
- reporting of test results stored in `index.html` (can be customized)
- providing command line options for configurations and all testcases allowing them to be called separately

## Command line options
When using a Testsuite command line options for all testcases added to the suite will be automatically added. command line option shortcut will be derived from the beginning characters of the description string passed to the testcase. So make sure to have varying descriptions for your testcases. Having a look at the help of `examples/main.py` again will give the following output:
```
shell: python3 main.py -h
usage: main.py [-h] [-no] [-p JSON_SYSTEM_PARAMS] [-o REPORT_OUTPUT] [-ht] [-ho]

optional arguments:
  -h, --help            show this help message and exit
  -no, --no-suite-setup
                        No Suite Prepare and Teardown
  -p JSON_SYSTEM_PARAMS, --json-system-params JSON_SYSTEM_PARAMS
                        Path to JSON params file.
  -o REPORT_OUTPUT, --report-output REPORT_OUTPUT
                        Path to report html file.
  -ht, --http_get       Test Http get
  -ho, --host_unix_time
                        Test Host unix time
```
So testcases can be called separately without having to execute all testcases in one run. It is also possible to pass multiple testcases in one execution. In case the Suite setup and teardown is not wanted this can be achieved by putting the `-no, --no-suite-setup` option.
## Testcases
### Create new testcases
Similar to the Testsuite testcases can be derived from the base Testcase class(`simple_system_tests/Testcase.py`), by overwriting the:
- prepare (optional)
- execute (required)
- teardown (optional)

functions. In contrast to the Testsuite however, the `execute` function must be overridden for testcases, else a `NotImplementedError` is raised. A testcase is considered a `PASS` as long as no exception is raised. For example:
```
import simple_system_tests as sst
class CustomTestCase(sst.TestCase):
    def execute(self):
        raise Exception("Fails always, anyways")
```
which will result in `FAIL`. Upon Object creation a description needs to be passed to the Testcase:
```
t = CustomTestCase("Always failing task")
```
### System parameters
Environment parameters for the testsuite can be used from a json file named `system_params.json` (the file path can be customized by passing the `-p` option). Those will be made available in the Testcase by the attribute `self.params`:
```
import simple_system_tests as sst
class CustomTestCase(sst.TestCase):
    def execute(self):
        self.logger.info(self.params["key_from_sys_params"])
        raise Exception("Fails always, anyways")
```
It is also possible to access and modify these json params from within the testsuite, eg. in case a global python object should be made available in Testsuite preparation for all testcases.
### Logging
The file path of the output file can be customized by passing the `-o` option, which defaults to `index.html`. A `logger` object attribute is available within testcases and testsuites, eg:
```
import simple_system_tests as sst
class CustomTestSuite(sst.TestSuite):
    def prepare(self):
        self.logger.info("Preparing the test suite")
```
However stdout is mapped to `logger.info`, hence `print` can also be used directly which will result in output of both console and html report file as `INFO` message.
### Retry and Timeout
Timeout (in seconds) and how often a testcase should be retried can be given in the testcase like following.
```
import simple_system_tests as sst
class CustomTestCase(sst.TestSuite):
    def execute(self):
        self.timeout = 0.5 # defaults to -1, which means no timeout check
        self.retry = 2     # defaults to 0
```
For now retry and timeout is reduced to the `execute` task of testcases. It is not checked for Testsuites or `prepare` and `teardown` of Testcases.
### Sub testcases
It might desirable to call one testcase just with different parameters. This can be done by using sub testcases, therefore when adding the testcase to the testsuite a list of parameters needs to be given. The count of list elements then defines also the count of sub testcases, eg. looking at an excerpt of `examples/main.py`:
```
T.add_test_case(HttpGetTestCase("Http get"), [
    {"host":"ipv6.google.com", "redundant_param":5},
    {"host":"ipv4.google.com", "redundant_param":3},
    {"host":"gmx.net", "redundant_param":2},
    {"host":"github.com", "redundant_param":4}
])
```
So in the above case 4 (sub) tests will be run for `HttpGetTestCase`, which will also be shown as 4 testcase results in the report. The datatype of the list elements can be either of type `dict` like above or also primitive data types. It is recommended to have the same data type / data structure for all list elements of one testcase, though. The `test_params` can be accessed from the testcase `execute` using `self.test_params` like shown in `examples/HttpGetTestCase.py`:
```
class HttpGetTestCase(sst.TestCase):
    def execute(self):
        self.timeout = 0.2
        self.retry = 1
        host = self.test_params["host"]
        self.logger.info("Test access to " + host)
        r = requests.get("https://" + host)
        assert(r.status_code == 200)
```