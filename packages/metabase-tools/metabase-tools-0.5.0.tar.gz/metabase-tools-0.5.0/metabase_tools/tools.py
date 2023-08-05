"""
MetabaseTools extends MetabaseApi with additional complex functions
"""
from json import dumps, loads
from pathlib import Path
from typing import Optional

from metabase_tools.exceptions import (
    EmptyDataReceived,
    InvalidParameters,
    ItemInPersonalCollection,
    ItemNotFound,
    NoUpdateProvided,
)
from metabase_tools.metabase import MetabaseApi
from metabase_tools.models.card import Card
from metabase_tools.models.collection import Collection
from metabase_tools.models.database import Database


class MetabaseTools(MetabaseApi):
    """Extends MetabaseApi with additional complex functions"""

    def download_native_queries(
        self,
        save_file: Optional[Path | str] = None,
        root_folder: Path | str = ".",
        file_extension: str = "sql",
    ) -> Path:
        """Downloads all native queries into a JSON file

        Args:
            save_file (Path | str, optional): Path to save mapping file, defaults to \
                mapping_{timestamp}.json
            root_folder (Path | str, optional): Root folder to save queries, by \
                default "."
            file_extension (str, optional): File extension to save the queries, by \
                default "sql"

        Returns:
            Path: Path to save file
        """
        # Determine save path
        root_folder = Path(root_folder)  # Convert root folder to a path object
        save_file = Path(save_file or "mapping.json")

        # Download list of cards from Metabase API and filter to only native queries
        cards = [
            card
            for card in Card.get(adapter=self)
            if (
                card.query_type == "native"
                and card.collection
                and card.collection.personal_owner_id is None
            )
        ]
        self._logger.debug("Found %s cards with native queries", len(cards))

        # Create dictionary of collections for file paths
        collections_by_id = self._get_collections_dict(key="id")
        self._logger.debug(
            "Generated flat list of %s collections", len(collections_by_id)
        )

        # Format filtered list
        formatted_list = {
            "root": str(root_folder),
            "file_extension": file_extension,
            "cards": [],
        }

        for card in cards:
            try:
                new_card = self._get_mapping_details(
                    card, collections_by_id=collections_by_id
                )
            except ItemInPersonalCollection:
                self._logger.warning("Skipping %s (personal collection)", card.name)
                continue
            formatted_list["cards"].append(new_card)

            try:
                self._save_query(
                    card=card,
                    save_path=f"{root_folder}/{new_card['path']}",
                    file_extension=file_extension,
                )
            except OSError:
                self._logger.warning("Skipping %s (name error)", card.name)
                continue
            self._logger.debug(
                "%s saved to %s", card.name, f"{root_folder}/{new_card['path']}"
            )

        # Save mapping file
        mapping_path = Path(f"{root_folder}")
        mapping_path.mkdir(parents=True, exist_ok=True)
        mapping_path /= save_file
        self._logger.debug(
            "Completed iterating through list, saving file: %s", mapping_path
        )
        with open(mapping_path, "w", newline="", encoding="utf-8") as file:
            file.write(dumps(formatted_list, indent=2))

        # Returns path to file saved
        return mapping_path

    def upload_native_queries(
        self,
        mapping_path: Path | str,
        dry_run: bool = True,
        stop_on_error: bool = False,
    ) -> list[dict] | dict:
        """Uploads queries to Metabase

        Args:
            mapping_path (Path | str): Path to the mapping configuration file, by \
                default None
            dry_run (bool, optional): Execute task as a dry run (i.e. do not make \
                any changes), by default True
            stop_on_error (bool, optional): Raise error and stop if an error is \
                encountered. Defaults to False.

        Raises:
            FileNotFoundError: The file referenced was not found

        Returns:
            list[dict] | dict: Results of upload
        """
        # Determine mapping path
        mapping_path = Path(mapping_path or "./mapping.json")

        # Open mapping configuration file
        with open(mapping_path, "r", newline="", encoding="utf-8") as file:
            mapping = loads(file.read())

        # Initialize common settings (e.g. root folder, file extension, etc.)
        root_folder = Path(mapping.get("root", "."))
        extension = mapping.get("file_extension", ".sql")
        cards = mapping["cards"]

        # Iterate through mapping file
        changes = {"updates": [], "creates": [], "errors": []}
        collections_by_id = self._get_collections_dict(key="id")
        collections_by_path = self._get_collections_dict(key="path")
        for card in cards:
            card_path = Path(f"{root_folder}/{card['path']}/{card['name']}.{extension}")
            if (
                card_path.exists() and "id" in card
            ):  # Ensures file exists and id is present
                try:
                    update = self._update_existing_card(
                        dev_card=card,
                        card_path=card_path,
                        collections_by_id=collections_by_id,
                        collections_by_path=collections_by_path,
                    )
                except NoUpdateProvided:
                    self._logger.debug("No updates necessary for %s", card["name"])
                    continue
                changes["updates"].append(update)
            elif card_path.exists():
                # Check if a card with the same name exists in the listed location
                dev_coll_id = collections_by_path[card["path"]]["id"]
                try:
                    card_id = self._find_card_id(
                        card_name=card["name"], collection_id=dev_coll_id
                    )
                except (
                    EmptyDataReceived,
                    ItemNotFound,
                ):  # No items in collection or not found
                    self._logger.debug(
                        "%s not found in listed location, creating", card["name"]
                    )
                    card_id = None

                if card_id:  # update card
                    prod_card = Card.get(adapter=self, targets=[card_id])[0]
                    with open(card_path, "r", newline="", encoding="utf-8") as file:
                        dev_code = file.read()
                    if dev_code != prod_card.dataset_query["native"]["query"]:
                        dev_query = prod_card.dataset_query.copy()
                        dev_query["native"]["query"] = dev_code
                        dev_def = {"id": card_id, "dataset_query": dev_query}
                        changes["updates"].append(dev_def)
                else:  # create card
                    with open(card_path, "r", newline="", encoding="utf-8") as file:
                        dev_query = file.read()
                    db_id = [
                        database.id
                        for database in Database.get(adapter=self)
                        if card["database"] == database.name
                    ][0]

                    new_card_def = {
                        "visualization_settings": {},
                        "collection_id": dev_coll_id,
                        "name": card["name"],
                        "dataset_query": {
                            "type": "native",
                            "native": {"query": dev_query},
                            "database": db_id,
                        },
                        "display": "table",
                    }
                    changes["creates"].append(new_card_def.copy())
            else:
                self._logger.error("Skipping %s (file not found)", card["name"])
                if stop_on_error:
                    raise FileNotFoundError(f"{card_path} not found")
                changes["errors"].append(card)

        # Loop exit before pushing changes to Metabase in case errors are encountered
        # Push changes back to Metabase API
        if not dry_run:
            results = []
            if len(changes["updates"]) > 0:
                update_results = Card.update(adapter=self, payloads=changes["updates"])
                if isinstance(update_results, list):
                    for result in update_results:
                        results.append(
                            {"id": result.id, "name": result.name, "is_success": True}
                        )

            if len(changes["creates"]) > 0:
                create_results = Card.create(adapter=self, payloads=changes["creates"])
                if isinstance(create_results, list):
                    for result in create_results:
                        results.append(
                            {"id": result.id, "name": result.name, "is_success": True}
                        )

            return results
        return changes

    def _get_mapping_details(self, card: Card, collections_by_id: dict) -> dict:
        try:
            mapping_details = {
                "id": card.id,
                "name": card.name,
                "path": collections_by_id[card.collection_id]["path"],
            }
        except KeyError as error_raised:
            raise ItemInPersonalCollection(
                "Item in personal collection"
            ) from error_raised

        mapping_details["database"] = Database.search(
            adapter=self, search_params=[{"id": card.database_id}]
        )[0].name

        return mapping_details

    def _save_query(self, card: Card, save_path: str, file_extension):
        # SQL file creation
        sql_code = card.dataset_query["native"]["query"]
        sql_path = Path(f"{save_path}")
        sql_path.mkdir(parents=True, exist_ok=True)
        sql_path /= f"{card.name}.{file_extension}"
        with open(sql_path, "w", newline="", encoding="utf-8") as file:
            file.write(sql_code)

    def _get_collections_dict(self, key: str):
        collections = Collection.get_flat_list(adapter=self)
        non_keys = [k for k in collections[0].keys() if k != key]
        return {item[key]: {nk: item[nk] for nk in non_keys} for item in collections}

    def _translate_path(
        self, collection_id: Optional[int] = None, collection_path: Optional[str] = None
    ) -> int | str:
        if collection_id:
            collections_by_id = self._get_collections_dict(key="id")
            return collections_by_id[collection_id]["path"]

        if collection_path:
            collections_by_path = self._get_collections_dict(key="path")
            return collections_by_path[collection_path]["id"]

        raise InvalidParameters

    def _find_card_id(self, card_name: str, collection_id: int) -> int:
        collection_items = Collection.get_contents(
            adapter=self, collection_id=collection_id, model_type="card", archived=False
        )
        for item in collection_items:
            if item["name"] == card_name:
                return item["id"]
        raise ItemNotFound

    def _update_existing_card(
        self,
        dev_card: dict,
        card_path: Path | str,
        collections_by_id: dict,
        collections_by_path: dict,
    ) -> dict:
        prod_card = Card.get(adapter=self, targets=[dev_card["id"]])[0]
        # Get query definition
        with open(card_path, "r", newline="", encoding="utf-8") as file:
            dev_card["query"] = file.read()
        # Generate update
        if (
            dev_card["query"] != prod_card.dataset_query["native"]["query"]
            or dev_card["path"] != collections_by_id[prod_card.collection_id]["path"]
        ):
            dev_card["dataset_query"] = prod_card.dataset_query.copy()
            dev_card["dataset_query"]["native"]["query"] = dev_card["query"]
            dev_card["collection_id"] = collections_by_path[dev_card["path"]]["id"]
            return {
                "id": dev_card["id"],
                "dataset_query": dev_card["dataset_query"],
                "collection_id": dev_card["collection_id"],
            }
        raise NoUpdateProvided
