# Running VEGAS at UCLA

## Preliminary

### Setting up your environment 

Both approaches are already set up for all UCLA users. Pick the one that works the best for your analysis needs! Feel free to reach out if you encounter any issue!

#### Docker (recommended)

- Docker is a very easy and organized way to set up the environment! Try call `docker` in the command line to see if you have the right permission! If you see an error message, contact Takeru to get added to the docker group!

- Once you can call docker, you are ready to go! Docker basically build individual containers (docker images) to run in different environments! 

- Docker images to use

  `77e08ff5c155` : VEGAS 2.5.9

  `333121b9bc36`: VEGAS 2.5.10

- You can go into the containers by calling

  ```shell
  docker run -it <imageid> bash
  ```

  You can test that VEGAS is running the correct version by calling

  ```
  vaStage1
  ```
  

#### Shell script (.bashrc)

- See https://veritas.sao.arizona.edu/wiki/Gamma_cluster_users to set up the .bashrc to source

- Note that to use different versions of VEGAS, you will need to either edit the current one or source a new one that configures the environment to the correct version

- You can also try source this for VEGAS 2.5.10 

  ```shell
  source /home/wning/userspace/onboarding/vegasV2510.bashrc
  ```

### Python packages

In order to run the scripts, please make sure you have the relevent packages! You can run the following to install the packages needed for this analysis!
```
python3 -m pip install -U matplotlib
python3 -m pip install scipy
```

Or you can copy the installer.txt in this repo and simply call
```
python3 -m pip install -r installer.txt
```


## Introduction to VEGAS

### Stages of Analysis

Check out what each stage does here:

https://github.com/VERITAS-Observatory/VEGAS/blob/documentation/v2_5_10/documentation/quickExampleAnalysis/Example1.md



### What do you need to run a basic analysis?

1. Environment being set up

2. Runlist

   Go to Loggen to generate a comma-separated runlist for the runs that you want to look at! Copy and save it into a .csv file!

3. Raw data

   Data is stored at UCLA, just copy them over to your scratch directory

4. IRF tables (lt, ea and templates if using ITM)

   Note: this is already set up for UCLA users in the helper package! Currently working for ua (after 201209) with 2.5.10! Will put in more tables when they are ready!



## Helper package for UCLA users

You can find the helper package in `/home/wning/userspace/runVEGAS`. It would be convenient to add a path to this in your `~/.bashrc`.

This package contains:

1. extendRunlist.py

   Extend the comma-separated runlist saved from loggen with additional information needed to generate the scripts

2. copyData.py

   Make a script to copy the necessary data from the database. Once the script is successfully generated, you should be able to submit it to the queue and have the data ready for your analysis!

3. scriptGen.py

   Generate the scripts for each stage to run VEGAS analysis.

4. submitScripts.py

   Submit the scripts to the queue to run. 





## Example

Try run through this example with the UCLA helper package!! Make a directory in your **userspace** to run this example!



Note: This example uses the same runlist as in example 2. It would be helpful to try run through example 1 and 2 in VEGAS documentation to understand what is going on in the analysis! See  https://github.com/VERITAS-Observatory/VEGAS/blob/documentation/v2_5_10/documentation/quickExampleAnalysis/Example2.md



### Set up the environment

#### Running without Docker

Make sure to source the correct bashrc



#### Running with Docker

Still working on getting this ready for UCLA users! Will be working on getting this updated soon!



### Generate a list of files from Loggen

