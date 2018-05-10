# Tracking The Dons  
#### Alex Howard and Taylor Pellerin

----- 
  
    
### About the authors
[Alex](https://www.linkedin.com/in/alexanderjhoward/) and [Taylor](https://www.linkedin.com/in/tjpell/) are both 
students at The University of San Francisco's 
[MS in Data Science program,](https://www.usfca.edu/arts-sciences/graduate-programs/data-science) slated to graduate at 
the end of June, 2018. Alex is an athlete on the university's 
[track and field team](https://usfdons.com/index.aspx?path=tf) and regularly uses 
[Strava](https://www.strava.com/features) to record and track his workout progress.
 
 
### About the project
While [Strava's](https://www.strava.com/features) application includes a handful of internal visualizations, 
[their API](http://developers.strava.com/) allows users to pull out their workout data to analyze on their own. Using 
this, many users have developed their own apps, which [Strava shares a selection of.](https://www.strava.com/apps)  

Alex has a strong idea about the statistics he is most interested in tracking and comparing, so we built an application 
using [Plotly Dash](https://plot.ly/products/dash/) that allows the user log in to Strava and interact with their data 
in a handy and intuitive to use dashboard. If you are not yet on Strava, but still want to play with the app, Alex has 
been kind enough to share his workout history for you to investigate and a handy tutorial explaining how to interact 
with the dashboard.

We are still in development, but once the app goes live, we will share it here!

### How to use locally
1. `$ git clone https://github.com/ajhoward7/tracking-the-dons.git`
2. `$ cd tracking-the-dons`
3. `$ pip install -r requirements.txt`
4. `$ sudo python index.py` (sudo becasue we are opening port 80)
5. Pop open your browser and enjoy!