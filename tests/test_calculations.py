import pytest
from app.calculations import add , BankAccount , InsufficintFunds


@pytest.mark.parametrize("x,y,res" ,
                         [
                          (3,2,5), 
                          (5,6,11)   
                         ])
def test_add(x,y,res):
    assert add(x,y) == res 

@pytest.fixture
def ac_amt_initialize():
    return BankAccount(100) 

@pytest.fixture
def zero_bak_acc():
    print("creating empty bank ac")
    return BankAccount() 



def test_bank_set_initial_amount(ac_amt_initialize):
    assert ac_amt_initialize.balance==100   

def test_bank_default_amount(zero_bak_acc):
    print("testing my bank account")
    assert zero_bak_acc.balance==0   

def test_windraw(ac_amt_initialize):
    ac_amt_initialize.withdraw(20)
    assert ac_amt_initialize.balance==80

def test_deposit(ac_amt_initialize):
    ac_amt_initialize.deposit(20)
    assert ac_amt_initialize.balance==120    


def test_bank_transac(zero_bak_acc):
    zero_bak_acc.deposit(200)
    zero_bak_acc.withdraw(50)
    assert zero_bak_acc.balance==150


@pytest.mark.parametrize("deposited,withdraw,expected" , [
    (200,20,180),
    (100,40,60)
])
def test_bank_transac2(zero_bak_acc , deposited , withdraw , expected):
    zero_bak_acc.deposit(deposited)
    zero_bak_acc.withdraw(withdraw)
    assert zero_bak_acc.balance==expected

def test_insufficient_funds(ac_amt_initialize):
    # with pytest.raises(Exception):
    with pytest.raises(InsufficintFunds):
       ac_amt_initialize.withdraw(200)


