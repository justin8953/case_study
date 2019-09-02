from django.test import TestCase
from app.models import Fund, Commitment, Call, FundInvest
from app.serializer import FundSerializer, CommitmentSerializer, \
CallSerializer, FundInvestSerializer, SingleFundInvestSerializer, FundSummarySerializer, CalculateSerializer
import datetime
import json
# Create your tests here.

# Fund table testing case
def create_fund():
   Fund.objects.create(name='Fund 1')
   Fund.objects.create(name='Fund 2')
   Fund.objects.create(name='Fund 3')
   Fund.objects.create(name='Fund 4')

def create_commit(fund1,fund2,fund3,fund4):
   Commitment.objects.create(fund=fund1, committedDate='2017-12-31', amount=10000000)
   Commitment.objects.create(fund=fund2, committedDate='2018-03-31', amount=15000000)
   Commitment.objects.create(fund=fund3, committedDate='2018-06-30', amount=10000000)
   Commitment.objects.create(fund=fund4, committedDate='2018-09-30', amount=15000000)
   Commitment.objects.create(fund=fund1, committedDate='2018-12-31', amount=10000000)

def create_call():
   Call.objects.create(call_id=1,investName="Investment 1",investRequire=9500000,calledDate='2018-01-31')
   Call.objects.create(investName="Investment 2",investRequire=10000000,calledDate='2018-04-30')

class FundSerializerTest(TestCase):
   def setUp(self):
      data = {
         'name': 'Fund 1'
      }
      serializer = FundSerializer(data=data)
      if (serializer.is_valid()):
         serializer.save()
         print(serializer.data)
   def testSerializerCreate(self):
      fund = Fund.objects.get(id=1)
      self.assertEqual(fund.name, 'Fund 1')


class FundTestCase(TestCase):
   def setUp(self):
      create_fund()
   
   # Test the records created
   def test_fund_successCreate (self):
      funds = Fund.objects.all()
      numberofFunds= len(funds)
      self.assertEqual(numberofFunds,4)
      
      # Clean testing case
      funds = Fund.objects.all()
      funds.delete()
   
   # Test each record followed auto increment id
   def test_fund_autoincrementID(self):
      
      fund1 = Fund.objects.get(pk = 1)
      fund2 = Fund.objects.get(pk = 2)
      fund3 = Fund.objects.get(pk = 3)
      fund4 = Fund.objects.get(pk = 4)

      self.assertEqual(fund1.name,"Fund 1")
      self.assertEqual(fund2.name,"Fund 2")
      self.assertEqual(fund3.name,"Fund 3")
      self.assertEqual(fund4.name,"Fund 4")
      
      # Clean testing case
      funds = Fund.objects.all()
      funds.delete()

class CommitSerializerTest(TestCase):
   def setUp(self):
      fundData = {
         'name': 'Fund 1',
      }
      serializer = FundSerializer(data=fundData)
      if (serializer.is_valid()):
         serializer.save()
         print(serializer.data)
      commitData = {
         'committedDate':'31/12/2018',
         'amount':10000000,
         'fund': 1
      }
      serializer2 = CommitmentSerializer(data=commitData)
      print(serializer2)
      if (serializer2.is_valid()):
         serializer2.save()
         print(serializer2.data)
      else:
         print(serializer2.errors)
   def testSerializerCreate(self):
      fund = Fund.objects.get(id=1)
      self.assertEqual(fund.name, 'Fund 1')
      commit = Commitment.objects.get(id=1)
      self.assertEqual(commit.fund, fund)


class CommitmentTestCase(TestCase):
   def setUp(self):
      # Create Funds
      create_fund()
      funds = Fund.objects.all()
      # get each Fund
      fund1 = funds[0]
      fund2 = funds[1]
      fund3 = funds[2]
      fund4 = funds[3]
      # Five commitments
      create_commit(fund1,fund2,fund3,fund4)
      
   # Test the records created
   def test_commitment_successCreate (self):
      commits = Commitment.objects.all()
      numberofCommit= len(commits)
      self.assertEqual(numberofCommit,5)
      

   # Test each record followed auto increment id
   def test_fund_autoincrementID(self):

      commits = Commitment.objects.all()

      #  get each commitment
      commits1 = commits[0]
      commits2 = commits[1]
      commits3 = commits[2]
      commits4 = commits[3]
      commits5 = commits[4]
      
      funds = Fund.objects.all()
      # get each fund 
      fund1 = funds[0]
      fund2 = funds[1]
      fund3 = funds[2]
      fund4 = funds[3]

      self.assertEqual(commits1.fund,fund1)
      self.assertEqual(commits2.fund,fund2)
      self.assertEqual(commits3.fund,fund3)
      self.assertEqual(commits4.fund,fund4)
      self.assertEqual(commits5.fund,fund1)


   def test_commitment_formattedDate(self):
      commits1 = Commitment.objects.get(pk = 1)
      self.assertEqual(commits1.formattedDate(),'31/12/2017')

class CallTestCase(TestCase):
   def setUp(self):
      print("Create call ....")
      create_call()
   
   # Test the records created
   def test_call_successCreate (self):
      calls = Call.objects.all()
      numberofCall= len(calls)
      self.assertEqual(numberofCall,2)
   
   def test_calls_autoincrementID(self):

      calls = Call.objects.all()
      #  get each commitment
      call1 = calls[0]
      call2 = calls[1]

      self.assertEqual(call1.pk,1)
      self.assertEqual(call2.pk,2)

   def test_call_formattedDate(self):
      call1 = Call.objects.get(pk = 1)
      self.assertEqual(call1.formattedDate(),'31/01/2018')

