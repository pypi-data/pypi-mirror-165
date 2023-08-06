import setuptools

setuptools.setup(
    name='batch_signals_to_bigquery',
    version='0.1',
    description='Dependencies',
    install_requires=[
        "google-cloud-bigquery==2.30.1",
        "google==3.0.0",
        "google-cloud-firestore==2.3.4",
        "google-cloud-storage==1.43.0",
        "google-cloud-pubsub==2.11.0",
        "dynaconf",
        "txp[cloud]"
    ],
    packages=setuptools.find_packages()
)
