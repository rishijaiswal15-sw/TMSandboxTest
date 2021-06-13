"""''
This test is for adding an item to the wishlist for a user that has been authenticated prior.
A pre-requisite is that the user has granted the required privileges to the application to make changes,
APIs triggered are retrieve latest listings, add item to listing and retrieve wishlist.
Inputs needed are the consumer key, consumer secret, oauth access token and oauth token secret

''"""

import logging
import requests
import pytest

from TMSandboxAPIs.TM_RetrieveLatestListings import TM_RetrieveLatestListings
from TMSandboxAPIs.UserAuthentication import AuthenticationAccess

@pytest.mark.xfail
def test_VerifyItemAddedToWatchlist():
    #Provide consumer key
    consumerKey = ''
    # Provide consumer secret
    consumerSecret = ''
    #Provide access token
    oauthToken = ''
    #Provide access secret
    oauthTokenSecret = ''

    retreiveWishlistURL = 'https://api.tmsandbox.co.nz/v1/MyTradeMe/Watchlist/All.json'

    header = AuthenticationAccess().generateAccessHeader(consumerKey, consumerSecret, oauthToken, oauthTokenSecret)
    logging.info(str(header))
    listings = TM_RetrieveLatestListings().getLatestListings(header, 1)
    listingId = listings[0]
    logging.info("Latest Listings: " + str(listingId))
    addListingURL = 'https://api.tmsandbox.co.nz/v1/MyTradeMe/Watchlist/' + str(listingId) + '.json'
    response = requests.request('POST', addListingURL, headers=header, data={})
    logging.info("Response from adding item to wishlist: " + str(response.json()))
    assert response.status_code == 200, 'Unsuccessful in adding to wishlist'
    response = requests.request('GET', retreiveWishlistURL, headers=header, data={})
    logging.info(str(response.json()))
    logging.info("Status code of retrieve wishlist: " + str(response.status_code))
    assert response.status_code == 200
    responseJSON = response.json()
    wishlist = responseJSON['List']
    receivedListingId = wishlist[0]['ListingId']
    logging.info('Received Listing id from wishlist: ' + str(receivedListingId))
    assert listingId == receivedListingId, 'Not Present'


