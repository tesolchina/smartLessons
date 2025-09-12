# The solar map as a knowledge base for solar energy use

Jouri Kantersa , Maria Walla , Elisabeth Kjellsson

a Energy and Building Design, Lund University, Lund, Sweden b Building Physics, Lund University, Lund, Sweden

# Abstract

Our existing urban environment has a significant potential to increase the use of renewable energy, mainly by using solar irradiation for heat and electricity. Quantification of the solar potential by means of a solar map is the first step in the acceleration process for using more solar energy in our urban environments. A solar map is a GIS system providing the annual solar irradiation on building surfaces, mostly accompanied by information of the output of solar thermal or photovoltaic systems. Many solar maps are already in place today; almost all of them are however using different approaches. In this paper, an analysis is done of current solar maps in order to see on which principles the solar maps were based upon.

$^ ©$ 2014 The Authors. Published by Elsevier Ltd. Selection and peer review by the scientific conference committee of SHC 2013 under responsibility of PSE AG

Keywords: Solar maps; solar cadastre; cities; tool; urban planning, solar resource assessment

# 1. Introduction

Cities, home to more than half of the earth’s population, consume the majority of energy in the world [1]. In order to become more resilient for the future, cities need not only to reduce their energy need, but also start producing their own energy [2]. One way to generate renewable energy within our existing urban environment is by making use of solar energy. It is important to get a more detailed overview of the amount of energy we can produce with solar thermal (ST) or photovoltaics (PV) on existing buildings. One way to analyse the potential of the existing built environment is by means of solar maps [3-8]. A solar map or solar cadastre is a GIS system providing the annual solar irradiation on building surfaces (roofs and / or facades), mostly accompanied by the output of solar thermal or photovoltaic systems, and connected to a website. Many city administrations already have solar maps in place and they mainly serve two purposes: as a front-end platform to inform citizens about the potential of their own roof, and as a back-end tool for city administrations to base energy decisions upon. Current solar maps have different levels of advancement; the amount of information provided to users can differ a lot. Sometimes, solar maps are part of larger programs to get more renewable energy production in cities and provide users with direct information of suppliers and installers of solar systems. Other solar maps simply provide the solar irradiation to users without any further information. Furthermore, all solar maps so far take only roofs into account, not facades.

# 1.1. Common methodology for solar maps

The most common methodology to produce a solar map is shown in Figure 1. LiDAR data is Light Detection and Ranging data; 3D data collected by laser scanning. DEM –Digital Elevation Model- is 3D data of the terrain, and LAI –Leaf Area Index- is 3D data describing the “exchange of fluxes of energy, mass (e.g., water and CO2), and momentum between the surface and the planetary boundary layer” [9]. A growing number of cities are obtaining LiDAR data, making it in theory possible for these cities to produce a solar map. The process to obtain a solar map might be the same, but parts of the methods can be performed very differently. Maybe the most important part is the used calculation method, both for the solar irradiation and the output of the solar technology (PV / ST). Jakubiec & Reinhart (2013) note that ‘limited attention has been paid to the assumptions and calculation methods underlying solar maps’ [10]. In their analysis of North American solar maps, it was found that the most used calculation method were the ‘constant irradiation level’ method, Solar Analyst, and PVWatts, while Jakubiec & Reinhart use Radiance / Daysim as calculation method.

![](img/3195f49f53a5f2fd4f273bb5808a3f365960317055b62ec3ba5ba149ebe27e67.jpg)  
Figure 1. Methodology to produce a solar map [11]

In this study, the focus is onother parameters than the calculation method:

which assumptions are made in the rating of the suitability of surfaces? which additional information is provided to accelerate the implementation of solar energy? how is the information provided from the solar maps used (by front- and back-end users)?

It was expected that this information would reveal the underlying status of solar energy in the cities.

# 2. Method

In order to get an overview of current solar maps, a simple Google search was done with the words “solar map city”. Additionally, literature and scientific databases were also searched for with the same search terms. In total, 19 solar maps were identified. The authors are aware of the fact that there are more solar maps available worldwide, but many of them rely on exactly the same process (e.g. bought from the same company), and were therefore not included in the list. Table 1 shows the overview of the 19 analysed solar maps.

