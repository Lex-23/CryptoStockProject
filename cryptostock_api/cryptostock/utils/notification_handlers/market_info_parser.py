from market.models import Market


class MarketInfoParser:
    """Class for parsing 'last_update_info' from Market"""

    def __init__(self):
        self.info = {}

    @property
    def get_info_not_null(self):
        return dict((key, value) for key, value in self.info.items() if value)

    def get_assets_by_list(self, asset_list: list):
        for market in Market.objects.all():
            self.info[market.name] = {
                asset["name"]: asset["price"]
                for asset in market.kwargs["last_update_info"]
                if asset["name"] in asset_list
            }
        return self.info

    def get_assets_by_dict(self, asset_dict: dict, key: str):
        self.info = self.get_assets_by_list(list(asset_dict.keys()))
        if self.get_info_not_null:
            if key == "max_asset_price":
                for key, values in self.info.items():
                    self.info[key] = {
                        asset_key: values[asset_key]
                        for asset_key in asset_dict.keys()
                        if values[asset_key] > asset_dict[asset_key]
                    }
            elif key == "min_asset_price":
                for key, values in self.info.items():
                    self.info[key] = {
                        asset_key: values[asset_key]
                        for asset_key in asset_dict.keys()
                        if values[asset_key] < asset_dict[asset_key]
                    }
        else:
            self.info = {}
        return self.info
