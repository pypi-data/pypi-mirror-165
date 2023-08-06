0.7.0 - simplifications
-----------------------

 - simplified the column names constants
 - the cli command is changed back to `sensospot_parse`
 - added more documentation
 - added type hints


0.6.0 - doing splits
--------------------

 - the modules `utils` and `dynamic_range` were deleted and will be moved into a separate project
 - the resulting output file format is now a tab-delimered csv for more compability


0.5.0 - real life fixes
-----------------------

 - parsing parameters now sets the exposure time as float
 - parsing metadata fails silently
 - big rework on column names
 - only most necessary functions exposed on import of package
 - renamed cli command to `parse_sensospot_data`
 - moved some functionality in separate modules `utils` and `dynamic_range`
 
0.5.1
=====
 - added standard aggregates functionality to utlis
 - exposed `utils` api functions in package

0.5.2
=====
 - providing the normalized exposure time to `normalize_values` is now optional

0.5.3
=====
 - renaming function `split_data_frame` to `split` 
 - added --quite flag to cli to bypass sanity checks
 - removed the aggregate functions from the utils module, is now a spearate project

0.5.4
=====
 - added api function "apply_map"


0.4.0  - api changes
--------------------

 - normilization api for measurement changed to 
   `split_channels` 
 - named tuple for exposure maps exposed in package as
   `ExposureInfo` 


0.3.0  - normalization api
--------------------------

 - normilization api for single channels has changed and is exposed in package
   `normalize_channel(single_channel_data_frame, normalized_time_in_ms)`
   


0.2.0  - remove custom normalization map
----------------------------------------

 - normilization of exposure time is always to the largest time available


0.1.0  - first working version
------------------------------

 - woohoo


0.0.1  - first version
----------------------

 - setting up the project