Table 1. Overview of analysed solar maps   

<html><body><table><tr><td></td><td>Country</td><td>City</td><td>Name</td><td>Owner</td></tr><tr><td>1</td><td>Austria</td><td>Graz</td><td>Solardachkataster</td><td>City of Graz</td></tr><tr><td>2</td><td>Austria</td><td>Vienna</td><td>Solarpotenzialkataster</td><td>City of Vienna</td></tr><tr><td>3</td><td>England</td><td>Bristol</td><td>Solar energy Bristol</td><td>City of Bristol</td></tr><tr><td>4</td><td>Germany</td><td>Aachen</td><td>Stadt Aachen Solarkataster</td><td>City of Aachen</td></tr><tr><td>5</td><td>Germany</td><td>Berlin</td><td>Solaratlas Berlin</td><td>City of Berlin</td></tr><tr><td>6</td><td>Germany</td><td>Dusseldorf</td><td>Solarkataster Dusseldorf</td><td>City of Dusseldorf</td></tr><tr><td>7</td><td>Germany</td><td>Marburg</td><td>Solarkataster Marburg</td><td>City of Marburg</td></tr><tr><td>8</td><td>Germany</td><td>Osnabruick</td><td>Sun-Area</td><td>City of Osnabruick</td></tr><tr><td>9</td><td>Germany</td><td>Solingen</td><td>Solarkataster Solingen</td><td>City of Solingen</td></tr><tr><td>10</td><td> Netherlands</td><td>Amersfoort</td><td>Zonnescan</td><td>City of Amersfoort</td></tr><tr><td>11</td><td>Netherlands</td><td>Arnhem</td><td>Zonatlas Arnhem</td><td>City of Arnhem</td></tr><tr><td>12</td><td>Portugal</td><td>Lisbon</td><td>Carta do Potencial Solar</td><td>City of Lisbon</td></tr><tr><td>13</td><td>Sweden</td><td>Gothenburg</td><td>SEES</td><td>Goteborg Energi</td></tr><tr><td>14</td><td>Switzerland</td><td>Basel</td><td> Solarpotenzial</td><td>City of Basel</td></tr><tr><td>15</td><td>Switzerland</td><td>Geneva</td><td>InfoEnergi</td><td>City of Geneva</td></tr><tr><td>16</td><td>Switzerland</td><td>Porrentruy</td><td>Cadastre Solaire</td><td>City of Porrentruy</td></tr><tr><td>17</td><td>USA</td><td>Boston</td><td>Renew Boston Solar</td><td>City of Boston</td></tr><tr><td>18</td><td> USA</td><td>Los Angeles</td><td>LA County Solar Map</td><td>LA County</td></tr><tr><td>19</td><td>USA</td><td>New York City</td><td>NYC Solar Map</td><td>NYC Solar America City</td></tr></table></body></html>

The owners were contacted to obtain additional information how the system was set up and what the conditions were, based on the following questions:

1. In your solar map you have different categories (good, very good, not suitable) for the assessment of solar energy. How did you choose the actual limits for the different categories? (based on financial motives, subsidies, etc.?)   
2. How do you plan to work with the gained information from the solar potential map (or how do you already work with it)?   
3. Is it only meant for citizens or do you use it as an instrument for urban / energy planning? (Is it used for deciding political goals for the use of solar energy?)   
4. Is the total potential summarized for the city or for different areas or categories of buildings?   
5. Are there analyses done for ranking or comparing areas with e.g. apartment buildings and single family buildings respectively?

Unfortunately, only 11 out of 19 answered to our short questionnaire (Aachen, Amersfoort, Arnhem, Basel, Dusseldorf, Geneva, LA County, Lisbon, NYC, Marburg, Osnabrück)

Of the different solar maps, the following parameters were analysed: (Table 2):

