# cebulany-manager

# Build

```
python setup.py install
cd spa/
yarn run build
```

# Init 

```
alembic upgrade head
python create_mock.py > mock.csv
./uwsgi-me.sh
# login (socek, socek) and upload mock.csv in transaction view
```

# Run?

```
./uwsgi-me.sh
```
