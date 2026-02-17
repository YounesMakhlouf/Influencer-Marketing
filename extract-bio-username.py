"""Import influencer bio/username data from TSV files into MongoDB."""

import logging
import os
import sys

from shared.mongo import MongoConnection

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def import_directory(directory: str) -> None:
    """Read TSV files from *directory* and insert records into MongoDB."""
    mongo = MongoConnection()
    collection = mongo.collection

    if not os.path.isdir(directory):
        logging.error("Directory does not exist: %s", directory)
        sys.exit(1)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    fields = line.strip().split("\t")
                    if len(fields) >= 7:
                        name = fields[0]
                        category = fields[6]
                        bio = fields[7] if len(fields) > 7 else ""

                        if not name and not category and not bio:
                            continue

                        json_obj = {
                            "Name": name,
                            "Category": category,
                            "Bio": bio,
                        }
                        logging.info(json_obj)
                        collection.insert_one(json_obj)
                except Exception as e:
                    logging.warning("Skipping line: %s", e)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>")
        sys.exit(1)
    import_directory(sys.argv[1])
