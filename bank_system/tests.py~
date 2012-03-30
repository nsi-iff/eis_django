import sys
sys.path.append("home/mari/eis-examples-mari")
sys.path.append("/home/mari/eis-mari")

from django.utils import unittest
#import unittest
from should_dsl import should, should_not
from domain.node.machine import Machine
from domain.supportive.association_error import AssociationError
from bank_system.models import BankAccountDecorator

from domain.node.person import Person
from domain.supportive.contract_error import ContractError
from bank_system.resources.loan_request import LoanRequest
from bank_system.resources.loan import Loan
from bank_system.models import CreditAnalystDecorator
from bank_system.models import EmployeeDecorator
from bank_system.rules.bank_system_rule_base import BankSystemRuleBase
from domain.supportive.rule_manager import RuleManager

################################################# BANK ACCOUNT ###################################################################
class BankAccountDecoratorTestCase(unittest.TestCase):
    def setUp(self):
        self.a_bank_account_decorator = BankAccountDecorator.objects.create(number="123456")
        self.a_machine = Machine()

    def testVerify_inclusion_of_a_bank_account_decorator(self):
        self.a_bank_account_decorator.number |should| equal_to('123456')

    def testDecorates_a_machine(self):
        #should work
        self.a_bank_account_decorator.decorate(self.a_machine)
        self.a_bank_account_decorator.decorated |should| be(self.a_machine)
        self.a_bank_account_decorator.decorated |should| have(1).decorators
        #should fail
        decorate, _, _ = self.a_bank_account_decorator.decorate('I am not a machine')
        decorate |should| equal_to(False)

    def testRegisters_a_credit(self):
        self.a_bank_account_decorator.balance = 100
        self.a_bank_account_decorator.register_credit(50)
        self.a_bank_account_decorator.balance |should| equal_to(150)

    def test_sends_a_message_to_the_account_holder(self):
        message = 'This is a message'
        self.a_bank_account_decorator.send_message_to_account_holder(message) |should| equal_to(message)

################################################# CREDIT ANALYST ###################################################################
class CreditAnalystDecoratorTestCase(unittest.TestCase):

    def setUp(self):
        #set the rule base
        RuleManager.rule_base = BankSystemRuleBase()
        #
        self.a_credit_analyst_decorator = CreditAnalystDecorator.objects.create(register='12345-6')
        #test doubles won't work given type checking rules, using classic
        self.a_person = Person()
        self.an_account = BankAccountDecorator.objects.create(number='1234567-8')

    def test_decorates_a_person(self):
        #should fail
        decorate, _, _ = self.a_credit_analyst_decorator.decorate(self.a_person)
        decorate |should| equal_to(False)
        #should work
        an_employee_decorator = EmployeeDecorator()
        an_employee_decorator.decorate(self.a_person)
        self.a_credit_analyst_decorator.decorate(self.a_person)
        self.a_credit_analyst_decorator.decorated |should| be(self.a_person)
        self.a_credit_analyst_decorator.decorated |should| have(2).decorators

    def test_creates_a_loan_request(self):
        an_employee_decorator = EmployeeDecorator()
        an_employee_decorator.decorate(self.a_person)
        self.a_credit_analyst_decorator.decorate(self.a_person)
        self.a_credit_analyst_decorator.create_loan_request(self.an_account, 10000)
        self.a_person.input_area |should| contain('1234567-8')

    def test_analyses_a_loan_request(self):
        an_employee_decorator = EmployeeDecorator()
        an_employee_decorator.decorate(self.a_person)
        #Stub removed, from now on Node really transfers resources internally
        self.a_credit_analyst_decorator.decorate(self.a_person)
        self.an_account.average_credit = 5000
        #should approve
        self.a_credit_analyst_decorator.create_loan_request(self.an_account, 10000)
        self.a_credit_analyst_decorator.analyse(self.an_account.number)
        self.a_credit_analyst_decorator.decorated.output_area['1234567-8'].approved |should| equal_to(True)
        #should refuse
        self.a_credit_analyst_decorator.create_loan_request(self.an_account, 50000)
        self.a_credit_analyst_decorator.analyse(self.an_account.number)
        self.a_credit_analyst_decorator.decorated.output_area['1234567-8'].approved |should| equal_to(False)

    def test_creates_a_loan(self):
        an_employee_decorator = EmployeeDecorator()
        an_employee_decorator.decorate(self.a_person)
        loan_request = LoanRequest(self.an_account, 7000, self.a_credit_analyst_decorator)
        self.a_credit_analyst_decorator.decorate(self.a_person)
        self.a_credit_analyst_decorator.decorated.output_area[self.an_account.number] = loan_request
        #creates a machine to be decorated by the account - will need to check its processing_area
        a_machine = Machine()
        self.an_account.decorate(a_machine)
        #creates the loan
        self.a_credit_analyst_decorator.create_loan(loan_request)
        #loan key is the analyst's register
        self.a_credit_analyst_decorator.decorated.output_area.values() |should| have_at_least(1).loan
        self.a_credit_analyst_decorator.decorated.output_area |should| include(self.a_credit_analyst_decorator.register)

    def test_moves_the_loan_to_an_account(self):
        #prepares the person Node
        an_employee_decorator = EmployeeDecorator()
        an_employee_decorator.decorate(self.a_person)
        self.a_credit_analyst_decorator.decorate(self.a_person)
        #prepares a Loan
        loan_request = LoanRequest(self.an_account, 7000, self.a_credit_analyst_decorator)
        self.a_credit_analyst_decorator.decorated.output_area[self.an_account.number] = loan_request
        self.a_credit_analyst_decorator.create_loan(loan_request)
        #should go wrong
        passing_a_wrong_key = 'wrong key'
        (self.a_credit_analyst_decorator.move_loan_to_account, passing_a_wrong_key, self.an_account) |should| throw(KeyError)
        passing_a_non_account = 'I am not an account'
        (self.a_credit_analyst_decorator.move_loan_to_account, self.an_account.number, passing_a_non_account) |should| throw(ContractError)
        #prepares the account
        a_machine = Machine()
        self.an_account.decorate(a_machine)
        #should work
        loan_key = self.a_credit_analyst_decorator.register
        self.a_credit_analyst_decorator.move_loan_to_account(loan_key, self.an_account)
        self.an_account.decorated.input_area |should| include(loan_key)
        self.an_account.balance |should| equal_to(7000)

    def test_changes_its_loan_limit(self):
        self.a_credit_analyst_decorator.change_loan_limit(100000)
        self.a_credit_analyst_decorator.loan_limit |should| be(100000)

