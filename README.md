# TMSandboxTest
The project has been coded in Python. To run the scripts the following modules, need to be installed:
1.	Pytest
2.	Requests
3.	Selenium
4.	Pytest-html
Conftest.py contains the basic configurations like setting the log levels and generating the report title.
UserAuthentication.py contains the authorization and authentication flow for a user. The entire OAUTH1 flow is automated via this class.
The following test scripts are present in the project:
1.	Test_VerifyCategoriesList.py: It retrieves the categories and verifies the count and if the specified category is present in the response.
2.	Test_VerifyItemAddedToWatchlist.py: It retrieves the latest listings and adds one listing to the user’s wishlist. It then verifies by querying the user’s wishlist and checking if the listing was added. This flow starts from authorization and authentication to verifying the end-to-end flow of adding items to the wishlist and verifying if the items were successfully added.
3.	Test_VerifyMultipleItemsAddedToWatchlist: It retrieves the latest listings and adds the specified number of listings to the user’s wishlist. It then queries the wishlist and verifies if all the items were added to the wishlist. This flow starts from authorization and authentication to verifying the end-to-end flow of adding items to the wishlist and verifying if the items were successfully added.
4.	Test_VerifyItemAddedToAuthenticatedUser: A pre-requisite to executing this test case is that the user must be authenticated prior to executing the scenario and must be in possession of the access token required for authorization purposes. It then retrieves the latest listing and adds it to the wishlist and verifies if the item was added successfully to the wishlist.
