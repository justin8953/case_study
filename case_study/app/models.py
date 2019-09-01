from django.db import models
import datetime

# Create your models here.

#  Table for funds with fund id and fund name
class Fund(models.Model):
   id = models.AutoField(primary_key = True)
   name = models.CharField(max_length = 50)

   # Return a name for the object
   def __str__(self):
      return self.name

# Table for commitments with commitment id, fund id, committed date, and the amount of the commitment
class Commitment (models.Model):
   id = models.AutoField(primary_key = True)
   fund = models.ForeignKey(Fund, on_delete = models.CASCADE)
   committedDate  = models.DateField()
   amount = models.BigIntegerField()
   

   def __str__(self):
      return "commitment"+str(self.id)
   # default format  is  YYYY-MM-DD
   def formattedDate(self):
        return self.committedDate.strftime('%d/%m/%Y')
   class Meta:
      ordering = ['committedDate']

# Table for calls from the investor with call id, investment name, the amount of investment requirement, and the called date 
class Call(models.Model):
   id = models.AutoField(primary_key = True)
   call_id = models.IntegerField(null=True, blank=True)
   investName = models.CharField(max_length = 100)
   investRequire = models.BigIntegerField()
   calledDate = models.DateField()

   # default format  is  YYYY-MM-DD
   def formattedDate(self):
        return self.calledDate.strftime('%d/%m/%Y')

   def __str__(self):
      return "call" + str(self.call_id)


# Table for each fund investment in each call with investment id, call id, commitment id, fund id, and the amount of investment in each fund 
class FundInvest(models.Model):
   id = models.AutoField(primary_key = True)
   call_id = models.ForeignKey(Call, on_delete = models.CASCADE)
   commit_id = models.ForeignKey(Commitment, on_delete = models.CASCADE)
   fund_id = models.ForeignKey(Fund, on_delete = models.CASCADE)
   investAmount = models.BigIntegerField()




   