In this example, we will use the same set of crab runs as in example 2. However, instead of the simple runlist, we will be using the comma-separated one that contains more information. Copy the following run numbers to Loggen (https://veritasm.sao.arizona.edu/DQM/loggen.html): 

```
65311 65312 66533 66556 88714 88715
```



It should return you the following list:

```
Date, Run, Source, LSR1, LSR2, LSR3, LSR4, UTC, DUR, USE, MODE, SKY, T1-FIR CRMS, EL, AZ, Hz, TEL, NSB, ATM, T3-FIR CRMS
20121208, 65311, Crab, 65310, 65310, 65310, 65310, 06:40, 30, 30, 0.5E, A, 0.1 (A), 74, 125, 437, 2/1234, 7.2 (d), winter, 0.2
20121208, 65312, Crab, 65310, 65310, 65310, 65310, 07:11, 30, 30, 0.5W, A, 0.1 (A), 79, 154, 438, 2/1234, 7.0 (d), winter, 0.1
20130201, 66533, Crab, 66535, 66535, 66535, 66535, 03:31, 30, 27, 0.5N, A-, 0.1 (A), 79, 146, 458, 2/1234, 6.5 (d), winter, 0.2
20130205, 66556, Crab, 66590, 66561, 66561, 66561, 04:06, 30, 30, 0.5E, A, 0.1 (A), 79, 208, 436, 2/1234, 6.8 (d), winter, 0.1
20180112, 88714, Crab, 88717, 88717, 88717, 88717, 03:59, 30, 30, 0.5N, A, 0.1 (A), 70, 113, 381, 2/1234, 7.2 (d), winter, 0.2
20180112, 88715, Crab, 88717, 88717, 88717, 88717, 04:29, 30, 30, 0.5S, A, 0.1 (A), 75, 131, 384, 2/1234, 7.1 (d), winter, 0.3
```



Copy the list and save it to **runlist_ex3.csv**.



### Extend the runlist with useful information

To automate the script generation process, we extend the runlist with information needed to run VEGAS. 

```shell
python3 extendRunlist.py runlist_ex3.csv runlist_ex3_ext.csv
```



This should return the following extended runlist:

```
Date,Run,Source,LSR1,LSR2,LSR3,LSR4,UTC,DUR,USE,MODE,SKY,T1-FIR CRMS,EL,AZ,Hz,TEL,NSB,ATM,T3-FIR CRMS,arrayConfig,epoch,atm,tels_used,obsConfig,obsMode,databaseTimeCuts,timeCuts
20121208,65311,Crab,65310,65310,65310,65310,06:40,30,30,0.5E,A,0.1 (A),74,125,437,2/1234,7.2 (d),winter,0.2,ua,1213w,61,1234,NOM,wobble,0/0,0/0
20121208,65312,Crab,65310,65310,65310,65310,07:11,30,30,0.5W,A,0.1 (A),79,154,438,2/1234,7.0 (d),winter,0.1,ua,1213w,61,1234,NOM,wobble,0/0,0/0
20130201,66533,Crab,66535,66535,66535,66535,03:31,30,27,0.5N,A-,0.1 (A),79,146,458,2/1234,6.5 (d),winter,0.2,ua,1213w,61,1234,NOM,wobble,"1740/1800,0/120","1740/1800,0/120"
20130205,66556,Crab,66590,66561,66561,66561,04:06,30,30,0.5E,A,0.1 (A),79,208,436,2/1234,6.8 (d),winter,0.1,ua,1213w,61,1234,NOM,wobble,0/0,0/0
20180112,88714,Crab,88717,88717,88717,88717,03:59,30,30,0.5N,A,0.1 (A),70,113,381,2/1234,7.2 (d),winter,0.2,ua,1718w,61,1234,NOM,wobble,0/0,0/0
20180112,88715,Crab,88717,88717,88717,88717,04:29,30,30,0.5S,A,0.1 (A),75,131,384,2/1234,7.1 (d),winter,0.3,ua,1718w,61,1234,NOM,wobble,0/0,0/0
```



### Copy data

To run your analysis, you will need the raw data from the VERITAS database. The copyData.py conveniently copy the data to your scratch directory for you.

```shell
python3 copyData.py runlist_ex3_ext.csv
```



This should generate a `cp_data.sh` script for you. You can either run this directly or submit it to the queue.

If running it directly:

```shell
./cp_data.sh
```

If submitting to the queue:

```shell
qsub -j oe cp_data.sh
```

You can check the status of the jobs you submitted to the queue with `qstat`.


### Generate scripts

Yay now we have the environment setup, the extended runlist, the data copied over and the IRF tables handy (already set up for UCLA users in the scripts, no need to do anything), we are ready to generate the scripts to run the analysis!! Let's first try generate the scripts for a standard analysis with ITM and medium cuts!!

```shell
python3 scriptGen.py runlist_ex3_ext.csv
```



This script should set up three directories: `scripts`, `data` and `log`. All the scripts we just generated can be found in `scripts`! The data directory has 7 subdirectories `stg1`, `stg2`, `stg4`, `stg5`, `stg6_wobble`, `stg6_spectrum` and `stg6_rbm`. The results from each stage will be saved in the corresponding directories! And the logs files for each stage can be found in `log`.



### Run the scripts

There are two options to run these shell scripts!! You can either run them directly on the command line or you can submit them to the queue!! 



#### Option 1: Run directly

To run a script directly, just call (for example for a laser run)

```shell
./scripts/65310_laser_stg1.sh
```



#### Option 2: Submit to the queue 

To submit a single script, you can do

```shell
qsub ./scripts/65310_laser_stg1.sh
```

For UCLA users, a script is available in the helper package to submit all the scripts of a given stage with the specified options. You can submit up to stage 5 together in one go!

To submit the scripts we just generated, try

```shell
python3 submitScripts.py -laser -s1 -s2 -s4 -s5
```



Once all the scripts up to stage 5 are done, we can proceed to stage 6! 

To get the spectrum, run

```shell
python3 submitScripts.py -s6_spectrum
```

And to get the skymaps, run

```shell
python3 submitScripts.py -s6_rbm
```



Yay! You just finish a standard VEGAS analysis of the crab!! You can now view your analysis results in the data directory!! 



## Other helpful links

Jamie set up this nice wiki page to help UCLA users:

https://veritas.sao.arizona.edu/wiki/Gamma_cluster_users

For more information on Docker, here is a wiki page that covers most of the basics:

https://veritas.sao.arizona.edu/OAWGwiki/Setting_Up_Local_Docker
