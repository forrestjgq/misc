class Secure:
    def __init__(self, base: float):
        self.pension: float = 0
        self.medical: float = 0
        self.job: float = 0
        self.house: float = 0
        self.injure: float = 0
        self.extra: float = 0
        self.base: float = base

    def as_employ(self):
        self.pension = 0.08
        self.medical = 0.02
        self.job = 0.005
        self.house = 0.12
        self.injure = 0
        self.extra = 5  # for medical

    def as_company(self):
        self.pension = 0.16
        self.medical = 0.058
        self.job = 0.005
        self.house = 0.12
        self.injure = 0.002
        self.extra = 0  # for medical

    def percent(self):
        return self.pension + self.medical + self.job + self.house + self.injure

    def expense(self):
        return self.percent() * self.base + self.extra

    def print(self, prefix: str):
        print(f'{prefix} security based on {self.base}:')
        print(f'\tpension: {self.base * self.pension}')
        print(f'\tmedical: {self.base * self.medical}')
        print(f'\tjob: {self.base * self.job}')
        print(f'\thouse: {self.base * self.house}')
        print(f'\tinjure: {self.base * self.injure}')
        print(f'\ttotal: {self.base * self.percent()}')


class Salary:
    def __init__(self, salary: float, secure: Secure, secure_company: Secure, tax_free: float):
        self.base = 5000
        # upper, rate, cut
        self.steps = [
            [36000, 0.03, 0],
            [144000, 0.1, 2520],
            [300000, 0.2, 16920],
            [420000, 0.25, 31920],
            [660000, 0.3, 52920],
            [960000, 0.35, 85920],
            [99999999999999, 0.45, 181920],
        ]
        self.salary = salary
        self.secure = secure
        self.secure_company = secure_company

        self.no_tax = tax_free
        self.tax = []

        self.calc()

    def tax_free(self):
        return self.secure.expense() + self.base + self.no_tax

    def calc(self):
        to_tax = 0  # accumulated salary which should be taxed
        taxed = 0
        for i in range(12):
            to_tax += self.salary - self.tax_free()
            if to_tax <= 0:
                self.tax.append(0)
            else:
                for seg in self.steps:
                    if to_tax <= seg[0]:
                        tax = to_tax * seg[1] - seg[2] - taxed
                        self.tax.append(tax)
                        taxed += tax
                        break

    def year_tax(self):
        return sum(self.tax)

    def month_tax(self, month: int):
        assert 0 <= month < 12
        return self.tax[month]

    def salaries(self):
        """
        @return: list of salary monthly
        """
        return [self.salary - self.secure.expense() - tax for tax in self.tax]

    def real_salaries(self):
        """
        @return: list of real salary monthly: after tax salary + personal house fund + company house fund
        """
        return [v + self.secure.house * self.secure.base + self.secure_company.house * self.secure_company.base for v in self.salaries()]

    def print(self):
        print(f'Salary Details:')
        print('-'*30)
        paid = [int(f) for f in self.salaries()]
        realpaid = [int(f) for f in self.real_salaries()]
        taxes = [int(f) for f in self.tax]
        print("{0:>8}".format("month") + "{0:>8}".format("paid") + "{0:>8}".format("cared") + "{0:>8}".format("tax"))
        print("="*40)
        for i in range(12):
            print(f"{i+1: 8d}{paid[i]: 8d}{realpaid[i]: 8d}{taxes[i]: 8d}")
        print("="*40)
        print("{0:>8}".format("total")
              + f'{int(sum(self.salaries())): 8d}'
              + f'{int(sum(self.real_salaries())): 8d}'
              + f'{int(sum(self.tax)): 8d}')

        print("")
        print("")
        print(f'Security Details:')
        print('-'*30)
        self.secure.print("Personal")
        self.secure_company.print("Company")

class Service:
    def __init__(self, payed: float):
        self.payed = payed
        self.tax = self._tax()
        self.income = self.payed - self.tax
        self.year = self.income * 12
        self.year_tax = self.tax * 12

    def _tax(self):
        if self.payed <= 800:
            return 0
        if self.payed < 4000:
            return (self.payed - 800) * 0.2
        if self.payed < 20000:
            return self.payed * 0.8 * 0.2
        if self.payed < 50000:
            return self.payed * 0.8 * 0.3 - 2000
        return self.payed * 0.8 * 0.4 - 7000

    def print(self):
        print(f"Service: month paid {int(self.payed)}, tax {int(self.tax)}, after tax {int(self.income)}, for one year {int(self.year)}\n")


