from reservation import app
from reservation.db import db
from reservation.pwd import bcrypt
from reservation.mail import mail

if __name__ == '__main__':
    bcrypt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    app.run(debug=True)
