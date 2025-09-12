# User Guide for

# The Hong Kong Solar Irradiation Map

![](img/7a9dcdda1335b070c1ea3338fee78ec40630612199b55cb7f0ab5124edeab759.jpg)

# Content

1. METHODOLOGY .

1.1. Area Suitable for PV Panel Installation .   
1.2. Average Annual Solar Irradiation.   
1.3. Estimated Annual Electricity Generation.   
1.4. Payback Calculation .

2. KEY FUNCTIONS OF THE MAP 3

2.1. Search for Location .   
2.2. Define Calculation Settings..   
2.3. Select the Area .   
2.4. Payback Calculation . 5   
2.5. Layer Control.. 6

3. INFORMATION USED. 6

By showing the solar irradiation of the building rooftops, the Hong Kong Solar Irradiation Map (the Map) enables users to perform a preliminary assessment of the solar energy potential for their building rooftops. Users can define the PV system settings and select an area of the building rooftops to display the corresponding solar irradiation and the estimated annual electricity generation, as well as the Feed-in Tariff (FiT) income.

# 1. Methodology

Airborne Light Detection and Ranging (LiDAR) data have been converted into digital surface model (DSM) to allow the Map to factor in roof slope and shading effect from nearby buildings or obstacles. The latest set of LiDAR data were acquired from December 2019 to February 2020 and thus the buildings, which were being or to be constructed or have been demolished, as well as the associated shading effects, are not shown nor reflected in the Map.

The resolution of the LiDAR data and the solar irradiation simulation are $0 . 5 \mathsf { m }$ and $1 \textrm { m }$ respectively, and therefore the Map may not accurately reflect the solar potential at each area of building rooftop.

The building polygons from the digital basemap obtained from the Lands Department (LandsD) were used to determine the location of the building rooftops for solar irradiation simulation.

# 1.1. Area Suitable for PV Panel Installation

The rooftops are divided into $1 \mathsf { m } ^ { 2 }$ pixels for simulation. To determine the suitability of the rooftop for PV panel installation, the following pixels are discarded:

An object with a height of less than $_ { 2 . 5 \mathsf { m } }$ ;   
Area with slope exceeding 40 degrees;   
1-m perimeter zone from the building edge;   
Global horizontal irradiation of less than 800 kWh/m2;   
Suitable area for PV installation is less than $3 \mathsf { m } ^ { 2 }$ .

# 1.2. Average Annual Solar Irradiation

The average annual solar irradiation is the average value of the annual solar irradiation of the area suitable for PV panel installation. Users should avoid installing the PV panels at the locations shown in deep blue in the Map. Otherwise, the annual electricity generation would be affected.

# 1.3. Estimated Annual Electricity Generation

The estimated generation capacity is calculated based on:

a rack-mounted solar PV system;   
no self-shading by PV panels;   
provision of maintenance space in-between different rows of PV panels;   
the estimated generation is calculated based on the global irradiation and regardless of the composition of direct and diffuse components.

The estimated annual electricity generation is then calculated based on the estimated generation capacity and the average annual solar irradiation of the selected area. The performance ratio used in this project is 0.75.

# 1.4. Payback Calculation

The payback calculator is developed based on the simple payback calculation. As the installation cost is subject to many factors, users should check with their contractors for the estimated installation cost.

The FiT rate adopted in 2021 are as follows:

<html><body><table><tr><td>Generation Capacity</td><td>FiT Rate ($ per kWh)</td></tr><tr><td>10 kW</td><td>$5</td></tr><tr><td>&gt; 10 kW to  200 kW</td><td>$4</td></tr><tr><td>&gt; 200 kW to  1MW</td><td>$3</td></tr></table></body></html>

# 2. Key Functions of the Map

# 2.1. Search for Location

Users may input the location or building name in the search box and click the Enter button or select the corresponding site from the list, as shown in Fig 1. The Map will then zoom in to the target location and show the information of the location, as shown in Fig 2.

![](img/c5b28f8517943e7a9d4f6e5b6d53e730181e9e417c7ee1bb9b6ca1cb9ab77534.jpg)  
Fig 1

![](img/9251ef26d29777cbcdc5f74717153a7e0f40a751bdbff008008a6b71f23ff9fb.jpg)  
Fig 2

Users may also click on the building polygon. Then a table will pop up and show the information of the selected polygon, as shown in Fig 3. The information shown in the table is calculated on the basis that the PV panel at $0 ^ { \circ }$ .

![](img/5c547ba9ce17194f38cb7d496a478640a979a903f5daac900393977e7e9ff75f.jpg)  
Fig 3

# 2.2. Define Calculation Settings

Users may define related calculation settings, including:

PV panel efficiency, PV panel tilting angle, and PV panel orientation.

Hong Kong is located in the northern hemisphere and the PV panels should be installed facing south with a tilted angle of 14 to 22 degrees to maximise the amount of electricity generated over the course of a year.

# 2.3. Select the Area

Users can draw a polygon within the building to calculate the estimated annual electricity generation. By clicking the “Draw” button as shown in Fig 4, users can singleclick on the map to draw the selected area and click the first vertex to complete the drawing. A pop-up table, as shown in Fig 5, showing the following information will be displayed:

area of the selected area, area suitable for PV panel installation, average annual solar irradiation, estimated generation capacity, estimated annual electricity generation, and estimated annual FiT income.

![](img/6207159aaf18bb6ea5f7a993bd258b9139d8f0801eea8d8177794c3d8fb3e0f5.jpg)  
Fig 4

![](img/15745a8864fdb50d9db52c50e63993d2a9af8cfcd5d7ec74bbd6411237b3df75.jpg)  
Fig 5

# 2.4. Payback Calculation

Click on the button of Payback Calculator at the bottom of the pop-up table, the calculator will be displayed, as shown in Fig 6. Input the generation capacity and the cost, the calculator will show the expected annual electricity generation, the FiT income and the payback period using the simple payback calculation.

![](img/d2b7938ad1ca93d6e5fb50a51c93c7912e73a27e7fa3485959a40750607c0657.jpg)  
Fig 6

# 2.5. Layer Control

In the layer control panel, users may turn on/off the solar irradiation layer to display the solar irradiation map and the building layer, as shown in Fig 7. Users may also control the solar irradiation layer transparency, as shown in Fig 8.

![](img/afe824fe635a7bd213178ec18e01c540cb05ca03e48283049dc74ef144ce0a6e.jpg)  
Fig 7

![](img/7931f74049e2af8169d196d3342f240da4758f8f6cc739953b9223c8d3ad01d1.jpg)  
Fig 8

# 3. Information Used

The following information are used to develop the project:

LiDAR data (acquired between Dec 2019 and Feb 2020) released by the Civil Engineering and Development Department;   
LiDAR data (acquired between Dec 2010 and Jan 2011) released by the Civil Engineering and Development Department;   
10-year hourly solar irradiation data (2009-2018) from the Hong Kong Observatory;   
Digital basemap (2019) obtained from the Lands Department;   
Ortho-DSM aerial photos (2016-2020) obtained from the Lands Department; and Map service provided by the Lands Department.