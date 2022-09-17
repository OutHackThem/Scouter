from jmespath import search as queryJson
import botocore
import boto3

session = boto3.Session()
fileName 		= "LambdFunction_with_exposed_Environment_Variables.csv"


def writeIntoFile(filename, stdout, method='w+'):
	with open(filename, method) as f: f.write(stdout)


def authorizedClientCall():
	client 		= session.client("lambda")
	return(client)

def parseJson(query, jsonObj):
	return(queryJson(query, jsonObj))

def getAccountId():
	return session.client('sts').get_caller_identity().get('Account')


def fetchLambdaNames(clientApiCall):
	fetchFunctions 	= clientApiCall.list_functions()
	nameArray 		= parseJson('Functions[*].FunctionName', fetchFunctions)
	AccountId 		= getAccountId()
	for name in nameArray:
		n = 4
		try:
			getlambdaDetails 	= clientApiCall.get_function_configuration(FunctionName=name)

			if( 'Environment' in getlambdaDetails ):
				envVariableData	= getlambdaDetails['Environment']['Variables']
				print(f"[+] {name} : {envVariableData}")
				writeIntoFile(fileName, f"ID:{AccountId},{name},{envVariableData}\n", method ='a+')
			else:
				print(f"[!] {name} : No Env Variables")

		except botocore.exceptions.ClientError:
			print(f"[!!!] {name}: -- Access Denied")


def main():
	writeIntoFile( fileName, "AccountID,Function Name,Env Vars\n", method = 'w+')
	clientCall 	= authorizedClientCall()
	fetchLambdaNames(clientCall)

# session = boto3.Session()

# accountId = session.client('sts').get_caller_identity().get('Account')

# lambdaClient = session.client('lambda')

# response = lambdaClient.list_functions()
# response2 = lambdaClient.get_function_configuration(FunctionName='myNewFunc')

# for x in response2['Environment']['Variables']:
# 	print(response2['Environment']['Variables'])

main()
