# container used to develop _Django Informer_

## tests

```
docker-compose run --rm application py.test tests
```

## coverage

```
docker-compose run --rm application py.test --cov informer
```

### html report

```
docker-compose run --rm application py.test --cov-report html --cov informer
```

## flake

```
docker-compose run --rm application py.test informer --flake
```

## _build_

```
docker-compose run --rm application python setup.py sdist bdist_wheel
```
