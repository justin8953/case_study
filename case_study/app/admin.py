from django.contrib import admin
from .models import Fund, Commitment, Call, FundInvest
# Register your models here.

admin.site.register(Fund)
admin.site.register(Commitment)
admin.site.register(Call)
admin.site.register(FundInvest)
