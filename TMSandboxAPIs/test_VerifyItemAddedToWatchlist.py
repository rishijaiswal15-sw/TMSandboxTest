"""''
This test case authenticates the user from the start. It executes the entire OAUTH1 flow and then triggers the APIs.
APIs triggered are retrieve latest listings, add item to listing and retrieve wishlist.
Inputs needed are the consumer key, consumer secret, user name and password.

''"""

import logging
import requests

from TMSandboxAPIs.TM_RetrieveLatestListings import TM_RetrieveLatestListings
from TMSandboxAPIs.UserAuthentication import AuthenticationAccess

#Provide consumerKey, consumer Secret, user name and password in the below fields
def test_VerifyItemAddedToWatchlist():
    #Proivice the consumer key
    consumerKey = ''
    #Provide the consumer secret
    consumerSecret = ''
    #Provide TM username
    username = ''
    #Provide TM password
    password = ''
    accessScope = 'MyTradeMeRead,MyTradeMeWrite'
    retreiveWishlistURL = 'https://api.tmsandbox.co.nz/v1/MyTradeMe/Watchlist/All.json'

    header = AuthenticationAccess().authenticateUser(consumerKey, consumerSecret, username, password, accessScope)
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
    logging.info("Listing Id " + str(receivedListingId) + " is present in the wishlist")


