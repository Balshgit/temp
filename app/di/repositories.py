from dependency_injector import containers, providers
from dependency_injector.providers import Singleton

from app.core.users.repositories import UserCacheRepository, UserRepository
from settings.config import AppSettings


class RepositoriesContainer(containers.DeclarativeContainer):
    settings: providers.Dependency[AppSettings] = providers.Dependency()
    adapters = providers.DependenciesContainer()

    user_repository: Singleton[UserRepository] = Singleton(
        UserRepository,
        db=adapters.database,
    )

    user_cache_repository: Singleton[UserCacheRepository] = Singleton(
        UserCacheRepository,
        cache_adapter=adapters.cache_adapter,
    )
