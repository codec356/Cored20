from django.shortcuts import render

from core.models import Auction


def auction_board(request):
    auctions = Auction.objects.all()
    return render(request=request, template_name='auction/auction_board.html', context={
        'auctions': auctions
    })