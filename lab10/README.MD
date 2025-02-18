# Lab 10

## Usage

1. `sudo cp flaskapi /etc/nginx/sites-available/`
2. `sudo ln -s /etc/nginx/sites-available/flaskapi /etc/nginx/sites-enabled/`
3. `sudo nginx -t`
4. `sudo systemctl reload nginx`
5. `python app.py`
6. Open [localhost:8080/api/](http://localhost:8080/api/)
