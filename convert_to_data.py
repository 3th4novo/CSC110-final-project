"""CSC110 Fall 2020 Final Project, Read Datasets Module.

Description
===============================
In this module, we convert the datasets we obtained into data types we can use for our algorithms
and generating our graph

Copyright and Usage Information
===============================
This file is the final project of four students taking CSC110 at the
University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Kevin Cai, Junsong Guo, Yiteng Zhang and Patrick Zhou.
"""
import csv
from dataclasses import dataclass
from typing import List
import re


@dataclass
class Population:
    """A data type representing a country's population.

    This corresponds to one row of the tabular data found in population.csv.

    Attributes:
        - name: the name of the country
        - number_year: the number of the population per year from 1960 to 2014

    Representation invariants:
        - self.name != ''
        - self.number_year != []
    """
    name: str
    number_year: List[str]


@dataclass
class CarbonEmission:
    """A data type representing a acountry's carbon emissions.

    This corresponds to one row of the tabular data found in ttc-subway-delays.csv.

    Attributes:
        - name: the name of the country
        - number_year: the amount of the total carbon emission per year from 1960 to 2014

    Representation invariants:
        - self.name != ''
        - self.amount_year != []
    """
    name: str
    amount_year: List[int]


@dataclass
class EmissionPerCapita:
    """A data type representing a specific subway delay instance.

    This corresponds to one row of the tabular data found in ttc-subway-delays.csv.

    Attributes:
        - name: the name of the country
        - start_year: start year of the data
        - end_year: end year of the data
        - number_year: the amount of emission per capita per year from start year
        to end year (inclusive)

    Representation invariants:
        - self.name != ''
        - self.amount_year != []
    """
    name: str
    start_year: int
    end_year: int
    epc_year: List[float]


def calculate_emission_per_capita(emissions: List[CarbonEmission],
                                  populations: List[Population],
                                  start_year: int, end_year: int) -> List[EmissionPerCapita]:
    """Calculate emissions per capita

    Preconditions:
        - emissions != []
        - population != []
        - 1965 < start_year < end_year
    """
    epc = []
    for i in range(len(emissions)):
        name1 = emissions[i].name
        for j in range(len(populations)):
            name2 = populations[j].name
            epc_per_year = []
            # check if the country has both data
            if name1.lower() == name2.lower():

                for year in range(len(emissions[i].amount_year)):
                    emission = emissions[i].amount_year[year]

                    # use the data from previous year if the data is missing a year
                    if populations[i].number_year[year] == '':
                        population = int(populations[i - 1].number_year[year])
                    else:
                        population = int(populations[i].number_year[year])

                    epc_per_year.append(emission / population)

            if not epc_per_year == [] and len(epc_per_year) == end_year - start_year + 1:
                epc.append(EmissionPerCapita(name2, start_year, end_year, epc_per_year))
    return epc


def read_csv_file(filename: str) -> any:
    """Return the data stored in a csv file with the given filename.

    Preconditions:
        - filename != ''
    """
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        data = [process_row_p(row) for row in reader]

    return data


def process_row_p(row: []) -> Population:
    """Convert a row of data to Population object.

    Preconditions:
        - row != []
    """
    return Population(name=row[0], number_year=[row[i] for i in range(1, len(row) - 5)])
    # 1960-2014


def extract_data_from_txt(filename: str) -> any:
    """Return the data stored in a text file with the given filename.

    Preconditions:
        - filename != ''
    """
    # List[Dict[str, List[int]]]
    ce_file = open(filename, 'r')
    ce_text = ce_file.read()
    ce_structure_pattern = re.compile(r"""
        \n(\w+)\n              # the line with the country name 
        \s+Total\s.*\n         # the line start with at least 1 spaces and "Total Fossil-Fuel"
        Year\s+.*\n\n          # the line start with "Year        Emissions"
        ((\d+\s+\d+\s+.*\n)+)  # the lines with actual data
        """, re.VERBOSE | re.MULTILINE)
    ce_line_pattern = re.compile(r"""
        (\d+)    # year number
        \s+      # the space between year number and Total Fossil-Fuel Emissions data 
        (\d+)    # the Total Fossil-Fuel Emissions data
        \s+      # the spaces after Total Fossil-Fuel Emissions
        .*\n     # the rest of the line
    """, re.VERBOSE)
    countries = ce_structure_pattern.findall(ce_text)

    data = [process_row_c(country_data, ce_line_pattern) for country_data in countries]
    return data


def process_row_c(country_data: str, ce_line_pattern: any) -> CarbonEmission:
    """Convert a row of data to Carbon_emission object.

    Preconditions:
        - country_data != ''
    """
    return CarbonEmission(name=country_data[0],
                          amount_year=[int(row[1]) for row in
                                       ce_line_pattern.findall(country_data[1])
                                       if int(row[0]) >= 1960])  # 1960-2014


if __name__ == '__main__':
    emissions_g = extract_data_from_txt('carbon_emission.txt')
    populations_g = read_csv_file('population.csv')
    emission_per_capita = calculate_emission_per_capita(emissions_g, populations_g, 1960, 2014)
    # 1960 - 2014 inclusive

    # import python_ta.contracts
    #
    # python_ta.contracts.check_all_contracts()
    # import doctest
    #
    # doctest.testmod()
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['csv', 'dataclasses', 're', 'python_ta.contracts'],
    #     # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })
