"""CSC110 Fall 2020 Final Project, Projection Data Module.

Description
===============================
In this module, we use a simple linear regression algorithm to do a
projection of the carbon emission per capita for each country in the future
20 years starting from 2015

Copyright and Usage Information
===============================
This file is the final project of four students taking CSC110 at the
University of Toronto St. George campus. All forms of distribution
of this code, whether as given or with any changes, are expressly
prohibited.

This file is Copyright (c) 2020 Kevin Cai, Junsong Guo, Yiteng Zhang and Patrick Zhou.
"""
from typing import List, Tuple
from convert_to_data import extract_data_from_txt, EmissionPerCapita, read_csv_file,\
    calculate_emission_per_capita


def predict_epc(all_epc_data: List[EmissionPerCapita], startyear: int, endyear: int,
                years: int) -> None:
    """Mutate the epc_data to include the epc of future years.

    Preconditions:
        - all_epc_data != []
        - 1965 < startyear < endyear
    """
    # line y = a + b * x.
    for epc_data in all_epc_data:
        convert_data = convert_to_xy(epc_data, startyear)

        a, b = simple_linear_regression(convert_data)
        for i in range(years):
            estimate = a + b * (endyear + 1 + i)
            epc_data.epc_year.append(estimate)


def simple_linear_regression(points: list) -> tuple:
    """Perform a linear regression on the given points.

    Preconditions:
        - points != []
    >>> simple_linear_regression([(1.0, 1.0), (2.0, 2.0), (3.0, 3.0)])
    (0.0, 1.0)
    """
    # the line y = a + b * x.
    x_avg = calculate_average(convert_points(points)[0])
    y_avg = calculate_average(convert_points(points)[1])
    b = sum([(points[x][0] - x_avg) * (points[x][1] - y_avg) for x in range(0, len(points))]) / sum(
        [(points[x][0] - x_avg) ** 2 for x in range(0, len(points))])

    a = y_avg - b * x_avg
    return (a, b)


def convert_points(points: List[Tuple[float, float]]) -> tuple:
    """Return a tuple of two lists, containing the x- and y-coordinates of the given points.

    Preconditions:
        - points != []
    >>> result = convert_points([(0.0, 1.1), (2.2, 3.3), (4.4, 5.5)])
    >>> result[0]  # The x-coordinates
    [0.0, 2.2, 4.4]
    >>> result[1]  # The y-coordinates
    [1.1, 3.3, 5.5]
    """
    x_coord = [points[x][0] for x in range(0, len(points))]
    y_coord = [points[x][1] for x in range(0, len(points))]

    return (x_coord, y_coord)


def calculate_average(numbers: list) -> float:
    """Calculate the average given a list of floats.

    Preconditions:
        - numbers != []
    """
    return sum(numbers) / len(numbers)


def convert_to_xy(epc_data: EmissionPerCapita, startyear: int) -> List[Tuple[float, float]]:
    """Convert epc_data into a list of tuples in the form (x, y) where x is the year
    and y is the epc.

    Preconditions:
        - epc_data != []
        - start_year > 1965
    """
    lst = []
    for i in range(len(epc_data.epc_year)):
        lst.append((float(startyear + i), epc_data.epc_year[i]))
    return lst


if __name__ == '__main__':
    emissions = extract_data_from_txt('carbon_emission.txt')
    populations = read_csv_file('population.csv')
    emission_per_capita = \
        calculate_emission_per_capita(emissions, populations, 1960, 2014)  # 1960 - 2014 inclusive

    start_year = emission_per_capita[0].start_year
    end_year = emission_per_capita[0].end_year

    predict_epc(emission_per_capita, start_year, end_year, 20)
    # update each country's epc_year list to include the projected data of future 20 years

    # import python_ta.contracts
    #
    # python_ta.contracts.check_all_contracts()
    # import doctest
    #
    # doctest.testmod()
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'extra-imports': ['convert_to_data', 'plotly.graph_objects', 'python_ta.contracts'],
    #     # the names (strs) of imported modules
    #     'allowed-io': [],  # the names (strs) of functions that call print/open/input
    #     'max-line-length': 100,
    #     'disable': ['R1705', 'C0200']
    # })


# uncomment to generate a graph for a specific country, for testing purposes

# def plot_points(x_coords: list, y_coords: list) -> None:
#     """Plot the given x- and y-coordinates using plotly. Then display results
#      in a web browser.
#     """
#     # Create a blank figure
#     fig = go.Figure()
#
#     # Add the raw data
#     fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='markers', name='Data'))
#
#     # Display the figure in a web browser.
#     fig.show()


# x = convert_to_xy(emission_per_capita[71], emission_per_capita[71].start_year)
# a, b = convert_points(x)
# plot_points(a, b)
