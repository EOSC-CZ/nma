from invenio_assets.webpack import WebpackThemeBundle

theme = WebpackThemeBundle(
    __name__,
    ".",
    default="semantic-ui",
    themes={
        "semantic-ui": {
            "entry": {
                "components": "./js/custom-components.js",
                "record_management": "./js/record-management/index.js",
                "home_page_search": "./js/home-page-search.js",
            },
            "dependencies": {},
            "devDependencies": {},
            "aliases": {},
        }
    },
)
