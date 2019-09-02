from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from app.models import Fund, Commitment, Call, FundInvest
from app.serializer import FundSerializer, CommitmentSerializer, CallSerializer, FundInvestSerializer,SingleFundInvestSerializer, FundSummarySerializer, CalculateSerializer
from rest_framework.response import Response
from rest_framework import status
import sys, json
# Create your views here.

class FundViewSet(viewsets.ViewSet):
   """
   A viewset for viewing and editing user instances.
   """
   def list(self, request):
      queryset = Fund.objects.all()
      serializer = FundSerializer(queryset, many=True)
      return Response (serializer.data)
   def retrieve(self, request, pk=None):
      queryset = Fund.objects.all()
      fund = get_object_or_404(queryset, pk=pk)
      serializer = FundSerializer(fund)
      return Response(serializer.data)
   def create(self, request):
      #  Transfer Queryset to string
      data = json.dumps(request.data)
      # Transfer string to Dict
      data = json.loads(data)
      serializer = FundSerializer(data=data)
      if (serializer.is_valid()):
         serializer.save()
         return Response(serializer.data)
      else:
         print(serializer.errors)
         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CommitViewSet(viewsets.ViewSet):
   """
   A viewset for viewing and editing user instances.
   """
   def list(self, request):
      queryset = Commitment.objects.all()
      serializer = CommitmentSerializer(queryset, many=True)
      return Response (serializer.data)    
   def retrieve(self, request, pk=None):
      queryset = Commitment.objects.all()
      commit = get_object_or_404(queryset, pk=pk)
      serializer = CommitmentSerializer(commit)
      return Response(serializer.data) 
   def create(self, request):
      #  Transfer Queryset to string
      data = json.dumps(request.data)
      # Transfer string to Dict
      data = json.loads(data)
      serializer = CommitmentSerializer(data = data)
      if(serializer.is_valid()):
         serializer.save()
         return Response(serializer.data)
      else:
         return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class CallViewSet(viewsets.ViewSet):
   """
   A viewset for viewing and editing user instances.
   """
   def list(self, request):
      queryset = Call.objects.all()
      serializer = CallSerializer(queryset, many=True)
      return Response (serializer.data)
      
   def retrieve(self, request, pk=None):
      queryset = Call.objects.all()
      call = get_object_or_404(queryset, pk=pk)
      serializer = CallSerializer(call)
      return Response(serializer.data)
   
   def create(self, request):
      try:
         # Need to fixed
         date = request.data['date']
         investName = request.data['investName']
         amount = request.data['requirement']
         call = Call.objects.create(calledDate = date, investName = investName, investRequire=amount)
         call.call_id = call.pk
         call.save()
         serializer = CallSerializer(call)
         return Response(serializer.data)

      except:
         return Response ("Fail to create",status=status.HTTP_404_NOT_FOUND)
  
class FundInvestViewSet(viewsets.ViewSet):

   """
   A viewset for viewing and editing user instances.
   """

   def list(self, request):
      queryset = FundInvest.objects.all()
      serializer = FundInvestSerializer(queryset, many=True)
      return Response (serializer.data)
      
   def retrieve(self, request, pk=None):
      queryset = FundInvest.objects.all()
      fundinvest = get_object_or_404(queryset, pk=pk)
      serializer = FundInvestSerializer(fundinvest)
      return Response(serializer.data)
   
   def create(self, request):
      print(request.data)
      try:
         # Need to fixed
         call_id = request.data['call_id']
         commit_id = request.data['commit_id']
         fund_id = request.data['fund_id']
         call = Call.objects.get(call_id=call_id)
         fund = Fund.objects.get(pk=fund_id)
         commit = Commitment.objects.get(pk=commit_id)
         investAmount = request.data['invest_amount']
         fundinvest = FundInvest.objects.create(call_id = call, commit_id = commit, fund_id=fund, investAmount=investAmount)
         serializer = FundInvestSerializer(fundinvest)
         return Response(serializer.data)

      except:
         return Response ("Fail to create",status=status.HTTP_404_NOT_FOUND)



#  Fund object with fund id and amount
class SingleFund(object):
   def __init__(self, id, amount):
      self.fund = id
      self.amount = amount

#  Fund summary object for dashboard
class FundSummary(object):
   def __init__ (self, id, date, funds):
      self.id = id
      self.date = date
      self.funds = funds


class DashboardViewSet(viewsets.ViewSet):

   def list(self, request):
      
      fundinvest = list(FundInvest.objects.select_related('call_id','commit_id','fund_id').all())
      
      #  Each Fund Investment
      FundInvestTable ={}
      for ele in fundinvest:
         call_id = ele.call_id.id
         calledDate = ele.call_id.formattedDate()
         fund_id = ele.fund_id.id
         amount = ele.investAmount
         if call_id not in FundInvestTable:
            FundInvestTable[call_id] = []
         fund = SingleFund(fund_id,amount)
         FundInvestTable[call_id].append(fund)
      
      #  Dash Board Summary List
      SummaryList = []
      for key, value in FundInvestTable.items():
         date = Call.objects.get(pk= key).calledDate
         SummaryList.append(FundSummary(key, date, value))
      serializer = FundSummarySerializer(SummaryList, many=True)
      return Response(serializer.data)



class CalculateTable(object):
   def __init__(self,commit_id, fund_id, fund ,date, amount, notice):
      self.commit_id = commit_id
      self.fund_id = fund_id
      self.fund = fund
      self.date = date
      self.amount = amount
      self.notice = notice


class CalculateViewSet(viewsets.ViewSet):

   def list(self, request):
      commits = Commitment.objects.all()
      commitList = []
      for ele in commits:
         commit_id = ele.id
         fund_id = ele.fund.id
         fund = ele.fund.name
         date = ele.committedDate
         amount = ele.amount
         if(FundInvest.objects.filter(commit_id=commit_id, fund_id=fund_id).exists()):
            total = FundInvest.objects.filter(commit_id=commit_id, fund_id=fund_id)
            if len(total)==1:
               spend = FundInvest.objects.get(commit_id=commit_id, fund_id=fund_id).investAmount
            else:
               spend =sum ([ele.investAmount for ele in total])
         else:
            spend = 0
         notice = ele.amount - spend
         commitList.append(CalculateTable(commit_id, fund_id, fund, date, amount, notice))   
      
      serializer  = CalculateSerializer(commitList, many=True)
      return Response(serializer.data)