class Company:
    def __init__(self, salary: float, secure_base: float):
        self.salary = salary
        self.secure = Secure(min(self.salary, secure_base))
        self.secure.as_company()

    def get_secure(self):
        return self.secure

    def expanse(self):
        return self.salary + self.secure.expense()

    def print(self):
        print(f"Company: salary {self.salary} security base {self.secure.base} expanse {self.expanse()}")


class Employ:
    def __init__(self, salary: float, secure_base: float):
        self.salary = salary
        self.secure = Secure(min(self.salary, secure_base))
        self.secure.as_employ()

    def get_secure(self):
        return self.secure

    def print(self):
        print(f"Employ: salary {self.salary} security base {self.secure.base}")


class Splitter:
    def __init__(self, salary: float, tax_free, secure_base: float = 31600):
        self.salary = salary
        self._tax_free = tax_free
        self._secure_base = secure_base

    def calc(self):
        sep = 5
        as_salary = self.salary
        max_got = (0, 0, 0, 0, 0)  # as_salary,  as_service, got, card, company to company
        max_cared = (0, 0, 0, 0, 0)  # as_salary, as_service, got, cared
        compnay = Company(self.salary, self._secure_base)
        company_total_pay = compnay.expanse()  # how much company should pay in total
        print("="*120)
        print(f'when we split salary with service, company total expanse: {int(company_total_pay)}')
        while as_salary >= 7000:
            pay_company = Company(as_salary, self._secure_base)
            company_to_company = pay_company.expanse() * 1.06  # for company to company taxing
            as_service = company_total_pay - company_to_company
            if as_service < 0:
                as_service = 0
            got, cared = self.split(as_salary, as_service)
            # print(f'as salary {int(as_salary)}, as service {int(as_service)}: salary for year {int(got)}  plus house fund {int(cared)}')

            # this shows details when salary is set to 9000, change False to True to enable it
            if False and as_salary == 9000:
                print('*'*120)
                print(f'as salary {int(as_salary)}, as service {int(as_service)}, company to company {int(company_to_company)}: salary for year {int(got)}  plus house fund {int(cared)}')
                self.split(as_salary, as_service, print=True)
                print('*' * 120)

            if got > max_got[2]:
                max_got = (as_salary, as_service, got, cared, company_to_company)
            if cared > max_cared[2]:
                max_cared = (as_salary, as_service, got, cared, company_to_company)
            as_salary -= sep
        print(f"According to salary: as salary {int(max_got[0])}, as service {int(max_got[1])} company to company {int(company_to_company)}:")
        print(f">>>>>> result: salary for year {int(max_got[2])}, plus house fund: {int(max_got[3])}")
        print("\ndetailed:")
        self.split(max_got[0], max_got[1], print=True)
        if max_got[0] != max_cared[0]:
            print("=" * 120)
            print(f"According to salary+house fund: as salary {int(max_cared[0])}, as service {int(max_cared[1])}: salary for year {int(max_cared[2])}, plus house fund: {int(max_cared[3])}")
            print("detailed:")
            self.split(max_cared[0], max_cared[1], print=True)

    def split(self, as_salary, as_service, print=False):
        employ = Employ(as_salary, self._secure_base)
        company = Company(as_salary, self._secure_base)
        service = Service(as_service)
        salary = Salary(as_salary, employ.secure, company.secure, self._tax_free)
        # calculate how much salaries after taxing
        got = sum(salary.salaries()) + service.year
        cared = sum(salary.real_salaries()) + service.year

        if print:
            employ.print()
            company.print()
            service.print()
            salary.print()
        return got, cared

class Formal:
    def __init__(self, salary, secure_base, tax_free):
        self.employ = Secure(secure_base)
        self.employ.as_employ()
        self.company = Secure(secure_base)
        self.company.as_company()
        self.salary = salary
        self.tax_free = tax_free

    def calc(self):
        sal = Salary(self.salary, self.employ, self.company, self.tax_free)
        print("="*120)
        print("For regular salary:")
        sal.print()


if __name__ == "__main__":
    salary = 27000   # your salary
    secure_base = 31600  # max security base in suzhou
    tax_free = 2000  # extra tax free
    extra = 525  # extra from salary

    print("paid means how much you actually got from salary, and cared will plus house fund")
    f = Formal(salary+extra, min(secure_base, salary+extra), tax_free)
    f.calc()

    s = Splitter(salary + extra, tax_free, secure_base)
    s.calc()

