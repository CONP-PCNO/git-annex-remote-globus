# git-annex special remote for Globus 

git-annex-remote-globus adds to git-annex the ability to retrieve files which are available through Globus.

* Note! code is not yest distributed therefore Usage information are going to change soon

## Usage

1. git clone this repository: ``` git clone https://github.com/CONP-PCNO/git-annex-remote-globus.git```
2. In a different folder, clone the following dataset: ```git clone https://github.com/conpdatasets/FRDR-multimodal.git```and ```cd FRDR-multimodal```
    from now on we are going to work from the dataset repo location where you cd'ed
3. Add the path of your git-annex-remote-globus location to your current PATH
4. Initialize a virtual environment and install requirements.txt. You may need to add the git-globus-annex path manually
 here not to make the system confuse qith the filename of other repos: run ```pip install -r path/to/git-annex-remote-globus/requirements.txt```
5. In the repository, run `git-annex-remote-globus setup` and follow the instructions to authenticate. Gmail and ORCHID are supported
6. Add a remote for globus. This example:

   * Adds a git-annex remote called `globus`
   * Encrypts can be set to none for now
   * The option -d will enable a verbose output
   * The endpoint name corresponds to the name of the dataset in Globus so globus can find it
   * As the prefixfile the location storing your files in Globus

```
git annex initremote globus -d type=external externaltype=globus encryption=none endpoint=FRDR_Prod_2 fileprefix=/5/published/publication_170/submitted_data/
```
To debug `git-annex initremote --debug`.
IMPORTANT: to reinitialize the remote you can run ```git annex enableremote globus```

Now globus is ready to use !

### Options
Options specific to git-annex-remote-googledrive
* `prefix` - The path to the folder that will be used for the remote. If it doesn't exist, it will be created.
* `root_id` - Instead of the path, you can specify the ID of a folder. The folder must already exist. This will make it independent from the path and it will always be found by git-annex, no matter where you move it. Can also be used to access shared folders which you haven't added to "My Drive".
* `token` - Path to the file in which the credentials were stored by `git-annex-remote-googledrive setup`. Default: token.json
* `keep_token` - Set to `yes` if you would like to keep the token file. Otherwise it's removed during initremote. Default: no

General git-annex options
* `encryption` - One of "none", "hybrid", "shared", or "pubkey". See [encryption](https://git-annex.branchable.com/encryption/).
* `keyid` - Specifies the gpg key to use for encryption.
* `mac` - The MAC algorithm. See [encryption](https://git-annex.branchable.com/encryption/).
* `exporttree` - Set to `yes` to make this special remote usable by git-annex-export. It will not be usable as a general-purpose special remote.
* `chunk` - Enables [chunking](https://git-annex.branchable.com/chunking) when storing large files.

## Using an existing remote (note on repository layout)

If you're switching from git-annex-remote-rclone or git-annex-remote-gdrive and already using the `nodir` structure, 
it's as simple as typing `git annex enableremote <remote_name> externaltype=googledrive`. If you were using a different structure, you will be notified to run `git-annex-remote-googledrive migrate <prefix>` in order to migrate your remote to a `nodir` structure.

If you have a huge remote and the migration takes very long, you can temporarily use the [bash based git-annex-remote-gdrive](https://github.com/Lykos153/git-annex-remote-gdrive) which can access the files during migration. I might add this functionality to this application as well ([#25](https://github.com/Lykos153/git-annex-remote-googledrive/issues/25)). 

I decided not to support other layouts anymore as there is really no reason to have subfolders. Google Drive requires us to traverse the whole path on each file operation, which results in a noticeable performance loss (especially during upload of chunked files). On the other hand, it's perfectly fine to have thousands of files in one Google Drive folder as it doesn't even use a folder structure internally.

## Choosing a Chunk Size

Choose your chunk size based on your needs. By using a chunk size below the maximum file size supported by
your cloud storage provider for uploads and downloads, you won't need to worry about running into issues with file size.
Smaller chunk sizes: leak less information about the size of file size of files in your repository, require less ram,
and require less data to be re-transmitted when network connectivity is interrupted. Larger chunks require less round
trips to and from your cloud provider and may be faster. Additional discussion about chunk size can be found
[here](https://git-annex.branchable.com/chunking/) and [here](https://github.com/DanielDent/git-annex-remote-rclone/issues/1)

## Google Drive API lockdown
Google has started to lockdown their Google Drive API in order to [enhance security controls](https://cloud.google.com/blog/products/identity-security/enhancing-security-controls-for-google-drive-third-party-apps) for the user. Developers are urged to "move to a per-file user consent model, allowing users to more precisely determine what files an app is allowed to access". Unfortunately they do not provide a way for a user to allow access to a specific folder, so git-annex-remote-googledrive still needs access to the entire Drive in order to function properly. This makes it necessary to get it verified by Google. Until the application is approved (IF it is approved), the OAuth consent screen will show a warning ([#31](https://github.com/Lykos153/git-annex-remote-googledrive/issues/31)) which the user needs to accept in order to proceed.

It is not yet clear what will happen in case the application is not approved. The warning screen might be all. But it's also possible that git-annex-remote-googledrive is banned from accessing Google Drive in the beginning of 2020. If you want to prepare for this, it might be a good idea to look for a different cloud service. However, it seems that [rclone](https://rclone.org) got approved, so you'll be able to switch to [git-annex-remote-rclone](https://github.com/DanielDent/git-annex-remote-rclone) in case git-annex-remote-googledrive is banned. To do this, follow the steps described in its README, then type `git annex enableremote <remote_name> externaltype=rclone rclone_layout=nodir`. This will not work for export-remotes, however, as git-annex-remote-rclone doesn't support them.

If you use git-annex-remote-googledrive to sync with a **GSuite account**, you're on the safe side. The GSuite admin can choose which applications have access to its drive, regardless of whether it got approved by Google or not.

## Issues, Contributing

If you run into any problems, please check for issues on [GitHub](https://github.com/Lykos153/git-annex-remote-gdrive/issues).
Please submit a pull request or create a new issue for problems or potential improvements.

## License

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