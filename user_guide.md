# User Guide for runVEGAS package at UCLA


## Use Cases

### Specify Cuts

The runVEGAS package runs with medium cuts by default but you can specify the cuts you need for your analysis purpose!

The package has built-in values for soft, medium and hard cuts so you can specify which cuts to use for your analysis with the flag `-cuts`. 

For example, you can call

````shell
scriptGen.py -cuts='soft' runlist_ext.csv
scriptGen.py -cuts='med' runlist_ext.csv
scriptGen.py -cuts='hard' runlist_ext.csv
````

I'm also working to get it to read in a config file so you can further tweak the cuts!



### Specify Exclusion Regions

To pass in your list of exclusion regions, use the flag `-exclRegions='path-to-xlist'` in scriptGen.py. 

For example, you can do

```shell
scriptGen.py -exclRegion='path-to-xlist' runlist_ext.csv
```



The exclusion list takes the form of

```
src_ra src_dec exclusion_radius src_name
```

An example for exclusion regions in the galactic ridge is as follows:

```
266.417 -29.008 0.3 SgrA*
266.847 -28.152 0.3 G0.9+0.1
265.250 -30.200 0.3 J1741-302
266.260 -30.370 0.3 J1745-303
266.582 -28.966 0.3 J1746-289
266.599 -28.876 0.3 J1746-285
266.835 -28.385 0.3 SgrB2
267.044 -28.107 0.3 D0
266.691 -28.621 0.3 D1
266.095 -29.474 0.3 D2
265.952 -29.867 0.3 D3
```



