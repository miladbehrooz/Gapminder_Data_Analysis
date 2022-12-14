from bokeh.io import output_notebook
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, CategoricalColorMapper, Button
from bokeh.palettes import Spectral6
from bokeh.models import Slider
from bokeh.layouts import column, row
from bokeh.io import curdoc
import pandas as pd 


def update_plot(attr, old, new):
    
    year = slider.value
    subset = df.loc[df['year'] == year]
    subset['population'] = subset['population']//15000000
    
    # Assign subset to source.data
    source.data = subset
    
    # Add title to plot
    p.title.text = f'Correlation between life expentency and fertility rate for year {year}'

def animate_update():
    year = slider.value + 1
    if year > 2015:
        year = 1950
    slider.value = year

#create global variable for callback
callback_animate = None


def animate():
    global callback_animate
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_animate = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_animate)



year = 1950
df = pd.read_csv('../data/data.csv')
subset = df.loc[df['year'] == year]
subset['population'] = subset['population']//15000000

source = ColumnDataSource(subset)

# Define collormapper
mapper = CategoricalColorMapper( factors = list(subset['continent'].unique()),
                                 palette=Spectral6)

# Create the figure: p
p = figure(title = f'Correlation between life expentency and fertility rate for year {year}',plot_height=600,plot_width=900, x_axis_label='fertility_rate', y_axis_label='life_expectancy')




# Add a circle glyph to the figure p
p.circle('life_expectancy', 'fertility_rate', size = 'population',fill_alpha=0.6,
         source=source,color={'field': 'continent', 'transform': mapper},legend_field='continent')

p.legend.location = 'bottom_left'
p.x_range.start = 0
p.x_range.end = 100
p.y_range.start = 0
p.y_range.end = 9


slider = Slider(start=1950, end=2015, step=1, value=1950, title='Year')
slider.on_change('value', update_plot)

#create the button and set on-click callback
button = Button(label='► Play', width=60)
button.on_click(animate)

layout = row(column(slider,button), p)


# Replace output_file and show(layout) with this
curdoc().add_root(layout)
curdoc().title = 'Gapminder'
