import setuptools

setuptools.setup(
    name='pub_sub_to_bigquery',
    version='0.1',
    description='Dependencies',
    install_requires=[
        "google-cloud-bigquery==2.30.1",
        "google==3.0.0",
        "google-cloud-firestore==2.3.4"
    ],
    packages=setuptools.find_packages()
)
