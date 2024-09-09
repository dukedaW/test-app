from app import app, db
import product
import purchase
import index
import buyer
import report


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
