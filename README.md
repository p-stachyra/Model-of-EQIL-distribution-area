# Model-of-EQIL-distribution-area
This project aims to create a simulation model for the earthquake-induced landslide (EQIL) area near Zagreb, Croatia to predict the extent (or reach) of the possible landslide (EQIL) triggered by Medvednica mountain’s orogeny.

Landslides are mass movements of soil and rocks along a slope. Landslides occur when the
shear strength of the hillside material decreases due to an increase in the shear stress of the
slope, or due to processes of change in the natural ecosystem caused by anthropogenic
activities (Moresi et al., 2020). Sometimes, landslides can be caused by human activities, or
more so, they can modify the threshold of occurrence of landslides by accelerating the
dynamics of natural processes (Sidle & Bogaard, 2016). They can cause severe damage, and
while most of them occur slowly over time, the most destructive ones happen suddenly after
being triggered by an event such as earthquakes or heavy rainfall (Conners, 2019).
Earthquake-induced landslides (EQIL) are the most destructive secondary natural hazards
associated with earthquakes and are also the focus of this paper (Jibson, 2007).

This research presents a study that aims to estimate earthquake-induced landslide distribution
area and to scrutinize its area-wise morphological characteristics. The results show the
estimates for the Zagreb/Zagorje region in Croatia. In this region, the Medvednica mountain
orogeny triggers seismic events which may potentially lead to earthquake-induced landslides.
This research raises the question: What is the EQIL distribution area in the Zagreb/Zagorje
(Croatia) neighborhood and what is specific for it in terms of terrain characteristics? To
answer it, we estimate the distribution area of an EQIL induced landslide in the region of
Zagreb, Croatia, and study its morphological characteristics.

This kind of research is relevant in terms of avoiding the possible effects of such natural
disasters. Those effects can include road crashes and debris falling which may cause deaths
or destroy properties. Governments and insurers can benefit from estimating
earthquake-induced landslide (EQIL) distribution areas by including their risk while
developing the infrastructure or selling insurance. Furthermore, residents should also know
about the possible dangers of living in such areas.

## The structure of the application
The main program uses the functionality of other modules, gradually creating the outputs 
used in this analysis. The following general overview of the main driver's flow explains the operations performed 
in order to build the simulation model. Each module has a certain task to perform:

1) mapProximity: create_proximity_map function
   - computes and visualizes the EQIL distribution area for the region of interest.
2) unifyResolutions 
   - The resolutions of rasters are unified to follow the smallest, most detailed resolution.
3) cropToDEM
   - The rasters are adjusted to the area of interest (digital elevation model map - DEM)
4) translateToMap
   - The .tif layers are translated to the format recognized by PCRaster library.
   - The outputs are binary rasters on which further operations will be performed
5) extractZone
   - Prepares to include the values only from a certain area, in this case:
     * area within PGA 0.12g contour
     * area of the simulated EQIL distribution area
     * ground failure area estimated by USGS 
6) morphologicalStatistics
   - Computes area-wise statistics for the area of interest:
     * Six morphological variables: topographic wetness index (TWI), profile curvature, 
       vector ruggedness measure (VRM), local relief, slope, distance to streams
     * mean, median, min, max, standard deviation, variation are computed
     * The statistical computation contain experimental part performing its operations
       using Numba just-in-time Python compiler
7) plotMorphology: visualize_csv function
   - produces visualizations of the 6 morphological variables' values distributions. 
     Uses the CSV files containing these values for the 4 areas of interest:
     * area within PGA 0.12g contour
     * area of the simulated EQIL distribution area
     * ground failure area estimated by USGS 
     * entire study area

