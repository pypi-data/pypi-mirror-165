def Pareto(data, x, aggcol=None, aggfunc='count', limit=10, others_bar=False, others_name='Other Categories', 
           ax1_ylabel=None, ax2_ylabel='Cumulative Percentage (%)', barcolor=None, linecolor=None, **kwargs):
    '''
    Function to create a Pareto chart.

    A Pareto chart is a sorted barchart with a second line that shows the cumulative 
    percentage on a second y-axis.

    Six Sigma practitioners often use pareto charts to quickly indicate the largest issue.

    Arguments:
      - data (required): 
      - x (required):
      - aggcol (default = None): The column to run the aggregation on. If it is None, a new 
        column of all ones is created.
      - limit (default = 10): The number of columns to display. If limit is set to None, 
        all columns are displayed.
      - others_bar (default = False): If limit is not None, this adds a bar for all other 
        values.
      - others_name (default = 'Other Categories'): If an others bar is created, this sets 
        the name for that bar.
      - ax1_ylabel (default = None): Y Axis label for bars (left y axis). If None, uses x.
      - ax2_ylabel (default = 'Cumulative Percentage (%)'): Y Axis label for line (right y 
        axis).
      - barcolor (default = None): The color of the bars portion of the Pareto chart. If None, 
        this is set to the first default color.
      - linecolor (default = None): The color of the lines portion of the Pareto chart. If None, 
        this is set to the second default color.
      - **kwargs: Any additional keyword arguments you would like to pass to 
        matplotlib.axes.Axes.bar or matplotlib.axes.Axes.plot.
    '''
    import pandas as pd
    import matplotlib.pyplot as plt

    assert x in data.columns, 'Please double-check that x is a column in data'

    ###################
    # Data Processing #
    ###################
    if aggcol == None:
        aggcol = aggfunc
        data[aggfunc] = 1
    
    # Groupby x, run aggfunc on aggcol
    data = data.groupby(x)[aggcol].agg(func=aggfunc)
    # Sort the values
    data = data.sort_values(ascending=False)
    # Reset index
    data = data.reset_index()

    ###################
    # Handle Settings #
    ###################
    if others_bar & (data.shape[0] > limit):
        data.loc[limit - 1, aggfunc] = data.iloc[limit:][aggfunc].sum()
        data.loc[limit - 1, x] = others_name

    if limit != None:
        data = data.head(limit)
    
    if linecolor == None:
        linecolor = plt.rcParams['axes.prop_cycle'].by_key()['color'][1]

    if ax1_ylabel == None:
        ax1_ylabel = aggfunc

    # Calculate cumulative percentage
    cumulative_percentage = 100 * data[aggfunc].cumsum() / data[aggfunc].sum()
    
    ##############
    # Make Plots #
    ##############
    fig = plt.gcf()
    
    # Create fist axis
    ax1 = fig.add_subplot()

    # Add bars
    ax1.bar(data[x], data[aggcol], color=barcolor, **kwargs)
    

    # Formatting
    ax1.set_ylabel(ax1_ylabel)
    #plt.xticks(ax1.get_xticks(), ax1.get_xticklabels(), rotation='vertical')

    # Create second axis
    ax2 = ax1.twinx()

    # Plot the cumulative Percentage Line
    ax2.plot(cumulative_percentage, color=linecolor, **kwargs)

    # Formatting
    ax2.set_ylim(0, 100)
    ax2.grid(False)
    ax2.set_ylabel(ax2_ylabel)

    return fig, ax1, ax2