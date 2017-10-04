
# 2015 U.S. Domestic Flight Delays Analysis

## Summary

Hundreds of thousands of U.S. passengers take domestic flights to fly across the country every day. Many of them have had a bad experience with an airline, which is a common problem in commercial air travel industry. The U.S. Department of Transportation's (DOT) Bureau of Transportation Statistics tracks the on-time performance of domestic flights operated by large air carriers. The visualization I created is based on 2015 flight delays data provided by DOT and available on [Kaggle](https://www.kaggle.com/usdot/flight-delays). The Tableau story attempts to provide the audience the answers of the following questions:  
1. Which airlines is most punctual?
2. Which airport are the busiest and what are their average flight delay time?
3. What are the average departure and arrival delays of a given route?

## Design

### Version 1

[View visualization on Tableau Public](https://public.tableau.com/views/flights_analysis_v1_0/Storyv1?:embed=y&:display_count=yes)

* First, I created a few new calculate fields in Tableau for the percentage of on-time arrival and on-time departure flights of each airline. I defined on-time arrival flights as those flights arrive at the gate less than 15 minutes after the scheduled arrival time. Similary, on-time departure flight departs gate less than 15 minutes after the scheduled departure time. Then I designed a slope chart to illustrate the ranking of the airlines on-time performance. Slope chart is chosen here because the lines in the slope chart can show the difference of the on-time departure ranking and on-time arrival ranking across all airlines.


* I created a Tableau map view to display the top 50 busiest airports based on total number of flights they handled. By plotting the data on a map, the audience can immediate spot which airport has more flights and their location. It is much more efficient than using bar chart. However, I only showed the top 50 busiest airports because there are more than 300 airports in the dataset, and showing them all in the map make the visualization very clutter.
I also created two sorted tables to display the total number of flights and the average flight delay of each airport. The audience can use these tables to find the exact value of this information of each airport shown the map.    



* I created two bar different charts to compare the average arrival and departure delays of a given route. Users can choose the airline, origin airport and destination airport of the route they interested in to find out the average delay time of the route. I chose to use bar charts to allow users to compare the flight delay across different routes.

---
### Version 2

[View visualization on Tableau Public](https://public.tableau.com/views/flights_analysis_v2_0/Storyv2?:embed=y&:display_count=yes&publish=yes)

Based on the feedback that I received, I made following changes to the visualization:  
* I added two small notes to explain the on-time arrival and on-time departure rates in the dashboard. In the slope chart, I also compared the on-time performance along with the total number of flights the airlines handled. I also created an additional scatter plot to visualize the relationship of the on-time performance and the total number of the flights. Scatter plot is the perfect choice to visualize relationships between numerical variables.


* I created two additional bar charts and organized them in a dashboard to show the total number of flights and the average flight delay of all airports. With these additional bar charts, now the user can compare the number of flights and the average delay of all airports, not limited to the top 50 busiest airports. I chose to use stacked bar chart for average flight delay of the airports because flight delay is comprised of arrival delay and departure delay.


* I created two maps to show the path of the routes and the flight delays information. The information displayed in the map is same as the bar charts created in previous version but with more attractive visualization. Map is chosen here because it allows the audience to visualize the route easily compared with the bar charts. By just hovering the mouse over the route, the tables beside the map can immediate show the total number of flights and departure/arrival delays of the route. It is more efficient compared with using bar charts because not all audience are familiar with the airport code of their flight.

## Feedback

### Feedback for Version 1

> I can immediate see the Hawaiian Airlines has highest on-time arrival and on-time departure rates. But how do you define on-time arrival and on-time departure rates?  

> Beside the punctuality ranking, I’m also interested in the relationship of the on-time performance and the total number of the flights the airlines scheduled in 2015.  

> From the map, I can immediate see the airports in Atlanta and Chicago handled a lot of flights. The average flight delay is also encoded with color scale. While the airports are represented in codes, but the tooltips display the whole name of the airports along with other useful information.  

> Beside the top 50 busiest airports, it would be nice if I could also compare the air traffic and the average delay of other airports too.  

>The final charts allow me to know the average departure and arrival delays of a certain route. It would be better if I could visualize the path between an origin airport and the destination airport on a map.  

___
### Feedback for Version 2
>From the chart, now I know while Hawaiian Airlines ranked lowest in total number of flights, but they have highest on-time performance. Southwest Airlines is the biggest airline in term of total number of flights, but their on-time performance is not as good as other airlines.

> The two additional charts allow me to check the total air traffics and average flight delays of any airport. These are useful additional features in addition to the map that shows the top 50 busiest airports.

> The newly created maps are very informative. Now I can see the path of the route in addition of the number of flights and average delay. Perhaps I will use it next time to check the average delays of my next flight.


## Resources
1. [2015 Flight Delays and Cancellations](https://www.kaggle.com/usdot/flight-delays)  
2. [How To: Using Ranks to Create Slope Graphs in Tableau](http://sirvizalot.blogspot.sg/2015/10/how-to-using-ranks-to-create-slope.html)  
3. [Creating a Stacked Bar Chart Using Multiple Measures](http://kb.tableau.com/articles/howto/stacked-bar-chart-multiple-measures)  
4. [Great Arcs in Tableau by Chris DeMartini](http://www.datablick.com/blog/2016/01/11/great-arcs-in-tableau-by-chris-demartini)  
5. [Create Maps that Show Paths Between Origins and Destinations in Tableau](https://onlinehelp.tableau.com/current/pro/desktop/en-us/maps_howto_origin_destination.html)
6. [Taking Off with the Path Function](https://public.tableau.com/en-us/s/blog/2015/07/taking-path-function)
7. [What are the chances your plane will be delayed?](https://public.tableau.com/en-us/s/blog/2010/01/what-are-chances-your-plane-will-be-delayed)
8. [A Rough Guide to Dashboard Actions](https://public.tableau.com/en-us/s/blog/2015/06/rough-guide-dashboard-actions)
