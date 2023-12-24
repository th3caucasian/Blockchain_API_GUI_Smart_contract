import web3
import json
class API():

    def __init__(self, current_user, password):
        self.w3 = web3.Web3(web3.HTTPProvider("http://127.0.0.1:8545"))
        print(self.w3.is_connected())

        with open("./ABI.txt", "r") as f:
            abi = json.loads(f.read())
        contract_address = web3.Web3.to_checksum_address("0x7B5749E25f43525CAe0cc5b1F1962936cc44169a")
        self.sc = self.w3.eth.contract(address = contract_address, abi = abi)

        self.current_user = current_user
        self.password = password

    def auth(self):
        print(self.current_user, self.password)
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)


    def GetAccounts(self):
        return self.w3.eth.accounts

    def GetBalance(self, address):
        return web3.Web3.from_wei(self.w3.eth.get_balance(address),"ether")

    def admin(self):
        return self.sc.functions.admin().call()

    def AddOrder(self, table_num: int, dish_name: str, dish_price: int):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        order = self.sc.functions.AddOrder(table_num, dish_name, dish_price).transact({"from": self.current_user})
        self.w3.eth.wait_for_transaction_receipt(order)
        self.w3.geth.miner.stop()

    def OrderIsReady(self):
        self.w3.geth.personal.unlock_account(self.current_user, "1", 0)
        self.w3.geth.miner.start()
        order = self.sc.functions.OrderIsReady().transact({"from": self.current_user})
        self.w3.eth.wait_for_transaction_receipt(order)
        self.w3.geth.miner.stop()

    def GetATable(self):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        table = self.sc.functions.GetATable().transact({"from": self.current_user})
        self.w3.eth.wait_for_transaction_receipt(table)
        self.w3.geth.miner.stop()

    def MakeCheck(self, table_num):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        check = self.sc.functions.MakeCheck(table_num).transact({"from": self.current_user})
        self.w3.eth.wait_for_transaction_receipt(check)
        self.w3.geth.miner.stop()

    def PayNLeave(self, table_num, value):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        order = self.sc.functions.PayNLeave(table_num).transact({"from": self.current_user, "value": value})
        self.w3.eth.wait_for_transaction_receipt(order)
        self.w3.geth.miner.stop()

    def GetMoney(self, value):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        # Используйте функцию withdraw контракта для вывода средств
        withdrawal_transaction = self.sc.functions.withdraw(value).buildTransaction({
            'from': self.current_user,
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(self.current_user),
            'chainId': 69
        })
        # Подпись транзакции
        signed_transaction = self.w3.eth.account.signTransaction(withdrawal_transaction, self.password)
        # Отправка транзакции
        tx_hash = self.w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

        # Ожидание подтверждения транзакции (опционально)
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        self.w3.geth.miner.stop()

    def GetTableInfo(self, table_num):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        info = self.sc.functions.GetTableInfo(table_num).call({"from": self.current_user})
        self.w3.geth.miner.stop()
        return info

    def ShowCheck(self, table_num):
        self.w3.geth.personal.unlock_account(self.current_user, self.password, 0)
        self.w3.geth.miner.start()
        check = self.sc.functions.ShowCheck(table_num).call({"from": self.current_user})
        self.w3.geth.miner.stop()
        return check

    def retorders(self):
        return self.sc.functions.retorders().call()

    def earnings(self):
        self.sc.functions.ernings().call()


if __name__ == '__main__':
    api = API('0xCae62C21d7A26B3c7057714BEa4111f4376B1f99', '0')
    print(api.retorders())
    api.OrderIsReady()
    print(api.retorders())




