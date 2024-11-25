# Balneabilidade Backend

## Requirements

- Docker and Docker compose
- API Key from [OpenWeather](https://home.openweathermap.org/api_keys)

## Run the project

- Run `make build`
- Create a .env file based on the .env.EXAMPLE file and input the secrets.
- Run `make migrate && make createsuperuser` to initialize the database and create the superuser.
- Run `make up` to start the project. It will be available at `http://localhost:8000`
- In the admin area `http://localhost:8000/admin/` create a country, state and city, some locations and a API Key (don't forget to store it safely) to allow API access.

## Recommended infrastructure actions

- Use [Vercel](https://vercel.com) to host this app and to provide a Redis DB.
- Use [Supabase](https://supabase.com/) for a free database (use the transaction port 5432 instead of the pooler port 6543).
- Use [Val Town](https://www.val.town) to manage cronjobs (located in `./cronjob_scripts`) that will update the Weather and Locations (Celery Beat is an option, but it's not possible to do it in Vercel)

## Documentation

### Entity-relationship diagram

![Entity-relationship diagram](./docs/erd_balneabilidade.png)

### Infrastructure

![Infrastructure](./docs/balneabilidade_infra.png)

### Postman Collection

[Postman Collection Schema](./docs/Balneabilidade.postman_collection.json)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
