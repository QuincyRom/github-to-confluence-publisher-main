# import yaml

# def getConfig(overrides=None):
#     with open("./converter/publisher/config/config.yaml", "r") as yamlFileConfig:
#         config = yaml.safe_load(yamlFileConfig)
#     if overrides:
#         config.update(overrides)
#     return config

import os
import dotenv

dotenv.load_dotenv()


def getConfig():
    try:
        config = {
            "confluence_url": os.environ["CONFLUENCE_URL"],
            "confluence_space": os.environ["CONFLUENCE_SPACE"],
            "confluence_parent_page_id": os.environ["CONFLUENCE_PARENT_PAGE_ID"],
            "confluence_search_pattern": os.environ["CONFLUENCE_SEARCH_PATTERN"],
            "github_folder_with_md_files": os.environ["GITHUB_FOLDER_WITH_MD_FILES"],
            "github_folder_with_image_files": os.environ[
                "GITHUB_FOLDER_WITH_IMAGE_FILES"
            ],
        }
    except KeyError as e:
        raise KeyError(f"Missing environment variable: {e}")

    return config
