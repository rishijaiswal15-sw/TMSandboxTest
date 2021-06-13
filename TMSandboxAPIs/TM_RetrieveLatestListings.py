"""''
This class triggers the retrieve latest listings API and returns the latest listings based on the requirements.
The default value to return is 1.
Parameters required for getLatestListings is the authorization header and the number of listings to be returned.

''"""
import requests
import logging

class TM_RetrieveLatestListings:
    def getLatestListings(self, header, countToReturn=1):
        #log = logging.getLogger()
        #log.setLevel(logging.INFO)

        baseURL = 'https://api.tmsandbox.co.nz/v1/Listings/Latest.json'
        response = requests.request('GET', baseURL, headers=header, data={})

        if response.status_code != 200:
            logging.info(str(response.text))
        assert response.status_code == 200, "Error received in Response. Please check logs"
        responseJson = response.json()
        listingList = responseJson['List']
        listings = [''] * countToReturn
        for i in range(countToReturn):
            listings[i] = listingList[i]['ListingId']

        return listings
