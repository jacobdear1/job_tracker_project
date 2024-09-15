To deploy locally: '' uvicorn app.main:app --reload ''


create a .env file with the location to your database, i used sqlite and set this equal to DATABASE_URL and then generate a sercet key as set out below: 


generate a secret key using the python secrets module; python -c "import secrets; print(secrets.token_urlsafe(32))"
 
 this generates a secret key that you will need to replace your_secret_key in .env with. 