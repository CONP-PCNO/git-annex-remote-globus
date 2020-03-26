# git-annex special remote for Globus 

git-annex-remote-globus adds to git-annex the ability to retrieve files present in [Globus.org](https://www.globus.org/).


## Requirements

* Datalad
* Git annex


## Setup

1. Initialize a virtual environment
2. Install the repository with ``` pip install git-annex-remote-globus```
3. Install the dataset to be retrieved via the remote ```datalad install -r <dataset>```and ```cd <dataset>```. 
4. If it is the first time a user uses globus remote, authentication to Globus.ors must take place to continue
    Thus run ```git-annex-remote-globus setup``` anf follow the steps. Gmail and ORCHID are supported
5. If the dataset was previously registered which is expected, it enough to enable the globus remote by running:
    
    ```git annex enableremote globus```
    
    else, full initialization must be run:
    
    ```git annex enableremote globus type=external externaltype=globus encryption=none endpoint=<dataset_name> fileprefix=<prefix_path>```
    
    where <datset_name> is the name of the dataset in Globus.org and <prefix_file> is the prefix path before the dataset files in Globus.org
6. Try to download the desired file with
    
    ```datalad get path/to/file```
    
If every step was followed correctly, it will ger successfully downloaded !


## Testing procedure for changes

This procedure is only for testing purposes:

1. git clone this repository: ``` git clone https://github.com/CONP-PCNO/git-annex-remote-globus.git``` and checkout the branch you want to test
    with `git checkout -a <branch>`. Using a virtual environment is suggested
2. In a different folder, install the following dataset: ```datalad install -r <dataset>```and ```cd <dataset>```. 
From now on we are going to work from the dataset repo location where you cd'ed
3. Add the path of your git-annex-remote-globus location to your current dataset PATH
4. In the repository, run `git-annex-remote-globus setup` and follow the instructions to authenticate. Gmail and ORCHID are supported
    If may you need in a fresh virtual env, install dependencies specified. It will work after that
5. Run `git annex enableremote globus`. This command should initialize the remote successfully if everything went all right
6 Try to download any file with `git annex get path/to/file`


## Manually registering a dataset with globus remote (internals)

In order to understand how globus remote works, we can give an example with one dataset file. 
The dataset file we will be working on is currently not available to use as it only includes a symlink generated by annex. 
First the globus remote must be initialized to start the process. Then the file can be registered with Globus and git annex
will then be able to get access to its Globus location to retrieve its content. 
The following steps are usually performed when datasets files get registered with the globus remote 
for the first time. Dedicated tools automate this process, but the point of this section is to explain in details what
happens when datasets are registered in the first place. So initialization first. 
We use [this](datalad install https://github.com/conpdatasets/FRDR-multimodal.git) repository as an example

```
git annex initremote globus type=external externaltype=globus encryption=none endpoint=FRDR_Prod_2 fileprefix=/5/published/publication_170/submitted_data/
```
To debug `git-annex initremote --debug`.

Run the following to find the file symlink, which includes the file hash

```
cd FRDR-multimodal
```
```
ll 2015_11_18_cortex/mask/mask.mat
```

The last command will allow you to visualize the symlink which contains the [MD6 hash](https://en.wikipedia.org/wiki/MD5) of the file content.
At this point, globus does not know anything about this file and its symlink, as you can see running the following command

```
git annex whereis 2015_11_18_cortex/mask/mask.mat
```

Globus is not listed indeed. We now need to tell globus of the existence of the file based on its hash, which we call key.
When initialized, globus was given a location ID by annex which distributes one to every remote it communicates with.
We can find Globus location ID by running the following command from the dataset root location:

```
cat .git/config
```

This file shows the remote "globus" which we just initialized, and the globus remote location ID given by annex. 
Therefore we need to make this location know about the file we want to retrieve.

To do that, run:

```
git annex setpresentkey <file_hash> <annex-uuid> 1
```

For example, for the file we are working with 2015_11_18_cortex/mask/mask.mat we would run:

```
git annex setpresentkey MD5E-s572--1e5e0b0c5896d16ac14170c8f546d4e1.mat 056ae102-61ce-4417-9180-b45eecc45082 1
```

The 1 at the end tells globus about the existence of this file with its given key. A 0 would remove knowledge of the file

Now, to make sure globus knows about this file, we can run the command below.

``` 
git annex whereis 2015_11_18_cortex/mask/mask.mat
```

At this point we can go ahead and register a url to be associated with the given file key. In this way, we will connect the points and tell annex where in globus
the file is located, so it can reach it. Therefore we will add a globus url which will contain the endpoint name and fileprefix:

```
git annex registerurl MD5E-s572--1e5e0b0c5896d16ac14170c8f546d4e1.mat globus://frdr_prod_2/5/published/publication_170/submitted_data/2015_11_18_cortex/mask/mask.mat
```

At this point we can finally obtain the file running the command below
```
git annex get 2015_11_18_cortex/mask/mask.mat
```

This is the point where the file becomes available on your machine

You can run whereis again to check that

``` 
git annex whereis 2015_11_18_cortex/mask/mask.mat
```


Moreover you can always run the following command if you want to mack sure the file has not been modified in globus compared to your previously downloaded version
by using the annex-uuid again

```
git annex checkpresentkey MD5E-s572--1e5e0b0c5896d16ac14170c8f546d4e1.mat 056ae102-61ce-4417-9180-b45eecc45082
```

It will return Success if the file in Globus has not change


## Issues, Contributing

If you run into any problems, please check for issues on [GitHub](https://github.com/CONP-PCNO/git-annex-remote-globus/issues).
Please submit a pull request or create a new issue for problems or potential improvements.

## License

MIT
