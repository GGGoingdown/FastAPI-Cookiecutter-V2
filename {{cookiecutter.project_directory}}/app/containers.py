from dependency_injector import containers, providers

from app.config import Settings
from app import services, __VERSION__


class Gateway(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()


class Service(containers.DeclarativeContainer):
    config: Settings = providers.Configuration()
    gateway: Gateway = providers.DependenciesContainer()

    logger_handler: services.LoggerHandler = providers.Resource(
        services.LoggerHandler,
        application_name=config.app.application_name,
        log_level=config.app.log_level,
        env_mode=config.app.environment,
    )

    sentry_handler: services.SentryHandler = providers.Resource(
        services.SentryHandler,
        dsn=config.sentry.dsn,
        release_name=config.app.application_name,
        version=__VERSION__,
        environment=config.app.environment,
        trace_sample_rates=config.sentry.trace_sample_rates,
    )

    async_request_handler: services.AsyncRequestClient = providers.Resource(
        services.AsyncRequestHandler,
        retry_attempts=3,
        timeout=10,
    )

    jwt_handler: services.JWTHandler = providers.Singleton(
        services.JWTHandler,
        secret_key=config.jwt.secret_key,
        algorithm=config.jwt.algorithm,
        expire_minutes=config.jwt.expire_minutes,
    )

    authentication_selector = providers.Singleton(
        services.AuthenticationSelector, jwt=jwt_handler
    )

    authentication_service = providers.Singleton(
        services.AuthenticationService, auth_selector=authentication_selector
    )

    authorization_service = providers.Singleton(
        services.AuthorizationService,
        auth_selector=authentication_selector,
    )


class Application(containers.DeclarativeContainer):
    config = providers.Configuration()
    gateway: Gateway = providers.Container(Gateway, config=config)
    service: Service = providers.Container(Service, config=config, gateway=gateway)
