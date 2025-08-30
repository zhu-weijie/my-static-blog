from src.builder import SiteBuilder


def run():
    """Initializes the site builder and runs the build process."""
    builder = SiteBuilder()
    builder.build()


if __name__ == "__main__":
    run()
