"""CSC110 Fall 2020 Final Project, Main Module.

Description
===============================
In this module, we import the Read Datasets Module, Projection Data Module,
and Visualization Module to run our project.

Copyright and Usage Information
===============================
This file is the final project of four students taking CSC110 at the
University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Kevin Cai, Junsong Guo, Yiteng Zhang and Patrick Zhou.
"""

from convert_to_data import extract_data_from_txt, read_csv_file, calculate_emission_per_capita
from predict_future_epc import predict_epc
from visualization import visualize


def run_example(predicted_years=20) -> None:
    """Run the project.

    Instructions:
      - 1. run this file in the python console.
      - 2. run run_example function in the python console. You can change
      the input to control the number of years you want to predict.
      - 3. wait until your web browser opens, and the a page with the title
      "CO2 Emission Data (Predicted after year: 2014)" at the upper left corner.
      - 4. click the "play" button.
      - 5. enjoy our show! :)

    Sample usage:
    >>> run_example()
    """

    # Get all the data needed.
    emissions = extract_data_from_txt('carbon_emission.txt')
    populations = read_csv_file('population.csv')
    emission_per_capita = calculate_emission_per_capita(emissions, populations, 1960, 2014)

    # Mutate the data with prediction.
    start_year = emission_per_capita[0].start_year
    end_year = emission_per_capita[0].end_year
    predict_epc(emission_per_capita, start_year, end_year, predicted_years)

    # Visualize the mutated data.
    visualize(emission_per_capita, predicted_years, "CO2 Emission Data", 1)


# __main__

# example 1: predict the data of 20 years in the future starting from 2015
# run_example()

# example 2: predict the data of 50 years in the future starting from 2015
# run_example(50)
