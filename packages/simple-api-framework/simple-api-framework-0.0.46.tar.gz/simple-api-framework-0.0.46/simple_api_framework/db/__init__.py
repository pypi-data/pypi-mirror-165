import datetime
import os
import random
import re
import string
from decimal import Decimal
from uuid import uuid4

import aiopg
import psycopg2
import psycopg2.extras

SYSTEM_ATTRIBUTES = ('TABLE_NAME', 'FRONTEND_EXCLUDE_FIELDS', 'SPECIAL_FIELDS', 'COMMON_FRONTEND_EXCLUDE_FIELDS',
                     'frontend', 'COMMON_FRONTEND_INCLUDE_FIELDS', 'FRONTEND_INCLUDE_FIELDS')


class DatabaseRecordNotFoundError(Exception):
    pass


class DatabaseError(Exception):
    pass


class Relationship:
    def __init__(self, relation_class, relation_field, key='id', parameters=None):
        self.relation = relation_class
        self.field = relation_field
        self.key = key
        self.parameters = parameters


class Relationships:
    def __init__(self, relation_class, relation_field, key='id', parameters=None, sort_column=None, sort_order='asc'):
        self.relation = relation_class
        self.field = relation_field
        self.key = key
        self.parameters = parameters
        self.sort_column = sort_column
        self.sort_order = sort_order


class RelationCount:
    def __init__(self, relation_class, relation_field, key='id', parameters=None):
        self.relation = relation_class
        self.field = relation_field
        self.key = key
        self.parameters = parameters


class QueryField:
    def __init__(self, query, parameters=None):
        self.query = query
        self.parameters = parameters


