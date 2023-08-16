# Marvel Challenge

## To obtain the information about all other characters Spectrum worked with in other comics:

### Build and tag the docker image:
```bash
docker build . -t marvel_challenge
```

### Run the image, which will automatically execut the script retrieving the desired information
```bash
docker run -it --rm --name marvel_container --env API_KEY=<marvel api key> --env API_SECRET=<marvel api secret> --env DB_USER=<db user> --env DB_PASS=<db pass> marvel_challenge
```

For security purposes, the keys to access to the DB and the Marvel API have been redacted, and can be provided separetely.

### Notes:
The part of the script responsible for creating the characters table and inserting data into it has been commented out, to avoid duplicating the entries if the script is run again.
The data has already been loaded in the DB and can be checked by connecting to it `rajje.db.elephantsql.com/jwzkbace`
