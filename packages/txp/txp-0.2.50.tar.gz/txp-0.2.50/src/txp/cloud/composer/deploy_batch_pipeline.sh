#!/bin/bash

composer_bucket=$1
composer_resources_bucket=$2

composer_dags_folder="$composer_bucket/dags"
composer_resources_batch_pipeline_folder="$composer_resources_bucket/pipelines/batch_pipeline"

script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $script_dir
cd ../
rm -rf dist
gsutil cp ./pipelines/batch_pipeline/setup.py $composer_dags_folder
gsutil cp ./pipelines/batch_pipeline/batch_pipeline.py $composer_resources_batch_pipeline_folder

location=$3
production=$4

cd ./composer

if [[ ( $production == "production") ]]; then
  echo Deploying batch pipeline as production
  gcloud composer environments update txp-composer --update-pypi-packages-from-file requirements.txt \
    --location $location
  gcloud composer environments update txp-composer --location $location --update-env-variables=PENDING_SIGNALS_CHUNKS_COLLECTION=pending_signal_chunks,SIGNALS_QUEUE_COLLECTION=signals_queue,DATASET=telemetry,MODEL_SIGNALS_TOPIC_NAME=txp-model-serving-signals,DATA_LAKE=tranxpert-mvp-telemetry-data-lake,RESOURCES_BUCKET=$composer_resources_bucket,LOCATION=$location
  gcloud composer environments storage dags import --environment txp-composer --location $location \
    --source ./dag_signals_publisher.py --project tranxpert-mvp

  cd ../cloud_functions/store_telemetry_event_to_data_lake
  gcloud functions deploy store_telemetry_event_to_data_lake --runtime python37 --trigger-topic txp-telemetry-batch

else
  echo Deploying batch pipeline as test
  gcloud composer environments update txp-composer-test --update-pypi-packages-from-file requirements.txt \
    --location $location
  gcloud composer environments update txp-composer-test --location $location --update-env-variables=LOCATION=$location
  gcloud composer environments storage dags import --environment txp-composer-test --location $location \
    --source ./dag_signals_publisher.py --project tranxpert-mvp

  cd ../cloud_functions/store_telemetry_event_to_data_lake
  gcloud functions deploy store_telemetry_event_to_data_lake_test --entry-point store_telemetry_event_to_data_lake \
    --runtime python37 --trigger-topic txp-telemetry-batch-test \
    --update-env-vars DATA_LAKE_BUCKET_NAME=telemetry-data-lake-test,PENDING_SIGNAL_CHUNKS_COLLECTION=pending_signal_chunks_test
fi
