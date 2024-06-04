from interface.click.root_group import root_cli_group
from infrastructure.dependency_injection.container import Container

if __name__ == '__main__':
    # Initialize dependency injection container
    container = Container()

    # Run root command group
    root_cli_group()
