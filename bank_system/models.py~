import sys
sys.path.append("home/mari/eis-examples-mari")
sys.path.append("/home/mari/eis-mari")

#todas as classes estao aqui. Eh a 'python way' de fazer...
#Para resources => subclasses. (tal como marca e modelo, para produto...)
#Para nodes => decorators.
#Para movements => configuracao.

from django.db import models
from should_dsl import should
from domain.resource.work_item import WorkItem
from domain.base.decorator import Decorator
from domain.node.person import Person
from domain.supportive.rule import rule
from domain.supportive.association_error import AssociationError
from domain.node.machine import Machine
from domain.supportive.contract_error import ContractError
from bank_system.resources.loan_request import LoanRequest
from bank_system.resources.loan import Loan
from bank_system.rules.bank_system_rule_base import BankSystemRuleBase
from domain.supportive.rule_manager import RuleManager
from domain.resource.operation import operation
from should_dsl import should, ShouldNotSatisfied
from domain.node.node import Node
from domain.resource.operation import operation


################################################# DECORATOR: BANK ACCOUNT ##############################################################
class BankAccountDecorator(models.Model, Decorator):
    '''Bank Account'''
    decoration_rules = ['should_be_instance_of_machine']

  #  def __init__(self, number):
    id = models.AutoField(primary_key=True)
    description = "A bank account decorator" #models.CharField(max_length=100)
    #log area for already processed resources
    log_area = {} #models.CharField(max_length=200)
    balance =  0 #models.IntegerField()
    #should it mask Machine.tag? decorated.tag = number?
    number = models.CharField(max_length="20")
    restricted = 0 #models.BooleanField()
    average_credit = 0 #models.IntegerField()
    def save(self, *args, **kwargs):
        super(BankAccountDecorator, self).save(*args, **kwargs)
        Decorator.__init__(self)

    @operation(category='business')
    def register_credit(self, value):
        ''' Register a credit in the balance '''
        self.balance += value

    @operation(category='business')
    def send_message_to_account_holder(self, message):
        ''' Sends a message to the account holder '''
        return message


############################################ DECORATOR: CREDIT ANALYST #############################################################
class CreditAnalystDecorator(models.Model, Decorator):
    '''Credit Analyst'''
    decoration_rules = ['should_have_employee_decorator']

    id = models.AutoField(primary_key=True)
    description = "An employee with credit analysis skills"
    register = models.CharField(max_length="20")
    loan_limit = 0

    def save(self, *args, **kwargs):
        super(CreditAnalystDecorator, self).save(*args, **kwargs)
        Decorator.__init__(self)

    @operation(category='business')
    def create_loan_request(self, account, value):
        ''' creates a loan request '''
        loan_request = LoanRequest(account, value, self)
        #places the loan_request in the node's input area
        self.decorated.input_area[loan_request.account.number] = loan_request

    #stupid credit analysis, only for demonstration
    @operation(category='business')
    def analyse(self, loan_request_key):
        ''' automatically analyses a loan request '''
        if not self.decorated.input_area.has_key(loan_request_key): return False
        #move the request from the input_area to the processing_area
        self.decorated.transfer(loan_request_key,'input','processing')
        #picks the loan for processing
        loan_request = self.decorated.processing_area[loan_request_key]
        #automatically approves or not
        if not loan_request.account.restricted:
           if loan_request.account.average_credit*4 > loan_request.value:
               loan_request.approved = True
           else:
               loan_request.approved = False
        else:
           loan_request.approved = False
        #transfers the loan to the output_area
        self.decorated.transfer(loan_request_key,'processing','output')

    @operation(category='business')
    def create_loan(self, loan_request):
        ''' creates a loan '''
        loan = Loan(loan_request)
        #puts the new loan on the analyst's output_area, using analyst's register as key
        self.decorated.output_area[loan.loan_request.analyst.register] = loan

    @operation(category='business')
    def move_loan_to_account(self, loan_key, account):
        ''' moves the approved loan to the account '''
        try:
            loan = self.decorated.output_area[loan_key]
            loan |should| be_instance_of(Loan)
        except KeyError:
            raise KeyError("Loan with key %s not found in Analyst's output area" % loan_key)
        except ShouldNotSatisfied:
            raise ContractError('Loan instance expected, instead %s passed' % type(loan))
        try:
            Node.move_resource(loan_key, self.decorated, account.decorated)
        except ShouldNotSatisfied:
            raise ContractError('Bank Account instance expected, instead %s passed' % type(account))
        account.register_credit(loan.loan_request.value)

    def change_loan_limit(self, new_limit):
        self.loan_limit = new_limit

################################################# DECORATOR: EMPLOYEE ##############################################################

class EmployeeDecorator(models.Model, Decorator):
    '''A general purpose Employee decorator'''
    decoration_rules = ['should_be_instance_of_person']

    id = models.AutoField(primary_key=True)
    description = "Supplies the basis for representing employes"
    name = models.CharField(max_length='40')

    def save(self, *args, **kwargs):
        super(EmployeeDecorator, self).save(*args, **kwargs)
        Decorator.__init__(self)

    def generate_register(self, register):
        ''' generates the register number for the employee '''
        self.register = register

#Um decorator Cliente envelopa um objeto Person.
#Se o cliente for uma empresa, ele envelopa uma Machine.
#Significa que suas association rules devem ser do tipo decorated |should| be_instance_of(Node) (que inclui Person e Machine)
#class CustomerDecorator(models.Model, Decorator): #decoracao concreta.... tem uma estancia de Person, que sera decorado'

#- Estoque(Decorator de No, com 'ponteiros' para as instancias de Produto)
#Note que movimentacoes de estoque sao representadas por um ou mais movements.
#Saida de item do estoque para o cliente => movement entre os nos Estoque e Cliente.
#class Stock(fk_product, in_stock)

#class Sale(fk_product, fk_cliente, data) ---> has_many products, belongs_to product / has_many clientes, belongs_to clientes
#Instancia de Process

#class Exchange(fk_product, fk_cliente, data, defeito_apresentado) ---> has_one product, belongs_to product
#Instancia de Process