Annual solar irradiation level $( \mathrm { k W h } / \mathrm { m } ^ { 2 } \mathrm { a } )$ ),   
Considered technologies (PV, ST),   
Total output per roof $\left( \mathrm { k W h / a } \right)$ ,   
Assumed efficiency of the technologies. In the case that the efficiency of the solar technologies was not provided, the efficiency was calculated using the total output, the area, and the solar irradiation levels (marked with a \*).   
Heritage limitations (are buildings with a cultural heritage are marked),   
Threshold value per category $( \mathrm { k W h } / \mathrm { m } ^ { 2 } \mathrm { a } )$ ),   
Minimum surface of the solar system $( \mathrm { m } ^ { 2 } )$ ,   
Maximum annual solar radiation (For European cities, the maximum solar irradiation level was acquired by using PVGIS [12], even though some solar maps stated other maximum values. In USA, mainly the solar maps of NREL were used [13]).   
The percentage of maximum available annual solar irradiation level,   
Information on which parameters categories were based upon.

In Table 2, N/A means here that this data were either not specified or not elucidated in the answers. The percentage of maximum available annual solar irradiation was calculated because it makes comparisons between solar maps easier. Not all solar maps had the same categorisation. If necessary, categories were re-labelled to the common categories -very good, good, and suitable.With the information from the owners and the websites of solar maps, an inventory was made of the categorisation method used in the maps.

# 3. Results

In this section, first a quantitative analysis of the solar maps is provided, followed by a qualitative analysis.

# 3.1. Quantitative analysis

Table 2 provides an overview of all the analysed parameters. The colours in the table represent different categories:

Blue: Reasonable   
Light green: good   
Dark green: very good   
Grey: solar maps did not divide areas in categories or did not specify –either in the documentation or in the reply- how categories were set up.

Table 2. Overview of the solar maps and their characteristics   

