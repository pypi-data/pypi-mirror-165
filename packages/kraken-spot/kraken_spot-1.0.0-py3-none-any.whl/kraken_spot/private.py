from typing import Dict, Optional

from .auth import generate_nonce, get_kraken_signature
from .errors import AuthError
from .http import KrakenResponse, clean_params, http_post


class PrivateEndpoints:
    """
    PrivateEndpoints is a mixin to be used on the Client class
    """

    _otp: Optional[int]

    def _authorised_query(
        self, url_path: str, body: Optional[Dict] = None
    ) -> KrakenResponse:
        """
        Makes a request to an endpoint that requires API Key authorisation
        """
        api_key = self.api_key  # type: ignore
        private_key = self.private_key  # type: ignore
        api_version = self.api_version  # type: ignore
        endpoint = self.endpoint  # type: ignore

        if not api_key or not private_key:
            raise AuthError(
                (
                    "you must configure the client with an api key and private key "
                    "to access private endpoints"
                )
            )

        full_url_path = f"/{api_version}/private/{url_path}"
        default_data = {"nonce": generate_nonce()}

        # set one time password for this request
        if hasattr(self, "_otp") and self._otp:
            default_data["otp"] = self._otp

        body = body or {}
        body = clean_params({**body, **default_data})
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "API-Key": api_key,
            "API-Sign": get_kraken_signature(full_url_path, body, private_key),
        }
        url = f"{endpoint}{full_url_path}"
        resp = http_post(url, body, headers)

        # reset otp
        if hasattr(self, "_otp"):
            self._otp = None

        return KrakenResponse(resp.body.get("result", {}), resp.body.get("error", {}))

    def set_otp(self, otp: int):
        self._otp = otp

    def get_account_balance(self) -> KrakenResponse:
        """
        Get all cash balances
        """
        return self._authorised_query("Balance")

    def get_trade_balance(self, asset: str) -> KrakenResponse:
        """
        Retrieve a summary of collateral balances, margin position valuations, equity and
        margin level.
        """
        return self._authorised_query("TradeBalance", {"asset": asset})

    def get_open_orders(
        self, trades: Optional[bool] = None, user_ref: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getOpenOrders
        """
        return self._authorised_query(
            "OpenOrders", {"trades": trades, "userref": user_ref}
        )

    def get_closed_orders(
        self,
        trades: Optional[bool] = None,
        user_ref: Optional[int] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        ofs: Optional[int] = None,
        close_time: Optional[str] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getClosedOrders
        """
        return self._authorised_query(
            "ClosedOrders",
            {
                "trades": trades,
                "userref": user_ref,
                "start": start,
                "end": end,
                "ofs": ofs,
                "closetime": close_time,
            },
        )

    def query_orders_info(
        self, tx_id: str, trades: Optional[bool] = None, user_ref: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getOrdersInfo
        """
        return self._authorised_query(
            "QueryOrders",
            {
                "trades": trades,
                "userref": user_ref,
                "txid": tx_id,
            },
        )

    def get_trades_history(
        self,
        trade_type: Optional[str] = None,
        trades: Optional[bool] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        ofs: Optional[int] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getTradeHistory
        """
        return self._authorised_query(
            "TradeHistory",
            {
                "type": trade_type,
                "trades": trades,
                "start": start,
                "end": end,
                "ofs": ofs,
            },
        )

    def get_trades_info(
        self, tx_id: Optional[str] = None, trades: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getTradesInfo
        """
        return self._authorised_query("QueryTrades", {"txid": tx_id, "trades": trades})

    def get_open_trades(
        self,
        tx_id: Optional[str] = None,
        do_calc: Optional[bool] = None,
        consolidation: Optional[str] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getOpenPositions
        """
        return self._authorised_query(
            "OpenPositions",
            {
                "txid": tx_id,
                "docalcs": do_calc,
                "consolidation": consolidation,
            },
        )

    def get_ledgers(
        self,
        asset: Optional[str] = None,
        a_class: Optional[str] = None,
        type: Optional[str] = None,
        start: Optional[int] = None,
        end: Optional[int] = None,
        ofs: Optional[int] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getLedgers
        """
        return self._authorised_query(
            "Ledgers",
            {
                "asset": asset,
                "aclass": a_class,
                "type": type,
                "start": start,
                "end": end,
                "ofs": ofs,
            },
        )

    def query_ledgers(
        self, ledger_id: Optional[str] = None, trades: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getLedgersInfo
        """
        return self._authorised_query(
            "QueryLedgers",
            {
                "id": ledger_id,
                "trades": trades,
            },
        )

    def get_trade_volume(
        self, pair: Optional[str] = None, fee_info: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/getTradeVolume
        @todo check 'pair' query parameter - seems to shadow body parameter
        """
        return self._authorised_query(
            "TradeVolume",
            {
                "pair": pair,
                "fee-info": fee_info,
            },
        )

    def request_export_report(
        self,
        report: str,
        description: str,
        format: Optional[str] = None,
        fields: Optional[str] = None,
        start_tm: Optional[int] = None,
        end_tm: Optional[int] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/addExport
        """
        return self._authorised_query(
            "AddExport",
            {
                "report": report,
                "description": description,
                "format": format,
                "fields": fields,
                "starttm": start_tm,
                "endtm": end_tm,
            },
        )

    def get_export_status(self, report: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/exportStatus
        """
        return self._authorised_query("ExportStatus", {"report": report})

    def retrieve_data_export(self, report_id: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/retrieveExport
        """
        return self._authorised_query("RetrieveExport", {"id": report_id})

    def delete_export_report(self, report_id: str, report_type: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Data/operation/removeExport
        """
        return self._authorised_query(
            "RemoveExport", {"id": report_id, "type": report_type}
        )

    # - User Trading

    def add_order(
        self,
        order_type: str,
        direction: str,
        volume: str,
        pair: str,
        price_1: Optional[str] = None,
        price_2: Optional[str] = None,
        trigger: Optional[str] = None,
        leverage: Optional[str] = None,
        stp_type: Optional[str] = None,
        o_flags: Optional[str] = None,
        time_in_force: Optional[str] = None,
        start_time: Optional[str] = None,
        expire_time: Optional[str] = None,
        close_order_type: Optional[str] = None,
        close_price: Optional[str] = None,
        close_price_2: Optional[str] = None,
        deadline: Optional[str] = None,
        validate: Optional[bool] = None,
        user_ref: Optional[str] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Trading/operation/addOrder
        """
        return self._authorised_query(
            "AddOrder",
            {
                "userref": user_ref,
                "ordertype": order_type,
                "type": direction,
                "volume": volume,
                "pair": pair,
                "price": price_1,
                "price2": price_2,
                "trigger": trigger,
                "leverage": leverage,
                "stp_type": stp_type,
                "oflags": o_flags,
                "timeinforce": time_in_force,
                "starttm": start_time,
                "expiretm": expire_time,
                "close[ordertype]": close_order_type,
                "close[price]": close_price,
                "close[price2]": close_price_2,
                "deadline": deadline,
                "validate": validate,
            },
        )

    def edit_order(
        self,
        tx_id: str,
        pair: str,
        user_ref: Optional[int] = None,
        volume: Optional[str] = None,
        price: Optional[str] = None,
        price_2: Optional[str] = None,
        o_flags: Optional[str] = None,
        deadline: Optional[str] = None,
        cancel_response: Optional[bool] = None,
        validate: Optional[bool] = None,
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Trading/operation/editOrder
        """
        return self._authorised_query(
            "EditOrder",
            {
                "userref": user_ref,
                "txid": tx_id,
                "volume": volume,
                "pair": pair,
                "price": price,
                "price2": price_2,
                "oflags": o_flags,
                "deadline": deadline,
                "cancel_response": cancel_response,
                "validate": validate,
            },
        )

    def cancel_order(self, tx_id: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Trading/operation/cancelOrder
        """
        return self._authorised_query("CancelOrder", {"txid": tx_id})

    def cancel_all_orders(self) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Trading/operation/cancelAllOrders
        """
        return self._authorised_query("CancelAll")

    def cancel_all_orders_after_timeout(self, timeout: int) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Trading/operation/cancelAllOrdersAfter
        """
        return self._authorised_query("CancelAllOrdersAfter", {"timeout": timeout})

    # - User funding

    def get_deposit_methods(self, asset: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/getDepositMethods
        """
        return self._authorised_query("DepositMethods", {"asset": asset})

    def get_deposit_addresses(
        self, asset: str, method: str, new: Optional[bool] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/getDepositAddresses
        """
        return self._authorised_query(
            "DepositAddresses",
            {
                "asset": asset,
                "method": method,
                "new": new,
            },
        )

    def get_status_of_recent_deposits(
        self, asset: str, method: Optional[str] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/getStatusRecentDeposits
        """
        return self._authorised_query(
            "DepositStatus", {"asset": asset, "method": method}
        )

    def get_withdrawal_information(
        self, asset: str, key: str, amount: str
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/getWithdrawalInformation
        """
        return self._authorised_query(
            "WithdrawInfo",
            {
                "asset": asset,
                "key": key,
                "amount": amount,
            },
        )

    def withdrawal_funds(self, asset: str, key: str, amount: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/withdrawFunds
        """
        return self._authorised_query(
            "Withdraw",
            {
                "asset": asset,
                "key": key,
                "amount": amount,
            },
        )

    def get_status_of_recent_withdrawal(
        self, asset: str, method: Optional[str] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/getStatusRecentWithdrawals
        """
        return self._authorised_query(
            "WithdrawStatus", {"asset": asset, "method": method}
        )

    def request_withdrawal_cancellation(
        self, asset: str, ref_id: str
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/cancelWithdrawal
        """
        return self._authorised_query(
            "WithdrawCancel", {"asset": asset, "refid": ref_id}
        )

    def request_wallet_transfer(
        self, asset: str, address_from: str, address_to: str, amount: str
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Funding/operation/walletTransfer
        """
        return self._authorised_query(
            "WalletTransfer",
            {
                "asset": asset,
                "from": address_from,
                "to": address_to,
                "amount": amount,
            },
        )

    def stake_asset(self, asset: str, amount: str, method: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Staking/operation/stake
        """
        return self._authorised_query(
            "Stake", {"asset": asset, "amount": amount, "method": method}
        )

    def unstake_asset(self, asset: str, amount: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Staking/operation/unstake
        """
        return self._authorised_query("Unstake", {"asset": asset, "amount": amount})

    def list_stakeable_assets(self) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Staking/operation/getStakingAssetInfo
        """
        return self._authorised_query("Staking/Assets")

    def get_pending_staking_transactions(self) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Staking/operation/getStakingAssetInfo
        """
        return self._authorised_query("Staking/Pending")

    def list_of_staking_transactions(self) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/User-Staking/operation/getStakingAssetInfo
        """
        return self._authorised_query("Staking/Transactions")

    def get_websockets_token(self):
        """
        https://docs.kraken.com/rest/#tag/Websockets-Authentication/operation/getWebsocketsToken
        """
        return self._authorised_query("GetWebSocketsToken")
