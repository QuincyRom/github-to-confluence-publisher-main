import logging
import os
import markdown
import re
from config.getconfig import getConfig
from pagesController import createPage
from pagesController import attachFile


CONFIG = getConfig()


def publishFolder(
    folder, login, password, parentPageID=None
):  # parentPageID has the default input parameter "None" (it means ROOT)
    logging.info("Publishing folder: " + folder)
    for entry in os.scandir(folder):
        if not entry.is_dir() and not entry.is_file():
            logging.info(
                f"Found unknown type of entry (not file, not directory, not symlink) {entry.path}  filename: {entry.name}"
            )
            continue

        if entry.is_dir():
            # create page with the DISPLAY CHILDREN macro for the directories in the folder with MD files
            logging.info("Found directory: " + str(entry.path))
            currentPageID = createPage(
                title=str(entry.name),
                content='<ac:structured-macro ac:name="children" ac:schema-version="2" ac:macro-id="80b8c33e-cc87-4987-8f88-dd36ee991b15"/>',  # name of the DISPLAY CHILDREN macro
                parentPageID=parentPageID,
                login=login,
                password=password,
            )

            # publish files in the current folder
            publishFolder(
                folder=entry.path,
                login=login,
                password=password,
                parentPageID=currentPageID,
            )

        elif entry.is_file():
            logging.info("Found file: " + str(entry.path))

            if (
                not str(entry.path).lower().endswith(".md")
            ):  # chech for correct file extension
                logging.info(
                    "File: "
                    + str(entry.path)
                    + "  is not a MD file. Publishing has rejected"
                )
                continue

            newFileContent = ""
            filesToUpload = []
            with open(entry.path, "r", encoding="utf-8") as mdFile:
                for line in mdFile:
                    # search for images in each line and ignore http/https image links
                    # Pattern: \A!\[.*]\(.*\)\Z
                    # example:  ![test](/data_images/test_image.jpg)

                    result = re.findall("\A!\[.*]\((?!http)(.*)\)", line)

                    if bool(result):  # line contains an image
                        # extract filename from the full path
                        result = str(
                            result
                        ).split(
                            "'"
                        )[
                            1
                        ]  # ['/data_images/test_image.jpg'] => /data_images/test_image.jpg
                        result = str(result).split("/")[
                            -1
                        ]  # /data_images/test_image.jpg => test_image.jpg
                        logging.debug("Found file for attaching: " + result)
                        filesToUpload.append(result)
                        # replace line with conflunce storage format <ac:image> <ri:attachment ri:filename="test_image.jpg" /></ac:image>
                        newFileContent += (
                            '<ac:image> <ri:attachment ri:filename="'
                            + result
                            + '" /></ac:image>'
                        )
                    else:  # line without an image
                        newFileContent += line

                # create new page
                pageIDforFileAttaching = createPage(
                    title=str(entry.name),
                    content=markdown.markdown(
                        newFileContent,
                        extensions=["markdown.extensions.tables", "fenced_code"],
                    ),
                    parentPageID=parentPageID,
                    login=login,
                    password=password,
                )

                # if do exist files to Upload as attachments
                if not bool(filesToUpload):
                    continue

                upload_files(filesToUpload, pageIDforFileAttaching, login, password)


def upload_files(files_to_upload, page_id_for_attaching, login, password):
    for file in files_to_upload:
        imagePath = (
            str(CONFIG["github_folder_with_image_files"]) + "/" + file
        )  # full path of uploaded image file
        if os.path.isfile(imagePath):  # check if the  file exist
            logging.info(
                "Attaching file: "
                + imagePath
                + "  to the page: "
                + str(page_id_for_attaching)
            )
            with open(imagePath, "rb") as attachedFile:
                attachFile(
                    pageIdForFileAttaching=page_id_for_attaching,
                    attachedFile=attachedFile,
                    login=login,
                    password=password,
                )
        else:
            logging.error("File: " + str(imagePath) + "  not found. Nothing to attach")
