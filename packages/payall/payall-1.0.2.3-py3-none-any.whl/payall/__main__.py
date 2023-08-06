import os
import sys
import argparse
from controller import *

from importlib_metadata import version
import warnings

warnings.filterwarnings("ignore")
v = version('payall')


def main():

	program_descripton = f'''
 ______                  _ _ 
(_____ \                | | |
 _____) )___ _   _  ____| | |
|  ____/ _  | | | |/ _  | | |
| |   ( ( | | |_| ( ( | | | |
|_|    \_||_|\__  |\_||_|_|_|
            (____/           

Cross Chain Streamlined Payment Engine - v{v}

Created by Hash-It
Copyright 2022. All rights reserved.
    '''
	parser = argparse.ArgumentParser(description=program_descripton,formatter_class=argparse.RawTextHelpFormatter, add_help=True, usage='python -m payall -c <crypto> -t <type>')
	parser.add_argument('-c', '--crypto', dest='crypto', type=str, help='sol for solana', metavar='')
	parser.add_argument('-t', '--type', dest='type', type=str, help='create/balance/transfer', metavar='')
	parser.add_argument('-ph', '--phone', dest='phone', type=str, help='If create, -ph <phone>', metavar='')
	# parser.add_argument('-tv', '--tovpa', dest='tovpa', type=str, help='If transfer, provide -tv <vpa>', metavar='')
	parser.add_argument('-p', '--pub', dest='pub', type=str, help='If transfer(receiver pub)/balance(your pub), provide -p <public-key>', metavar='')
	parser.add_argument('-a', '--amount', dest='amount', type=str, help='If transfer, provide -a <amount>', metavar='')

	args = parser.parse_args()

	if (args.crypto).lower()=='sol':
		if (args.type).lower()=='create':
			sol_create_wallet(args.phone)
		elif (args.type).lower()=='balance':
			sol_get_balance(args.pub)
		elif (args.type).lower()=='transfer':
			sol_payment(args.phone,args.pub,args.amount)
		else:
			print("# Incorrect Input")
			exit(1)
	else:
		print("# Incorrect Input")
		exit(1)

if __name__=="__main__":
	main()

