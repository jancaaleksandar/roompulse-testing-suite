from datetime import datetime, timedelta
import secrets
from typing import Any
from ....types import UserInput

def get_hitlon_config(params : UserInput) -> dict[str, Any]:
    hotel_id = params["provider_id"]
    check_in_date = datetime.strptime(params["request_check_in_date"], "%Y-%m-%d")
    check_out_date = check_in_date + timedelta(days=params["request_nights"])
    cache_id_random_string_number = str(secrets.randbelow(9000000) + 1000000)
    currency = params.get("request_currency")
    if currency is None:
        raise ValueError("currency is none")
    # Build the full URL with parameters for room offers
    url = f"https://www.hilton.com/graphql/customer?appName=dx-res-ui&operationName=hotel_shopAvailOptions_shopPropAvail&originalOpName=getRoomRates&bl=en&ctyhocn={hotel_id}"

    payload: dict[str, Any] = {
        "query": "query hotel_shopAvailOptions_shopPropAvail($arrivalDate: String!, $ctyhocn: String!, $departureDate: String!, $language: String!, $guestLocationCountry: String, $numAdults: Int!, $numChildren: Int!, $numRooms: Int!, $displayCurrency: String, $guestId: BigInt, $specialRates: ShopSpecialRateInput, $rateCategoryTokens: [String], $selectedRoomRateCodes: [ShopRoomRateCodeInput!], $ratePlanCodes: [String], $pnd: String, $offerId: BigInt, $cacheId: String!, $knownGuest: Boolean, $selectedRoomTypeCode: String, $childAges: [Int], $adjoiningRoomStay: Boolean, $modifyingReservation: Boolean, $programAccountId: BigInt, $ratePlanDescEnhance: Boolean) {\n  hotel(ctyhocn: $ctyhocn, language: $language) {\n    ctyhocn\n    shopAvailOptions(input: {offerId: $offerId, pnd: $pnd}) {\n      maxNumChildren\n      altCorporateAccount {\n        corporateId\n        name\n      }\n      contentOffer {\n        name\n      }\n    }\n    shopAvail(\n      cacheId: $cacheId\n      input: {guestLocationCountry: $guestLocationCountry, arrivalDate: $arrivalDate, departureDate: $departureDate, displayCurrency: $displayCurrency, numAdults: $numAdults, numChildren: $numChildren, numRooms: $numRooms, guestId: $guestId, specialRates: $specialRates, rateCategoryTokens: $rateCategoryTokens, selectedRoomRateCodes: $selectedRoomRateCodes, ratePlanCodes: $ratePlanCodes, knownGuest: $knownGuest, childAges: $childAges, adjoiningRoomStay: $adjoiningRoomStay, modifyingReservation: $modifyingReservation, programAccountId: $programAccountId, ratePlanDescEnhance: $ratePlanDescEnhance}\n    ) {\n      statusCode\n      addOnsAvailable\n      summary {\n        specialRates {\n          specialRateType\n          roomCount\n        }\n        requestedRates {\n          ratePlanCode\n          ratePlanName\n          roomCount\n        }\n      }\n      notifications {\n        subText\n        subType\n        title\n        text\n      }\n      currencyCode\n      roomTypes(filter: {roomTypeCode: $selectedRoomTypeCode}) {\n        roomTypeCode\n        adaAccessibleRoom\n        adjoiningRoom\n        numBeds\n        roomTypeName\n        roomTypeDesc\n        roomOccupancy\n        executive\n        suite\n        code: roomTypeCode\n        name: roomTypeName\n        thumbnail: carousel(first: 1) {\n          _id\n          altText\n          variants {\n            size\n            url\n          }\n        }\n        quickBookRate {\n          ratePlan {\n            specialRateType\n            serviceChargesAndTaxesIncluded\n          }\n        }\n        roomOnlyRates {\n          roomTypeCode\n          ratePlanCode\n          rateAmount\n          rateAmountFmt(decimal: 0, strategy: ceiling)\n          rateAmountUSD: rateAmount(currencyCode: \"USD\")\n          amountAfterTaxFmt(decimal: 0, strategy: ceiling)\n          fullAmountAfterTax: amountAfterTaxFmt\n          rateChangeIndicator\n          feeTransparencyIndicator\n          cmaTotalPriceIndicator\n          guarantee {\n            guarPolicyCode\n            cxlPolicyCode\n          }\n          ratePlan {\n            attributes\n            commissionable\n            confidentialRates\n            ratePlanName\n            ratePlanDesc\n            ratePlanCode\n            hhonorsMembershipRequired\n            advancePurchase\n            serviceChargesAndTaxesIncluded\n          }\n          hhonorsDiscountRate {\n            rateChangeIndicator\n            ratePlanCode\n            roomTypeCode\n            rateAmount\n            rateAmountFmt(decimal: 0, strategy: ceiling)\n            rateAmountUSD: rateAmount(currencyCode: \"USD\")\n            amountAfterTaxFmt(decimal: 0, strategy: ceiling)\n            fullAmountAfterTax: amountAfterTaxFmt\n            guarantee {\n              guarPolicyCode\n              cxlPolicyCode\n            }\n            ratePlan {\n              attributes\n              commissionable\n              confidentialRates\n              ratePlanName\n              ratePlanDesc\n              ratePlanCode\n              advancePurchase\n              serviceChargesAndTaxesIncluded\n            }\n          }\n          serviceChargeDesc: serviceChargeDetails\n        }\n        requestedRoomRates {\n          ratePlanCode\n          rateAmount\n          rateAmountFmt(decimal: 0, strategy: ceiling)\n          rateAmountUSD: rateAmount(currencyCode: \"USD\")\n          amountAfterTaxFmt(decimal: 0, strategy: ceiling)\n          fullAmountAfterTax: amountAfterTaxFmt\n          rateChangeIndicator\n          feeTransparencyIndicator\n          cmaTotalPriceIndicator\n          ratePlan {\n            attributes\n            commissionable\n            confidentialRates\n            ratePlanName\n            ratePlanDesc\n            hhonorsMembershipRequired\n            serviceChargesAndTaxesIncluded\n          }\n          serviceChargeDesc: serviceChargeDetails\n        }\n        specialRoomRates {\n          ratePlanCode\n          rateAmount\n          rateAmountFmt(decimal: 0, strategy: ceiling)\n          rateAmountUSD: rateAmount(currencyCode: \"USD\")\n          amountAfterTaxFmt(decimal: 0, strategy: ceiling)\n          fullAmountAfterTax: amountAfterTaxFmt\n          rateChangeIndicator\n          feeTransparencyIndicator\n          cmaTotalPriceIndicator\n          ratePlan {\n            attributes\n            commissionable\n            confidentialRates\n            ratePlanName\n            ratePlanDesc\n            hhonorsMembershipRequired\n            serviceChargesAndTaxesIncluded\n          }\n          serviceChargeDesc: serviceChargeDetails\n        }\n        packageRates {\n          roomTypeCode\n          rateAmount\n          rateAmountFmt(decimal: 0, strategy: ceiling)\n          rateAmountUSD: rateAmount(currencyCode: \"USD\")\n          amountAfterTaxFmt(decimal: 0, strategy: ceiling)\n          fullAmountAfterTax: amountAfterTaxFmt\n          rateChangeIndicator\n          feeTransparencyIndicator\n          cmaTotalPriceIndicator\n          ratePlanCode\n          ratePlan {\n            attributes\n            commissionable\n            confidentialRates\n            ratePlanName\n            ratePlanDesc\n            ratePlanCode\n            hhonorsMembershipRequired\n            serviceChargesAndTaxesIncluded\n          }\n          guarantee {\n            guarPolicyCode\n            cxlPolicyCode\n          }\n          serviceChargeDesc: serviceChargeDetails\n        }\n        redemptionRoomRates(first: 1) {\n          cashRatePlan\n          rateChangeIndicator\n          pointDetails(perNight: true) {\n            effectiveDateFmt(format: \"medium\", language: $language)\n            effectiveDateFmtAda: effectiveDateFmt(format: \"long\", language: $language)\n            pointsRate\n            pointsRateFmt\n          }\n          sufficientPoints\n          pamEligibleRoomRate {\n            ratePlan {\n              ratePlanCode\n              rateCategoryToken\n            }\n            roomTypeCode\n          }\n          roomTypeCode\n          ratePlan {\n            ratePlanDesc\n            ratePlanName\n            redemptionType\n          }\n          ratePlanCode\n          totalCostPoints\n          totalCostPointsFmt\n        }\n      }\n      lowestPointsInc\n    }\n  }\n}",
        "operationName": "hotel_shopAvailOptions_shopPropAvail",
        "variables": {
            "guestLocationCountry": "RS",
            "arrivalDate": check_in_date.strftime("%Y-%m-%d"),
            "departureDate": check_out_date.strftime("%Y-%m-%d"),
            "numAdults": 2,
            "numChildren": 0,
            "numRooms": 1,
            "displayCurrency": currency,
            "ctyhocn": hotel_id,
            "language": "en",
            "guestId": None,
            "specialRates": {
                "aaa": False,
                "governmentMilitary": False,
                "hhonors": False,
                "pnd": "",
                "senior": False,
                "teamMember": False,
                "owner": False,
                "ownerHGV": False,
                "familyAndFriends": False,
                "travelAgent": False,
                "smb": False,
                "specialOffer": False,
                "specialOfferName": None
            },
            "pnd": None,
            "cacheId": cache_id_random_string_number,
            "offerId": None,
            "knownGuest": False,
            "modifyingReservation": False,
            "childAges": [],
            "adjoiningRoomStay": False,
            "selectedRoomTypeCode": None,
            "ratePlanDescEnhance": False
        }
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-GB,en;q=0.9',
        'content-type': 'application/json',
        'dx-platform': 'web',
        'origin': 'https://www.hilton.com',
        'priority': 'u=1, i',
        'referer': 'https://www.hilton.com/en/book/reservation/rooms/',
        'sec-ch-ua': '"Brave";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    cookies = {
        # "webGuestToken": "%7B%22accessToken%22%3A%22DX.eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJwaWQiOiJ3ZWIiLCJraWQiOiI4UVl1RTZfdHBValdjUmVnem1RZFlBaF9RYlk1ckVqUlpPTThwWmNKeU5BIn0.D-SsnwL_lIKhZ_PV_8p6VJCkMmylJs9yfGSwZweKGq25lyJFJgtTsnr_E_XUbpdWxIEtz2oU1hVTt1dyE-N6URTo9snxUa3igsLeBpkuASRd645YklglGjsGj5cT9nKX3rZCfTVNbRHqCKxKTzHJZKAtXLu7NzsNLA1osH-ro0q-m-DhyGNdL_JZl1x0IG--1XOM8zicfSW-Uto7HrE4U_fvYX0IGqjF-Y23KXl_iWl9dgAc5fQpjSlqand6yyCXkw5zYqXdFWbzk5Iwl2HU9HLM6CQk1negwhr9VHxd-BM_Zui53DarkYoxY2LmHPAYs5m056oe7QG9cwgp4yz5XQ.PUV8GaTApGptDmaz.cj-1HY_IXO0ECcb6vJmoloQEktoItrTCZkXRCxqDRRqtMGuY2rfKh5-jATS10F70C73VmCqeUhOQmcS7JY-WkSgF1Y2pbK3r2sokRI0GxeCmNmRvh2b42isy_4vCJ7CMlX6oyCleFua-_S54FxsXh2UFAAoB008XiqoZCJ304cwCCVZcknPXBnwngJx3cCNKLql1fOIU1U_YrWVF7gBeFO6YkWKtD3-Rt7UvnPl6-nOid5SoEMo-Emcg5jPWltBIIBwzsLsj-YQGUqXpl2iDD-YPGxlFcZXV4JsvDaZips2XTcfLmG0u72ICaxZh5vk9FU_QujLptCnU6kInROjh4fReTFXoHElhFYz6vRazcAaJb7umbaoOnK02TBdpxCm8Mw1MvhbVJsXYdjc2ekZbrNloFwZxQU1sFMVd_vMXEQ7PGXaRBDkbE0X403eulhBFStxz--ZQP2NTKnfF0uSrIaMK2HQqQFmTWIhIHuHpVT65fMCNFUF8BT2ZcltF1UAoRaoW2Y_0qAQKuUXEcznS8NF-0Zz5choqGbWiZYMidRk05LHMLsUeKhARxn2DpZC8wYfNMymorufurDRgMyKyHWHlPV-V0SkTCakkwajsON_DAY13uRpGByYoAADegkbI9dsdqIRFBc7LGTw7A2Mh7qNAvssds6TipNrNCFiDaKkRsEMJLzBBvxXfHyb6mF94mM_1JW1Xwu_Sd41lqjsnxbzUzFMbdBF57FUoQ0XJixkDI4N_9aZbYgMgoxkpSubDLuMlN66CjnjpPksnhJun0SFkRUmf9G2wOdT6MYmzEqzH0Sw9BA.dQAYsSy_DHHx4lOFdaAFYg%22%2C%22tokenType%22%3A%22Bearer%22%7D",
        "webGuestToken" : "%7B%22accessToken%22%3A%22DX.eyJhbGciOiJSU0EtT0FFUCIsImVuYyI6IkEyNTZHQ00iLCJwaWQiOiJ3ZWIiLCJraWQiOiI4UVl1RTZfdHBValdjUmVnem1RZFlBaF9RYlk1ckVqUlpPTThwWmNKeU5BIn0.ISdTGx9nNthbnBcLQo--usxSi9Clt87XZC6_40uWsuMB82u3uQ5mPABLUOOl_oHOebsZMBvEctUrwUxKXxRJlTt8kLmUInqpSk-1lYEAq-nRgMB7snCwr-H49sSRdTnDH8Za6bbRrdMN2AFXRCkWwkpXBuf39R1G_sA9c1AR5Ifhu0LZh05OMm9ivaO-ujqtChIML4i6sBp2rmG5ORgB1JQ8SVSqHUErY5rXdd-QOXm4sR9QhdFQS7Jy4YxiwkchARfVYwKbvA4xQOohSQ5qv4TqqntiFoQj_IupEoqKPfL-b8tVXJ_ZREy_-tzhXIlGX3pBKpfincAWPd7DQZf1AQ.-EWEVD6zIi_FlA09.K03oW-Te6ge6cwt8cy-zv-1MfWfCzj8PucbxvsLL2Li3glFOzoq1XwT01J7ZgJjp4iFfrvDPwH4J7QnWbFLxv1bQfApOLdI4pZhtoKMvftL43AYB2fZgbhfTQJEah8kHhaCNTaW7eA5hO1sPXrnQUWG0tQ2Pq8JJq4PBoSFEqYnKRb6oihuUz8A3o1qvqrBfI6okYbL36yzaNIbWQJNZGzHfaGkfz7gNmYtLj3H1XhyhtCGajhSfqtIwFj4FNNdZK5UmHWribs_srQStIHwT2IR8QfSrmLZ42L6BWSfSpcf7b8Ha7yEahWP5s8gsynTwPqcU2cEH7LrpcHISg7uMjXkdcaHIH9dhcrRtJMSHn1Xd25eNCHAJRZh2xrMjWEUIYZrhfDzpgDj6KV20fcClexCdiDzz-Oed6yh3xQRhqq3tKLMPd0Pqy52bl_gOQSGp78tlIlTK8f3vWFJrXei0Lw9v8c6RBc5owXGYGNotFfg9wCtAXmqwRlvxbytePMNl96Vm6Wu88pEMkWOQme0MOnRGJiVMI4W_F8VhlpCWHvN4tU7NIqBOghxYni9A_ymkted-xr_oylgD4uqX3nRD_WFRUIjLoCmloWBe44DSom8-pzpnsIyFsefv-h5Yi7tsx1IM8rD347FZUzEJf94HJou55XOReitaQkEqrKBxS7QQz3uUh248g_iwJZrolz5hw4L4Vt0aHJTlkyM0bEj_jFKOhrAdHH5Lyuj0P6Cg4uK9PN636jHeDtwJnVfIghU4xgfWjFw9c1CBEIE_cXJA8bI96IJRTZaaMKtJ2BiNwwd_RC2ZYQ.1PBIr-UVV_eWwlkEXGXlqw%22%2C%22tokenType%22%3A%22Bearer%22%7D; webGuestMetadata=%7B%22webGuestTokenType%22%3A%22app%22%7D"
    }

    
    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "payload": payload
    }
    
