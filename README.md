# cebulany-manager

# Build

```
virtualenv venv3 -p python3.7
source venv3.7/bin/activate

python setup.py install
cd spa/
yarn install
yarn run build
```

to run front-end in developming mode
```
yarn run dev
```

# Init 

```
# in root
alembic upgrade head
python create_mock.py > mock.csv
./uwsgi-me.sh
# login (socek, socek) and upload mock.csv in transaction view
```

# Run?

```
./uwsgi-me.sh
```
