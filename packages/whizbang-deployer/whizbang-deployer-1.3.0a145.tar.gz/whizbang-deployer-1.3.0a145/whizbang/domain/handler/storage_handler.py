from abc import abstractmethod
from typing import List

from whizbang.config.app_config import AppConfig
from whizbang.domain.exceptions import AzCliResourceDoesNotExist
from whizbang.domain.handler.handler_base import IHandler, HandlerBase
from whizbang.domain.manager.az.az_storage_manager import IAzStorageManager
from whizbang.domain.models.firewall_rule_cidr import FirewallRuleCIDR
from whizbang.domain.models.storage.azure_blob import AzureBlob
from whizbang.domain.models.storage.azure_table import AzureTable, AzureTableEntry
from whizbang.domain.models.storage.datalake_state import DatalakeState
from whizbang.domain.models.storage.storage_network_rule import StorageVnetIPNetworkRule, StorageIPNetworkRule
from whizbang.domain.models.storage.storage_resource import StorageContainer, StorageBlobSource
from whizbang.domain.workflow.datalake.datalake_deploy_workflow import DatalakeDeployWorkflow
from whizbang.util import path_defaults
from whizbang.util.json_helpers import import_local_json


class IStorageHandler(IHandler):
    """"""

    @abstractmethod
    def deploy_datalake_directories(self, solution_name, storage_account_name):
        """"""

    @abstractmethod
    def get_storage_account_key(self, storage_account_name: str) -> str:
        """"""

    @abstractmethod
    def add_ip_network_rules(self, storage_account_name: str, whitelist_addresses: List[str],
                             resource_group_name: str, firewall_rule_name: str = None):
        """"""

    @abstractmethod
    def remove_ip_network_rules(self, storage_account_name: str, whitelist_addresses: List[str],
                                resource_group_name: str, firewall_rule_name: str = None):
        """"""

    @abstractmethod
    def add_vnet_network_rule(self, storage_vnet_network_rule: StorageVnetIPNetworkRule):
        """"""

    @abstractmethod
    def remove_vnet_network_rule(self, storage_vnet_network_rule: StorageVnetIPNetworkRule):
        """"""

    @abstractmethod
    def update_account_networking(self, storage_account_name: str, allow: bool):
        """"""

    @abstractmethod
    def download_blob_to_local_path(self, destination_path: str, blob_name: str,
                                    container_name: str, account_name: str):
        """"""

    @abstractmethod
    def create_container(self, container_name: str, account_name: str):
        """"""
    
    @abstractmethod
    def upload_blob(self, blob_name: str, container_name: str, account_name: str, local_path: str):
        """"""

    @abstractmethod
    def create_table(self, table_name: str, storage_account_name: str):
        """"""

    @abstractmethod
    def upsert_table_entry(self, table_name: str, storage_account_name: str, entry: dict):
        """"""

    @abstractmethod
    def get_table_entry(self, table_name: str, storage_account_name: str, partition_key: str, row_key: str) -> dict:
        """"""


