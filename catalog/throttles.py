from rest_framework.throttling import UserRateThrottle


class TwentyCallsPerMinute(UserRateThrottle):
    scope = 'twenty_per_minute'
