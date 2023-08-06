class switch:
    def __init__(self, val):
        self.__val = val

        self.__cases = []
        self.__default = None
        self.__run_default = True
        self.__finished = False

    def __enter__(self):
        self.__cases = []
        self.__default = None
        self.__run_default = True
        self.__finished = False
        return self

    def case(self, case_condition, case_func):
        if case_condition:
            self.__cases.append(case_func)

    def equal(self, value):
        def wrapper(case_func):
            self.case(self.__val == value, case_func)
            return case_func
        return wrapper

    def included_in(self, values: list):
        def wrapper(case_func):
            self.case(self.__val in values, case_func)
            return case_func
        return wrapper

    def not_equal(self, value):
        def wrapper(case_func):
            self.case(self.__val != value, case_func)
            return case_func
        return wrapper

    def not_included_in(self, values):
        def wrapper(case_func):
            self.case(self.__val not in values, case_func)
            return case_func
        return wrapper

    def greater(self, value):
        def wrapper(case_func):
            self.case(self.__val > value, case_func)
            return case_func
        return wrapper

    def greater_equal(self, value):
        def wrapper(case_func):
            self.case(self.__val >= value, case_func)
            return case_func
        return wrapper

    def less(self, value):
        def wrapper(case_func):
            self.case(self.__val < value, case_func)
            return case_func
        return wrapper

    def less_equal(self, value):
        def wrapper(case_func):
            self.case(self.__val <= value, case_func)
            return case_func
        return wrapper

    def default(self, func):
        self.__default = func

    def end(self):
        self.__finished = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        for case in self.__cases:
            case(self.__val)
            if self.__finished:
                break
        if not self.__finished:
            self.__default(self.__val)