class StorageHandler(HandlerBase, IStorageHandler):
    def __init__(self, app_config: AppConfig, storage_manager: IAzStorageManager,
                 datalake_deploy_workflow: DatalakeDeployWorkflow):
        HandlerBase.__init__(self, app_config=app_config)
        self.__storage_manager = storage_manager
        self.__datalake_deploy_workflow = datalake_deploy_workflow

    def deploy_datalake_directories(self, solution_name, storage_account_name, recursive: bool = False,
                                    permissions: str = "r", path: str = '"/"'):
        """
        :param solution_name: Name of solution for finding config files
        :param storage_account_name: Name of the storage account to deploy to
        :param recursive: Install acls recursively. Needed for the creation of multiple layers of files. This can be much slower
        :param permissions: What permissions the service principal should get
        :param path: The path to start applying the deployment
        :return: None
        """
        datalake_state_path = path_defaults.get_datalake_state_path(app_config=self._app_config,
                                                                    solution_name=solution_name)
        datalake_json = import_local_json(f'{datalake_state_path}/datalake.json')

        for container in datalake_json['containers']:
            storage_container = StorageContainer(container_name=container['container-name'],
                                                 storage_account_name=storage_account_name)
            datalake_state = DatalakeState(storage_container=storage_container,
                                           datalake_json=container,
                                           recursive=recursive,
                                           permissions=permissions,
                                           path=path)
            self.__datalake_deploy_workflow.run(request=datalake_state)

    def get_storage_account_key(self, storage_account_name: str) -> str:
        return self.__storage_manager.get_storage_account_key(storage_account_name)

    def add_ip_network_rules(self, storage_account_name: str, whitelist_addresses: List[str],
                             resource_group_name: str, firewall_rule_name: str = None):
        name = firewall_rule_name or ""
        for ip_address in whitelist_addresses:
            firewall_rule_cidr = FirewallRuleCIDR(
                name=name,
                cidr_ip_range=ip_address
            )
            storage_ip_network_rule = StorageIPNetworkRule(
                storage_account_name=storage_account_name,
                resource_group_name=resource_group_name,
                firewall_rule_cidr=firewall_rule_cidr
            )
            self.__storage_manager.add_ip_network_rule(storage_ip_network_rule=storage_ip_network_rule)

    def remove_ip_network_rules(self, storage_account_name: str, whitelist_addresses: List[str],
                                resource_group_name: str, firewall_rule_name: str = None):
        name = firewall_rule_name or ""
        for ip_address in whitelist_addresses:
            firewall_rule_cidr = FirewallRuleCIDR(
                name=name,
                cidr_ip_range=ip_address
            )
            storage_ip_network_rule = StorageIPNetworkRule(
                storage_account_name=storage_account_name,
                resource_group_name=resource_group_name,
                firewall_rule_cidr=firewall_rule_cidr
            )
            self.__storage_manager.remove_ip_network_rule(storage_ip_network_rule=storage_ip_network_rule)

    def add_vnet_network_rule(self, storage_vnet_network_rule: StorageVnetIPNetworkRule):
        return self.__storage_manager.add_vnet_network_rule(storage_vnet_network_rule=storage_vnet_network_rule)

    def remove_vnet_network_rule(self, storage_vnet_network_rule: StorageVnetIPNetworkRule):
        return self.__storage_manager.remove_vnet_network_rule(storage_vnet_network_rule=storage_vnet_network_rule)

    def update_account_networking(self, storage_account_name: str, allow: bool):
        return self.__storage_manager.update_account_networking(storage_account_name=storage_account_name,
                                                                allow=allow)

    def download_blob_to_local_path(self, destination_path: str, blob_name: str,
                                    container_name: str, account_name: str):
        storage_blob = StorageBlobSource(name=blob_name, local_path=destination_path,
                                         container_name=container_name, storage_account_name=account_name)
        return self.__storage_manager.download_blob(storage_blob=storage_blob)

    def create_container(self, container_name: str, account_name: str):
        storage_container = StorageContainer(container_name=container_name, storage_account_name=account_name)
        return self.__storage_manager.create_container(storage_container=storage_container)

    def upload_blob(self, blob_name: str, container_name: str, account_name: str, local_path: str, tier: str):
        storage_blob = StorageBlobSource(name=blob_name, container_name=container_name, storage_account_name=account_name,
                                         local_path=local_path, tier=tier)
        return self.__storage_manager.upload_blob(storage_blob=storage_blob)

    def create_table(self, table_name: str, storage_account_name: str):
        """
        Creates a table in an azure storage account
        :param table_name: The name of the table
        :param storage_account_name: The name of the storage account
        :return: None if success - Throws AzCliExceptions on failure
        """
        azure_table = AzureTable(
            table_name=table_name,
            storage_account_name=storage_account_name
        )

        self.__storage_manager.create_table(table=azure_table)

    def upsert_table_entry(self, table_name: str, storage_account_name: str, entry: dict):
        """
        Upserts an entry into an azure table in a storage account
        :param table_name: The name of the table
        :param storage_account_name: The name of the storage account
        :param entry: The table entry
        :return: AzCliResponse
        """
        if entry.get("PartitionKey") is None:
            raise KeyError("Azure Table Storage Entry must have a field named PartitionKey")

        if entry.get("RowKey") is None:
            raise KeyError("Azure Table Storage Entry must have a field named RowKey")

        entry_string = ""
        for key, value in zip(entry.keys(), entry.values()):
            entry_string = entry_string + f"\"{key}={value}\" "

        azure_table_entry = AzureTableEntry(
            table_name=table_name,
            storage_account_name=storage_account_name,
            entry=f'{entry_string}',
            partition_key=entry.get("PartitionKey"),
            row_key=entry.get("RowKey")
        )

        try:
            self.__storage_manager.show_table_entry(table_entry=azure_table_entry)
            response = self.__storage_manager.replace_table_entry(table_entry=azure_table_entry)
        except AzCliResourceDoesNotExist:
            response = self.__storage_manager.create_table_entry(table_entry=azure_table_entry)

        return response

    def get_table_entry(self, table_name: str, storage_account_name: str, partition_key: str, row_key: str) -> dict:
        """
        Queries an entry into an azure table in a storage account
        :param table_name: The name of the table
        :param storage_account_name: The name of the storage account
        :param partition_key: The partition key of the entry
        :param row_key: The row key of the entry
        :return: AzCliResponse
        """
        azure_table_entry = AzureTableEntry(
            table_name=table_name,
            storage_account_name=storage_account_name,
            entry="",
            partition_key=partition_key,
            row_key=row_key
        )
        return self.__storage_manager.get_table_entry(table_entry=azure_table_entry)