################################################# EMPLOYEE ###################################################################
class EmployeeDecoratorSpec(unittest.TestCase):

    def setUp(self):
        self.an_employee_decorator = EmployeeDecorator.objects.create(name="Steve")
        #test doubles won't work given type checking rules, using classic
        self.a_person = Person()

    def test_decorates_a_person(self):
        #should work
        self.an_employee_decorator.decorate(self.a_person)
        self.an_employee_decorator.decorated |should| be(self.a_person)
        self.an_employee_decorator.decorated |should| have(1).decorators
        #should fail
        decorate,_,_ = self.an_employee_decorator.decorate('I am not a person')
        decorate |should| equal_to(False)

    def test_generates_register(self):
        self.an_employee_decorator.generate_register('123456-7')
        self.an_employee_decorator.register |should| equal_to('123456-7')


################################################# LOAN REQUEST ###################################################################
class LoanRequestSpec(unittest.TestCase):

    def test_check_associations_with_bank_account_and_credit_analyst(self):
        #set the rule base
        RuleManager.rule_base = BankSystemRuleBase()
        #
        an_account = BankAccountDecorator.objects.create(number='12345-6')
        an_analyst = CreditAnalystDecorator.objects.create(register='abcde-f')
        (LoanRequest, 'I am not an account', 123, an_analyst) |should| throw(AssociationError)
        (LoanRequest, an_account, 123, 'I am not an analyst') |should| throw(AssociationError)
        (LoanRequest, an_account, 123, an_analyst) |should_not| throw(AssociationError)

################################################# LOAN ###################################################################
class LoanSpec(unittest.TestCase):

    def test_check_association_with_loan_request(self):
        #set the rule base
        RuleManager.rule_base = BankSystemRuleBase()
        #
        (Loan, 'I am not a loan request') |should| throw(AssociationError)
        a_credit_analyst_decorator = CreditAnalystDecorator.objects.create(register='12345-6')
        an_account = BankAccountDecorator.objects.create(number='1234567-8')
        a_loan_request = LoanRequest(an_account, 7000, a_credit_analyst_decorator)
        (Loan, a_loan_request) |should_not| throw(AssociationError)

