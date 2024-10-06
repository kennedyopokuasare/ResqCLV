# Customer Life Value Analysis and Data Pipeline

**Customer Life Value (CLV)** is a critical metric that computes how much revenue a customer provides to a company during the Customer relationship. It is an important metric for making decisions such as how much to spend on acquring new customers and return on investment (ROI) and customer segmentation and relationship management [ [1][gartner_clv], [2][SalesCommmunication.fi] ].

## The Project

The marketing team at wants to know how much can they spend on acquiring new customers to the platform. Therefore,they need CLV Analysis on an all customers for theor entire customer relation duration.

The Data Analysis team was a  data pipeline where from which they can easy query the top partners by sales, Customers’ favourite partner segments (default offer types) and the M1 retention for any given customer cohort.

This projoects implements the a data pipeline and the CLV analysis for the company. 

## Setting up the project

This project uses a python virtual environment to set up all the dependencies.

To begin the setup of the virtual environment

*  Install python `(version 3.12.6)`
*  Install anaconda or [miniconda][minconda]

All project dependencies have been exported to a virtual environment configuration file **environment.yml**.

Create and activate the virtual environment with the command below

````bash 
    conda env create -f environment.yml
    conda activate resq 
````
If the virtual environment is set up and activated correctly, the prompt should show
   `(resq)`

## Data Pipeline

The [Data pipeline](data-exploration-and-pipeline.ipynb) is a notebook that explores the data in the sqlite database, and answers the Analyst's questions to make life easier for the Analyst. The [Data pipeline](data-exploration-and-pipeline.ipynb) also has a simple Data Pipeline that creates the needed presentation tables and Views in the sql database. The Analysis can further query the database via the views without having to do complex sql and joins. 

Click [here (Data pipeline) ](data-exploration-and-pipeline.ipynb) to view the pipeline script

## References

* [Gartner - Customer Lifetime Value (CLV): A Critical Metric for Building Strong Customer Relationships, Gartner][gartner_clv]
* [SalesCummications.fi - Customer Lifetime Value (CLV) - What is it and why is it important for a company?][SalesCommmunication.fi]


[gartner_clv]: https://www.gartner.com/en/digital-markets/insights/what-is-customer-lifetime-value
[SalesCommmunication.fi]: https://www.salescommunications.fi/vastaukset/kuinka-asiakkaan-elinkaaren-arvo-lasketaan
[minconda]: https://docs.conda.io/en/latest/miniconda.html
