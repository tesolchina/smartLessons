

Let's compile a list of email for different media contacts 

and update the CSV /Users/simonwang/Documents/Usage/VibeCoding/letter_writing/media.csv 


Then we draft an email to these media outlets about our website 

https://question-no8.hkbu.me/





=========ignore======

# https://portal.csdi.gov.hk/csdi-webpage/info/apiQuery 




let's also keep a CSV data file to keep raw data and make it publicly available
Credit: Dr Simon Wang, Lecturer and Innovation Officer, the Language Centre, HKBU

with help from GitHub Co-pilot agent
email: simonwang@hkbu.edu.hk

in the background raise the concern over an earlier than usual announcement of the decision to keep no 8 signal until 11 am 9 Sept

* We should indicate clearly whether the actual wind strength matches with the current signal no~~

signal 3+ stations should exclude the signal 17 stations 

current signal should be pulled from HKO website or API 

| ``Data Providers | [Hong Kong Observatory](https://data.gov.hk/en-datasets/provider/hk-hko)            |
| ----------------------- | -------------------------------------------------------------------------------- |
| Data Category           | [Climate and Weather](https://data.gov.hk/en-datasets/category/climate-and-weather) |
| Format                  | **JSON**                                                                   |
| API                     | Available                                                                        |
| Update Frequency        | As and when there is update                                                      |

URL[https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&amp;lang=en](https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=warnsum&lang=en)

[

```
https://portal.csdi.gov.hk/server/services/common/hko_rcd_1634953844424_88011/MapServer/WFSServer?service=wfs&request=GetFeature&typenames=latest_10min_wind&outputFormat=geojson&maxFeatures=10
```

](https://portal.csdi.gov.hk/server/services/common/hko_rcd_1634953844424_88011/MapServer/WFSServer?service=wfs&request=GetFeature&typenames=latest_10min_wind&outputFormat=geojson&maxFeatures=10)

# Dataset Detail

![](https://portal.csdi.gov.hk/geoportal/custom/2024-revamp/images/content/headers/dataset-detail.jpg)

[Home](https://portal.csdi.gov.hk/csdi-webpage) / [Search Catalog](https://portal.csdi.gov.hk/geoportal/#searchPanel) / **Dataset Detail**

Regional weather in Hong Kong – the latest 10-minute mean wind direction and wind speed and maximum gust

Provided by: [Hong Kong Observatory](javascript:void(0))

CSDI Data Category: [Climate and Weather](javascript:void(0))

CSDI Data Theme: [Common Sharable Spatial Data (CSSD)](javascript:void(0))

[]()[]()[]( "Share dataset via email")[]( "Copy dataset URL")

Abstract

Provide data on regional weather in Hong Kong – the latest 10-minute mean wind direction and wind speed and maximum gust (the data provided is provisional)

Dataset Maintenance

Creation date

2022

Revision date

2022

Maintenance and update Frequency

Every 10 Minutes

Contact

Organization

Hong Kong Observatory

Position

General Enquiries

Phone

[29268200](tel:29268200)

Email Address

[mailbox@hko.gov.hk](mailto:mailbox@hko.gov.hk)

Technical Information

Coordinate Reference System (EPSG Code)

4326

Metadata Standard

ISO 19139/19115

Metadata Date

14/02/2022

Dataset Remarks

Use Limitation

N/A

Related Datasets

| Tropical cyclone track information                                                                                                                                                             | Locally felt earth tremor report                                                                                                                                                               | Tropical cyclone best track data (post analysis)                                                                                                                                               | Quick earthquake messages                                                                                                                                                                      |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hong Kong Observatory                                                                                                                                                                          | Hong Kong Observatory                                                                                                                                                                          | Hong Kong Observatory                                                                                                                                                                          | Hong Kong Observatory                                                                                                                                                                          |
| [![](https://portal.csdi.gov.hk/geoportal/custom/2024-revamp/images/icon/related-dataset.svg)Dataset Details](https://portal.csdi.gov.hk/geoportal/?datasetId=d8387d09-8773-5b8c-acbe-b2f81537afdb) | [![](https://portal.csdi.gov.hk/geoportal/custom/2024-revamp/images/icon/related-dataset.svg)Dataset Details](https://portal.csdi.gov.hk/geoportal/?datasetId=36a7087c-9fee-560f-b27f-445373edc7ca) | [![](https://portal.csdi.gov.hk/geoportal/custom/2024-revamp/images/icon/related-dataset.svg)Dataset Details](https://portal.csdi.gov.hk/geoportal/?datasetId=b7b4acbe-adb8-bcac-bbb6-af908d8b9e93) | [![](https://portal.csdi.gov.hk/geoportal/custom/2024-revamp/images/icon/related-dataset.svg)Dataset Details](https://portal.csdi.gov.hk/geoportal/?datasetId=0b0a19d6-5c34-5770-8aa5-3d6a1087c2c9) |



we need a script to access real time wind data - updated every 10 minutes with spatial data

https://portal.csdi.gov.hk/geoportal/?datasetId=hko_rcd_1634953844424_88011&lang=en





https://data.gov.hk/en-data/dataset/hk-hko-rss-latest-ten-minute-wind-info/resource/3dadbf08-148c-4daa-8051-7ce315fa013b


[https://portal.csdi.gov.hk/geoportal/?datasetId=hko_rcd_1634953844424_88011&amp;lang=en](https://portal.csdi.gov.hk/geoportal/?datasetId=hko_rcd_1634953844424_88011&lang=en) 


Simplified Data Specification for Common Sharable Spatial Data
共享空間數據的簡易數據規格
共享空间数据的简易数据规格

Regional weather in Hong Kong – the latest 10-minute mean wind direction and wind speed and maximum gust
香港分區天氣–最新的十分鐘平均風向、平均風速、最高陣風風速
香港分区天气–最新的十分钟平均风向、平均风速、最高阵风风速

---

# 1 Summary / 摘要 / 摘要

The following section lists all the data types in Regional weather in Hong Kong – the latest 10-minute mean wind direction and wind speed and maximum gust Dataset.
以下章節列出 香港分區天氣–最新的十分鐘平均風向、平均風速、最高陣風風速 內的所有數據類型
以下章节列出 香港分区天气–最新的十分钟平均风向、平均风速、最高阵风风速 内的所有数据类型

## 1.1 Data Layers / 數據圖層 / 数据图层

| Name / 名稱 / 名称 | Type / 種類 / 种类                  | Description / 描述 / 描述                                                                                                                                                                                                           |
| ------------------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| latest_10min_wind  | Spatial Layer / 空間圖層 / 空间图层 | Regional weather in Hong Kong – the latest 10-minute mean wind direction and wind speed and maximum gust / 香港分區天氣–最新的十分鐘平均風向、平均風速、最高陣風風速 / 香港分区天气–最新的十分钟平均风向、平均风速、最高阵风风速 |

## 1.2 Domain Tables / 定義域表 / 定义域表

| Name / 名稱 / 名称 | Description / 描述 / 描述 |
| ------------------ | ------------------------- |

# 2 Entity Descriptions / 實體描述 / 实体描述

The following section lists the attribute description for each data layers.
以下章節列出每個數據圖層的屬性描述。
以下章节列出每个数据图层的属性描述。

## 2.1 latest_10min_wind

| Field Name / 資料欄名稱 / 资料栏名称 | Data Type / 數據類型 / 数据类型 | Null Option / 空值選項 / 空值选项 | Description / 描述 / 描述                                                   |
| ------------------------------------ | ------------------------------- | --------------------------------- | --------------------------------------------------------------------------- |
| AutomaticWeatherStation_en           | String / 字串 / 字串            | Null                              | Automatic Weather Station (English) / 自動氣象站 (英文) / 自动气象站 (英文) |
| AutomaticWeatherStation_uc           | String / 字串 / 字串            | Null                              | Automatic Weather Station (Chinese) / 自動氣象站 (中文) / 自动气象站 (中文) |
| AutomaticWeatherStation_sc           | String / 字串 / 字串            | Null                              | Automatic Weather Station (Chinese) / 自動氣象站 (中文) / 自动气象站 (中文) |
| Data_url                             | String / 字串 / 字串            | Null                              | Data URL / 數據網址 / 数据网址                                              |

# 3 Domains / 定義域 / 定义域

The following section lists the description of domain coded value (if any).
以下章節列出定義域編碼值的描述（如有）。
以下章节列出定义域编码值的描述（如有）。

# 4 Physical Data Model / 實體數據模型 / 实体数据模型

The following section shows a physical data model diagram depicting the relationship between data layers.
以下章節以實體數據模型圖描述數據圖層之間的關係。
以下章节以实体数据模型图描述数据图层之间的关系。

![]()
