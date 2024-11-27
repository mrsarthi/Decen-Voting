from web3 import Web3
import json

# Connect to local Ethereum blockchain (Ganache)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Check connection
if not w3.isConnected():
    print("Unable to connect to the Ethereum network")
    exit()

# Load the compiled contract
with open("build/contracts/Voting.json", "r") as file:
    contract_json = json.load(file)

# Extract ABI and Bytecode
contract_abi = contract_json["abi"]
contract_bytecode = contract_json["bytecode"]

# Set the deployer account
deployer_account = w3.eth.accounts[0]

# Set up the contract
VotingContract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)

# Build the transaction
transaction = VotingContract.constructor().build_transaction({
    "from": deployer_account,
    "nonce": w3.eth.get_transaction_count(deployer_account),
    "gas": 3000000,
    "gasPrice": w3.to_wei("20", "gwei")
})

# Sign the transaction
private_key = "<private_key_of_deployer_account>"  # Replace with the private key
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction receipt
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)

# Get the contract address
print(f"Contract deployed at address: {txn_receipt.contractAddress}")
