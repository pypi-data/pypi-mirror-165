import datetime
import decimal
import json
import logging
import os
import re
import uuid
from asyncio import Future
from typing import Awaitable, Optional, Union
import ddtrace

from simple_api_framework.monitors import DataDogMonitor

if os.getenv("DD_SERVICE") and os.getenv("DD_API_KEY") and os.getenv("DD_API_KEY") and os.getenv("DD_ENV"):
    ddtrace.patch(tornado=True)
    ddtrace.patch(logging=True)
    if os.getenv("REDIS_URL"):
        ddtrace.patch(aioredis=True)
    if os.getenv("DB_URL"):
        ddtrace.patch(aiopg=True)

import dotenv
import magic
import sentry_sdk
from sentry_sdk.integrations.tornado import TornadoIntegration
from tornado import web, ioloop, escape
from tornado.log import enable_pretty_logging

from simple_api_framework.db.mongo import MongoDB
from simple_api_framework.redis import Redis


def setup_logging():
    logger = logging
    enable_pretty_logging()
    return logger


class ValidationException(Exception):
    field = None
    message = None

    def __init__(self, **kwargs):
        for attribute in kwargs.keys():
            if hasattr(self, attribute):
                setattr(self, attribute, kwargs.get(attribute))
        super().__init__()


class ManyValidationExceptions(Exception):
    exceptions = None

    def __init__(self, **kwargs):
        for attribute in kwargs.keys():
            if hasattr(self, attribute):
                setattr(self, attribute, kwargs.get(attribute))
        super().__init__()


class NotFoundHandler(web.RequestHandler):
    MESSAGE = {
        'title': 'Not Found',
        'status': 404,
    }

    async def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def get(self):
        self.MESSAGE['instance'] = self.request.path
        self.set_header('Content-type', 'application/problem+json')
        self.set_status(404)
        return self.finish(self.MESSAGE)

    async def post(self):
        self.MESSAGE['instance'] = self.request.path
        self.set_header('Content-type', 'application/problem+json')
        self.set_status(404)
        return self.finish(self.MESSAGE)

    async def put(self):
        self.MESSAGE['instance'] = self.request.path
        self.set_header('Content-type', 'application/problem+json')
        self.set_status(404)
        return self.finish(self.MESSAGE)

    async def patch(self):
        self.MESSAGE['instance'] = self.request.path
        self.set_header('Content-type', 'application/problem+json')
        self.set_status(404)
        return self.finish(self.MESSAGE)

    async def delete(self):
        self.MESSAGE['instance'] = self.request.path
        self.set_header('Content-type', 'application/problem+json')
        self.set_status(404)
        return self.finish(self.MESSAGE)

    async def options(self):
        self.MESSAGE['instance'] = self.request.path
        self.set_header('Content-type', 'application/problem+json')
        self.set_status(404)
        return self.finish(self.MESSAGE)


