import os, subprocess

def get_balance(public_key):
    output = subprocess.getoutput(f"solana balance {public_key}")
    return output

def create_wallet(from_mob):
    output1 = subprocess.getoutput(f"solana-keygen new --no-passphrase -o /root/solanakey/{from_mob}.json")
    return output

def transfer(from_mob,to_public_key,amount):
    output=subprocess.getoutput(f"solana transfer --from /root/solanakey/{from_mob}.json {to_public_key} 1 --allow-unfunded-recipient --url https://api.devnet.solana.com --fee-payer /root/solanakey/{from_mob}.json")
    return output
