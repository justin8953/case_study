from populate import base
from app.models import Fund, Commitment, Call, FundInvest



def populate():
    FundInvest.objects.all().delete()
    Call.objects.all().delete()
    Commitment.objects.all().delete()
    Fund.objects.all().delete()
    fund_name = ['Fund 1', 'Fund 2', 'Fund 3', 'Fund 4']
    print("Create Fund ......")
    for ele in fund_name:
        Fund.objects.create(name = ele)
    print("Create Success ......")
    commitment = {'2017-12-31':[1, 10000000], '2018-3-31':[2,15000000],'2018-6-30':[3,10000000],'2018-9-30':[4,15000000],'2018-12-31':[1,10000000] }
    print("Create Commitment ......")
    for key, value in commitment.items():
        fund = Fund.objects.get(pk=value[0])
        Commitment.objects.create(fund = fund, committedDate = key, amount = value[1])
    print("Create Success ......")
    print("Create Call ......")    
    Call.objects.create(call_id = 1, calledDate = '2018-1-31', investName = 'Investment 1', investRequire = 9500000)
    print("Create Success ......")
    print("Create Fund Investment ......")    
    call  = Call.objects.get(id=1)
    commit  = Commitment.objects.get(id=1)
    fund = Fund.objects.get(id=1)
    FundInvest.objects.create(call_id=call, commit_id=commit, fund_id = fund, investAmount =9500000 )
    print("Create Success ......")

    print("Finish .....")

    

    
if __name__ == '__main__':
    populate()
