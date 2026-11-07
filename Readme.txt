Little Lemon • API guide for peer reviewers

Start the server using README.md. In Insomnia, use http://127.0.0.1:8000 as
the base URL. Set body type to JSON for POST, PUT and PATCH requests.

1. Create a local reviewer account
   POST /auth/users/
   {"username":"reviewer","password":"Choose-A-Local-Password-7021"}

2. Obtain a token
   POST /auth/token/login/
   Send the same username and password. Copy auth_token from the response.
   For the remaining API requests set the header:
   Authorization: Token YOUR_TOKEN

3. Test the menu
   GET    /restaurant/menu/items/          List dishes
   POST   /restaurant/menu/items/          Create a dish
   {"title":"Greek salad","price":"12.50","inventory":8}

   Use the id returned by POST in place of <id>.
   GET    /restaurant/menu/items/<id>/     Read one dish
   PUT    /restaurant/menu/items/<id>/     Replace all editable fields
   PATCH  /restaurant/menu/items/<id>/     Change selected fields
   {"inventory":5}
   DELETE /restaurant/menu/items/<id>/     Remove the dish

4. Test table bookings
   GET    /restaurant/booking/tables/      List bookings
   POST   /restaurant/booking/tables/      Create a booking
   {"name":"Alex","no_of_guests":2,"booking_date":"2030-08-15T18:00:00Z"}

   GET    /restaurant/booking/tables/<id>/     Read one booking
   PUT    /restaurant/booking/tables/<id>/     Replace all editable fields
   PATCH  /restaurant/booking/tables/<id>/     Change selected fields
   {"no_of_guests":4}
   DELETE /restaurant/booking/tables/<id>/     Cancel the booking

5. End the session
   POST /auth/token/logout/ with the Authorization header. Reusing the
   revoked token returns 401. The bookings and menu endpoints also return
   401 for anonymous requests.

Successful creates return 201. Successful reads and updates return 200.
Successful deletes return 204. Try a negative price or a zero guest count
to see a 400 validation response. Prices have two decimal places and dates
use ISO 8601 with a timezone.

Other paths
   GET  /                         Restaurant homepage
   GET  /restaurant/              Restaurant homepage
   GET  /auth/users/me/           Current user (requires authentication)
   POST /api-token-auth/          Alternate DRF login; response key: token