## Example results
![alt text](https://github.com/p-stachyra/Model-of-EQIL-distribution-area/blob/main/visualizations/sensitivity_analysis.png)

|index|directory             |terrain_variable               |mean_value            |variance_biased       |variance_unbiased     |standard_deviation_biased|standard_deviation_unbiased|max_value    |min_value     |median_value  |
|-----|----------------------|-------------------------------|----------------------|----------------------|----------------------|-------------------------|---------------------------|-------------|--------------|--------------|
|1    |PGA_zone              |dem                            |201.94863257257387    |17079.648327961608    |17080.200477715203    |130.6891285760281        |130.69124101375425         |993.0        |82.0          |157.0         |
|2    |PGA_zone              |distance_stream_downstream     |13901.147484686871    |117626576.87123239    |117631116.33468066    |10845.578678486105       |10845.787953610408         |41508.4      |0.0           |11114.157     |
|3    |PGA_zone              |EQIL_area                      |0.06864826711754674   |0.51290556884061      |0.5129221500182792    |0.7161742587112511       |0.7161858348349813         |10.0         |0.0           |0.0           |
|4    |PGA_zone              |ground_failure_estimate_cropped|0.00044701708876363763|3.7956180887110275e-07|3.7957407932042455e-07|0.0006160858778377433    |0.0006160958361492346      |0.015451672  |0.0           |0.0005625602  |
|5    |PGA_zone              |local_relief                   |3.3305738600615915    |8.717205243711724     |8.717493912009086     |2.9524913621739395       |2.952540247314012          |9.0          |1.0           |1.0           |
|6    |PGA_zone              |profile_curvature              |0.11128384083136816   |3514.897502003044     |3515.0129034575716    |59.286571008981824       |59.28754425220842          |6686.0767    |-6033.268     |-2.7533576e-06|
|7    |PGA_zone              |slope                          |3.5090130031539903    |18.6773326575407      |18.677938710258513    |4.321727971256486        |4.321798087631873          |30.360462    |0.0           |1.8577819     |
|8    |PGA_zone              |TWI_raster                     |-13.016356720274482   |4.404441835135551     |4.404584359868914     |2.0986762101704852       |2.098710165761083          |-4.9608107   |-17.829576    |-13.03805     |
|9    |PGA_zone              |vector_ruggedness_measure      |0.0017229498014403985 |1.2117352018472649e-05|1.2117743747435842e-05|0.0034809987099211413    |0.0034810549762156646      |0.047728363  |9.271834e-08  |0.00037510128 |
|10   |ground_failure_zone   |dem                            |774.4444444444445     |3574.135802469136     |3784.3790849673205    |59.78407649591265        |61.51730719860323          |876.0        |656.0         |774.5         |
|11   |ground_failure_zone   |distance_stream_downstream     |15269.94775390625     |23684853.1151668      |25078079.76900014     |4866.7086532036          |5007.801889951333          |26276.666    |12655.301     |13266.959     |
|12   |ground_failure_zone   |EQIL_area                      |0.8447704580095079    |3.6752518435088657    |3.891443128421152     |1.9170946360336167       |1.9726741059843493         |6.0827627    |0.0           |0.0           |
|13   |ground_failure_zone   |local_relief                   |2.7777777777777777    |0.17283950617283958   |0.1830065359477125    |0.4157397096415491       |0.4277926319464987         |3.0          |2.0           |3.0           |
|14   |ground_failure_zone   |pga_contour_raster_cropped     |0.2724381486574809    |9.888122256788523e-05 |0.00010469776507187848|0.00994390378915068      |0.010232192583795444       |0.29956156   |0.26          |0.26934892    |
|15   |ground_failure_zone   |profile_curvature              |6.398951930306238e-07 |3.5080181788444543e-13|3.714372189364716e-13 |5.922852504363463e-07    |6.094564947036594e-07      |2.3903008e-06|8.7693635e-08 |4.492072e-07  |
|16   |ground_failure_zone   |slope                          |24.425234370761448    |6.276500191140483     |6.645706084736982     |2.505294432026001        |2.577926702747187          |28.02322     |19.12525      |24.929588     |
|17   |ground_failure_zone   |TWI_raster                     |-15.70289765463935    |0.4878731211233206    |0.5165715400129277    |0.6984791486675322       |0.7187291144881552         |-14.334189   |-17.10681     |-15.754505    |
|18   |ground_failure_zone   |vector_ruggedness_measure      |0.0065969138457957245 |1.113066037581076e-05 |1.1785405103799628e-05|0.003336264434335318     |0.003432987780898678       |0.014293254  |0.0027362937  |0.0051409993  |
|19   |EQIL_distribution_area|dem                            |720.5886075949367     |15239.01430059286     |15287.392123769345    |123.446402542127         |123.64219394595578         |981.0        |404.0         |720.5         |
|20   |EQIL_distribution_area|distance_stream_downstream     |22621.837090214598    |8892256.003877142     |8920485.388016436     |2981.9885988845          |2986.718163472482          |27561.291    |12633.724     |21406.955     |
|21   |EQIL_distribution_area|ground_failure_estimate_cropped|0.002261018167585842  |3.851177432398852e-06 |3.863403392501705e-06 |0.0019624417016560905    |0.0019655542201887245      |0.011194711  |0.00062405755 |0.0012637093  |
|22   |EQIL_distribution_area|local_relief                   |4.1835443037974684    |3.181501361961223     |3.1916013662849094    |1.7836763613282605       |1.7865053501976729         |9.0          |2.0           |5.0           |
|23   |EQIL_distribution_area|pga_contour_raster_cropped     |0.2906822777247127    |0.0001627926208497987 |0.00016330942282075044|0.012759021155629404     |0.012779257522280018       |0.3195611    |0.27278692    |0.28980446    |
|24   |EQIL_distribution_area|profile_curvature              |1.0127504615122613e-05|1.1250372185392921e-08|1.1286087652648136e-08|0.00010606777166223923   |0.00010623599979596435     |0.001764685  |-4.1868538e-05|2.41667e-09   |
|25   |EQIL_distribution_area|slope                          |14.306402396552171    |16.316898041568045    |16.36869771789048     |4.039418032534891        |4.045824726540991          |25.352772    |2.1681957     |14.60791      |
|26   |EQIL_distribution_area|TWI_raster                     |-15.105869250961497   |2.4253059383153044    |2.4330053222464643    |1.5573393780147295       |1.5598093865105647         |-10.349417   |-17.52993     |-15.439365    |
|27   |EQIL_distribution_area|vector_ruggedness_measure      |0.01002197717228032   |3.7511528433965274e-05|3.7630612651215957e-05|0.0061246655773164686    |0.006134379565303728       |0.034200232  |0.0012128265  |0.008357128   |
