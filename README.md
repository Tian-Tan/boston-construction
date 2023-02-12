# boston-construction
A hackbeanpot 2023 project

First, download requirements for the project using `pip install -r requirements.txt`.

To run from a fresh git clone, execute ./update.sh.

Populate the database by accessing http://127.0.0.1:8000/get-data in a web browser.

Send the emails by accessing http://127.0.0.1:8000/mailing-list/activate in a web browser.


# NOTES
to run docker container and get host networking, use --net=host
e.g. `podman build --net=host .`
