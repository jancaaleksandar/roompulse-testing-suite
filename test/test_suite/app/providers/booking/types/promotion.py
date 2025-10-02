from typing import TypedDict


class PromotionChoice(TypedDict):
    promotion_choice_cancellation_free: bool
    promotion_choice_cancellation_days: list[int]
    promotion_choice_pay_nothing: bool
    promotion_choice_pay_nothing_days: list[int]


class PromotionDeal(TypedDict):
    promotion_deal_preferred: bool
    promotion_deal_preferred_plus: bool
    promotion_deal_basic: bool
    promotion_deal_booking_pays: bool
    promotion_deal_new_property: bool
    promotion_deal_getaway: bool
    promotion_deal_early_booker: bool
    promotion_deal_last_minute: bool
    promotion_deal_limited_time: bool
    promotion_deal_partner_offer: bool
    promotion_deal_genius: bool
    promotion_deal_promotion_id : str | None
    promotion_deal_offer_airport_shuttle: bool
    
class PromotionDealWithChoice(PromotionDeal, PromotionChoice):
    pass