<html><body><table><tr><td rowspan="2">City</td><td rowspan="2"></td><td rowspan="2">Technologies Output/ roof</td><td rowspan="2">Efficiency</td><td rowspan="2">HeritageCategories</td><td colspan="2"></td><td rowspan="2">Thres- Min.</td><td colspan="3"> Max solar % of max solCategories</td></tr><tr><td></td><td>hold</td><td>surface rad.</td><td>rad</td><td>based on</td></tr><tr><td>Graz</td><td></td><td>N/A No</td><td></td><td></td><td>yes Good</td><td></td><td>N/A 12</td><td>1330</td><td>N/A</td><td>N/A</td></tr><tr><td rowspan="2">2 Vienna</td><td rowspan="2">PV/ST</td><td></td><td>PV: 14%*</td><td></td><td>Very good</td><td>N/A</td><td>12</td><td></td><td>N/A</td><td>N/A</td></tr><tr><td>Yes (PV/ST)</td><td>ST: 90%*</td><td>yes</td><td>Good Very good</td><td>900 1100</td><td> 5</td><td>1300</td><td>69%</td><td>N/A</td></tr><tr><td rowspan="3">3 Bristol</td><td rowspan="3">PV</td><td rowspan="3">Yes</td><td>PV: 9% *</td><td></td><td></td><td></td><td>5</td><td>1300</td><td>85%</td><td>N/A</td></tr><tr><td>(PV)</td><td>yes</td><td>Reasonable Good</td><td>880 940</td><td>N/A</td><td>1170</td><td>75%</td><td>N/A N/A</td></tr><tr><td></td><td></td><td>Very good</td><td>1000</td><td>N/A N/A</td><td>1170 1170</td><td>80% 85%</td><td>N/A</td></tr><tr><td rowspan="3">Aachen 4</td><td rowspan="3"></td><td rowspan="3">PV/ST</td><td>Yes (PV )</td><td>PV: 11.6% no</td><td>Reasonable</td><td>800</td><td>10</td><td>1090</td><td>73%</td><td>N/A</td></tr><tr><td>ST)</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>ST: 13.5%*</td><td></td><td>Good</td><td>870 1020</td><td>10</td><td>1090</td><td>80%</td><td>N/A</td></tr><tr><td rowspan="3">5 Berlin</td><td rowspan="3"></td><td rowspan="3">PV/ST</td><td rowspan="3">Yes(PV) PV:12%</td><td rowspan="3">yes</td><td>Very good</td><td></td><td>10</td><td>1090</td><td>94%</td><td>N/A</td></tr><tr><td>Reasonable</td><td>920 1035</td><td>N/A</td><td>1150</td><td>80%</td><td>N/A</td></tr><tr><td>Good Very good</td><td>1092.5</td><td>N/A N/A</td><td>1150 1150</td><td>90%</td><td>N/A</td></tr><tr><td rowspan="2">6</td><td rowspan="2">Dusseldorf</td><td rowspan="2">PV/ST</td><td rowspan="2">Yes (PV) ST)</td><td rowspan="2">PV: 14% yes</td><td></td><td>Reasonable</td><td>654 20</td><td></td><td>95%</td><td>N/A</td></tr><tr><td></td><td></td><td></td><td>1090</td><td>60%</td><td>N/A</td></tr><tr><td rowspan="3">7</td><td rowspan="3">Marburg</td><td rowspan="3">PV /ST</td><td rowspan="3">Yes (PV)</td><td rowspan="3">ST: 14% PV: 9-15% no</td><td>Good</td><td></td><td>872 20</td><td>1090</td><td>80%</td><td>N/A</td></tr><tr><td>Reasonable</td><td>825</td><td>N/A</td><td>1100</td><td>75%</td><td>Irradiation</td></tr><tr><td>Good</td><td>891</td><td>N/A</td><td>1100</td><td>81%</td><td></td></tr><tr><td rowspan="2"></td><td rowspan="2">8 Osnabruick</td><td rowspan="2">PV /ST</td><td rowspan="2">Yes</td><td rowspan="2">PV: 15%</td><td rowspan="2">yes</td><td>Very good</td><td>1045</td><td>N/A</td><td>1100</td><td>95%</td><td></td></tr><tr><td>Good</td><td>766</td><td>N/A</td><td>1090</td><td>70%</td><td>N/A</td></tr><tr><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2">(PV/ST) N/A</td><td rowspan="2">No</td><td rowspan="2">ST: 50%*</td><td rowspan="2"></td><td>Very good</td><td>909</td><td>N/A</td><td>1090</td><td>83%</td><td>N/A</td></tr><tr><td>Reasonable</td><td> N/A</td><td>N/A</td><td>1090</td><td>N/A</td><td>N/A</td></tr><tr><td rowspan="3">9 Solingen</td><td rowspan="3"></td><td rowspan="3"></td><td rowspan="3"></td><td rowspan="3"></td><td rowspan="3">yes</td><td>Good</td><td>N/A</td><td>N/A</td><td>1090</td><td>N/A</td><td>N/A</td></tr><tr><td>Very good</td><td>N/A</td><td>N/A</td><td>1090</td><td>N/A</td><td>N/A</td></tr><tr><td>Reasonable</td><td> 500</td><td>N/A</td><td>1110</td><td>45%</td><td>payback time</td></tr><tr><td rowspan="2">10 Amersfoort</td><td rowspan="2">PV</td><td rowspan="2"></td><td rowspan="2"></td><td rowspan="2">Yes (PV) PV: 11% *</td><td rowspan="2">yes</td><td></td><td>900</td><td>N/A</td><td>1110</td><td>81%</td><td rowspan="2"></td></tr><tr><td>Good</td><td>700</td><td></td><td></td><td>N/A</td></tr><tr><td rowspan="2">11 Arnhem</td><td rowspan="2">PV</td><td rowspan="2"></td><td rowspan="2">Yes (PV)</td><td rowspan="2">PV: 15%</td><td rowspan="2">no</td><td>Reasonable</td><td></td><td>11</td><td>1100</td><td>64%</td><td></td></tr><tr><td>Very good Reasonable</td><td>900 1000</td><td>11 N/A</td><td>1100 1860</td><td>82% 54%</td><td>N/A Orientation</td></table></body></html>