class Service(web.Application):
    WORKING_DIRECTORY = os.path.dirname(os.path.realpath(__file__)) + '/../'
    NAME = None
    ENVIRONMENT = None

    redis = None
    mongo = None
    monitor = None

    def __init__(self, **kwargs):
        dotenv.load_dotenv(override=True)
        self.logging = setup_logging()
        self.io_loop = ioloop.IOLoop.instance()
        self.ENVIRONMENT = os.getenv('ENV')

        queues = kwargs.get('queues', [])

        urls = kwargs.get('urls')
        if urls:
            if not isinstance(urls, list):
                raise TypeError('Variable "urls" must be a list')
            for url in urls:
                if not isinstance(url, dict):
                    raise TypeError('All items in "urls" must be a dictionaries')

        if not hasattr(self, 'NAME') or not self.NAME:
            raise ValueError('No NAME attribute')

        version = os.getenv("API_VERSION", 1)

        url_prefix = f'/api/v{version}/{self.NAME.lower()}'
        uuid_format = "([a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})"

        urls.append({'url': 'ping', 'handler': HealthCheckEndpoint})

        handlers = []
        for url in urls:
            uri = url.get('url')
            if '{uuid}' in uri:
                uri = uri.format(uuid=uuid_format)
            if not url.get('without_prefix'):
                handlers.append(web.url(re.compile(f'{url_prefix}/{uri}(/.*)?$'), url.get("handler")))
            else:
                handlers.append(web.url(re.compile(f'{uri}$'), url.get('handler')))

        del kwargs['urls']

        if kwargs.get('static'):
            static = kwargs.get('static')
            handlers.append(
                (
                    f"{url_prefix}/{static.get('url')}",
                    web.StaticFileHandler,
                    {'path': f"{self.WORKING_DIRECTORY}{static.get('path')}"})
            )
            del kwargs['static']

        handlers.append((r"/.*", NotFoundHandler))

        super().__init__(handlers=handlers, debug=True if self.ENVIRONMENT in ['local', 'dev'] else False,
                         xsrf_cookies=False, logging=self.logging, **kwargs)

        if os.getenv("REDIS_URL"):
            self.logging.info("[PLUGINS] Redis enabled")
            self.redis = Redis(prefix=os.getenv("REDIS_PREFIX"), url=os.getenv("REDIS_URL"))

        if os.getenv("MONGODB_URL"):
            self.logging.info("[PLUGINS] MongoDB enabled")
            self.mongo = MongoDB(url=os.getenv("MONGODB_URL"))

        if os.getenv('SENTRY_DSN_URL'):
            self.logging.info("[PLUGINS] Sentry enabled")
            sentry_sdk.init(
                dsn=os.getenv('SENTRY_DSN_URL'),
                environment=self.ENVIRONMENT,
                integrations=[
                    TornadoIntegration(),
                ],
                traces_sample_rate=1.0,
                release=f"{self.SERVICE_NAME}@{os.getenv('GITLAB_COMMIT')}" if os.getenv('GITLAB_COMMIT') else None,
            )

        if os.getenv("DD_SERVICE") and os.getenv("DD_API_KEY") and os.getenv("DD_API_KEY") and os.getenv("DD_ENV"):
            self.logging.info(
                f"[PLUGINS] DataDog enabled (service: {os.getenv('DD_SERVICE')}, env: {os.getenv('DD_ENV')})"
            )
            self.monitor = DataDogMonitor(
                host=os.getenv("DD_HOST", '127.0.0.1'),
                service=os.getenv("DD_SERVICE"),
                env=os.getenv("DD_ENV"),
                api_key=os.getenv("DD_API_KEY"),
                app_key=os.getenv("DD_APP_KEY"),
            )

        host = os.getenv('SERVICE_HOST', '0.0.0.0')
        if not kwargs.get('bind_port'):
            try:
                port = int(os.getenv('SERVICE_PORT', 50000))
            except (ValueError, TypeError):
                port = 50000
        else:
            port = kwargs.get('bind_port')

        self.logging.info(f"Starting {self.NAME.capitalize()} service on [{host}:{port}]")
        self.listen(address=host, port=port)
        for queue in queues:
            self.io_loop.add_callback(queue)
        try:
            self.io_loop.start()
        except KeyboardInterrupt:
            self.logging.info(f"Service {self.NAME.capitalize()} stopped")
            exit(0)


