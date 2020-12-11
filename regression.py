'''CSC110 Fall 2020 Final assignment Multiple Variable Linear Regression

Provides an implementation of Multiple Variable Linear Regression, as well as a test case


Copyright and Usage Information
===============================

This file is provided solely for the final assignment of CSC110 at the University of Toronto
St. George campus. All forms of distribution of this code, whether as given or with any changes,
are expressly prohibited.

This file is Copyright (c) 2020 Kenneth Miura.
'''
import numpy as np
import data_processing
from sklearn.linear_model import LinearRegression
import math


def linear_regression(X: np.array, y: np.array, num_of_iterations: int,
                      learning_rate: float) -> np.array:
    '''Return a list of coefficients for X that best predict Y.


    Let n be the length of the tuples inside X.
    The returned list of coefficients will be in the form (x_1,x_2, ... , x_n , b),
    where x_1 is the weight for the 1st independent variable. b is an offset.

    Preconditions:
    - X.size != 0
    - y.size != 0
    - num_of_iterations > 0
    - learning_rate > 0

    '''
    error_over_time = []
    num_of_data_points = X.shape[0]
    # Adding a coefficient of 1 to allow for the offset
    X = np.append(X, np.ones((num_of_data_points, 1)), axis=1)
    y = np.array(y).astype(np.float64).reshape((-1, 1))
    params = np.zeros((X.shape[1], 1))

    for _ in range(num_of_iterations):
        prediction = np.dot(X, params)
        error = (y - prediction)
        mean_squared_error = (np.dot(error.T, error)) / num_of_data_points

        error_over_time.append(mean_squared_error.item())
        gradient = (np.dot(X.T, prediction) - np.dot(X.T, y)) * 2 / num_of_data_points
        params = params - learning_rate * gradient
    print(f'Final error: {error_over_time[-2]}')
    # breakpoint()
    return params


def test_linear_regression(iterations=10000, learning_rate=0.4) -> None:
    '''


    Based off https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols_3d.html#sphx-glr-auto-examples-linear-model-plot-ols-3d-py (CITE THIS LATER!)
    and
    https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression
    '''

    # NOTE: the sklearn methods want np array in form (index of the datapoint, variable), which they are rn
    _, proportions = data_processing.read_powerplant_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                          'countries of the world.csv')
    _, emissions = data_processing.read_carbon_emission_file('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                             'countries of the world.csv')
    np_proportions = np.array(proportions)
    np_emissions = np.array(emissions).astype(float).reshape((-1, 1))
    train_index = math.floor(len(np_proportions) * 0.8)

    X_train = np_proportions[:train_index, :]
    X_test = np_proportions[train_index:, :]
    y_train = np_emissions[:train_index, :]
    y_test = np_emissions[train_index:, :]
    reg = LinearRegression().fit(X_train, y_train)
    print(f'sklearn coeff: {reg.coef_}, sklearn intercept: {reg.intercept_}')
    reg_error = reg.predict(X_test) - y_test
    reg_error_average = np.average(reg_error)
    print(f'sklearn average error: {reg_error_average}')

    homebrew_coeff = linear_regression(X_train, y_train, iterations, learning_rate)
    print(f'homebrew coeff: {homebrew_coeff[:-1]}, homebrew intercept: {homebrew_coeff[-1]}')
    np_coeffs = np.array(homebrew_coeff)[:-1]
    offset = homebrew_coeff[-1]
    prediction = np.dot(X_test, np_coeffs) + offset
    homebrew_error = prediction - y_test
    homebrew_error_average = np.average(homebrew_error)
    print(f'homebrew average error:{homebrew_error_average}')

    print(f' difference in average error:{abs(homebrew_error_average) - abs(reg_error_average)}')

    tolerance = 1
    assert (abs(homebrew_error_average) <= abs(reg_error_average) + tolerance)


def test_nuclear_regression(iterations=10000, learning_rate=0.4):
    _, num_of_nuclear = data_processing.read_nuclear_powerplant('global_power_plant_database.csv', 'owid-co2-data.csv',
                                                                'countries of the world.csv')
    _, nuclear_emissions = data_processing.read_nuclear_powerplant_co2('global_power_plant_database.csv',
                                                                       'owid-co2-data.csv',
                                                                       'countries of the world.csv')
    np_nuclear = np.array(num_of_nuclear).reshape(-1, 1)
    np_nuclear_emissions = np.array(nuclear_emissions).astype(float).reshape(-1, 1)

    train_index = math.floor(len(np_nuclear) * 0.8)

    X_train = np_nuclear[:train_index]
    X_test = np_nuclear[train_index:]
    y_train = np_nuclear_emissions[:train_index]
    y_test = np_nuclear_emissions[train_index:]
    reg = LinearRegression().fit(X_train, y_train)
    print(f'sklearn coeff: {reg.coef_}, sklearn intercept: {reg.intercept_}')
    reg_error = reg.predict(X_test) - y_test
    reg_error_average = np.average(reg_error)
    print(f'sklearn average error: {reg_error_average}')

    homebrew_coeff = linear_regression(X_train, y_train, iterations, learning_rate)
    print(f'homebrew coeff: {homebrew_coeff[:-1]}, homebrew intercept: {homebrew_coeff[-1]}')
    np_coeffs = np.array(homebrew_coeff)[:-1]
    offset = homebrew_coeff[-1]
    prediction = np.dot(X_test, np_coeffs) + offset
    homebrew_error = prediction - y_test
    homebrew_error_average = np.average(homebrew_error)
    print(f'homebrew average error:{homebrew_error_average}')
    print(f' difference in average error:{abs(homebrew_error_average) - abs(reg_error_average)}')


if __name__ == '__main__':
    import python_ta

    # TODO: configure pyta

    # python_ta.check_all(config={
    #     'max-line-length': 100,
    #     'extra-imports': ['python_ta.contracts', 'numpy', 'data_processing', 'sklearn.linear_model'],
    #     'disable': ['R1705', 'W1114']
    # })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
    import pytest

    # pytest.main(['regression.py'])