<html><body><table><tr><td colspan="5"></td><td>Good</td><td>1000</td><td>N/A</td><td>1400</td><td>71%</td><td>N/A</td></tr><tr><td rowspan="4">16 Porrentruy</td><td rowspan="4">PV</td><td rowspan="4">Yes (PV)</td><td rowspan="4">PV: 12.75%</td><td rowspan="4">no</td><td>Very good</td><td>1145</td><td>N/A</td><td>1400</td><td>82%</td><td>N/A</td></tr><tr><td>Reasonable</td><td>750</td><td>N/A</td><td>1250</td><td>60%</td><td>N/A</td></tr><tr><td>Good</td><td>950</td><td>N/A</td><td>1250</td><td>76%</td><td>N/A</td></tr><tr><td></td><td>Very good</td><td>1150 N/A</td><td>1250</td><td>92%</td><td>N/A</td></tr><tr><td>17 Boston 18 Los Angeles</td><td>PV PV/ST</td><td>Yes (PV) Yes (PV /</td><td>PV: 11%* PV: 18%</td><td>yes</td><td>N/A</td><td>N/A</td><td>N/A</td><td>1307</td><td>N/A</td><td>N/A Payback time</td></tr><tr><td rowspan="4"></td><td rowspan="4"></td><td rowspan="4">ST)</td><td rowspan="2">ST: 64%*</td><td rowspan="2">no</td><td>Reasonable</td><td>1204.5</td><td>N/A</td><td>1805</td><td>67%</td><td rowspan="4"></td></tr><tr><td>Good</td><td>1460</td><td>N/A</td><td>1805</td><td>81%</td></tr><tr><td rowspan="2">Yes (PV) PV: -</td><td rowspan="2"></td><td>Very Good</td><td>1789</td><td>N/A</td><td>1805</td><td>99%</td></tr><tr><td>no Suitable</td><td>1030</td><td>10</td><td>1456</td><td>71%</td><td>N/A</td></tr></table></body></html>

# 3.1.1. Categorisation

Table 3 and Figure 2 show the values of the categories ‘reasonable, ‘good’, and ‘very good’ of the different solar maps. In the box plot (Figure 2), the white part of the box represents the $2 ^ { \mathrm { n d } }$ quartile of the range, the black box the third quartile of the range.

Table 3.Median for the categories ‘reasonable’, ‘good’, ‘very good’ $\mathrm { i n } \%$ of local maximum annual solar irradiation)

<html><body><table><tr><td> reasonable</td><td>65%</td></tr><tr><td> good</td><td>77%</td></tr><tr><td>very good</td><td>89%</td></tr></table></body></html>

![](img/072dab5de6de55fc1cc6f6eb5e8257f362189d94c4c5d26f104851b76a11f211.jpg)  
Figure 2. Box plot of categories applied in solar maps

Figure 2 shows that the categorisation of the solar maps is not straightforward. By comparing the categories as a percentage of the local maximum solar irradiation, the differences between the thresholds of the categories can only be explained from other parameters than solar irradiation, i.e. political, social, financial parameters. Interestingly, the maximum value of the ‘reasonable’ category range is higher than the minimum of the ‘good’ category. This is also true for the highest value of the ‘good’ category and the lowest value of the ‘very good’ category. The spread of the values in the ‘reasonable’ category is quite high $( 3 5 \% )$ , while spreading in the ‘good’ category is smaller $( 1 5 \% )$ , and $1 3 \%$ in the ‘very good’ category. The owners were asked to clarify on which information they based their categorisation of surfaces. It was expected that they would base their categories on a certain payback time of the applied solar technologies. There was a mixture of answers: sometimes owners answered that the categories were based on the radiation level (which does not answer the question); in other cases, categorisation was done by best guesses, and only in some cases, categorisation was based on detailed calculations of payback times. The LA solar map for example based the categories on a payback time shorter than 15 years, taking into account the general electricity costs and installation costs after subsidies.

The minimum system size of the solar system was often related to the payback time of the system and / or the resolution of the data. Most solar maps did not set a requirement for the minimum surface area, while other maps had minimum requirements (this was based upon the capacity and payback time). Owners responded that only with a certain system size $\mathbf { ( k W p ) }$ , a reasonable payback time could be reached.

# 3.1.2. Other parameters

