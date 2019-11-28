# GLOBUSannex





#### Globus Connect Personal

This option will allow you to share and transfer files to and from your laptop or desktop computer — even if it's behind a firewall. Supported operating systems include: macOS, Windows and Linux.
Globus Connect Server
This option is primarily intended for resource providers who wish to offer reliable, secure, high-performance research data management capabilities to their users and their collaborators, directly from their own storage. Globus Connect Server runs on a number of Linux distributions



#### Globus Connect Server

This option is primarily intended for resource providers who wish to offer reliable, secure, high-performance research data management capabilities to their users and their collaborators, directly from their own storage. Globus Connect Server runs on a number of Linux distributions


Installation summary of Globus Connect Server (this happens only once)

In this section, we summarize the steps for creating an endpoint and making it accessible to users with Globus Connect Server version 5.

    The server administrator installs the Globus Connect Server version 5 software and uses it to create the endpoint. The endpoint includes the configuration for the server and its network use.

    The administrator registers the endpoint with Globus so that Globus can be used to secure access to the endpoint.

    The administrator creates one or more storage gateways (see terminology above) to define access policies for the endpoint’s storage.

    The administrator may also create mapped collections that allow data access by users who have local accounts.



With the above in place, authorized users interact with the endpoint as follows with git annex.

    Discover storage gateways and create new guest collections as allowed by storage gateway policies.

    Access data on existing collections using the GridFTP and/or HTTPS protocols. They may use a web browser (for HTTPS links), the Globus Web app, the Globus command-line interface (CLI), the Globus software development kit (SDK), or the Globus REST APIs.






COMMANDS:

Initialize remote:
$ git-annex-remote-globus setup
$ git annex initremote globus -d  type=external externaltype=globus encryption=none endpoint=FRDR_Prod_2 fileprefix=/5/published/publication_170/submitted_data/