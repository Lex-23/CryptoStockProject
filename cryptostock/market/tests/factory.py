from factory.django import DjangoModelFactory
from market.models import Market

assets_list = [
    {"name": "BTC", "description": "Bitcoin", "price": "50996.99"},
    {"name": "ETH", "description": "Ethereum", "price": "4353.60"},
    {"name": "BNB", "description": "BinanceCoin", "price": "586.37"},
    {"name": "USDT", "description": "Tether", "price": "1.0012"},
    {"name": "SOL1", "description": "Solana", "price": "199.38"},
    {"name": "ADA", "description": "Cardano", "price": "1.4383"},
    {"name": "USDC", "description": "USDCoin", "price": "1.0001"},
    {"name": "XRP", "description": "XRP", "price": "0.832515"},
    {"name": "DOT1", "description": "Polkadot", "price": "28.54"},
    {"name": "LUNA1", "description": "Terra", "price": "69.42"},
    {"name": "HEX", "description": "HEX", "price": "0.136504"},
    {"name": "DOGE", "description": "Dogecoin", "price": "0.178727"},
    {"name": "AVAX", "description": "Avalanche", "price": "96.68"},
]


class MarketFactory(DjangoModelFactory):
    class Meta:
        model = Market
