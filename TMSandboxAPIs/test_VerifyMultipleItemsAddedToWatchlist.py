"""''
This test case authenticates the user from the start. It executes the entire OAUTH1 flow and then triggers the APIs.
APIs triggered are retrieve latest listings, add item to listing and retrieve wishlist.
This test adds multiple items to the wishlist and retrieves the wishlist and verifies if all items have been added successfully.
Inputs needed are the consumer key, consumer secret, user name and password and the total listings to add.
The limit is based on the total listings returned by the API.

''"""

import logging
import requests

from TMSandboxAPIs.TM_RetrieveLatestListings import TM_RetrieveLatestListings
from TMSandboxAPIs.UserAuthentication import AuthenticationAccess
from TMSandboxAPIs.UtilityClass import UtilityClass


def test_verifyItemsAddedToWatchlist():
    #Provide Consumer Key
    consumerKey = ''
    #Provide Consumer secret
    consumerSecret = ''
    #Provide TM username
    username = ''
    #Provide TM Password
    password = ''
    accessScope = 'MyTradeMeRead,MyTradeMeWrite'
    totalListingstoAdd = 5
    header = AuthenticationAccess().authenticateUser(consumerKey, consumerSecret, username, password, accessScope)
    #Retreive Latest Listings
    listings = TM_RetrieveLatestListings().getLatestListings(header, totalListingstoAdd)
    retreiveWishlistURL='https://api.tmsandbox.co.nz/v1/MyTradeMe/Watchlist/All.json'
    # To add multiple items to the wishlist
    for i in range(len(listings)):
        addListingURL = 'https://api.tmsandbox.co.nz/v1/MyTradeMe/Watchlist/' + str(listings[i]) + '.json'
        response = requests.request('POST', addListingURL, headers=header, data={})
        assert response.status_code == 200, 'Adding Item failed'
        logging.info(str(listings[i]) + ' Added successfully')

    # To retrieve and check if all items have been added
    count = 0
    response = requests.request('GET', retreiveWishlistURL, headers=header, data={})
    wishlistResponse = response.json()
    itemsWishlist = wishlistResponse['List']
    print(str(wishlistResponse['TotalCount']) + " Items present in the wishlist")

    for i in range(wishlistResponse['TotalCount']):
        response = UtilityClass().checkIfKeyExists(itemsWishlist, 'ListingId', listings[i])
        assert response, 'Item Not present'
        if response:
            count = count + 1
        else:
            continue
    assert count == totalListingstoAdd, 'Items not added successfully'