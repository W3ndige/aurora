# Aurora

![Linting](https://github.com/W3ndige/aurora/actions/workflows/lint.yml/badge.svg?branch=master) ![Testing](https://github.com/W3ndige/aurora/actions/workflows/test.yml/badge.svg?branch=master)


Automated malware similarity platform with modularity in mind.

![Aurora preview](docs/source/_static/aurora-preview.gif)

## Usage

### Essential services

Remember, that aurora uses a number of services running under a hood. 

* [PostgreSQL](https://www.postgresql.org/) for a database.
* [Karton](https://github.com/CERT-Polska/karton) for backend pipeline.
    * [Redis](https://redis.io/) for Karton.
    * [Minio](https://docs.min.io) for Karton.

In order to set up Karton, please see the [Karton documentation](https://karton-core.readthedocs.io), which gives a great
head start into how Karton ecosystem works and how you can easily write new karton for different similarity tasks.

### Configuration

Rename the `.env.template` file to `.env` and fill the blank values.

### Manual installation

Make sure that `libmagic` and `libfuzzy` libraries are installed.

For Ubuntu:

```
apt-get install -y libmagic-dev libfuzzy-dev libfuzzy2
```

For Arch Linux:

```
pacman -S ssdeep
```

Install `aurora` package.

```yaml
pip install .
```

Start the server.

```
uvicorn aurora.app
```

### Docker installation

In addition, you can use both Docker image and Docker Compose to quickly setup full environment.

```
docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up
```

## License

This software is licensed under 
This software is licensed under [GNU Affero General Public License version 3](http://www.gnu.org/licenses/agpl-3.0.html) except for kartons.


For more information, read [LICENSE](LICENSE) file.