class Endpoint(web.RequestHandler):
    WORKING_DIRECTORY = None
    ENVIRONMENT = None

    logging = None
    redis = None
    mongo = None
    monitor = None

    def initialize(self):
        self.logging = self.application.logging
        self.WORKING_DIRECTORY = self.application.WORKING_DIRECTORY
        self.ENVIRONMENT = self.application.ENVIRONMENT
        self.redis = self.application.redis
        self.mongo = self.application.mongo
        self.monitor = self.application.monitor

    def set_default_headers(self) -> None:
        if os.getenv("CORS_ENABLED"):
            if os.getenv("CORS_ALLOWED_ORIGINS") == '*':
                self.set_header("Access-Control-Allow-Origin", "*")
            elif os.getenv("CORS_ALLOWED_ORIGINS"):
                allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS").split(',')
                if self.request.headers.get('origin') in allowed_origins:
                    self.set_header("Access-Control-Allow-Origin", self.request.headers.get('origin'))

            self.set_header("Access-Control-Allow-Headers", "Content-Type, Depth, User-Agent, X-File-Size, "
                                                            "X-Requested-With, X-Requested-By, If-Modified-Since, "
                                                            "X-File-Name, Cache-Control, Authorization")
            if hasattr(self, 'methods') and isinstance(self.methods, list):
                self.methods.append('OPTIONS')
                self.set_header('Access-Control-Allow-Methods', ', '.join(self.methods))

    @property
    def user_ip(self):
        ip = self.request.headers.get('X-Real-Ip')
        if not ip:
            ip = self.request.remote_ip
        return ip

    @property
    def user_agent(self):
        return self.request.headers.get('User-Agent')

    @property
    def hostname(self):
        host = self.request.headers.get('origin')
        if not host:
            host = self.request.host

        if host:
            host = host.replace('https', '').replace('http', '').replace('://', '')
            if ':' in host:
                host = host.split(':')[0]
            return host
        return None

    @property
    def current_page(self):
        try:
            page = int(self.get_argument('page', 1)) - 1
        except ValueError:
            page = 0
        return page

    @property
    def pagination(self):
        limit = os.getenv("DB_RESULTS_LIMIT", 20)
        return {'limit': limit, 'offset': self.current_page * limit}

    def finish_with_error(self, status_code, code=None, fields=None):
        title = 'Unknown error'
        if status_code == 500:
            title = 'Internal Server Error'
        elif status_code == 400:
            title = 'Bad Request'
        elif status_code == 401:
            title = 'Unauthorized'
        elif status_code == 403:
            title = 'Forbidden'
        elif status_code == 404:
            title = 'Not Found'
        elif status_code == 405:
            title = 'Method Not Allowed'

        message = {
            'title': title,
            'status': status_code,
            'instance': self.request.path,
        }

        if code:
            message['code'] = code

        if fields:
            message['fields'] = fields

        self.set_header('Content-type', 'application/problem+json')
        self.set_status(status_code)
        return self.finish(message)

    def finish_with_pagination(self, result, total_count=0, parameters=None, limit=None):
        try:
            page = int(self.get_argument('page', 1)) - 1
        except ValueError:
            page = -1

        if limit is None:
            limit = os.getenv("DB_RESULTS_LIMIT", 20)

        count = 0
        pages = 0
        next_page = None
        prev_page = None
        if limit and len(result) and page >= 0 and total_count:
            count = total_count
            pages = int(count / limit)
            if count % limit != 0:
                pages += 1

            request_url = self.request.path
            if request_url[-1] != '/':
                request_url += '/'

            if (page + 1) < pages:
                next_page = f"{request_url}?page={page + 2}"
            if page > 0:
                prev_page = f"{request_url}?page={page}"

        if parameters:
            for name, value in parameters.items():
                if value:
                    if next_page:
                        next_page += f"&{name}={value}"
                    if prev_page:
                        prev_page += f"&{name}={value}"

        for i, s in enumerate(result):
            if isinstance(s, dict):
                for key, value in s.items():
                    if isinstance(value, datetime.date):
                        s[key] = value.strftime("%Y-%m-%d")
                    if isinstance(value, decimal.Decimal):
                        s[key] = float(value)
                continue
            result[i] = s.frontend

        return self.finish({
            'status': 200,
            'title': 'OK',
            'count': count if count else len(result),
            'size': limit if total_count else 0,
            'pages': pages,
            'next': next_page,
            'previous': prev_page,
            'results': result,
        })

    def finish_with_ok_status(self):
        self.set_header('Content-type', 'application/json')
        self.set_status(200)
        return self.finish({'ok': True})

    def finish(self, chunk: Optional[Union[str, bytes, dict]] = None) -> "Future[None]":
        if hasattr(chunk, 'frontend'):
            chunk = chunk.frontend
        elif isinstance(chunk, list):
            result = {'data': []}
            for row in chunk:
                if hasattr(row, 'frontend'):
                    result['data'].append(row.frontend)
                else:
                    result['data'].append(row)
            chunk = result
        return super().finish(chunk)

    def get_argument(self, name: str, default=None, strip: bool = True, argument_type=None, required: bool = False,
                     process=None, possible_values=None, validation=None, fields=None, argument_format=None):
        try:
            json_data = escape.json_decode(self.request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            json_data = {}

        result = None

        if json_data.get(name) is not None:
            if str(json_data.get(name)).lower() == 'true':
                result = True
            elif str(json_data.get(name)).lower() == 'false':
                result = False
            else:
                result = json_data.get(name)
        elif super().get_argument(name, None) is not None:
            value = super().get_argument(name)
            if str(value).lower() == 'true':
                result = True
            elif str(value).lower() == 'false':
                result = False
            else:
                result = value

        if required:
            if result is None:
                raise ValidationException(field=name, message="Field is required")

        if result is not None and argument_type:
            if argument_type == int:
                try:
                    result = int(result)
                except (TypeError, ValueError, AttributeError):
                    raise ValidationException(field=name, message="Invalid numeric value")
            elif argument_type == float:
                try:
                    result = float(result)
                except (TypeError, ValueError, AttributeError):
                    raise ValidationException(field=name, message="Invalid decimal value")
            elif argument_type == str:
                try:
                    result = str(result)
                except (TypeError, ValueError, AttributeError):
                    raise ValidationException(field=name, message="Invalid string")
            elif argument_type == datetime.datetime:
                try:
                    if not argument_format:
                        argument_format = '%Y-%m-%dT%H:%M:%SZ%z'
                    result = datetime.datetime.strptime(result, argument_format)
                except (TypeError, ValueError, AttributeError):
                    raise ValidationException(field=name, message="Invalid datetime value")
            elif argument_type == datetime.date:
                try:
                    if not argument_format:
                        argument_format = '%Y-%m-%d'
                    result = datetime.datetime.strptime(result, argument_format).date()
                except (TypeError, ValueError, AttributeError):
                    raise ValidationException(field=name, message="Invalid date value")
            elif argument_type == list and not isinstance(result, list):
                raise ValidationException(field=name, message="Invalid array value")
            elif argument_type == bool and not isinstance(result, bool):
                raise ValidationException(field=name, message="Invalid boolean value")
            elif argument_type == dict and not isinstance(result, dict):
                raise ValidationException(field=name, message="Invalid object value")
            elif argument_type == 'uuid':
                try:
                    uuid.UUID(result, version=4)
                except (TypeError, ValueError, AttributeError):
                    raise ValidationException(field=name, message="Invalid UUID value")
            elif argument_type == 'email':
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if not re.fullmatch(regex, result):
                    raise ValidationException(field=name, message="Invalid email")

        if required and not result:
            raise ValidationException(field=name, message="Field is required and should not be empty")

        if argument_type in ['email']:
            if not process:
                process = []
            process.extend(['lower', 'strip'])

        if result is not None and argument_type is str and process:
            if 'capitalize_first' in process:
                result = result.capitalize()
            if 'capitalize' in process:
                spaces_split = result.split(' ')
                for index, row in enumerate(spaces_split):
                    spaces_split[index] = str(row).capitalize()
                result = ' '.join(spaces_split)
            if 'strip' in process:
                result = result.strip()
            if 'lower' in process:
                result = result.lower()
            if 'upper' in process:
                result = result.upper()
            if 'phone' in process:
                result = result.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')

        if result is not None and possible_values and result not in possible_values:
            raise ValidationException(field=name, message="Invalid value")

        if result is not None and validation:
            for validate, parameters in validation.items():
                if validate == 'length':
                    if 'min' in parameters.keys():
                        if len(result) < parameters['min']:
                            raise ValidationException(
                                field=name, message=f"Value length too small (min: {parameters['min']})"
                            )
                    if 'max' in parameters.keys():
                        if len(result) > parameters['max']:
                            raise ValidationException(
                                field=name, message=f"Value length too big (max: {parameters['max']})"
                            )
                if validate == 'contains':
                    if 'upper' in parameters and not any(char.isupper() for char in result):
                        raise ValidationException(field=name, message="Value should contain upper letter")
                    if 'number' in parameters and not any(char.isdigit() for char in result):
                        raise ValidationException(field=name, message="Value should contain number")

        if result is not None and process and 'encode' in process:
            result = result.encode('utf-8')

        if result is not None:
            return result

        return default

    def get_arguments(self, arguments: dict) -> dict:
        result = {}
        exceptions = []
        for argument, parameters in arguments.items():
            try:
                result[argument] = self.get_argument(name=argument, default=parameters.get('default'),
                                                     argument_type=parameters.get('type'),
                                                     required=parameters.get('required'),
                                                     process=parameters.get('process'),
                                                     possible_values=parameters.get('possible_values'),
                                                     validation=parameters.get('validate'),
                                                     fields=parameters.get('fields'),
                                                     argument_format=parameters.get('format'))
            except ValidationException as e:
                exceptions.append(e)
        if exceptions:
            raise ManyValidationExceptions(exceptions=exceptions)
        return result

    @staticmethod
    def update_errors(error_fields, key, error):
        if key not in error_fields:
            error_fields[key] = [error]
        else:
            error_fields[key].append(error)
        return error_fields

    def get_file(self, attribute_name):
        file_handler = self.request.files.get(attribute_name)
        if not file_handler:
            return None
        file_handler = file_handler[0]

        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(file_handler.get('body'))

        result = {
            "file": file_handler.get('body'),
            "type": file_type,
            "name": file_handler.get('filename'),
            "extension": os.path.splitext(file_handler.get('filename'))[1]
        }

        return result

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    async def options(self, *args, **kwargs):
        if hasattr(self, 'methods') and isinstance(self.methods, list):
            self.set_header('Allow', ', '.join(self.methods))
            self.set_status(204)
            return self.finish()
        return self.finish_with_error(404)

    async def get(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def post(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def put(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def patch(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def delete(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def copy(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def head(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def link(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def unlink(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def purge(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def lock(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def unlock(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def propfind(self, *args, **kwargs):
        return self.finish_with_error(405)

    async def view(self, *args, **kwargs):
        return self.finish_with_error(405)


class HealthCheckEndpoint(Endpoint):
    methods = ['GET']

    def _log(self) -> None:
        return

    async def get(self, *args, **kwargs):
        return self.finish_with_ok_status()
