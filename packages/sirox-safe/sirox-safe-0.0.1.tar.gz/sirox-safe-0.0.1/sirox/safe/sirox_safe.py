from gnosis.safe import Safe, SafeOperation
from typing import List, Tuple, Union, Optional
from requests import Response
from requests import post
from urllib.parse import urljoin
from gnosis.safe.safe_tx import SafeTx
from gnosis.eth import EthereumClient
from dataclasses import dataclass
from gnosis.safe.multi_send import MultiSend, MultiSendOperation, MultiSendTx
from eth_utils import to_checksum_address
from web3.main import Web3
from web3.types import ChecksumAddress


@dataclass
class Tx:
    to: str
    tx_input: bytes


# Tested successfully on Ethereum Mainnet and Polygon Mainnet
# TODO: understand diference between MULTISEND and MULTISEND_CALL_ONLY
# MULTISEND_CALL_ONLY = to_checksum_address('0x40A2aCCbd92BCA938b02010E17A5b8929b49130D')  # from ape_safe
MULTISEND_CALL_ONLY = to_checksum_address("0xA238CBeb142c10Ef7Ad8442C6D1f9E89e07e7761")

transaction_service = {
    1: "https://safe-transaction.mainnet.gnosis.io",
    137: "https://safe-transaction.polygon.gnosis.io",
}


class SiroxMultiSend(MultiSend):
    def __init__(
        self,
        ethereum_client: Optional[EthereumClient] = None,
        address: Optional[ChecksumAddress] = None,
    ):
        super().__init__(ethereum_client, address)

    # Overriding method as using wrong method 'build_transaction'
    def build_tx_data(self, multi_send_txs: List[MultiSendTx]) -> bytes:
        """
        Txs don't need to be valid to get through

        :param multi_send_txs:
        :return:
        """
        multisend_contract = self.get_contract()
        encoded_multisend_data = b"".join([x.encoded_data for x in multi_send_txs])
        return multisend_contract.functions.multiSend(
            encoded_multisend_data
        ).buildTransaction({"gas": 1, "gasPrice": 1})["data"]


class SiroxSafe(Safe):
    def __init__(
        self,
        address: Union[str, ChecksumAddress],
        w3: Web3,
        signer_pk: str,
        chain: int = 1,
    ):
        ethereum_client = EthereumClient(w3.provider.endpoint_uri)
        super().__init__(to_checksum_address(address), ethereum_client)
        self.chain = chain
        self.gnosis_safe_base_url = transaction_service[self.chain]
        self.multisend = MULTISEND_CALL_ONLY

        self.safe = Safe(
            address=self.address,
            ethereum_client=self.ethereum_client,
        )
        self.signer_account = self.w3.eth.account.from_key(signer_pk)

    def post_tx_to_gnosis(self, safe_tx: SafeTx):
        data = {
            "to": safe_tx.to,
            "value": safe_tx.value,
            "data": safe_tx.data.hex() if safe_tx.data else None,
            "operation": safe_tx.operation,
            "gasToken": safe_tx.gas_token,
            "safeTxGas": safe_tx.safe_tx_gas,
            "baseGas": safe_tx.base_gas,
            "gasPrice": safe_tx.gas_price,
            "refundReceiver": safe_tx.refund_receiver,
            "nonce": safe_tx.safe_nonce,
            "contractTransactionHash": safe_tx.safe_tx_hash.hex(),
            "sender": self.signer_account.address,
            "signature": safe_tx.signatures.hex() if safe_tx.signatures else None,
            "origin": "sir0x_bot",
        }
        # TODO: change to log
        print(f"Posting tx to Gnosis Safe: {self.safe.address} with data: {data}")

        url = urljoin(
            self.gnosis_safe_base_url,
            f"/api/v1/safes/{self.safe.address}/multisig-transactions/",
        )
        return post(url, json=data)

    def safe_nonce(self, nonce_offset: int = None):
        # gets actual nonce without taking into account queue. Use nonce_offset to avoid overwriting
        safe_nonce = self.safe.retrieve_nonce()
        if nonce_offset:
            safe_nonce += 1
        return safe_nonce

    def build_and_post_multi_tx_to_gnosis(
        self, txs: List[Tx], nonce_offset: int = None
    ) -> Tuple[SafeTx, Response]:
        safe_nonce = self.safe_nonce(nonce_offset)
        txs = [
            MultiSendTx(MultiSendOperation.CALL, tx.to, 0, tx.tx_input) for tx in txs
        ]
        data = SiroxMultiSend(
            address=self.multisend, ethereum_client=self.ethereum_client
        ).build_tx_data(txs)

        safe_tx = self.safe.build_multisig_tx(
            self.multisend,
            0,
            data,
            SafeOperation.DELEGATE_CALL.value,
            safe_nonce=safe_nonce,
        )

        safe_tx.sign(self.signer_account.key)

        res = self.post_tx_to_gnosis(safe_tx)

        return safe_tx, res

    def build_and_post_tx_to_gnosis(
        self, tx: Tx, nonce_offset: int = None
    ) -> Tuple[SafeTx, Response]:
        safe_nonce = self.safe_nonce(nonce_offset)
        safe_tx = self.safe.build_multisig_tx(
            tx.to,
            0,
            tx.tx_input,
            operation=0,
            safe_nonce=safe_nonce,
        )
        safe_tx.sign(self.signer_account.key)
        res = self.post_tx_to_gnosis(safe_tx)

        return safe_tx, res
