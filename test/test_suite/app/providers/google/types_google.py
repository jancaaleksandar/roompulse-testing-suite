from typing import TypedDict, NotRequired


class Provider(TypedDict):
    provider_offer_is_brand_offer: bool
    provider_offer_is_sold_out: bool
    provider_name: NotRequired[str]
    provider_offer_url: NotRequired[str]
    provider_offer_price_amount: NotRequired[float]
    provider_offer_price_currency: NotRequired[str]
    provider_icon_url: NotRequired[str]

        

    
