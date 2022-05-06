# Project name

[![GitHub contributors][ico-contributors]][link-contributors]
[![GitHub last commit][ico-last-commit]][link-last-commit]
[![License: MPL 2.0][ico-license]][link-license]

The project takes a request containing a list of urls, downloads the content of the urls, zips those files and uploads them to the cloud.

[Contributing](#contributing) | [Built With](#built-with) | [Development](#development) | [Feedback](#feedback) | [License](#license) | [About Code for Romania](#about-code-for-romania)

## Contributing

This project is built by amazing volunteers, and you can be one of them! Here's a list of ways in [which you can contribute to this project][link-contributing]. If you want to make any change to this repository, please **make a fork first**.

If you would like to suggest new functionality, open an Issue and mark it as a **[Feature request]**. Please be specific about why you think this functionality will be of use. If you can, please include some visual description of what you would like the UI to look like, if you are proposing new UI elements.

## Built With

### Programming languages

* [Python 3.10](https://www.python.org)

### Frameworks

* [FastAPI](https://fastapi.tiangolo.com/)
* [Google Cloud Storage](https://cloud.google.com/storage/)

### Package managers

* [pip](https://pip.pypa.io/) & [pip-tools](https://pip-tools.readthedocs.io/en/latest/)

## Development

### Starting the project using docker

The easiest way is to use Docker and Docker Compose.
To start the project locally with the hot-reload functionality, run the following command:

```shell
ENVIRONMENT=development docker-compose up -d --build
```

To start the project in the production mode, run the following command:

```shell
ENVIRONMENT=production docker-compose up -d --build
```

You can also pass the `API_PORT` environment variable to the command to change the exposed port.
By default, the port is set to `8123`.

### Starting the project without docker

0. Create a virtual environment for your project.
1. Install the dependencies using pip.

    ```shell
    # to install the dev dependencies run:
    pip install -r requirements-dev.txt
    ```

2. From the root of the project, start it using the following command:

    ```shell
    uvicorn app.main:app --host 0.0.0.0 --port 8123 --reload
    ```

### Navigating the project

* [localhost:8123](http://localhost:8123) - the default address of the project
* [localhost:8123/zip-docs](http://localhost:8123/zip-docs) - the address where you can send a POST with the data to be zipped
* [localhost:8123/docs](http://localhost:8123/docs) - Swagger docs
* [localhost:8123/redoc](http://localhost:8123/redoc) - ReDoc docs

### Sending a POST request

The request should contain:

* a list of URLs with the files that should be zipped
* a link where the zip will be uploaded to
* a URL where a POST with the notification will be sent

```json
{
    "urls": [
        "https://storage.example.com/file_link_1",
        "https://storage.example.com/file_link_2"
    ],
    "path": "https://storage.example.com/file_destination.zip",
    "webhook": {
        "url": "https://notification.example.com/api/webhook",
        "data": {
            "sample_data": "some_data"
        }
    }
}
```

### Updating the requirements

1. Add the new dependencies to the `requirements.in` or `requirements-dev.in` file.
1. Run `make requirements-build` to update the requirements.

:warning:
Do not manually add requirements to the `*.txt` files since they are auto-generated.
`*.txt` files should only be edited if a sub-dependency should be updated and updating the `*.in` file is not possible.

## Feedback

* Request a new feature on GitHub.
* Vote for popular feature requests.
* File a bug in GitHub Issues.
* Email us with other feedback contact@code4.ro

## License

This project is licensed under the MPL 2.0 License - see the [LICENSE](LICENSE) file for details

## About Code for Romania

Started in 2016, Code for Romania is a civic tech NGO, official member of the Code for All network. We have a community of around 2.000 volunteers (developers, UX/UI, communications, data scientists, graphic designers, devops, IT security and more) who work pro bono for developing digital solutions to solve social problems. #techforsocialgood. If you want to learn more details about our projects [visit our site][link-code4] or if you want to talk to one of our staff members, please e-mail us at contact@code4.ro.

Last, but not least, we rely on donations to ensure the infrastructure, logistics and management of our community that is widely spread across 11 timezones, coding for social change to make Romania and the world a better place. If you want to support us, [you can do it here][link-donate].

[ico-contributors]: https://img.shields.io/github/contributors/code4romania/redirectioneaza-zipping.svg?style=for-the-badge
[ico-last-commit]: https://img.shields.io/github/last-commit/code4romania/redirectioneaza-zipping.svg?style=for-the-badge
[ico-license]: https://img.shields.io/badge/license-MPL%202.0-brightgreen.svg?style=for-the-badge

[link-contributors]: https://github.com/code4romania/redirectioneaza-zipping/graphs/contributors
[link-last-commit]: https://github.com/code4romania/redirectioneaza-zipping/commits/main
[link-license]: https://opensource.org/licenses/MPL-2.0
[link-contributing]: https://github.com/code4romania/.github/blob/main/CONTRIBUTING.md

[link-code4]: https://www.code4.ro/en/
[link-donate]: https://code4.ro/en/donate/
