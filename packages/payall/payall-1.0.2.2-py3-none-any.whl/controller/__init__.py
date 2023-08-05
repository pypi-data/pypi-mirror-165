import json, re
import solanaprocessor as solanaprocessor

def sol_get_balance(from_public_key):
    return solanaprocessor.get_balance(from_public_key)

def sol_payment(from_mob,to_public_key,amount):
    return solanaprocessor.transfer(from_mob,to_public_key,amount)

def acc_statement():
    pass

def sol_create_wallet(from_mob):
    resp=solanaprocessor.create_wallet(from_mob)
    reg="(?<=pubkey: ).*(?=)"
    reg2="(?<=keypair:\n).*(?=)"
    public_key = re.findall(reg, resp)
    phrase = re.findall(reg2, resp)
    return public_key[0],phrase[0]