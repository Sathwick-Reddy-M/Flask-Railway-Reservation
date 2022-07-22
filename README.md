# Flask-Railway-Reservation
This Railway Reservation System helps users choose their favorite train seat anywhere on the train, unlike platforms that only allow a selection of preferences of the seat.


## API Endpoints
`/` - Displays the home page of the reservation system

`/signup` - Adds new users to the database and stores their encrypted version of the credentials in the database incorporating the OTP verification for the account activation.

`/login` - Login the user if the credentials entered match those in the database, and the user should activate the account.

`/logout` - Removes any user-related cookies (if present) or info stored and successfully logs out the user.

`/search` - Presents the user with a list of trains running between the source station and the destination station.

`/seats/<train_id>/<date_time>`- Presents the user with the compartment and seat layout of the train with id `<train_id>` on the date `<date_time>`.

`/details` - This is where the user the passenger details like name and age for the selected train seats.

`/otp` - OTP Verification
 
## Test Run Info
1. Clone the repository using `git clone https://github.com/Rockk-Star/Flask-Railway-Reservation.git`
2. Install all the packages mentioned in the `requirement.txt`
3. Insert the mail configuration details (`__init__.py`)
4. `python run.py` to start the flask application
5. SignUp using the `/signup` endpoint
6. Search Trains using the `/search` endpoint
7. Select the train name the check the seat availablity
8. Choose your favourite seats
9. Enjoy the ride 🚂

## Database Details
1. Includes `25` trains with IDs ranging from `17001` to `17025`
2. Each train name is a randomly generated string of length four ending with the word `Express`
3. The train includes a set of compartments. The compartment can be (`C1` with a capacity of `40`), (`C2` with a capacity of `40`), (`C3` with a capacity of `40`), (`C4` with a capacity of `40`), and (`C5` with a capacity of `40`).
4. Includes `50` stations whose names are `Station ` followed by a randomly generated strings of length `3`
5. Randomly generated routes between these `50` stations

**Train Names**


HLOI Express, XDHV Express, SRSF Express, LOYK Express, AAJH Express, QDIO Express, KQUE Express, AYTP Express, EKFU Express, FJBQ Express, FFRL Express, TAGQ Express, YUNO Express, NCAZ Express, YUYZ Express, EVOC Express, UATP Express, PVWI Express, GDGB Express, PAUF Express, TEZZ Express, EMRB Express, CELO Express, NVRR Express, LEAZ Express


**Station Names**


Station RIC, Station IZG, Station FGD, Station ZKT, Station XCU, Station HJR, Station MPQ, Station MKZ, Station BAE, Station ZQZ, Station IHZ, Station PUB, Station MMY, Station QZN, Station YEA, Station ESJ, Station DIX, Station EPP, Station ZTC, Station VRN, Station RZP, Station BES, Station AUB, Station YRE, Station GPO, Station PVG, Station ZMB, Station GSE, Station INX, Station WHD, Station KRM, Station DPV, Station WEQ, Station XZW, Station ERL, Station SCM, Station CWB, Station CBK, Station RMG, Station HHR, Station SVR, Station MUQ, Station ZPM, Station AZM, Station RHB, Station TBL, Station EZI, Station BBX, Station TFC, Station MYR

## Constraints for seat booking
Constraints are only functional till 5 hours before the train begins.
1. Age requirements must be satisfied for reserving a seat which may vary based on the seat position and type.

These constraints can be configured or even removed to suit different purposes.

### References

You can find the awsome CSS railway seat booking style sheet here - https://codepen.io/siiron/pen/MYXZWg
