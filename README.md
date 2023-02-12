# boston-construction
A hackbeanpot 2023 project

# NOTES
to run docker container and get host networking, use --net=host
e.g. `podman build --net=host .`

# TODO
- use permittee instead of contractor? may be more interesting
- document stuff, code cleanup, etc
- maybe if user has been notified of some construction projects in the past week, don't send.
- just save a list of integers in mailingrecord, the stuff we've already seen. (one user to many integer ids / pks of constructionrecords)
- give specific data types https://docs.djangoproject.com/en/dev/ref/models/fields/#commaseparatedintegerfield
