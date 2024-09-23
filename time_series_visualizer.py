import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data
lower_bound = df['value'].quantile(0.025)
upper_bound = df['value'].quantile(0.975)

df = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)

    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    ax.set_xticks(pd.date_range(start='2016-05-01', end='2019-12-31', freq='6M'))
    ax.set_xticklabels(pd.date_range(start='2016-05-01', end='2019-12-31', freq='6M').strftime('%Y-%m'))

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    df_bar = df_bar.reindex(columns=month_order)
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12,10))
    df_bar.plot(kind='bar', ax=ax)

    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    ax.legend(title='Months')
    plt.xticks(rotation=90)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
