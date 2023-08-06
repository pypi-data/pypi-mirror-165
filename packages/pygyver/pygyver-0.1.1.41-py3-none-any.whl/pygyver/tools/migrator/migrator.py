import logging
from google.cloud import bigquery_datatransfer, bigquery_datatransfer_v1
from google.cloud import bigquery
import google
import time
from google.protobuf.timestamp_pb2 import Timestamp

class Migrator():
    
    def __init__(self, source_project_id, destination_project_id):
        self.source_project_id = source_project_id
        self.destination_project_id = destination_project_id

    def _create_dataset(self, dataset_id, location):
        
        client = bigquery.Client()
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = location

        dataset = client.create_dataset(dataset, timeout=30) 
        logging.info(f"Created dataset {dataset_id}")

    def _build_dataset_migration_configuration(self, transfer_client, source_dataset_id, destination_dataset_name):
        
        transfer_config = bigquery_datatransfer.TransferConfig(
            destination_dataset_id=destination_dataset_name,
            display_name=f"{source_dataset_id}_to_{self.destination_project_id}.{destination_dataset_name}",
            data_source_id="cross_region_copy",
            params={
                "source_project_id": self.source_project_id,
                "source_dataset_id": source_dataset_id,
            },
            schedule=None
            ,
            schedule_options=bigquery_datatransfer_v1.types.ScheduleOptions(
                disable_auto_scheduling=True
            )
        )

        transfer_config = transfer_client.create_transfer_config(
            parent=transfer_client.common_project_path(self.destination_project_id),
            transfer_config=transfer_config,
        )

        return transfer_config

    def _get_dataset_attributes(self, dataset_id):

        attributes = {}

        # Construct a BigQuery client object.
        client = bigquery.Client()

        dataset = client.get_dataset(dataset_id)  # Make an API request.

        attributes["location"] = dataset.location

        return attributes
    
    def _trigger_data_transfer_run(
            self,
            transfer_client: object,
            config_name: str
    ) -> str:
        """
        Triggers a data transfer run immediately (on-demand schedule).
        - transfer_client: bigquery_datatransfer client object
        - config_name: full GCP resource name
            e.g projects/{}/locations/{}/transferConfigs/{}
        - returns: run_id
        """
        start_time = Timestamp(seconds=int(time.time() + 10))
        request = bigquery_datatransfer.StartManualTransferRunsRequest(
            {"parent": config_name, "requested_run_time": start_time}
        )
        # trigger
        response = transfer_client.start_manual_transfer_runs(request, timeout=360)

        # get run_id
        run_id = response.runs[0].name

        return run_id


    def _check_data_transfer_run_state(
            self,
            transfer_client: object,
            run_id: str
    ) -> str:
        """
        Returns the state of a data transfer run.
        - transfer_client: bigquery_datatransfer client object
        - run_id: full GCP resource name
            e.g {config_name}/runs/{}
        - returns: status (PENDING / SUCCEEDED etc)
        """
        # request
        request = bigquery_datatransfer.GetTransferRunRequest(name=run_id)
        response = transfer_client.get_transfer_run(request=request, timeout=360)

        # get state
        state = response.state.name

        return state


    def wait_delete_datatransfers(
            self,
            runs : list,
            wait_limit: int = 60
    ) -> bool:
        """
            Waits for the runs in the list to finish
            - transfer_client: bigquery_datatransfer client object
            - runs: a list of dicts, each one should contain the keys "run_id" and "trasnfer_config"]
            - wait_limit : int, default=60
            - returns: True if successful
        """
        
        transfer_client = bigquery_datatransfer.DataTransferServiceClient()

        # state check loop
        total_wait = 1
        current_wait = 1
        runs_to_check = runs

        while total_wait <= wait_limit:
            
            if len(runs_to_check) == 0:
                return True

            logging.info(f"Waiting for {60 * current_wait} seconds to check state")
            time.sleep(60 * current_wait)

            for run in runs_to_check:

                run_id = run["run_id"]
                config_name = run["transfer_config"]
                state = self._check_data_transfer_run_state(transfer_client, run_id)
                if state == "SUCCEEDED":
                    logging.info(f"State for run_id '{run_id}' is '{state}'")

                    runs_to_check.remove(run)

                    logging.info(f"Deleting the above configuration")
                    self._delete_config(transfer_client, config_name)
                    logging.info(f"Configuration was deleted successfully")

                elif state == "PENDING":
                    logging.info(f"State for run_id '{run_id}' is '{state}'")
                    current_wait += 1
                    total_wait += current_wait
                else:
                    raise ValueError(f"Unknown state for run_id '{run_id}': '{state}'")
            
        raise TimeoutError(f"Data transfer for run_id '{run_id}' timed out")



    def _delete_config(self, transfer_client, config_name):
        
        try:
            transfer_client.delete_transfer_config(name=config_name)
        except google.api_core.exceptions.NotFound:
            logging.info("Transfer config not found.")
        else:
            logging.info(f"Deleted transfer config: {config_name}")


    def migrate_dataset(self, 
                        source_dataset_name:str, 
                        destination_dataset_name:str = "same", 
                        destination_location:str = "same") -> dict:
        """
            Configures the datatransfer and triggers it. (Need to call wait_delete_datatranfer as a next ste)
            - source_dataset_name: str , the name of the dataset that need to be migrated
            - destination_dataset_name: str, optional, if not set, dataset will be migrated to the new project with the same name as source
            - destination_location : str, ("US","EU", etc) optional, if not set, dataset will be migrated to the new project stored in the same region
            - returns: True if successful
        """

        transfer_client = bigquery_datatransfer.DataTransferServiceClient()
        
        source_dataset_id = f"{self.source_project_id}.{source_dataset_name}"
        source_dataset_attributes = self._get_dataset_attributes(source_dataset_id)
        
        destination_location = source_dataset_attributes["location"] if destination_location == "same" else destination_location
        destination_dataset_name = source_dataset_name if destination_dataset_name == "same" else destination_dataset_name
        
        destination_dataset_id = f"{self.destination_project_id}.{destination_dataset_name}"
        self._create_dataset(destination_dataset_id, destination_location)
        logging.info(f"Created destination dataset '{destination_dataset_id}' in location '{destination_location}' successfully")

        transfer_config = self._build_dataset_migration_configuration(
            transfer_client,
            source_dataset_name, 
            destination_dataset_name
            )

        logging.info(f"Created transfer config: {transfer_config.name}")

        run_id = self._trigger_data_transfer_run(
            transfer_client,
            transfer_config.name
        )

        return {"run_id" : run_id, "transfer_config" : transfer_config.name}