class Model:
    COMMON_FRONTEND_EXCLUDE_FIELDS = ('id', 'is_active', 'is_deleted', 'created', 'modified', )
    COMMON_FRONTEND_INCLUDE_FIELDS = ()
    id = 0
    uuid = None
    is_active = True
    is_deleted = False
    created = None
    modified = None

    def __init__(self, **kwargs):
        for attribute in kwargs.keys():
            if hasattr(self, attribute):
                setattr(self, attribute, kwargs.get(attribute))
        if self.uuid is None:
            self.uuid = str(uuid4())
        if self.created is None:
            self.created = datetime.datetime.utcnow()
        if self.modified is None:
            self.modified = datetime.datetime.utcnow()

    @classmethod
    def table_short_name(cls):
        name = f"{cls.TABLE_NAME}"
        name = name.lower().replace('incase.', '')
        return name.strip()

    @classmethod
    def table_full_name(cls):
        return f"{cls.TABLE_NAME} {cls.table_short_name()}"

    @classmethod
    def attributes(cls, exclude_fields=()):
        attributes = []
        for attribute in dir(cls):
            if attribute in exclude_fields:
                continue
            if attribute in SYSTEM_ATTRIBUTES:
                continue
            if attribute.startswith('__'):
                continue
            if isinstance(getattr(cls, attribute), Relationship) \
                    or isinstance(getattr(cls, attribute), Relationships) \
                    or isinstance(getattr(cls, attribute), RelationCount):
                continue
            if callable(getattr(cls, attribute)):
                continue
            attributes.append(attribute)
        return sorted(attributes)

    @classmethod
    def sql_fields(cls, exclude_fields=(), db_exec=False):
        fields = []
        for attribute in cls.attributes(exclude_fields):
            if hasattr(cls, 'SPECIAL_FIELDS') and attribute in cls.SPECIAL_FIELDS:
                continue
            value = getattr(cls, attribute)
            if isinstance(value, QueryField) and not db_exec:
                fields.append(f'({value.query}) AS "{cls.table_short_name()}__{attribute}"')
                continue
            elif isinstance(value, QueryField) and db_exec:
                continue
            if db_exec:
                fields.append(f'"{attribute}"')
            else:
                fields.append(f'{cls.table_short_name()}.{attribute} AS "{cls.table_short_name()}__{attribute}"')
        return fields

    @classmethod
    def sql_format_fields(cls, exclude_fields=()):
        fields = []
        for attribute in cls.attributes(exclude_fields):
            value = getattr(cls, attribute)
            if hasattr(cls, 'SPECIAL_FIELDS') and attribute in cls.SPECIAL_FIELDS:
                continue
            if isinstance(value, QueryField):
                continue
            fields.append(f"%({attribute})s")
        return ", ".join(fields)

    @staticmethod
    def _process_parameter(table, field, value):
        field_name = f"{field}_{''.join(random.choice(string.ascii_lowercase) for _ in range(6))}".replace('::', '_')
        sql_name = f'{table.table_short_name()}.{field}'
        try:
            if isinstance(getattr(table, field), QueryField):
                sql_name = f'{table.table_short_name()}__{field}'
        except AttributeError:
            if '::' not in field and '->' not in field:
                return [], []

        if isinstance(value, str):
            if value.lower() == 'is not null':
                return [f"{sql_name} IS NOT NULL"], []
            if value.lower() == 'is null':
                return [f"{sql_name} IS NULL"], []
            if 'now()' in value.lower():
                add = ''
                if '::date' in value.lower():
                    add = '::date'
                if 'interval' in value.lower():
                    sign = '+'
                    if '-' in value:
                        sign = '-'
                    add = f" {sign} {value.lower()[value.index('interval'):]}"
                if value.startswith('>='):
                    return [f"{sql_name} >= NOW(){add}"], []
                elif value.startswith('<='):
                    return [f"{sql_name} <= NOW(){add}"], []
                elif value.startswith('>'):
                    return [f"{sql_name} > NOW(){add}"], []
                elif value.startswith('<'):
                    return [f"{sql_name} < NOW(){add}"], []
                elif value.startswith('!='):
                    return [f"{sql_name} <> NOW(){add}"], []
                elif value.startswith('='):
                    return [f"{sql_name} = NOW(){add}"], []
                else:
                    return [], []
            if value.startswith("!="):
                return [f"{sql_name} != %({field_name})s"], [{field_name: value.replace('!=', '').strip()}]
            if value.startswith('>='):
                return [f"{sql_name} >= %({field_name})s"], [{field_name: value.replace('>=', '').strip()}]
            if value.startswith('<='):
                return [f"{sql_name} <= %({field_name})s"], [{field_name: value.replace('<=', '').strip()}]
            if value.startswith('>'):
                return [f"{sql_name} > %({field_name})s"], [{field_name: value.replace('>', '').strip()}]
            if value.startswith('<'):
                return [f"{sql_name} < %({field_name})s"], [{field_name: value.replace('<', '').strip()}]
            if value.lower().startswith('like'):
                return [f"{sql_name} LIKE %({field_name})s"], [{field_name: value[4:].replace("'", '').strip()}]
            if value.lower().startswith('ilike'):
                return [f"{sql_name} ILIKE %({field_name})s"], [{field_name: value[5:].replace("'", '').strip()}]
            if 'value between' in value.lower():
                values = value.split(' ')
                return [f"%({field_name})s BETWEEN {table.table_short_name()}.{values[3]} "
                        f"AND {table.table_short_name()}.{values[4]}"], [{field_name: values[0]}]
            if 'between' in value.lower():
                values = value.split(' ')
                return [f"{sql_name} BETWEEN %({field_name}_1)s AND %({field_name}_2)s"], \
                       [{f"{field_name}_1": values[1]}, {f"{field_name}_2": values[2]}]
            if 'query=[' in value.lower() or 'query in [' in value.lower():
                query = " ".join([line.strip() for line in value.splitlines()])
                query = re.search(r'\[(.*?)]', query).group(1).strip()
                if value.lower().startswith('query=['):
                    return [f"{sql_name} = ({query})"], []
                elif value.lower().startswith('query in ['):
                    return [f"{sql_name} IN ({query})"], []
                else:
                    return [], []
            if 'query!=[' in value.lower() or 'query not in [' in value.lower():
                query = " ".join([line.strip() for line in value.splitlines()])
                query = re.search(r'\[(.*?)]', query).group(1).strip()
                if value.lower().startswith('query!=['):
                    return [f"{sql_name} != ({query})"], []
                elif value.lower().startswith('query not in ['):
                    return [f"{sql_name} NOT IN ({query})"], []
                else:
                    return [], []
        if isinstance(value, tuple):
            fields = []
            values = []
            for item in value:
                f, v = Model._process_parameter(table, field, item)
                fields.append(f)
                values.append(v)
            return [f"({' OR '.join(fields)})"], values
        if isinstance(value, list):
            return [f'{sql_name} IN ({", ".join([str(e) for e in value])})'], []
        return [f"{sql_name} = %({field_name})s"], [{field_name: value}]

    @classmethod
    def _process_parameters(cls, parameters, table_class=None):
        if not parameters:
            return "", {}

        if table_class is None:
            table_class = cls

        fields = []
        result_parameters = {}
        if isinstance(parameters, dict):
            parameters = [parameters]

        for parameter in parameters:
            if isinstance(parameter, dict):
                for name, value in parameter.items():
                    f, values = table_class._process_parameter(table_class, name, value)
                    fields.extend(f)
                    for v in values:
                        result_parameters.update(v)
            if isinstance(parameter, list):
                or_fields = []
                for row in parameter:
                    for name, value in row.items():
                        f, values = table_class._process_parameter(table_class, name, value)
                        or_fields.extend(f)
                        for v in values:
                            result_parameters.update(v)
                if or_fields:
                    fields.append(f"({' OR '.join(or_fields)})")

        query = ''
        if fields:
            query = ' AND '.join(fields)
        return query, result_parameters

    @classmethod
    def process_relationships(cls):
        fields = []
        parameters = {}
        for attribute in dir(cls):
            value = getattr(cls, attribute)
            if not isinstance(value, Relationship) and not isinstance(value, Relationships) \
                    and not isinstance(value, RelationCount):
                continue
            rel = value.relation
            if isinstance(value, RelationCount):
                query = f"SELECT COUNT(*) FROM {rel.table_full_name()} "
                query += f"WHERE {rel.table_short_name()}.{value.field} = {cls.table_short_name()}.{value.key}"
                where, params = cls._process_parameters(value.parameters, table_class=rel)
                if where:
                    query += f" AND {where}"
                    parameters.update(params)
                fields.append(f"({query}) AS count__{cls.table_short_name()}__{attribute}")
                continue

            rel_fields = []
            for rel_attr in rel.attributes():
                if hasattr(rel, 'SPECIAL_FIELDS') and rel_attr in rel.SPECIAL_FIELDS:
                    continue
                if isinstance(getattr(rel, rel_attr), QueryField):
                    rel_fields.append(f"'{rel.table_short_name()}__{rel_attr}', "
                                      f"({getattr(rel, rel_attr).query})")
                else:
                    rel_fields.append(f"'{rel.table_short_name()}__{rel_attr}', {rel.table_short_name()}.{rel_attr}")
            rel_child_fields, params = rel.process_relationships()
            parameters.update(params)
            for rel_child_field in rel_child_fields:
                json_select = rel_child_field[:rel_child_field.rindex(' AS ')]
                json_name = rel_child_field[rel_child_field.rindex(' AS ')+4:]
                rel_fields.append(f"'{json_name}', {json_select}")

            if isinstance(value, Relationship):
                query = f"SELECT json_build_object({', '.join(rel_fields)}) "
            else:
                query = f"SELECT json_agg(json_build_object({', '.join(rel_fields)})) "
            query += f"FROM {rel.table_full_name()} "
            query += f"WHERE {rel.table_short_name()}.{value.field} = {cls.table_short_name()}.{value.key}"
            where, params = cls._process_parameters(value.parameters, table_class=rel)
            if where:
                query += f" AND {where}"
                parameters.update(params)
            fields.append(f"({query}) AS json__{cls.table_short_name()}__{attribute}")
        return fields, parameters

    @staticmethod
    async def fetch(query, values=None, many=False, expected_result=True, postgres_uri=None):
        if not postgres_uri:
            postgres_uri = os.getenv('DB_URL')

        if not postgres_uri:
            raise DatabaseError("No database connection URL was provided")

        try:
            timeout = int(os.getenv("DB_TIMEOUT", 30))
        except (TypeError, ValueError):
            timeout = 30

        try:
            pool = await aiopg.create_pool(postgres_uri, timeout=timeout)
            async with pool.acquire() as connection:
                async with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    try:
                        await cursor.execute(query, values)
                    except Exception as exception:
                        await connection.close()
                        raise DatabaseError(exception)
                    if expected_result:
                        if not many:
                            result = await cursor.fetchone()
                            if result:
                                result = dict(result)
                        else:
                            result = []
                            rows = await cursor.fetchall()
                            for row in rows:
                                result.append(dict(row))
                await connection.close()
        except Exception as exception:
            raise DatabaseError(exception)

        if expected_result:
            return result

    @staticmethod
    def _process_record(cls, record):
        if not record:
            return None

        columns = {}
        for attribute in cls.attributes():
            if hasattr(cls, 'SPECIAL_FIELDS') and attribute in cls.SPECIAL_FIELDS:
                continue
            record_key = f"{cls.table_short_name()}__{attribute}"
            columns[attribute] = record.get(record_key)

        for attribute in dir(cls):
            value = getattr(cls, attribute)
            if not isinstance(value, Relationship) and not isinstance(value, Relationships) \
                    and not isinstance(value, RelationCount):
                continue
            rel = value.relation
            if isinstance(value, RelationCount):
                try:
                    columns[attribute] = record.get(f"count__{cls.table_short_name()}__{attribute}", 0)
                except (ValueError, TypeError):
                    columns[attribute] = 0
                continue
            json_record_key = f"json__{cls.table_short_name()}__{attribute}"
            json_record = record.get(json_record_key)
            if isinstance(value, Relationship):
                columns[attribute] = Model._process_record(rel, json_record)
            else:
                columns[attribute] = Model._process_records(rel, json_record)
                if value.sort_column:
                    columns[attribute] = sorted(
                        columns[attribute],
                        key=lambda d: getattr(d, value.sort_column),
                        reverse=True if value.sort_order == 'desc' else False
                    )

        return cls(**columns)

    @staticmethod
    def _process_records(cls, records):
        objects = []
        for record in records if records else []:
            objects.append(Model._process_record(cls, record))
        return objects

    @classmethod
    def _generate_sql(cls):
        fields = cls.sql_fields()
        f, parameters = cls.process_relationships()
        for attribute in cls.attributes():
            value = getattr(cls, attribute)
            if isinstance(value, QueryField) and value.parameters:
                for key, v in value.parameters.items():
                    parameters.update({key: v})
                continue

        fields.extend(f)
        query = f"SELECT {', '.join(fields)} FROM {cls.table_full_name()}"
        return query, parameters

    @classmethod
    async def get(cls, pk=0, parameters=None, active=True):
        if pk:
            try:
                pk = int(pk)
                parameters = {'id': pk}
            except (ValueError, TypeError):
                pass

        query, params = cls._generate_sql()
        where, parameters = cls._process_parameters(parameters)
        parameters.update(params)
        if where:
            query += f" WHERE {where}"
        if active:
            if not where:
                query += f" WHERE {cls.table_short_name()}.is_active = TRUE"
            else:
                query += f" AND {cls.table_short_name()}.is_active = TRUE"

        record = await cls.fetch(query, parameters)
        if not record:
            if pk:
                raise DatabaseRecordNotFoundError(f"Record id={pk} was not found")
            else:
                raise DatabaseRecordNotFoundError(f"Record with parameters {parameters} was not found")
        return cls._process_record(cls, record)

    @classmethod
    async def get_by_query(cls, query, parameters=None):
        if not hasattr(cls, 'TABLE_NAME'):
            raise ValueError(f"There is no TABLE_NAME attribute in class {cls.__name__}")

        record = await cls.fetch(query, parameters)
        if not record:
            return None
        return cls(**record)

    @classmethod
    async def all(cls, parameters=None, sort_column=None, sort_order='asc', limit=None, offset=None):
        query, params = cls._generate_sql()
        where, parameters = cls._process_parameters(parameters)
        parameters.update(params)
        if where:
            query += f" WHERE {where}"

        if sort_column:
            query += f" ORDER BY {cls.table_short_name()}__{sort_column} {sort_order}"
        if limit:
            query += f" LIMIT {limit}"
        if offset:
            query += f" OFFSET {offset}"

        records = await cls.fetch(query, parameters, many=True)
        return cls._process_records(cls, records)

    @classmethod
    async def count(cls, parameters=None, processed=None):
        if not parameters and not processed:
            query = f"SELECT COUNT(*) as count FROM {cls.table_full_name()}"
            count = await cls.fetch(query, parameters)
            if not count or not count.get('count'):
                return 0
            return count.get('count')

        if not processed:
            where, parameters = cls._process_parameters(parameters)
        else:
            where, parameters = processed

        query = f"SELECT COUNT(*) AS count FROM {cls.table_full_name()}"
        if where:
            query += f" WHERE {where}"

        count = await cls.fetch(query, parameters)
        if not count or not count.get('count'):
            return 0
        return count.get('count')

    @classmethod
    async def paginated(cls, parameters=None, sort_column=None, sort_order='asc', pagination=None):
        query, params = cls._generate_sql()
        where, parameters = cls._process_parameters(parameters)
        parameters.update(params)
        if where:
            query += f" WHERE {where}"

        count = await cls.count(processed=(where, parameters))
        if not count:
            return 0, []

        if sort_column:
            query += f" ORDER BY {cls.table_short_name()}__{sort_column} {sort_order}"
        if pagination:
            query += f" LIMIT {pagination.get('limit')} OFFSET {pagination.get('offset')} "

        records = await cls.fetch(query, parameters, many=True)
        return count, cls._process_records(cls, records)

    async def insert(self):
        if not hasattr(self, 'TABLE_NAME'):
            raise ValueError(f"There is no TABLE_NAME attribute in class {self.__name__}")

        fields = self.sql_fields(exclude_fields=('id',), db_exec=True)
        values = {}
        for field in fields:
            field = field.replace('"', '').strip()
            values[field] = getattr(self, field)

        query = f"INSERT INTO {getattr(self, 'TABLE_NAME')} " \
                f"({', '.join(fields)}) " \
                f"VALUES ({self.sql_format_fields(exclude_fields=('id',))}) RETURNING id"

        record_id = await self.fetch(query, values)
        self.id = record_id.get('id')

    async def update(self):
        if not hasattr(self, 'TABLE_NAME'):
            raise ValueError(f"There is no TABLE_NAME attribute in class {self.__name__}")

        self.modified = datetime.datetime.utcnow()

        fields = []
        values = {}
        for field in self.sql_fields(exclude_fields=('id', 'uuid', 'created', ), db_exec=True):
            field = field.replace('"', '').strip()
            values[field] = getattr(self, field)
            fields.append(f"{field} = %({field})s")

        values['id'] = self.id

        query = f"UPDATE {getattr(self, 'TABLE_NAME')} SET {', '.join(fields)} WHERE id = %(id)s"
        await self.fetch(query, values, expected_result=False)

    @classmethod
    async def delete(cls, pk=None, parameters=None):
        if not parameters:
            query = f"DELETE FROM {getattr(cls, 'TABLE_NAME')} WHERE id = %(id)s"
            await cls.fetch(query, {'id': pk}, expected_result=False)
            return

        where, parameters = cls._process_parameters(parameters)
        query = f"DELETE FROM {getattr(cls, 'TABLE_NAME')} {cls.table_short_name()}"
        if where:
            query += f" WHERE {where}"
        await cls.fetch(query, parameters, expected_result=False)

    @property
    def frontend(self):
        result = {}
        for attribute in dir(self):
            if attribute in SYSTEM_ATTRIBUTES:
                continue
            if attribute.startswith('__'):
                continue
            if callable(getattr(self, attribute)):
                continue
            if isinstance(getattr(self, attribute), RelationCount):
                result[attribute] = 0
                continue
            if isinstance(getattr(self, attribute), Relationship):
                result[attribute] = None
                continue
            if isinstance(getattr(self, attribute), Relationships):
                result[attribute] = []
                continue
            if isinstance(getattr(self, attribute), QueryField):
                result[attribute] = None
                continue

            include_fields = self.COMMON_FRONTEND_INCLUDE_FIELDS
            if hasattr(self, 'FRONTEND_INCLUDE_FIELDS'):
                include_fields += self.FRONTEND_INCLUDE_FIELDS
            exclude_fields = self.COMMON_FRONTEND_EXCLUDE_FIELDS
            if hasattr(self, 'FRONTEND_EXCLUDE_FIELDS'):
                exclude_fields += self.FRONTEND_EXCLUDE_FIELDS

            if attribute not in include_fields and attribute in exclude_fields:
                continue

            value = getattr(self, attribute)
            if isinstance(value, datetime.datetime):
                result[attribute] = value.strftime('%Y-%m-%dT%H:%M:%SZ')
            elif isinstance(value, datetime.date):
                result[attribute] = value.strftime('%Y-%m-%d')
            elif isinstance(value, Decimal):
                result[attribute] = float(value)
            elif isinstance(value, object) and hasattr(value, 'frontend'):
                result[attribute] = value.frontend
            elif isinstance(value, list):
                result_list = []
                for val in value:
                    if isinstance(val, object) and hasattr(val, 'frontend'):
                        result_list.append(val.frontend)
                    else:
                        result_list.append(val)
                result[attribute] = result_list
            else:
                result[attribute] = value
        return result

    def set_currency_field(self, field, value):
        try:
            value = int(Decimal("%0.2f" % value) * 100)
        except ValueError:
            raise ValueError(f"Invalid string value: got '{value}', expected decimal")

        if not value:
            value = 0
        setattr(self, field, value)
