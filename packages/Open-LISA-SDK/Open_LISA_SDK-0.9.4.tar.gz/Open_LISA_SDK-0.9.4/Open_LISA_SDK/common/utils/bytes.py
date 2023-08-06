KB = 1024
MB = KB * 1024


def format_bytes(number):
    if number < KB:
        return "{} bytes".format((number))
    elif number >= KB and number < MB:
        return "{:.2f} KB".format((number / KB))
    elif number >= MB:
        return "{:.2f} MB".format((number / MB))
