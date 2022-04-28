# Playground API

See [tutorial](https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-1-hello-world/) and [repo](https://github.com/ChristopherGS/ultimate-fastapi-tutorial) for detailed instructions.  
Progress: Lesson 7 (database) is done, _without_ `poetry`.  
API docs URL: http://127.0.0.1/docs

# Setup and start

Let db start:
```
python ./little_api/backend_pre_start.py
```

Run migrations:
```
alembic upgrade head
```

Create initial data:
```
python ./little_api/initial_data.py
```

Check db:

```
sqlite3 example.db
> .tables
> SELECT * FROM cats;
> .exit
```

Start app:
```
python ./little_api/app.py
```