from rest_framework import serializers
from app.models import Fund, Commitment, Call, FundInvest

class FundSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = Fund
      fields = '__all__'


class SingleFundInvestSerializer(serializers.Serializer):
    fund = serializers.IntegerField()
    amount = serializers.IntegerField()

class FundSummarySerializer(serializers.Serializer):
   id = serializers.IntegerField()
   date = serializers.DateField(format="%d/%m/%Y")
   funds = SingleFundInvestSerializer(many=True)

class CalculateSerializer(serializers.Serializer):
   commit_id = serializers.IntegerField()
   fund_id = serializers.IntegerField()
   fund = serializers.CharField()
   date = serializers.DateField(format="%d/%m/%Y")
   amount = serializers.IntegerField()
   notice = serializers.IntegerField()


class CommitmentSerializer(serializers.ModelSerializer):
   committedDate = serializers.DateField(format="%d/%m/%Y")
   class Meta:
      model = Commitment
      fields = '__all__'

class CallSerializer(serializers.ModelSerializer):
   calledDate = serializers.DateField(format="%d/%m/%Y")

   class Meta:
      model = Call
      fields = '__all__'

class FundInvestSerializer(serializers.ModelSerializer):
   
   class Meta:
      model = FundInvest
      fields = '__all__'