Figure 3 and Table 2 provide an overview of the main parameters users of the solar maps can extract: Heritage limitations, Irradiation levels, PV output, and ST output. More than half of the solar maps provided an assessment of the output of a PV system installed on the roof, while less than half could provide an assessment of the output of a ST system. Half of the solar maps showed culturally / historically important buildings where the implementation of solar energy might not be allowed or needs to be considered very carefully. Also, half of the solar maps were able to show the irradiation levels on roofs, while the other half did not show the irradiation levels but rather the output of solar energy systems. This might be due to the fact that, for laymen, it is easier to relate to the output of a system and the corresponding surface area than the incoming radiation.

![](img/66d64944e35a420b8f5b99864ff51d8ae9147e18ee54135d025ed100bc898d0f.jpg)  
Figure 3. Main parameters of the solar maps

Many solar maps do not only focus on the quantification of the solar potential of roofs in the involved cities, but they also serve as a platform to inform inhabitants about the possibilities of solar energy. In the following section, the qualitative side of the solar maps is discussed.

# 3.2. Purposes of the solar maps

In general, the analysed solar maps served both as a front-end and as a back-end tool platform. Most solar maps came with a short description of what the solar energy potential is and which methods were used in order to calculate it. Many solar maps also provided a rather detailed set of assumptions which are needed to calculate the output of solar energy systems, however it is often stated that the solar potential is just a ´first estimation´, and that the owner (of the solar map) cannot be hold responsible for the calculations.

One example of how a solar map can be used both as a back- and front end tool is in case of the City of Basel, Switzerland [14]. This city launched an environmental program where they encourage people to first renovate their roofs, and then install PV –if their roofs had the right conditions; for both of the measures, the city will provide subsidies. On one website, it is explained how inhabitants should proceed. Besides that, the city also approached the owners of the 500 best roofs to implement PV.

# 3.2.1. Follow-up of the information gained by the user and owners

Using the solar map and obtaining the solar energy potential of roofs is often the first step in decision-making for both inhabitants and cities. Front-end users need guidance in order to understand what the solar energy potential actually means. Some of the solar maps therefore focus on two additional items:

Finances of the system: revenues and costs Installations: which installers are available etc. With this information, a founded decision can be made on the implementation of solar energy.

For the back-end users (and most often the owners of the solar maps), solar maps serve as an underlying information base for local energy decisions. In their answers, the involved cities say that they use the solar map for estimating the solar potential of all their own real estate. Some cities have underlying information about building types and year of construction. Performing such analyses takes time and money, the benefit of such an analysis was not always clear to the cities.

# 4. Discussion and conclusions

An analysis was done of 19 solar maps which are publically available on the internet. The solar maps were analysed, focussing on mainly the following elements:

Annual solar irradiation $( \mathrm { k W h } / \mathrm { m } ^ { 2 } \mathrm { a } )$ ),   
Considered technologies (PV, ST),   
Total output per roof $\left( \mathrm { k W h / a } \right)$ ,   
Assumed efficiency of the technologies,   
Heritage limitations (are buildings with a cultural heritage marked?),   
Threshold value per category $( \mathrm { k } \bar { \mathsf { W h } } / \mathrm { m } ^ { 2 } \mathrm { a } )$ ,   
Minimum surface of solar system $( \mathrm { m } ^ { 2 } )$ ,

esides this analysis, owners of the solar maps were asked to fill in a questionnaire, focussing mainly on:

information on which parameters categories were based upon, what purposes the solar map serves.

# 4.1. Classification of solar maps

With the analysis of the solar maps and the results of the surveys, it is possible to classify the solar maps (Table 4). The basic solar map is a solar map with basic information: the irradiation level. Preferably, irradiation levels are also categorised. Such a solar map is the base for the medium and advanced solar map, of which features are all based on the analysis of annual solar irradiation of surfaces. The medium solar map provides the energy output of the suitable areas as PV / ST. The most advanced solar map is not only providing quantitative data, but also provides information about what to do next when people want to install PV or ST.

Table 4. Classification of solar maps   

