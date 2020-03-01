import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.forms.auction.forms import AuctionCreationForm
from core.models import Auction, AuctionBets


def auction_board(request):
    auctions = Auction.objects.all().order_by('dt_expiration')
    return render(request=request, template_name='auction/auction_board.html', context={
        'auctions': auctions,
    })


def create_auction(request):
    if request.POST:
        form = AuctionCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:auction')
    else:
        form = AuctionCreationForm(initial={
            'user': request.user
        })
    return render(request=request, template_name='auction/create_auction.html', context={
        'form': form
    })


def create_bet_iframe(request, auction):
    if request.POST:
        res = AuctionBets.objects.create(auction_id=int(request.POST.get('auction')),
                                         amount=int(request.POST.get('amount')),
                                         user=request.user).save()
        print(res)
        auction = Auction.objects.get(id=int(request.POST.get('auction')))
        return HttpResponse(json.dumps(res),
                            content_type='application/json')
    else:
        auction = Auction.objects.get(id=auction)
    return render(request=request, template_name='auction/bet_iframe.html', context={
        "auction": auction
    })


def get_auction_history(request, auction):
    bets = AuctionBets.objects.filter(auction=auction).order_by('-dt_created')
    return render(request=request, template_name='auction/history_iframe.html', context={
        'bets': bets
    })