class FundSerializerTestCase (TestCase):
   
   def setUp(self):
      create_fund()
      funds = Fund.objects.all()
      self.fundserializer = FundSerializer(funds[0])
   
   def test_fundserializer_successCreate (self):
      data = self.fundserializer.data
      self.assertEqual(data, {'id':1, 'name':'Fund 1'})


class CommitmentSerializerTestCase (TestCase):
   
   def setUp(self):
      create_fund()
      funds = Fund.objects.all()
      # get each Fund
      fund1 = funds[0]
      fund2 = funds[1]
      fund3 = funds[2]
      fund4 = funds[3]
      # Five commitments
      create_commit(fund1,fund2,fund3,fund4)
      commits = Commitment.objects.all()
      self.commitmentserializer = CommitmentSerializer(commits[0])
   
   def test_commitserializer_successCreate (self):
      data = self.commitmentserializer.data
      self.assertEqual(data, {'id':1,'fund':1,'committedDate':'2017-12-31' ,'amount':10000000})

class CallSerializerTestCase (TestCase):
   
   def setUp(self):
      create_call()
      calls = Call.objects.all()
      self.callserializer = CallSerializer(calls[0])
   
   def test_callserializer_successCreate (self):
      data = self.callserializer.data
      self.assertEqual(data,
       {'id':1, 'call_id':1, 'investName':'Investment 1',
      'investRequire':9500000,'calledDate':'2018-01-31'})    

class SummaryTestCase(TestCase):

   def setUp(self):
      create_fund()
      funds = Fund.objects.all()
      # get each Fund
      fund1 = funds[0]
      fund2 = funds[1]
      fund3 = funds[2]
      fund4 = funds[3]
      # Five commitments
      create_commit(fund1,fund2,fund3,fund4)
      create_call()
      commit1  = Commitment.objects.all()[0]
      call1 = Call.objects.all()[0]
      FundInvest.objects.create(call_id = call1,commit_id =commit1,fund_id = fund1, investAmount= 9000000)
      FundInvest.objects.create(call_id = call1,commit_id =commit1,fund_id = fund2, investAmount= 500000)

   def test1(self):
      class SingleFund(object):
         def __init__(self, fund, amount):
            self.fund = fund
            self.amount = amount
      
      class FundSummary(object):
         def __init__ (self, id, date, funds):
            self.id = id
            self.date = date
            self.funds = funds


      fundinvest = list(FundInvest.objects.select_related('call_id','commit_id','fund_id').all())
      fundIds =[ele.pk for ele  in list(Fund.objects.all())]
      FundInvestTable = {}
      
      for ele in fundinvest:
         call_id = ele.call_id.id
         calledDate = ele.call_id.formattedDate()
         fund_id = ele.fund_id.id
         amount = ele.investAmount
         if call_id not in FundInvestTable:
            FundInvestTable[call_id] = []
         fund = SingleFund(fund_id,amount)
         FundInvestTable[call_id].append(fund)
      
      SummaryList = []

      for key, value in FundInvestTable.items():
         date = Call.objects.get(pk= key).calledDate
         SummaryList.append(FundSummary(key, date, value))
      serializer = FundSummarySerializer(SummaryList[0])
      
      self.assertEqual(serializer.data['id'], 1)
      self.assertEqual(serializer.data['date'], '31/01/2018')
      self.assertEqual(len(serializer.data['funds']), 2)

class CalulateTestCase(TestCase):
   def setUp(self):
      create_fund()
      funds = Fund.objects.all()
      # get each Fund
      fund1 = funds[0]
      fund2 = funds[1]
      fund3 = funds[2]
      fund4 = funds[3]
      # Five commitments
      create_commit(fund1,fund2,fund3,fund4)
      create_call()
      commit1  = Commitment.objects.all()[0]
      call1 = Call.objects.all()[0]
      call2 = Call.objects.all()[1]

      FundInvest.objects.create(call_id = call1,commit_id =commit1,fund_id = fund1, investAmount= 9500000)

   def test1 (self):
      commits = Commitment.objects.all()
      fundinvests = FundInvest.objects.all()

      
      class CalculateTable(object):
         def __init__(self,commit_id, fund_id, fund,date, amount, notice):
            self.commit_id = commit_id
            self.fund_id = fund_id
            self.fund = fund
            self.date = date
            self.amount = amount
            self.notice = notice

      commitList = []
      for ele in commits:
         commit_id = ele.id
         fund_id = ele.fund.id
         fund = ele.fund.name
         date = ele.committedDate
         amount = ele.amount
         if(FundInvest.objects.filter(commit_id=commit_id, fund_id=fund_id).exists()):
            spend = FundInvest.objects.get(commit_id=commit_id, fund_id=fund_id).investAmount
         else:
            spend = 0
         notice = ele.amount - spend
         commitList.append(CalculateTable(commit_id, fund_id, fund, date, amount, notice))   
      serializer  = CalculateSerializer(commitList, many=True)

      test = serializer.data[0]

      self.assertEqual(test['commit_id'], 1)
      self.assertEqual(test['date'], '31/12/2017')
      self.assertEqual(test['fund'], 'Fund 1')
      self.assertEqual(test['fund_id'], 1)
      self.assertEqual(test['amount'], 10000000)
      self.assertEqual(test['notice'], 500000)
