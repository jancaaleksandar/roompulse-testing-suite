from hotel_info_lib import ProcessRequestParsingTask

def get_booking_cookie(task : ProcessRequestParsingTask) -> str:
    if str(task.task__parsing_price_variables_rates_type) == "PUBLIC":
        return "uz=e;bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLb9qg0InA%2FFDc0pyKTkeznOVuVClFtKe622j3ZMY2LtA%2BhW1BFrjfmOfFF%2FX8pvC%2BPo8Z56aTafulKESi8bSOgtnFYhJvto4gGq%2FuV0k2kS3NiXBfxOUUuFwbiqFwDH6tOKOJHaPTqsKrPJFUIRkY8YnCvwO0W97mnF6oNHdNpgaEYfVFz7mx93S53EuoofhF0Ed3ioZ3mGBQzJa4MzNVP7Q%3D%3D; domain=.booking.com; path=/; expires=Tue, 03-Jul-2029 15:10:49 GMT; Secure; HTTPOnly; SameSite=None"
    else:
        return "bkng_sso_auth=CAIQsOnuTRqKAYQrLi0pkYcX82Q1TqFjWOfKt6jHjF35tvg/sXXSn/2VD7aTphHj2pVDFJrPDD83sS2fJklXbckFMErs5dEbCjNXpru5fQvrIq5Ej+qrXSkF3LWbOvINpbOXghQtzzNpJRysIaYMy/pkIow7mV09LBH2MNYiWPUa+0Xo3Y9gyUUwI0Rapv3QkF/k1w==;"