# <font color="Salmon">data</font>

This directory contains data collected throughout the process.

## <font color="IndianRed">Items:</font>
- <font color="orange">{school}</font>: the folder containing all the data for the particular school.

## <font color="IndianRed">Items within each folder:</font>
- <font color="orange">data_during_process</font>: less important or outdated data collected during the process.
- <font color="orange">{school}_directories_sans_med.json</font>: contains links to each department's directory.
- <font color="orange">{school}_w_profiles_processed.json</font>: contains the processed profiles scraped from each department.
- <font color="orange">{school}_w_profiles_detected_pct.json</font>: contains the gender and race data in the form of pct.
- <font color="orange">{school}_detected_pct.json</font>: contains the gender and race inferred from pct data.
- <font color="orange">{school}_v2_finalized.json</font>: on top of {school}_detected_pct, having metadata added for each department.
- <font color="orange">{school}_NCES_pct.json</font>: contains the data scraped from NCES in the form of pct.

## <font color="IndianRed">To do:</font>
- Change the naming of the files for better clarity.
- Change the input and output locations in the notebooks to reflect the new structure of the data folder.
