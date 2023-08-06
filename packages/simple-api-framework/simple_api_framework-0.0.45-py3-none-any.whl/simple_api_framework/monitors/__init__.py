import datadog


class DataDogMonitor:
    def __init__(self, **kwargs):
        self.__service_name = kwargs.get('service')
        self.__env = kwargs.get('env')
        datadog.initialize(api_key=kwargs.get('api_key'), app_key=kwargs.get('app_key'), host_name=kwargs.get('host'))

    def duration(self, name, duration):
        datadog.statsd.histogram(
            f'{self.__service_name}.durations.{name}',
            duration,
            tags=['app:' + self.__service_name, 'env:' + self.__env]
        )

    def count(self, name):
        datadog.statsd.increment(
            f'{self.__service_name}.metric.{name}',
            tags=['app:' + self.__service_name, 'env:' + self.__env],
            value=1
        )