<html><body><table><tr><td>Basic</td><td>Medium</td><td>Advanced</td></tr><tr><td>-Irradiation levels</td><td>-Irradiation levels (not in all cases)</td><td>-Irradiation levels (not in all cases)</td></tr><tr><td>-Categorisation of irradiation levels (not in all cases)</td><td>-Output of solar systems (PV / ST)</td><td>-Output of solar systems (PV / ST)</td></tr><tr><td></td><td>-Categorisation of suitable area for production</td><td>-Categorisation of suitable area for production</td></tr><tr><td></td><td>-System effect (PV)</td><td>-System effect (PV)</td></tr><tr><td></td><td></td><td>-Monthly output (not in all cases)</td></tr><tr><td></td><td></td><td>-Financial considerations (investment costs, revenue)</td></tr><tr><td></td><td></td><td>-Information regarding installers</td></tr><tr><td></td><td></td><td>-Information about solar energy</td></tr></table></body></html>

A useful addition to solar maps could also be a feature which maps solar systems that are already installed within the city, with its according size and output.

# 4.2. In action

The role of solar maps as a decision support tool can be divided into three different aspects: 1) the difference in users (politicians, urban planners, investors, real estate owners), 2) scale (city, urban district, building), and 3) soft aspects (raise interest, vitalise the debate, get a common base for discussion). By taking all these three aspects into account, a full deployment of solar energy in cities can be accelerated.

# Acknowledgement

The authors would like to thank the Swedish Research Council FORMAS, the Swedish Energy Agency and the Swedish Environmental Protection Agency for their financial support.

# References

[1] POLIS, Identification and mobilization of solar potentials via local strategies. Guidelines based on the experiences of pilot actions., in, Intelligent Energy Europe, 2012.   
[2] P.S. Grewal, P.S. Grewal, Can cities become self-reliant in energy? A technological scenario analysis for Cleveland, Ohio, Cities.   
[3] L.K. Wiginton, H.T. Nguyen, J.M. Pearce, Quantifying rooftop solar photovoltaic potential for regional renewable energy policy, Computers, Environment and Urban Systems, 34 (2010) 345-357.   
[4] I. Theodoridou, M. Karteris, G. Mallinis, A.M. Papadopoulos, M. Hegger, Assessment of retrofitting measures and solar systems' potential in urban areas using Geographical Information Systems: Application to a Mediterranean city, Renewable and Sustainable Energy Reviews, 16 (2012) 6239-6261.   
[5] A. Kapfenberger-Pock, B. Horst, GIS-based local analysis for solar plants; a planning tool, in: Eurosun 2010, Graz, Austria, 2010.   
[6] L. Girardin, F. Marechal, M. Dubuis, N. Calame-Darbellay, D. Favrat, EnerGis: A geographical information based system for the evaluation of integrated energy conversion systems in urban areas, Energy, 35 (2010) 830-840.   
[7] S. Izquierdo, C. Montañés, C. Dopazo, N. Fueyo, Roof-top solar energy potential under performance-based building energy codes: The case of Spain, Solar Energy, 85 (2011) 208-213.   
[8] S. Gadsden, M. Rylatt, K. Lomas, D. Robinson, Predicting the urban solar fraction: a methodology for energy advisers and planners based on GIS, Energy and Buildings, 35 (2003) 37-48.   
[9] Y. Knyazikhin, J.V. Martonchik, R.B. Myneni, D.J. Diner, S.W. Running, Synergistic algorithm for estimating vegetation canopy leaf area index and fraction of absorbed photosynthetically active radiation from MODIS and MISR data, Journal of Geophysical Research: Atmospheres, 103 (1998) 32257-32275.   
[10] J.A. Jakubiec, C.F. Reinhart, A method for predicting city-wide electricity gains from photovoltaic panels based on LiDAR and GIS data combined with hourly Daysim simulations, Solar Energy, 93 (2013) 127-143.   
[11] N. Lukač, D. Žlaus, S. Seme, B. Žalik, G. Štumberger, Rating of roofs’ surfaces regarding their solar potential and suitability for PV systems, based on LiDAR data, Applied Energy, 102 (2013) 803-812.   
[12] PVGIS, Europe Solar Potential, in, European Commission, 2006.   
[13] NREL, Solar maps, in, 2012.   
[14] City of Basel, Die Dächer Basels – das erste kantonale Solarkraftwerk, in, 2013.