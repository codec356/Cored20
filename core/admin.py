from django.contrib import admin

from core.models import *

admin.site.register(Towns)
admin.site.register(Regions)
admin.site.register(Category)


admin.site.register(Balances)
admin.site.register(BalanceType)
admin.site.register(BalanceMovements)

admin.site.register(LevelMap)


admin.site.register(RateType)
admin.site.register(OfferReviewRates)
admin.site.register(OfferReviews)

admin.site.register(SectionType)
admin.site.register(Topic)
admin.site.register(Section)


admin.site.register(ResortType)
admin.site.register(Resort)
admin.site.register(ResortMessages)
