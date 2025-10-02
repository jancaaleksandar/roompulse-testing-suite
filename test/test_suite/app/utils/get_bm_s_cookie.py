# import random
# import requests
# import time
# import json

# def get_bm_s_cookie() -> str:


#     proxies = {"https": "http://spyrtor1t6:bf_FeyvG6vrY9A17ae@isp.decodo.com:10000", "http": "hhttp://spyrtor1t6:bf_FeyvG6vrY9A17ae@isp.decodo.com:10000"}

#     url = "https://www.expedia.com/graphql"
    
#     payload = json.dumps([
#     {
#         "operationName": "AncillaryPropertyOffersQuery",
#         "variables": {
#         "propertyId": "922557",
#         "searchCriteria": {
#             "primary": {
#             "dateRange": {
#                 "checkInDate": {
#                 "day": 8,
#                 "month": 8,
#                 "year": 2025
#                 },
#                 "checkOutDate": {
#                 "day": 10,
#                 "month": 8,
#                 "year": 2025
#                 }
#             },
#             "destination": {
#                 "regionName": "Kassandra, Central Macedonia, Greece",
#                 "regionId": "180586",
#                 "coordinates": {
#                 "latitude": 40.047371,
#                 "longitude": 23.41223
#                 },
#                 "pinnedPropertyId": None,
#                 "propertyIds": None,
#                 "mapBounds": None
#             },
#             "rooms": [
#                 {
#                 "adults": 2,
#                 "children": []
#                 }
#             ]
#             },
#             "secondary": {
#             "counts": [],
#             "booleans": [],
#             "selections": [
#                 {
#                 "id": "privacyTrackingState",
#                 "value": "CAN_TRACK"
#                 },
#                 {
#                 "id": "productOffersId",
#                 "value": "2de8be89-2c44-493e-a450-caf7193d4518"
#                 },
#                 {
#                 "id": "searchId",
#                 "value": "e06764bd-bbe5-4223-b5e0-5f1cb303e70f"
#                 },
#                 {
#                 "id": "sort",
#                 "value": "RECOMMENDED"
#                 },
#                 {
#                 "id": "useRewards",
#                 "value": "SHOP_WITHOUT_POINTS"
#                 }
#             ],
#             "ranges": []
#             }
#         },
#         "shoppingContext": {
#             "multiItem": None,
#             "queryTriggeredBy": "OTHER"
#         },
#         "travelAdTrackingInfo": None,
#         "searchOffer": {
#             "offerPrice": {
#             "offerTimestamp": "1754036315418",
#             "price": {
#                 "amount": 855,
#                 "currency": "USD"
#             },
#             "pointsApplied": False
#             },
#             "roomTypeId": "200202046",
#             "ratePlanId": "208181505",
#             "offerDetails": []
#         },
#         "referrer": "HSR",
#         "selectedSavedQuoteInput": None,
#         "context": {
#             "siteId": 1,
#             "locale": "en_US",
#             "eapid": 0,
#             "tpid": 1,
#             "currency": "USD",
#             "device": {
#             "type": "DESKTOP"
#             },
#             "identity": {
#             "duaid": "c0374c4d-1a9e-4a88-92f0-a68853b01cff",
#             "authState": "ANONYMOUS"
#             },
#             "privacyTrackingState": "CAN_TRACK"
#         }
#         },
#         "extensions": {
#         "persistedQuery": {
#             "version": 1,
#             "sha256Hash": "8c81129f7aca9a3985b660339c9102755801a802fe275fe45af315719933f723"
#         }
#         }
#     },
#     {
#         "operationName": "RoomsAndRatesPropertyOffersQuery",
#         "variables": {
#         "propertyId": "922557",
#         "searchCriteria": {
#             "primary": {
#             "dateRange": {
#                 "checkInDate": {
#                 "day": 8,
#                 "month": 8,
#                 "year": 2025
#                 },
#                 "checkOutDate": {
#                 "day": 10,
#                 "month": 8,
#                 "year": 2025
#                 }
#             },
#             "destination": {
#                 "regionName": "Kassandra, Central Macedonia, Greece",
#                 "regionId": "180586",
#                 "coordinates": {
#                 "latitude": 40.047371,
#                 "longitude": 23.41223
#                 },
#                 "pinnedPropertyId": None,
#                 "propertyIds": None,
#                 "mapBounds": None
#             },
#             "rooms": [
#                 {
#                 "adults": 2,
#                 "children": []
#                 }
#             ]
#             },
#             "secondary": {
#             "counts": [],
#             "booleans": [],
#             "selections": [
#                 {
#                 "id": "privacyTrackingState",
#                 "value": "CAN_TRACK"
#                 },
#                 {
#                 "id": "productOffersId",
#                 "value": "2de8be89-2c44-493e-a450-caf7193d4518"
#                 },
#                 {
#                 "id": "searchId",
#                 "value": "e06764bd-bbe5-4223-b5e0-5f1cb303e70f"
#                 },
#                 {
#                 "id": "sort",
#                 "value": "RECOMMENDED"
#                 },
#                 {
#                 "id": "useRewards",
#                 "value": "SHOP_WITHOUT_POINTS"
#                 }
#             ],
#             "ranges": []
#             }
#         },
#         "shoppingContext": {
#             "multiItem": None,
#             "queryTriggeredBy": "OTHER"
#         },
#         "travelAdTrackingInfo": None,
#         "searchOffer": {
#             "offerPrice": {
#             "offerTimestamp": "1754036315418",
#             "price": {
#                 "amount": 855,
#                 "currency": "USD"
#             },
#             "pointsApplied": False
#             },
#             "roomTypeId": "200202046",
#             "ratePlanId": "208181505",
#             "offerDetails": []
#         },
#         "referrer": "HSR",
#         "selectedSavedQuoteInput": None,
#         "context": {
#             "siteId": 1,
#             "locale": "en_US",
#             "eapid": 0,
#             "tpid": 1,
#             "currency": "USD",
#             "device": {
#             "type": "DESKTOP"
#             },
#             "identity": {
#             "duaid": "c0374c4d-1a9e-4a88-92f0-a68853b01cff",
#             "authState": "ANONYMOUS"
#             },
#             "privacyTrackingState": "CAN_TRACK"
#         }
#         },
#         "extensions": {
#         "persistedQuery": {
#             "version": 1,
#             "sha256Hash": "a919befd692721e63c7bfb4097ae9f8fe4c11cfa51c133571efc2cc51e14d053"
#         }
#         }
#     }
#     ])
#     headers = {
#     'accept': '*/*',
#     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
#     'client-info': 'shopping-pwa,0039e5b59fb5953b880520e2e56f997224cacb67,us-east-1',
#     'content-type': 'application/json',
#     'ctx-view-id': '2852c48a-cd6d-4e8c-b525-2379eebab6bc',
#     'origin': 'https://www.expedia.com',
#     'priority': 'u=1, i',
#     'referer': 'https://www.expedia.com/Kassandra-Hotels-Aegean-Melathron-Thalasso-Spa-Hotel.h922557.Hotel-Information?chkin=2025-08-08&chkout=2025-08-10&x_pwa=1&rfrr=HSR&pwa_ts=1754036315418&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jb20vSG90ZWwtU2VhcmNo&useRewards=false&rm1=a2&regionId=180586&destination=Kassandra%2C+Central+Macedonia%2C+Greece&destType=MARKET&latLong=40.047371%2C23.41223&sort=RECOMMENDED&top_dp=855&top_cur=USD&userIntent=&selectedRoomType=200202046&selectedRatePlan=208181505&searchId=e06764bd-bbe5-4223-b5e0-5f1cb303e70f',
#     'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"macOS"',
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'traceparent': '00-0000000000000000675814a2442fbb66-0b28a6c0e3840b73-00',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
#     'x-datadog-origin': 'rum',
#     'x-datadog-parent-id': '804075880866646899',
#     'x-datadog-sampling-priority': '0',
#     'x-datadog-trace-id': '7446724671018351462',
#     'x-hcom-origin-id': 'page.Hotels.Infosite.Information,H,30',
#     'x-page-id': 'page.Hotels.Infosite.Information,H,30',
#     'x-parent-brand-id': 'expedia',
#     'x-product-line': 'lodging',
#     'x-shopping-product-line': 'lodging',
#     # 'Cookie': 'feeInclusivePricingSheetLastShown=1754036530051; tpid=v.1,1; iEAPID=0; currency=USD; CRQS=t|1`s|1`l|en_US`c|USD; CRQSS=e|0; linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; EG_SESSIONTOKEN=ClAKJgokYmYzMzEwZGUtMzgyNi00Mzc0LTk3ZDMtZTk2NWQzNjEwNDQ2EiYKJDk3YmNkNWExLTJiODItNDZjNS1hOGM5LWY4NTZiYjY5NjRhZQ.VqoakaB_bHhUpUae.9Vt2-c_40VhLC8Ucl1CiDmRhIm171zzCeGUSMZlS9tKwFQ6cHyGvcX_aC4iocALG25HGmmx7z5RjyXhGvNSi1cdHyL0hqPTZFkh5HmFM2Z3M-ewyIClWxsOkUY-s4Zz6cW1FL13GOLHtk7RlkO3R9N-6IRaN694cl42U0DXGOrtjPj3hwwUvqmn3FOzPhjGjzpS1A7JSrIT7P9Movs7O5l19j49RCe-MDXO9_EwwlE4.HBn_k2i5AwvG1XoAqNvEAg; cesc=%7B%22lpe%22%3A%5B%2244c73f42-4f45-40ac-9c1d-ce3b2cdf39e7%22%2C1754036535240%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1754036535240%5D%2C%22lmc%22%3A%5B%22DIRECT.WEB%22%2C1754036535240%5D%2C%22hitNumber%22%3A%5B%2235%22%2C1754036535239%5D%2C%22amc%22%3A%5B%22DIRECT.WEB%22%2C1754036535240%5D%2C%22visitNumber%22%3A%5B%225%22%2C1754033342872%5D%2C%22ape%22%3A%5B%22d7d18ced-bb56-4d83-95ed-7152beb677d2%22%2C1754036535240%5D%2C%22cidVisit%22%3A%5B%22Brand.DTI%22%2C1754036535240%5D%2C%22entryPage%22%3A%5B%22Homepage%22%2C1754036535239%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1754033342872%5D%7D; HMS=5b939516-d090-3d65-9b72-d3088f3eec2b; MC1=GUID=545938f49cfb4539971890d0026d1ea4; DUAID=545938f4-9cfb-4539-9718-90d0026d1ea4; bm_ss=ab8e18ef4e; bm_mi=C22C036A96DADE33754745826188B69F~YAAQ88gwF0PP5EeYAQAAy3+5ZBx9buARZYHTJKbvXwiUFw2zwJyzv6gcMGHMVDqSJLnD4vX87ZMgJChIRv2qmWAZOAb2c29GptwS49mi6XZz2CP3gCJWiESN762THQQOXxn6wjDgdtL9UViDUe+Tro2kosCqg/6VJ3gZvlFlNIuaVn73D6BWWpqQRFabstaYzFw/ICPZLxxH8IdBCuArM5mosIm2gqHnua6Saxs7WOAAJPHkVvYm//BiHDqIJGBYs+JDCuRJV6K+CJic1Wj/pNFv9dCcE14wfN1MeHx8ShBXlPd99kt2aTpU45umcPnJndL2s8k4/jbaoHVONhl/AiOoMnXQ2514HCkhHJuKLXCSCxBBpqlEAhtaR9FR2vXZAzpYA+4dRlpu1ZV4nlo9SNz+YGCGNrVUm3LVTlo=~1; bm_s=YAAQ88gwF0TP5EeYAQAAy3+5ZANViW0CpVlp7DL/3W2SNqbISujdJ2yiwhfcW+oYBPPT8rmCMDC+/0vlE5CcWoKUSTnjq9jU+yQmyPaNt0Vq3OvDwfh2N0fz5b/BzZuKSMZ51GpTIAsy/HWvinmMCn7k477wpmrehk9wvOjiTzE2cH1sC0KJFuoqdopN4D1eaEi/4xuZ24rjtLI8TuyT+mE8S4N0bBq9eN9S5vFM0iJSZfz1VjtX9OzGBnNKHo5i166JHqTlbfAMtsUdhLRt2ooin/PPzEYeztohCZxfLCUXfnSxo3b5muBmJSMesMzKiOtsj775jmtA6+GdVJALrJxytP/W698xkTBizw6MfT2zV7MCu7nl+2bQhw90GxX6FLo3liBMBvRTIypPOHiukmRW74KTs8gRUhyYtPvgbce/KBeocr0QWsHyqRKHsZu4t5OE9oygHl8Llur4RK7JNFIDnqw0nJjbyRYmrVV7k3CXzwM5oZy01/QtxjtaDaYQb3+ynEVxO43pFQtviIP81VYWSorP7Fcm0OaNyoOBtkUF0iXOnC1ga2q+UKU50AzGJUrgyxRPCA==; bm_so=D99F529D6C1B42F329361A111AC2C199B436ED623EB07F365ECAFA8A9923E810~YAAQ88gwF0XP5EeYAQAAy3+5ZASdHXtaVJIACqbseI7OcRFrZEB8lIne2M+FJlofjeaqE/QMPawnDDnqA9cniBg8/y7Qx5P/7ZwvX4PHPMCDGrneEKqETi5dtKMGsLddlkSLnO4RUpP/iI2ia+Sjj/0qEsLueN9wMuW/Sxa5MTb6WzO0AgxaJxppjBCvR+ti5e5AecTN/Elrp3vLEkmvqvyyb313F9WFUgU7lxz46RPmWX7O2jHtZcQS1+CWKesnZZ3ivY5E6POp/6qbgqVQY3WyYzCpdzLvUqueqIhYcmYHdqgcQMYpTh1mebVsL95Udemnoz5o62oNSEki/gW4Zz8KhDkpQ4tNKZAr3gGfVFjgtjU5luitBIxO4UKehNJualrIA8N1Y5hOuYR+YruzjjehMvHr1jU3/Aa3UhR053W5z9ATKn/gY+4wZdoK3JJipQp6ZY0huLQIZp63PJq5iQ==; bm_sz=89CD29591A7F17FEC4EEE5F87E7F2725~YAAQ88gwF0fP5EeYAQAAy3+5ZBx50E+PAo6/Y0QN3mHvM+j/1iAO95eECs7OTRe2qSVx82fBN/ZDgqxnIAy29nyqEQfeBjFSJaMg3uQPW4LA0LchJgjtH6out170/QcLuRcg+IRlmlWezuod5fxi4pR9ubIS5fFj2skHjD3cP454G2YtojoXPzvmY+i7NbMU5569s8nnqoneGe3sNkbLet0YaIegBl6ykUzhmv0SkaKFkk6nLKXgEQyUTHa9fdQCLp7XtC+X0awiTWu5bUmquVILVEUfyRyfj1MwAGJKBzGrilhLYBeCboR92v/cLwAmxSBmyDhACV5Mip46flRxanlp8YmdrepAbIomOxXupmWKEa24e7E/YXIvwkQafXVAN0kdN4k1wbj197ShK/dCA2hjM8DPJWBS7lJ0NLTsfkM2BHStOGaDRmvg5eeR/5nxoHfx6SzAl6ZBv7/qV/o6fH8wrBurPqDY4mMz/3lwTKFwEAlfF1WiBbPWWE4+~3159600~3289911; bm_lso=D99F529D6C1B42F329361A111AC2C199B436ED623EB07F365ECAFA8A9923E810~YAAQ88gwF0XP5EeYAQAAy3+5ZASdHXtaVJIACqbseI7OcRFrZEB8lIne2M+FJlofjeaqE/QMPawnDDnqA9cniBg8/y7Qx5P/7ZwvX4PHPMCDGrneEKqETi5dtKMGsLddlkSLnO4RUpP/iI2ia+Sjj/0qEsLueN9wMuW/Sxa5MTb6WzO0AgxaJxppjBCvR+ti5e5AecTN/Elrp3vLEkmvqvyyb313F9WFUgU7lxz46RPmWX7O2jHtZcQS1+CWKesnZZ3ivY5E6POp/6qbgqVQY3WyYzCpdzLvUqueqIhYcmYHdqgcQMYpTh1mebVsL95Udemnoz5o62oNSEki/gW4Zz8KhDkpQ4tNKZAr3gGfVFjgtjU5luitBIxO4UKehNJualrIA8N1Y5hOuYR+YruzjjehMvHr1jU3/Aa3UhR053W5z9ATKn/gY+4wZdoK3JJipQp6ZY0huLQIZp63PJq5iQ==^1754036536867; eg_ppid=852eb018-0ddc-45b8-a177-215ccc8b8211; bm_sv=AC3AA67F79176D04DDDA3F627038EF7F~YAAQ88gwF4bS5EeYAQAACIe5ZBzDZxEHtciv2Hv2a6YMIScZCnxAWpUtUhiZSZwdcCMkOgHl5pXNnR2SkgEwtvJ0+xLk0tqX4e/WtKOch5p2nE7LvMsIu7m5OCSdUeJ3FPvu1TcreXucXdSvnBhecqrXotMdL3wFd15NsQ/V8hMVkHH/kv7erskjVDADcV7raDcpDdX3EKM0NAs13+bDKTV0L1eWMDxdSBy0SESiK6ZNIBUFTJvF+w4XnETRw10Mz0Y=~1; _abck=3D5485AF8D1616AD53B8BF02A9267B94~-1~YAAQ88gwF7LS5EeYAQAAcIe5ZA77FeAKnpJXS2YIPyOXY9chmg8flNg0LZ4DMTvUY3ks2WhckS4lk4IwaDx0fPMxWhmVUNNMt7N+r+j5EK0xLfcuYUYvA9T+F9RpbQ5YCuM/EjENPq5+7g+/3u563DjA8jVY6+Gj5tj4yOqW9n+SXudUfSgrNoliMHYuXBm10/PcylKVk9MrHqa25hdkrKqoBBC2xx14SAbCVxaDAgpob6nMpP9NN2T13yLvp4cMpjaRx9p12lyzqmhL8YHe4EiU/O9Gp7yXFe+ATquVuHP+lqnZOpzrqd+Y289jp6jOCS2uoAsUtrUXVqBw9bfOlmmISvMeM+cL/eLd1PMrP197mULif4TEw7yQpZknEN0rZ4pdS3H9bgMnOZR0PpIN9LcH9RQZNaI1S3YRCs3fHgp9h7RWPO30nBQ=~-1~-1~-1; NavActions=acctWasOpened; _dd_s=rum=2&id=89f45d4a-a3c6-4e8d-acad-a2951002ab92&created=1754033344591&expire=1754037437317; eg_adblock=e=1|aaa=1; ak_bmsc=468BD26A0234D5729F2D6753C007FE05~000000000000000000000000000000~YAAQ88gwF03T5EeYAQAA6oi5ZBzUq3DQ99u+1fu+flmRLZ9FwwL9k6791g8NEv1oioInifcqxCvOqc1wApSUuJLh2SCgYThCtolt15iYG1oOG2dVQKXnnfXoE6XZlz6QgDEdB9jUQ/iEv2uUDOxC+2gdb+viedUHHALRdejnBo0WG73fHzxCYWtavsbq2TnVggr2GgCRVYn1ICYF85QUDUGX2pHg9ne5Q/n2I3tTQXFNy3bzZysLWaZXDzZdqJQ4Vn2qwB+5KY61s3M6UzU4sdwjLllXCi9QIhSQL1XrnUo2TmNxiBxKZwy90k2iZeRSARZEK/J3V0pSsHTMGSChmHAptEZ7jsRjZIsR9TB59JM+opFL9gv1raMGSWZySFzvm/jcm2gqIQ2EIAsPB6ArhT4XBsxI1SYKMMKRhv4vezTcC0IYMgVKfxf2OixGtz8AzQngmE1p/yZ+qzRCPZ8VIWThrrGfHGdmqD42zY3yBYMqpzXpSb/U3mA7q83ibOevIZr+Ixl7mNaRGETOH+/U9EMTFAwRgBUy1hnfgKuSjY7Z2tU8GyCahQVhik4HS+TdzRAbfMg=; DUAID=545938f4-9cfb-4539-9718-90d0026d1ea4; EG_SESSIONTOKEN=ClAKJgokYmYzMzEwZGUtMzgyNi00Mzc0LTk3ZDMtZTk2NWQzNjEwNDQ2EiYKJDk3YmNkNWExLTJiODItNDZjNS1hOGM5LWY4NTZiYjY5NjRhZQ.znKuOLnrXvbYEhXU.Kgbua_zGmBR2nDEC14SkzREjuI5N3SDonDArehCH98OGr1Z_Em7MGa-tVM0NPF9RWDx_0S2HmZrKIGVStrzXR1UvzAhmY7d2a5Kl8VYpIz6M4i0yhus5Qa8TsPZyCersJtZ78XlI-ReXCiXv4hJWVbA-LVQQd_egmcEyTG7msNaGV6FUY0cfRg2sxR1j1gsSvuNZfgpssIBrxh-g9m45x7xy4o9--HhIlpi2Gs5mRic.Cdgzt9KO58U2YQRZmMuuKg; HMS=5b939516-d090-3d65-9b72-d3088f3eec2b; MC1=GUID=545938f49cfb4539971890d0026d1ea4; _abck=3D5485AF8D1616AD53B8BF02A9267B94~-1~YAAQ8MgwF7+dCl2YAQAA2L25ZA7sNuU4RjjCg+TpKMcRwC97J8ZfXx8luIsD9Iyu3YL7mctbLNWDfQo224peRhOu6yspJmomoPM2ckxW9nehtY5RYBLh0uBgw3Ehpq0hUDmmHsIOacNYlPqy+C3VA4Ec0HD9SlEbkyauNK/svq/PVYXzQmRj0lm05v7OPmpoikaM+yDp95uAhGfsDirn3y5390NtGyMsi/bbhBQWGuGruQQGIWvae1wErFgs9LKv03CJtA42uu23vV9SPDPJYTTXFwoDqY42tzzPKC/n9g1UCFvdXO3fBYPhltvF8Xre3YJbJZXfD+xK+AXLGKLU+rB4LNk8lK/bSMDEzAJjY1ru//0AZo6pBZvv5sUEPVQb3JhLUe4n2k6rFUBUPLERbbY5RsPsQQ56f4flynfn7hKJneBeix9Y4yfUuD0+hr5w2Y2JG4+yVQQ5cnAIWo7Hrw==~-1~-1~-1; bm_s=YAAQ/MgwF9qB42GYAQAAYOSMZAPYwydB54LYLG8F09DcqItRDhw8LPo/z6ZYZGFNeUL1MIIGWN4LZf9RTqqTT0l6Y3/qoKfcGQdsJYjkChWamVg9WzoZgHDZQoiUorPor4xY3qT4fiY0mGrxT3TF2CeFF5bGQxrjQoLLbx0D4H4N+xJtjWLpqgALQs+Z4c6Gn2UD22YYTpZf7jGc2SNa9bip870HPu/dW2NMZ9HTEprrkPa2tzW7LbzHGKSHEdUHs7PvgQ1CJdpMgEleh5yRZrgOrwCzcPjnivXb0ZQBL3L077d1pmoFdACkHlTrV1CqQyPoTf0dzMDaPfaakoDPMpH+k7aWV/Nnr8Iedm89zniSNpqXk5XE6HPtuHXoKN+3nAXpaNE82bFrXuKUty+x1hIRtEfD/b+Sq1s6fMJyaJkDbfOUEwNFRRAR7xlwGeQe1oHpUH1MX815GCnfRXXg/4N+aW0z+R1JNLLB7GkPKJ1v/8TIdQhRW0ElQYkaGXNkuwPhAsS3peqdEJwPhdFIsNVzEgIIWjNSQ6N08EkTULxS4BaYbddw; bm_ss=ab8e18ef4e; bm_sv=AC3AA67F79176D04DDDA3F627038EF7F~YAAQ8MgwF8CdCl2YAQAA2L25ZBwPJbOdYI5xvWHuuhJwMu+/Z0DgDXzcm5OxgDeiYUq+sWSXiqhmgBeF00qV672Rn582KrGVd1kTn33iAAw+5m2mXqtrncZtfVL4CEKbwMgh+CnGxmN2/hPyun3M7BIOoeEHzAvLBRMbI8+JNlkx8gEl3dWsAXv9iCyHzf4x/X1XUbmzlSEzZS5G2ETUzEaklJL4685Zl0gnL4ZkQ/NtSXn0bN5A1RIPAhFdA/GRcBY=~1; bm_sz=18D0E834B3C9DDD2B3D423EB6E3CAB36~YAAQ/MgwF9uB42GYAQAAYOSMZByr3VKXBrHVbhCgqL07cMxvEEWvlsWKLy6OHaVg8V6ycPDq3lxNGtkQ2Knzoppq1WDVi+/8y27L4sjzwHRcP14lQaGrQk+C6r27ZOw4lfNaliNEM6YenBqrlGTNl4OuIA2b8ZyUV31N3lRFr7xgqsUiCaKKWzL1i+CcsN7muXgQNGr5tDzUBsl+0JYphPotRKXvrH30j/Y1yTmYQnaIj2VFBYHns/BY3e2r3uYNhnh4OLCFuZn4MP2O5A0gH1oTZaBfLrqxkFVoiJtEafZIyOILVbX0wZ0j6z1Hpt0yGeaT33UDglC4IT2bo6bJQ9RInKiCHg0tU6UUJ3/wyVY=~3555632~4600371; cesc=%7B%22lpe%22%3A%5B%2244c73f42-4f45-40ac-9c1d-ce3b2cdf39e7%22%2C1754036551121%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1754036551121%5D%2C%22lmc%22%3A%5B%22DIRECT.WEB%22%2C1754036551121%5D%2C%22hitNumber%22%3A%5B%2236%22%2C1754036551121%5D%2C%22amc%22%3A%5B%22DIRECT.WEB%22%2C1754036551121%5D%2C%22visitNumber%22%3A%5B%225%22%2C1754033342872%5D%2C%22ape%22%3A%5B%22d7d18ced-bb56-4d83-95ed-7152beb677d2%22%2C1754036551121%5D%2C%22cidVisit%22%3A%5B%22Brand.DTI%22%2C1754036551121%5D%2C%22entryPage%22%3A%5B%22Homepage%22%2C1754036551121%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1754033342872%5D%7D'
#     }
#     response = requests.request("POST", url, headers=headers, proxies=proxies)

#     print(response.cookies)
#     print(response.cookies.get_dict())
    
#     return 
        
        