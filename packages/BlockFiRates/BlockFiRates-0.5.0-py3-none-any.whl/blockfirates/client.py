import cloudscraper
from functools import lru_cache
import itertools
import json


class BlockFiRates:
    def __init__(self) -> None:
        pass

    __RATES_URL = "https://blockfi.com/page-data/rates/page-data.json"

    @lru_cache(None)
    def get_all_rates(self) -> list:
        scraper = cloudscraper.create_scraper()
        html = scraper.get(self.__RATES_URL).content
        rate_data = []
        for i in range(0, 10):
            try:
                rate_data.append(
                    json.loads(html)["result"]["data"]["allContentfulComposePage"][
                        "nodes"
                    ][i]["content"]["assetList"]
                )
            except:
                pass

        # Combine and deduplicate
        all_rates = list(itertools.chain.from_iterable(rate_data))
        deduped_rates = [dict(t) for t in {tuple(d.items()) for d in all_rates}]

        return [
            {
                "asset_name": x["assetName"],
                "enabled": x["rowEnableCoinInList"],
                "row_data": {
                    "no_tier_limit": x["rowNoTierLimit"],
                    "tier_1": {
                        "apy": x["rowTier1APY"],
                        "amount_min": x.get("rowTier1AmountMinimum"),
                        "amount_max": x.get("rowTier1AmountMaximum"),
                    },
                    "tier_2": {
                        "apy": x["rowTier2APY"],
                        "amount_min": x.get("rowTier2AmountMinimum"),
                        "amount_max": x.get("rowTier2AmountMaximum"),
                    },
                    "tier_3": {
                        "apy": x["rowTier3APY"],
                        "amount_min": x.get("rowTier3AmountMinimum"),
                        "amount_max": x.get("rowTier3AmountMaximum"),
                    },
                },
                "symbol": x["ticker"].upper(),
                "us_data": {
                    "no_tier_limit": x["usNoTierLimit"],
                    "tier_1": {
                        "apy": x["usTier1APY"],
                        "amount_min": x.get("usTier1AmountMinimum"),
                        "amount_max": x.get("usTier1AmountMaximum"),
                    },
                    "tier_2": {
                        "apy": x["usTier2APY"],
                        "amount_min": x.get("usTier2AmountMinimum"),
                        "amount_max": x.get("usTier2AmountMaximum"),
                    },
                    "tier_3": {
                        "apy": x["usTier3APY"],
                        "amount_min": x.get("usTier3AmountMinimum"),
                        "amount_max": x.get("usTier3AmountMaximum"),
                    },
                },
            }
            for x in deduped_rates
        ]

    def get_info(self, symbol: str, category: str = "us", tier: int = 1) -> dict:
        assert category in {"row", "us"}, "Category must be 'row' or 'us'"

        assert tier in {1, 2, 3}, "TIER must be 1, 2 or 3"

        rates = self.get_all_rates()

        raw_info = [i for i in rates if i["symbol"] == symbol][0]

        return {
            "asset_name": raw_info["asset_name"],
            "enabled": raw_info["enabled"],
            "info": raw_info[f"{category}_data"][f"tier_{tier}"],
            "no_tier_limit": raw_info[f"{category}_data"]["no_tier_limit"],
            "symbol": raw_info["symbol"],
        }
