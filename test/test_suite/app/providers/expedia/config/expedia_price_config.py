from datetime import datetime, timedelta
from typing import Any

from ....types import UserInput


def get_expedia_price_config(params: UserInput) -> dict[str, Any]:
    currency = params.get("request_currency")
    if currency is None:
        raise ValueError("currency is none")

    currency_changeable_data = {}
    # print("Input params in config:", params)  # Debug log

    check_in_date = datetime.strptime(params["request_check_in_date"], "%Y-%m-%d")
    check_out_date = check_in_date + timedelta(days=params["request_nights"])

    if currency == "EUR":
        currency_changeable_data = {
            "siteId": 4400,
            "locale": "en_IE",
            "eapid": 400,
            "tpid": 63,
            "url": "https://euro.expedia.net/graphql",
        }

    elif currency == "USD":
        currency_changeable_data = {
            "siteId": 1,
            "locale": "en_US",
            "eapid": 0,
            "tpid": 1,
            "url": "https://www.expedia.com/graphql",
            # "url": "https://httpbin.org/anything"
        }

    elif currency == "GBP":
        currency_changeable_data = {
            "siteId": 3,
            "locale": "en_GB",
            "eapid": 0,
            "tpid": 3,
            "url": "https://www.expedia.co.uk/graphql",
        }

    return {
        # "impersonate": random.choice(IMPERSONATIONS),
        "method": "post",
        # "cookies" : 'currency=USD; CRQS=t|1`s|1`l|en_US`c|USD; linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; EG_SESSIONTOKEN=ClAKJgokYmYzMzEwZGUtMzgyNi00Mzc0LTk3ZDMtZTk2NWQzNjEwNDQ2EiYKJDk3YmNkNWExLTJiODItNDZjNS1hOGM5LWY4NTZiYjY5NjRhZQ.jssuNgu28xKpgTbz.ckWdlHuR7iicGG7wFIT1cSOyzTmzOfNtKB96Nzvndd2YeOnogjD3mE6UJuo_6OyYjFeUAG_AYAHxRN6wZcUDz6eQ4QqqUx0Ks4YytVj8nh-ZdnPLeBh_LCokTzBZ7ktCt8VuDf-Dg6Zu33g7ePtgCoAtK2XH79z11N9NoqKjaQIu3_UOIHJQyVQc1LI6ne63t6q4F96kbFCGaN53fbEIbVFocGgP8h30fyjaFWNykas.bvgtWsWX8WghkGZ1Pmhbvg; MC1=GUID=6a3f85e8ad3e4cec8a748b8bd252c320; DUAID=6a3f85e8-ad3e-4cec-8a74-8b8bd252c320; SUA_TUID=1; iEAPID=0; CRQSS=e|0; NavActions=acctWasOpened; should-display-fee-inclusive-coachmark=true; tpid=v.1,1; HMS=c934c2b1-c816-3e4f-85a8-b12f1ba6201a; bm_ss=ab8e18ef4e; _abck=985A65E20C2D4CEE53D99FA7716875E4~-1~YAAQ+8gwF+q140CYAQAArzUwWw69cEW4CCKwTXB1w4SHpDUEU3l4tiHWlt+TFFdFVFweOM4GAz+ekiyYtp5Wg3YYMJ+l3hWuf8X8GEjtINTGjfcVzhweUXzuUQRRfmZeo0gcy69vQlyplzwAfuyVWPh9bITxW8dBTGF1ZMSSPtEkcd+exFKtdpXKSjdOJnRBYungOtkHBh0iIl/sl3Jav49JkICv9QsakjYkfJHmnJdd832SZkeV077zoRFqOL7jygJhIapoeM+phA7+DcmunUdfMuZWfgRD/mcZ9ae7oj724tMtc1CUGpzTa7DO9VOPSHf9+7x2ogAaHrq+kWPqu7//2ZqYhiZeXn6XgSatEfsyOFKR3l2Y9laHz+AYn0aUZzTMF8OnFV5mmorJDJ5H5ZRhkCgwXNusKwn0egwMi0c8dUXrSPzY+3CpU37v3FN6msRi+Ov63FrpPip29cIMHrIuTkGLd18kZyNTy+GFaRYW0I1tE3PQ154K5VZJVrtj+YtXkpbQXpnnipYOcvFF91G+w38jHxCFQfY1jdpYpA/EQweJVmgx6vfE8KS6QIXIC2hpa0KTSgt1uR778E9zzWgAVlTV/P/kGQbrhQ==~-1~-1~-1; ak_bmsc=CC13C849166D6AB14453A22BE8F8D553~000000000000000000000000000000~YAAQ+8gwF0O340CYAQAAezowWxzGXxLwP/1W9mRQizHbcXdcWYerHai+6h81m4ntCHN1lmNF1IamQpivpF4PyUU0Rc/gvK9rQ9oHlPjKnQCQ1RLc2QiFS/Cwlb8hUMo7UN5/BsMKTqfccWmVHGma/sjiB5v81O80tns0u7sl6lHRWfrL3CUl46UmdyKOQSoqYza1VMqO6abEzwv45tPFWvdxMEzTvxZysPc6LA1R2L8iDtWuvXh7jOp7aK8ArJk3YeeoKW3NrdTuA67Jseenqzlm6mXhkxDL74+hTtg/AbAdCfl3grdYEfex33EMAqgafvDBoElJRyqvNpy57Dzh7qYcxjnZA8Xt6U1H6mT4SH9oGK55e+/Thi7A94u6/7HKfyDkY3mCFt9/Xytj0QVPpNRJWednPeGnpa96ARC5RbOcfoLxej8pPgH2F36QCs6J4IfsDg==; feeInclusivePricingSheetLastShown=1753876549851; session_id=c934c2b1-c816-3e4f-85a8-b12f1ba6201a; bm_so=9BD98D36EFC394D0C64DAEBC227498C3A2E6D9B01BB94D9225330C97266D7F7B~YAAQ5MgwF3Dr00mYAQAAnvUxWwTB7S6Op5u/h6OENErGp56HbOvVEpVqMevVeAXSrF4VMyqlH9sQJOTtxBNGPr5ApqDfoklQadwbKhuO/V++SSwc0sB+4Ew8pe0tP5qSR3uJPOxVZIQ8JalyilZNX7nu148Iw8AhJti+wj0Nf+i9bMwp5arRQlwQj1MtGiWlLZkV2HQARnJVPsRYIH+aCMm9dNvhL96frD3+pN/TRJfLC377eZB01nJf55OZ1VAMZ2VatSzn8hwNt1XnGYTq2ixbfpFRnL8eFbBvHS3SVEUB7hbLiFnqY6e1i5CHutro8wD4N9259+a+UBPb0ZIYGYUksp0q5dG2+LKIpbuZDo7Fg2Qdr8P5N0eYjtK6May0ru8WaQwygt0i6+/tzvyk3ws/wHMfzYEUWgKZxn6AJMpBgwebTlGNOnwUiT6I9z23GKVY/e/zY013AFbwHpLVGw==; bm_sz=C7DACE9CEC456DC6714DB9EAC34231D7~YAAQ5MgwF3Lr00mYAQAAnvUxWxwV8S+qGNvBUsTQ1vYOjt5qqSzAAOrNIepr6BWMkWwEtJz2yNg13C8AYq7qZShJ17vobqOOdmSDS52PY+RE7nteeKFfvNPZQ6RJGYpp38PbqptVhPAegpJP5LJAGexJ38ihL3FRfBoupy4oQM+sjK8d2w+uOlyZTyNrp7IeAnZItPnWKTpHYGClZSF18ov+CkE2lisl+K4K2QKyz62oKXYt2OzH7D5EMrUBNwHuE9CC2s6Iajcs1VmB9cWHElKFc6vQqDqyUDKrlllSZmdMt3G0T6YWY4jPcRAZaD5cnzEbOb5Py793VtBiOjGscToQ9TkIYfPp4nsP3gUey7Bcnx/BmDYPyLzuiKbNUvqKeRxoyL8KgfRP+iHXqQAkm80aPJ9/TIt/r7rG6XeSB9XxAJqKxK09~3291192~3162423; bm_lso=9BD98D36EFC394D0C64DAEBC227498C3A2E6D9B01BB94D9225330C97266D7F7B~YAAQ5MgwF3Dr00mYAQAAnvUxWwTB7S6Op5u/h6OENErGp56HbOvVEpVqMevVeAXSrF4VMyqlH9sQJOTtxBNGPr5ApqDfoklQadwbKhuO/V++SSwc0sB+4Ew8pe0tP5qSR3uJPOxVZIQ8JalyilZNX7nu148Iw8AhJti+wj0Nf+i9bMwp5arRQlwQj1MtGiWlLZkV2HQARnJVPsRYIH+aCMm9dNvhL96frD3+pN/TRJfLC377eZB01nJf55OZ1VAMZ2VatSzn8hwNt1XnGYTq2ixbfpFRnL8eFbBvHS3SVEUB7hbLiFnqY6e1i5CHutro8wD4N9259+a+UBPb0ZIYGYUksp0q5dG2+LKIpbuZDo7Fg2Qdr8P5N0eYjtK6May0ru8WaQwygt0i6+/tzvyk3ws/wHMfzYEUWgKZxn6AJMpBgwebTlGNOnwUiT6I9z23GKVY/e/zY013AFbwHpLVGw==^1753876660278; page_name=page.Hotels.Infosite.Information.Dated; cesc=%7B%22lpe%22%3A%5B%220e6c4c1b-57ea-496d-99c6-ad55bdc25ebd%22%2C1753876662536%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1753876662536%5D%2C%22lmc%22%3A%5B%22DIRECT.WEB%22%2C1753876662536%5D%2C%22hitNumber%22%3A%5B%2213%22%2C1753876662535%5D%2C%22amc%22%3A%5B%22DIRECT.WEB%22%2C1753876662536%5D%2C%22visitNumber%22%3A%5B%2228%22%2C1753876542869%5D%2C%22ape%22%3A%5B%220e6c4c1b-57ea-496d-99c6-ad55bdc25ebd%22%2C1753876662536%5D%2C%22cidVisit%22%3A%5B%22Brand.DTI%22%2C1753876662536%5D%2C%22entryPage%22%3A%5B%22Homepage%22%2C1753876662535%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1751546055201%5D%7D; bm_s=YAAQ5MgwF7fy00mYAQAACgkyWwOdkAAG/N4tkSFvt6Vqb9YzA/bEQ9aV/PGkFDT5hxEOML8TWSiwiUU3KyobYrVfZZIGmuEkFWkMbnY41Dbtf5LUws9C6zTGxZ5peS+G6Yp6EOLljrF9dQhJ0w0LDOlF9v29vDAVKD+PNOTT1th+Vdt59i+MGNJZCkU9CoRSgiW9t1B2Za23Blp8IJ14P0a8v1LS0frRK74579buClc0FpQxH23vFRlBf2FZfa8hmTTcuaKegdVVEPzowH3FJNB9VM9YR1hrwgucYNGIj7FfrPYvLvnFc32HHq4V69NsUG3JVuo+9BA4sUfL2z85e7W7VCv30zeuLVCkqwiUJio5KneY8qWkZUNv76yKQ8sUbqpSx0KeCaKmiNXXmyuCxEUvXr+2FqJKd1A2xTebNiPbO2STA+bHsTFPj2Nc+FXsLPBK7lwlEP/a3JToqmYQ7UYO4lsYnCc+xe1q0MIZ6yb/j0ibc20+DjaWMnidwqoIUtkeGI/GIvzgYAbXN1tS1n4HQ2+VzVZaOUUFS/OI0oVnySNSfEA5qF8AFNn0J4zGuBBiNB6PFUcLJg==; minfo=v.5,EX01AD567512Y$28$32$5B$29$1A$3F$15O$D4b$91$9Cg$FA$17$A3$7B$DB$3D$C7z$1A$0A6$29$7F$10$E7a$DDHZ$5B$86$0F$34$80p$FD$F2$7D$82$3B$EFB$35Ab$B3; accttype=v.2,8,1,EX019B968373Y$28$32$5B$34$1A$24$15O$D0b$91$9Ag$F1$17$A4$7B$DD$3D$C0z$1E$0A6$29$7F$10$E6a$DD$5Dp$5B; bm_sv=F05FD57BC153305BDD4EE90F1F86E146~YAAQ5MgwF4n700mYAQAARSUyWxyFjpaKPqFbrLfvg+qomIHJfUHLqwy6RzIHswNIYSwMaDV4WHr4GoBxbfD/bkk+c2jVEtxToHZBVy+903QUa+u9ceGqqXicpOmS4mZSSzLm2F1MUxpmDId+Y76fu4d7KQ/Q+bLgrgzVBMc1TTi11r18a+f3bmnURugqVnYptRNjZLsKIPnlYeY3W++US6Q8+TI65Ot4QuR2/9n9Ku+ogan4vRbp2iaQDbI7x77XUQo=~1; _dd_s=rum=0&expire=1753877578807; DUAID=6a3f85e8-ad3e-4cec-8a74-8b8bd252c320; EG_SESSIONTOKEN=dFwqN5GX80KJIrE96NfyhJcU8nllKSeqdlxYNaZzIKWXhI:Ks13RQx7IhYZOs1JlztWXJRQkrkXfwd7HVI3Ped_qbuuchOMQEnIf6e6lJizEnsqNkYs3HXQn3-GzEkx1tjv-A; HMS=c934c2b1-c816-3e4f-85a8-b12f1ba6201a; MC1=GUID=6a3f85e8ad3e4cec8a748b8bd252c320; _abck=0316671524B414C36B965A7A6875F3F1~-1~YAAQknnKFwOZYMaXAQAAbgVH0A7hx/dtqnwz9gUptx6xj4g9UGzAZMc90gVuo6jfEpOMkPod0SlaUZ6gCB0HHWsm/CiZIm3NnoX8D0YO7G4D8nepyWVsE316vHpJUeiTgmGWh+e7sc1uVfqZd750ZUg4L04yeDhk/alW59M4/UljRwDbbFo/mZU2fkdcpEcQIydcU2j1ib3PR4/PUVh9FiDkCgRzR1sDSDcF7amMD8xGZ5YX6gQob/f7xpczHsVpl8In3lyIBs4Ai7Oxn5ZH4RBln3KekEzy0VBXrQ3cMhndtuVCLSkH2EnULRmd5IY4ullVxsjyrdrb1lTcJX/rfUF9eOaalUyTfGUad6GdtVpKXZbR61Ozl6dSB3eptbAPKCxVHhp/fa+5yajkibeDoSXPRQg=~-1~-1~-1; bm_s=YAAQknnKFwWZYMaXAQAAbgVH0APDJkhTb+GQjKSji6MLkahMlUzaQ0FCRh7pYQvr41NuL1JKbG/k5NKIl9lafS19qwjh3Tb/ldRCZrhXMYFmAaAGjnBFcGxdW9Sjrd9pdmWbzCUAaQiiPmFj38KttxI4SPBBrqduCc+5S4sIizNd/kX3bYUz9YzDE1DAj3bKa693DRVT1ht4bvPCWLSMJJUEQBPqyMQxKXmmpybse6uc4YwsBfl/SRQf729H5My9HdyHbrzQeMCOnHHJdnzuB05hgx4IULx9LwxTAxrDsSTMNkDDQHVFrmL8q7ROXWmIjWS1bEfNpCtXkaa3STgIrDaVaYNI2A94Uq5XLj0OYkK4e9706UE0TrIsxulBorVCL+yhT+hkSQrldR3Xytts7BSDVumuZAibjOQEeP38Nbi3p7mzegVB6RTItuq+Cczj4G9QHFDpYzP3Zr4S1ISR30BOras6BbP/FxPxb304NsKWmcnIO6vBff8OspKsrJfvL2l7xJE3tE+Ypca0Zu0iahQmGJrPaCo0HElMmRviLy5nAb1xdaixXg==; bm_sv=F05FD57BC153305BDD4EE90F1F86E146~YAAQ+8gwF6sc50CYAQAA6jE/Wxxt8at2DcGTaXNj2lm8m7N1xHwDkybdqd7941mZR03W5O7427RxPVbmJ6lA8cHp/bHaLmwYW6eVEZeWoW4KlTGNCpDNF/QN4iV50imrIvxa91RhpQfz5Kf//4yfGR+//K8S7cUd5T5dW4SClM0CDf9Ekv6hCAEaQqWFf6FRJCF+LkUXO9i1k8zJSoO/grV1FUqeasOghUnWavla0iQr6DZzuCReTsiOwndGgFc1GKA=~1; cesc=%7B%22lpe%22%3A%5B%220e6c4c1b-57ea-496d-99c6-ad55bdc25ebd%22%2C1753877524967%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1753877524967%5D%2C%22lmc%22%3A%5B%22DIRECT.WEB%22%2C1753877524967%5D%2C%22hitNumber%22%3A%5B%2214%22%2C1753877524967%5D%2C%22amc%22%3A%5B%22DIRECT.WEB%22%2C1753877524967%5D%2C%22visitNumber%22%3A%5B%2228%22%2C1753876542869%5D%2C%22ape%22%3A%5B%220e6c4c1b-57ea-496d-99c6-ad55bdc25ebd%22%2C1753877524967%5D%2C%22cidVisit%22%3A%5B%22Brand.DTI%22%2C1753877524967%5D%2C%22entryPage%22%3A%5B%22Homepage%22%2C1753877524967%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1751546055201%5D%7D',
        "cookies": "currency=USD; CRQS=t|1`s|1`l|en_US`c|USD; linfo=v.4,|0|0|255|1|0||||||||1033|0|0||0|0|0|-1|-1; EG_SESSIONTOKEN=ClAKJgokYmYzMzEwZGUtMzgyNi00Mzc0LTk3ZDMtZTk2NWQzNjEwNDQ2EiYKJDk3YmNkNWExLTJiODItNDZjNS1hOGM5LWY4NTZiYjY5NjRhZQ.jssuNgu28xKpgTbz.ckWdlHuR7iicGG7wFIT1cSOyzTmzOfNtKB96Nzvndd2YeOnogjD3mE6UJuo_6OyYjFeUAG_AYAHxRN6wZcUDz6eQ4QqqUx0Ks4YytVj8nh-ZdnPLeBh_LCokTzBZ7ktCt8VuDf-Dg6Zu33g7ePtgCoAtK2XH79z11N9NoqKjaQIu3_UOIHJQyVQc1LI6ne63t6q4F96kbFCGaN53fbEIbVFocGgP8h30fyjaFWNykas.bvgtWsWX8WghkGZ1Pmhbvg; MC1=GUID=6a3f85e8ad3e4cec8a748b8bd252c320; DUAID=6a3f85e8-ad3e-4cec-8a74-8b8bd252c320; SUA_TUID=1; tpid=v.1,1; iEAPID=0; CRQSS=e|0; NavActions=acctWasOpened; should-display-fee-inclusive-coachmark=true; HMS=300b7c71-6a64-348d-862c-4d97cf35ddfa; bm_ss=ab8e18ef4e; _abck=985A65E20C2D4CEE53D99FA7716875E4~-1~YAAQlTMTAsIjGNGYAQAAral0CQ6JDpCTF7LmIy3L2p8dwaopl2BSFQXjOpVyzAM7iWnCdgHSKWi6Qqlqc6rb21736ors0/UCwtF4I0BS3M2qO4HUYQS1DNI/9ao0m169MSzELtXntgYOaLzMhMh6WnhlUidemEheya+7Ol5r3gG8obvsYolBZtgG+POlQuj5NLjCLaM2MHzDIpnhDFYALe5SBGvUaN6QN5R071nq1kT78gbWdSPqEqhNxcNjufLs6DD1rfU5flJS9QU7UDNM2O49sBqyCVbtkeTW1LNZNZsd7GvRvTCpf+wzcdNYeGKMvypryd/eCDU2XiSKyBuShHXj+XAePKIn/R/ax/h1iLE7lEaYXuzffJLsD9FDl/4A+OK7PVAsN3ezbgBHX2Ts1asqtS7j/BIbay3sj55tA4cfPTA8g7nWA43bZesYn0F7ns5dDYQQqL/wI5w4uE7OfPf2nqro1Vdq5IaiLSp9cCDDTjzTANi+SZ1AIMufr/mdQ1NNEbD7W2QSUx9H84ihUzQeiOPpB9HbLw1TOazYfxkSiFqSRGlpiXVXMhzMjAl8dzpBQihEhNOGVr4JqgtMVs28vzbd0DT1OOGQyg==~-1~-1~-1~~; pageVisited=true; ak_bmsc=FAB6179644B5152765BC0F7BFF912138~000000000000000000000000000000~YAAQjzMTAniOSfCYAQAAl650CRxVy8ydEYAeIEOPZnvgcYn3Pig5JJphvNwDiFW66D535QPOKRbgzpAZBuk1HCUYDaUVWc6xsAN6FHpZQqy/E4jK2h3M1bgDKOl+I0OlP+JI7ulnvbr7wpKfnLdp7hU4mCup+3ddUlpatOP5P6kpDZ/qqCzP2PeRPuez0yqInbMUKygcP9sLuny1VkIbf/GcXH2j0NYTYcrDbV59dVcCI+a9Klc340bTX2RmcskWyoBAPCpd4cVhqVkI70oYNEx4VO/fUzRpg6VWbwF20/e2SrlA4MsDyfrMfrf+wwcnI8H1+I1p6xtWX5FYRyjvYPhKTi7HI3tvy3Iuz18BV2XKc6MifAO16ZobpTxpsogKs1A/G7kx8QT4Pw4Rm2dFuVXE+MmMLJNZvfsa3/Xc3oHlb6UFtjk679PyXgsCJXKJuuXtfq+n7ZI=; bm_lso=2D2E8C5512244D775E627080956652EA9504AFC115B3E5BB5A6C9203097F07C8~YAAQjzMTAsSQSfCYAQAAuTh1CQS5q5ZKgiYYSFC3m4owflcg515lPnRLL7f91gURPwlV6+nYJLm789/tovfwKS7Luh/7m/rv0gxZsnGqWXik2qXpRbNxj7nEiXPmR/c0/1Mrq/iL4/4Zkz9eGQ6yGE63c1AVg/wkMgZnGYDJ5BRgJFl1lajkLrlB8pIrI2kqRuOET7HcFNqqfdQtxyx6gnnTgwMkndQ+16FgW94APvUKjQOunN8TWruxZotTkVgWqFpVqXCL6L2ZiOY/XTJqbM8dbyEp7s1lsxVvWZsOqxqFMYRkkJMusIcFEHF3/2jkC0HvoKarIvnohZfW5eVl1TlIl9ZSXdHOaxdNG9VoStqaZh34BNAhJWxf/UEj6Q20hpJwyOHCgsJcqi8kxn16dIXc1dbPSQNJY8W6jygFHbSf8Hsn/C0RQI73pSa6miCTsle6qnRbRMW6yVSf/en4MA==^1756800304568; session_id=300b7c71-6a64-348d-862c-4d97cf35ddfa; feeInclusivePricingSheetLastShown=1756800305711; page_name=page.Hotels.Infosite.Information.Dated; minfo=v.5,EX0172B7B46F$F0$FE$7D9$C2$AC$B7$A3$13$D2$B1$9Aq$E2$B9$EA$28q$E4$F6$38$DDE$98$8D8$22$D9$82$CB$EDV$F7$0A$F9$FEF$89$D7$15$E3$D4$D5$F6$B6$9C; accttype=v.2,8,1,EX014A265FBB$F0$FE$7D9$DF$AC$B7$B8$17$D2$B2$9Aa$E2$BB$EA$2Dr$E0$F6$34$DDE$9C$8D8$17; cesc=%7B%22lpe%22%3A%5B%2240ebe511-f95a-4860-95dd-0b52a4c7dfff%22%2C1756801184280%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1756801184280%5D%2C%22lmc%22%3A%5B%22DIRECT.WEB%22%2C1756801184280%5D%2C%22hitNumber%22%3A%5B%2212%22%2C1756801184280%5D%2C%22amc%22%3A%5B%22DIRECT.WEB%22%2C1756801184280%5D%2C%22visitNumber%22%3A%5B%2235%22%2C1756800264582%5D%2C%22ape%22%3A%5B%2240ebe511-f95a-4860-95dd-0b52a4c7dfff%22%2C1756801184280%5D%2C%22cidVisit%22%3A%5B%22Brand.DTI%22%2C1756801184280%5D%2C%22entryPage%22%3A%5B%22Homepage%22%2C1756801184280%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1754306499512%5D%7D; bm_s=YAAQjzMTAtTQSfCYAQAAPLKCCQQW4JzK+A6TyqWbL+ygZOdDvyvf+Pwb+DQssKqdPgYB7ArROL2c9Xy2T+PB7iFpPCn2wsZPdm4fnh9z5ki7dv/Szzwo4ZsMDojqPlOpaX2EcTPQTKLp1AWB9YKIoVdnuGDB2qva4RR5d3J+6F07LYKtCV27UJLqmPhu8RY5/E1tOPt/CFE5Zwip7W99AonHARxbGQj9cCiV2rzxLMRV9C2c9Ue5cEz+amk/hJPVZTrrsXX67FpRG5F95iNrbSTJnGggYcBnkCyjLST2FU9/ajBD9ggFIvKubBa28ewpost/udAwID2bssIZlNnrR2V1wQntGc8keLJgbUuvWzHoVXYMv4pMfPXmtn2qqQ7/DMjJly2u+zqb09d4kDUpkllqoubUzrMRAeHX4iAvF4HXmmZ7MiiZWC8eWAjjCmg89zIUvHO2iT5yan5mk4FsLnAX3kMdrrjDlF+8KaqqLwcnm6MxBPdR1rbWvYfTuFGSRs7osOflcDjifJdGgWlO94O3FU2RxaiWHR/YdSa8Xlfcg5DiOJH3uG6gPyowyOw=; bm_so=43D3C50A6F1F3D89A4C895CDDD017F9420CE508323699FCE2DA6ECF8D43E13AD~YAAQjzMTAtXQSfCYAQAAPLKCCQRRjOQFQB7pw0jfYGz9bJiTQ12qH9aRRhXZxfx+fzPDUdMtW53tUPVjMWxmR/ObiKfYmKEld5JTBJWA43Ia9qkQ1IxnCzW7G9HWoHctY+vizUEfC+T9eVpB777o8WEvonsWWpX73jEKT3igVr8ImeRO8H2h0gm49A5FEx/ONdugBx+NZ7Y9gsmi8kNojSzcrB7IoOpiwMsNeGQU1gBC2cX+EXhKlfqRbIJBYQHXVlSEdvtC5u+TRmOqnmy4d1I/3XDkL1Ik+DTdNPJIO5qOVffcuh9WV5WRLsPekBLFLTN2goE2wlAHU+A9zjg0HZQ6OhcNCQI0/1kLhV2ceyTAVPmMKVz2IJYEohV5fdNyZ3U2ruiQSB2seiWAUXRmPub5RmPmpWbuG0lwMZeILXzA61zIzeL6rA1qohgqNUL5RVflKhs6QzeLidNr+HMt2Q==; bm_sv=EE4488BEFBCDD70FFE593546F730B8F9~YAAQjzMTAtbQSfCYAQAAPLKCCRyEe24tKJ6oGlDD0PCy4y4xIhz/hSpwSMJehCSz0ITWDbEQtf0j/e8Hhzy2z/gfhrOLwnci6WXGGtuP2hP0EPxaLrYAzbgA0J7wLUVYIEItarRd8H1n+R/C97a6xNcRHXX0UlWku5R7rKF6UhnAryJiJcCbOCKC178QIS6QfPsSurpfcgp+1zqQPZjqzgr1TUoyFXMY5WE+yQBja8/qC865LK5uGCtuGHMw0GJsEpA=~1; bm_sz=AFB98EB7FEA7B26722B68458C796E524~YAAQjzMTAtfQSfCYAQAAPLKCCRxe/OvvxqddyJNctzRISxSZaocl1ziBH1POdUbr6uGjXEImgKyO7/t2O3vF25RXmEYsDgSBnA9iOU7F5bG1Qm97Ue1mmJ/jx94zjkzxJjBC9+uuthIF0fXYDemwi8iTCCV+5MdCV8T0IuQc3GtTV+vsVSjipMexgrIXJXOK8+DP6VXdFbvRV3NcPLd0Cx/3QiwI64LJpauwJvqXGy5GUID2T+3NamHTRCic6gL+j1HFQ1ui8WYMN3fdf6U0N8/3Q1FC5TMTwEvT/5/ikNBSk/S2n8392AXMiLmEvYgeEpOsgEjamzZMnj+clYAivWgY7OnQA8WNTxDwnEG7dwjDEDvRr1Or/DBXdTAlV5nteTL9D4sMNxMvo/t2RYnirxqsBA3JIF6EpdEy013htrF0OVU=~4339777~3749186; _dd_s=rum=0&expire=1756802085675; DUAID=6a3f85e8-ad3e-4cec-8a74-8b8bd252c320; EG_SESSIONTOKEN=ClAKJgokYmYzMzEwZGUtMzgyNi00Mzc0LTk3ZDMtZTk2NWQzNjEwNDQ2EiYKJDk3YmNkNWExLTJiODItNDZjNS1hOGM5LWY4NTZiYjY5NjRhZQ.znKuOLnrXvbYEhXU.Kgbua_zGmBR2nDEC14SkzREjuI5N3SDonDArehCH98OGr1Z_Em7MGa-tVM0NPF9RWDx_0S2HmZrKIGVStrzXR1UvzAhmY7d2a5Kl8VYpIz6M4i0yhus5Qa8TsPZyCersJtZ78XlI-ReXCiXv4hJWVbA-LVQQd_egmcEyTG7msNaGV6FUY0cfRg2sxR1j1gsSvuNZfgpssIBrxh-g9m45x7xy4o9--HhIlpi2Gs5mRic.Cdgzt9KO58U2YQRZmMuuKg; MC1=GUID=6a3f85e8ad3e4cec8a748b8bd252c320; _abck=3D5485AF8D1616AD53B8BF02A9267B94~-1~YAAQEUIkF5AcGVqYAQAAFfPrZA6vQkDUhWqr5csiuQTuK5AY0eC/CLAeACkrD0plGHhXWZjpNXeQSIyMj2jYY1+pcS1KHqwkJgM3kgbApefQNwPK5c9mAWB3cpICT6Nzk+tpuWCEclj5VjqJ1QiltLGZE1qvzE8ICRH7ixn8hdWmKv+A/kxsbBQoAmiIKSZGj56kzyLy+3jIhArAutQQVHVdpgIa5a5CzOfIZTH8x9Yk1MUryp6HMEyYP8ztLLM2dXAZh96MiBgCSbgvaNjwXvStPg2WUn3kSOByILTaBMRfU1y5MQCNJWzlah0HOkN1akQJYKpNi/jA1cOOHKHvj/dtTZ25OzZm6Ls5Pk7/jKetiS3gicTYFv7eCPdh4CMq0m/WSP6QrWP7UN/I1rd+smL6cipd6/ZlH3j10hpERjqxXAHllC6rx+4gwB4brzNDEC7e0ka45hAzxjW9VGqxAw==~-1~-1~-1; cesc=%7B%22lpe%22%3A%5B%22295d21f8-f72f-4dff-8f49-03f559ebbc11%22%2C1754306582414%5D%2C%22marketingClick%22%3A%5B%22false%22%2C1754306582414%5D%2C%22lmc%22%3A%5B%22DIRECT.WEB%22%2C1754306582414%5D%2C%22hitNumber%22%3A%5B%2216%22%2C1754306582414%5D%2C%22amc%22%3A%5B%22DIRECT.WEB%22%2C1754306582414%5D%2C%22visitNumber%22%3A%5B%2231%22%2C1754306499512%5D%2C%22ape%22%3A%5B%22295d21f8-f72f-4dff-8f49-03f559ebbc11%22%2C1754306582414%5D%2C%22cidVisit%22%3A%5B%22Brand.DTI%22%2C1754306582414%5D%2C%22entryPage%22%3A%5B%22Homepage%22%2C1754306582414%5D%2C%22cid%22%3A%5B%22Brand.DTI%22%2C1754306499512%5D%7D",
        "maxBodyLength": float("inf"),
        "url": currency_changeable_data["url"],
        # "url" : "http://httpbin.org/ip",
        "headers": {
            # "User-Agent": user_agent,
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "content-type": "application/json",
            # * maybe change the 78d....... to unknown
            "client-info": "shopping-pwa,78dcadebae7c41dfd3cc87c1859b7eaf495fcc92,us-east-1",
            "x-shopping-product-line": "lodging",
            "x-product-line": "lodging",
            "x-parent-brand-id": "expedia",
            "x-page-id": "page.Hotels.Infosite.Information,H,30",
            "x-hcom-origin-id": "page.Hotels.Infosite.Information,H,30",
            "Origin": "https://www.expedia.com",
            "Alt-Used": "www.expedia.com",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Priority": "u=4",
            "TE": "trailers",
            # 'Cookie': 'bm_s=YAAQHUIkF6ac+VmYAQAAAqzxZAPvFR2aqdlQ1Jy5pIc9423Ps/jA81WgjEvl6jI1OHKWaYdoc7Ph+wa/+eEduDfUmA3LMMw0QAc1Sq2l+XZMJbMFVX5blk0V6VdEJmHYTIPkPcu0hLWPeJCiFNASdhUOcD7Gzd1Juj6TFa0QqenQ1UK+Pd/JwNwKAQXHTL/RIo3Cb3CUCgyVj0TTMDRcNzeJOEi7ssxF+n2YEtgL+SWekWZtnbjgVyE1++DAcdzn1cPKARRQYJauITn/ECeQ+u6oWqvd0vZySUE0Wfq33GcSbgqdI8l4YBr9c/UrXqiNKjseYQ8BDj6WgDNhuGxDzr4NN5fy/fozb4tbdNeEda5vn3/rX/yWXJpMm62mB8M4u0x8fBsb3P0a8t62KCmqCOSWaCfI4dmQlou3gN9BzUimOcxYs9ZJmoJ4GGIzMDhxUldp6oHySBrBMhAg9h7GLia5fGNzxOGGhjvSkfEJBc5Mnn1cNxG+F3zSsHX/0DoO5Ov2f7fjtYFDeDTGcdqPBKLHLmY4cSeTT3bVgPUJQGeR1NViZPSj;'
            # 'Cookie' : 'bm_s=YAAQC0IkFx8dzlqYAQAADsP7ZAM0YH6zxwB5DQAHgZUbgl1pUEJfKnBbfjtcnRpE+JnX4Ve9ZzNeNxh/Uj7s1QM5BJJSwkdlmD8IMx7azQPPOfxAbS3uK05LfYdhPMV4QVghYBrkLTqeXK16Z5tFf489bubKaZnUPiP/mk1O5wDXpuq3kgNxX5tPRlQUWYStzT0ZSivQtMo4yr4peiqds0NZhJ80rbOMp6spOfNc0EhC1vKlDaNshZ4ZbpA/bcbUfXi7ak4i5olmU+oV/yl/pTxrLGkVaA2VHRSHT6g99xiGT53QNpbHg+joEXOK36DGDLkonH+S/6Gq3E9T2ebISir3X8Sr8WYPQ8vzcVZZzY5ok2R+VMDJ8q1JszyiQ14CWDfPG1MpXOw6rG50uAmduPORq47z5I6OonEQOTAcLN3vcwfgRWRCQnC0wASUNnEborNQ/tUNhd2JW6cU5B92/4jmIPqRXVV5WncfdsTFVVJTbY8CU0I89VDBYC0jTcfYPTPWEutcnB1KfWlX7xY4x874oam1P3bkyIAT470AdVqtx/3rMCTf'
            # 'Cookie': 'bm_s=YAAQhInMF9a0N1qYAQAAA9ndZANuZiTzfMbAWanuaPxLKBMYg04YuEJsknSB881PQbhxuAQJGIvV306t9+gKJRdoULurK3tFtUhdue5wFn2zPYvwxU0N0iDjM65LxXyHGSWvewey4skjSJigcWWzITEb4PpeRux4IRcR4GUZ1Z4TI3TRcgysN59mtYdj7890TNA6GMrO5EoxiX164S0tTtGYT+UTTiHbR3oPikwlFvi9mmcYza3RvpOP2/M/aQh4pMdvzCNDvb4J2V8uGyHUfEwq8qdjYQ5ZDR6qPN4HFCPrd9dT7NjdcRy6iftCgkDOgpRMcMUWVOJDXixZO5GRhDNCmWqnAUUy02mtiku3E0C0EXQeSO0WSUXNptklcU+yvv3n0H61PbdqP6cNg9iry0r+nPcKlZ0asHkoASnuiRTWvs9uNzBijYLBUHQe0rjBmQJ2htBLIuZS1PiMeGPPc03s6BSZKYfZpGiZVZ13h8gWHXvNdUmWYWrFCPkIozGF1Y2R6KT0Y4IGxfU9QEuqm5TLikBksJ6tjWZswYGyYLdkpg4M1iBdYn77RT0l7vW4ZwNOUemiuw==;'
            # 'Cookie' : 'bm_s=YAAQHAEQAocMhyyYAQAAjkNVZQMP17pX9ia7yxK1LA79YmIH6QRLsvFaOoDT1P24nIEH1nt7TYi2yJWS6bXc8xzItlVQfUf6IT+ea7jBoWipMrTJdkfXe9gk23A28u2fHE5ngVu30/QqVF+WGquYxLJvryONciJoP36ByPftq0OpEKY4h57PX5rI8YlUk3hFXb59U4/7sbszVeSYr3OEveVU8d3cbFmNfvGclRe5Fn4fHCo4EQCrG0MkUW9BSCLD5R9sLSV2pj25rxkNGvwto7FnlMfvqRjyGmcZNMtKAf1N/Cf4vcwPgvaXk/kv387DR5DrAbAteFAa3Rqf5KiJZOIKIJLbKEAc9USR0qMaps6DAePU8geBLjdKsGmMImeZP0Fi06qtFh+66Hu47e5uFGmfjdBd/mzp9YsR6pWZNmgjU+2C0cZIc55MeaZJdPqnZ21zO+cu6teqa/IqZj8v/WhOxytBylDjAQDP8YyXmEXanUo0EnYbPXuYKoMadtLYDtrRa8lvmIwTeSkG+Pi+BhX8VI01E5lvc5TR74PwnizwnAL4NSE='
        },
        "payload": {
            "operationName": "RoomsAndRatesPropertyOffersQuery",
            "variables": {
                "propertyId": params["provider_id"],
                "searchCriteria": {
                    "primary": {
                        "dateRange": {
                            "checkInDate": {
                                "day": check_in_date.day,
                                "month": check_in_date.month,
                                "year": check_in_date.year,
                            },
                            "checkOutDate": {
                                "day": check_out_date.day,
                                "month": check_out_date.month,
                                "year": check_out_date.year,
                            },
                        },
                        "destination": {
                            "regionName": None,
                            "regionId": None,
                            "coordinates": None,
                            "pinnedPropertyId": None,
                            "propertyIds": None,
                            "mapBounds": None,
                        },
                        "rooms": [{"adults": 2, "children": []}],
                    },
                    "secondary": {
                        "counts": [],
                        "booleans": [],
                        "selections": [
                            {"id": "privacyTrackingState", "value": "CAN_NOT_TRACK"},
                            {"id": "searchId", "value": "be32e279-5b6f-4839-9ed6-b4f90a7024ea"},
                            {"id": "sort", "value": "RECOMMENDED"},
                            {"id": "useRewards", "value": "SHOP_WITHOUT_POINTS"},
                        ],
                        "ranges": [],
                    },
                },
                "shoppingContext": {"multiItem": None},
                "travelAdTrackingInfo": None,
                "context": {
                    "siteId": currency_changeable_data["siteId"],
                    "locale": currency_changeable_data["locale"],
                    "eapid": currency_changeable_data["eapid"],
                    "tpid": currency_changeable_data["tpid"],
                    "currency": currency,
                    "device": {"type": "DESKTOP"},
                    "identity": {"duaid": "bf2e8fd7-9639-4627-a771-4bf5f3333eb5", "authState": "ANONYMOUS"},
                    "privacyTrackingState": "CAN_NOT_TRACK",
                    "debugContext": {"abacusOverrides": []},
                },
            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "0c29b592f89c56e3ca69b787f406b01163a6fcb19c014cd71d7559fd72139704",
                }
            },
        },
    }
