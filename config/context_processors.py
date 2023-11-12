from thinking_feedback import settings


def dev_processor(request):
    dev = settings.DEV
    return {'dev': dev}
