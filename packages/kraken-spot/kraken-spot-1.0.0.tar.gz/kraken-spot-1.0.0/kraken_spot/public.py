from typing import Any, Dict, Optional

from .http import KrakenResponse, clean_params, http_get


class PublicEndpoints:
    """
    Call any of the public endpoints. These require no authentication.
    """

    def _public_query(
        self, url_path: str, params: Optional[Dict[str, Any]] = None
    ) -> KrakenResponse:
        request_url = f"{self._base_url()}/public/{url_path}"  # type: ignore
        if params:
            params = clean_params(params)
        resp = http_get(request_url, params)
        return KrakenResponse(resp.body.get("result", {}), resp.body.get("error", {}))

    def get_server_time(self) -> KrakenResponse:
        """
        Get's the server time.

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getServerTime
        """
        return self._public_query("Time")

    def get_system_status(self) -> KrakenResponse:
        """
        Get current system status

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getSystemStatus
        """
        return self._public_query("SystemStatus")

    def get_asset_info(
        self, asset: Optional[str] = None, a_class: Optional[str] = None
    ) -> KrakenResponse:
        """
        Get information about an asset

        https://docs.kraken.com/rest/#tag/Market-Data/operation/getAssetInfo
        """
        params = {"asset": asset, "aclass": a_class}
        return self._public_query("Assets", params)

    def get_tradable_asset_pairs(
        self, pair: str, info: Optional[str] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/Market-Data/operation/getTradableAssetPairs
        """
        params = {"pair": pair, "info": info}
        return self._public_query("AssetPairs", params)

    def get_ticker_information(self, pair: str) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/Market-Data/operation/getTickerInformation
        """
        return self._public_query("Ticker", {"pair": pair})

    def get_ohlc_data(
        self, pair: str, interval: Optional[int] = None, since: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/Market-Data/operation/getOHLCData
        """
        params = {"pair": pair, "interval": interval, "since": since}
        return self._public_query("OHLC", params)

    def get_order_book(self, pair: str, count: Optional[int] = None) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/Market-Data/operation/getOrderBook
        """
        params = {"pair": pair, "count": count}
        return self._public_query("Depth", params)

    def get_recent_trades(
        self, pair: str, since: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/Market-Data/operation/getRecentTrades
        """
        params = {"pair": pair, "since": since}
        return self._public_query("Trades", params)

    def get_recent_spreads(
        self, pair: str, since: Optional[int] = None
    ) -> KrakenResponse:
        """
        https://docs.kraken.com/rest/#tag/Market-Data/operation/getRecentSpreads
        """
        params = {"pair": pair, "since": since}
        return self._public_query("Spread", params)
