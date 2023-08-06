class TestCase(object):
    def __init__(self, desc):
        self.__desc = desc
        self.params = {}
        self.logger = None
        self.timeout = -1
        self.retry = 0
        self.__sub_desc = ""
        self.__sub_params = []
        self.test_params = None
        self.execute_func = None
        self.prepare_func = None
        self.teardown_func = None
    def prepare(self):
        if self.prepare_func:
            self.prepare_func(self)
    def execute(self):
        if not self.execute_func:
            raise Exception("Not implemented.")
        self.execute_func(self)
    def teardown(self):
        if self.teardown_func:
            self.teardown_func(self)
    def set_sub_params(self, params):
        if not isinstance(params, list):
            raise Exception("Subtest parameters needs to be of type list.")
        self.__sub_params = params
    def get_sub_params(self):
        return self.__sub_params
    def get_description(self):
        if self.__sub_desc != "":
            return self.__sub_desc
        return self.__desc
    def set_sub(self, i):
        p = self.__sub_params[i]
        suffix = ""
        if isinstance(p, dict):
            for k in p:
                if suffix == "":
                    suffix = k + ":" + str(p[k])
                else:
                    suffix = suffix + ", " + k + ":" + str(p[k])
        else:
            suffix = str(p)
        self.__sub_desc = self.__desc + " - " + suffix
        self.test_params = p
    def set_params(self, params):
        self.params = params
    def is_active(self, args):
       active = vars(args)[self.__desc.replace("-","_").replace(" ", "_").lower()]
       return active
    def __del__(self):
       pass
