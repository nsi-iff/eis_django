from should_dsl import should, ShouldNotSatisfied
from domain.supportive.rule import rule
from domain.supportive.core_rules import CoreRules


class BankSystemRuleBase(CoreRules):
    @rule('association')
    def should_be_instance_of_bank_account(self, associated):
        '''Associated object should be instance of Bank Account Decorator'''
        from bank_system.models import BankAccountDecorator
        try: associated |should| be_instance_of(BankAccountDecorator)
        except ShouldNotSatisfied: return False
        else: return True

    @rule('association')
    def should_be_instance_of_credit_analyst(self, associated):
        '''Associated object should be instance of Credit Analyst Decorator'''
        from bank_system.models import CreditAnalystDecorator
        try: associated |should| be_instance_of(CreditAnalystDecorator)
        except ShouldNotSatisfied: return False
        else: return True

    @rule('association')
    def should_be_instance_of_loan_request(self, associated):
        '''Associated object should be instance of Loan Request'''
        from bank_system.resources.loan_request import LoanRequest
        try: associated |should| be_instance_of(LoanRequest)
        except ShouldNotSatisfied: return False
        else: return True

    @rule('association')
    def should_have_employee_decorator(self, associated):
        '''Associated object should be previously decorated by Employee'''
        from bank_system.models import EmployeeDecorator
        import domain.supportive.contract_matchers
        try: associated |should| be_decorated_by(EmployeeDecorator)
        except ShouldNotSatisfied: return False
        else: return True

