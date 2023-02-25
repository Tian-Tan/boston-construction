# boston-construction
A hackbeanpot 2023 project

For a demo, see the devpost:

https://devpost.com/software/bpworks

# notes

As of 2023-02-14, API keys are deactivated.

First, download requirements for the project using `pip install -r requirements.txt`.

To run from a fresh git clone, execute django_backend/update.sh.

It will ask you to create an admin panel account - something basic is fine, you can leave email blank.

Populate the public works database by accessing http://127.0.0.1:8000/get-data in a web browser.

Send the emails by accessing http://127.0.0.1:8000/mailing-list/activate in a web browser.

to run docker container and get host networking, use --net=host
e.g. `podman build --net=host .`
