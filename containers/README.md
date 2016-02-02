# container used to develop _Django Informer_

## tests

```
docker-compose run --rm application py.test tests
```

```
docker-compose run --rm legacy py.test tests
```

## flake

```
docker-compose run --rm application py.test tests informer --flake
```

## coverage

```
docker-compose run --rm application py.test tests --cov informer
```

### html report

```
docker-compose run --rm application py.test tests --cov-report html --cov informer
```

## _build_

### before built or run _development sample app_, you need get packages from UI

```
docker-compose run --rm node npm install
```

### and then build the package

```
docker-compose run --rm --no-deps application python setup.py sdist bdist_wheel
```
