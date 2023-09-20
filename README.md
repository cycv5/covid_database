# Web API for Covid-19 data
assignment-2-8-cycv5-qe201020335

## API Documentation
Our API is deployed on Heroku with base URL `https://simple-covid.herokuapp.com/`. The base url will lead you to the swagger page where you can test the api.

We have documented our API in much detail with Swagger. **Click [HERE](https://simple-covid.herokuapp.com/docs/index.html?url=swagger.json) for the documentation.**

## Pair Programming

Our team did pair programming throughout the entire project. For the most part we only work on the code together when one of us is stuck, but we did do some real pair programming together as well.

From the beginning, Yichen tried to start with writing the basic structure for a flask app. Since Tianhe has more experience in API development, Yichen asked Tianhe to help him with the overall structure of the app. That includes setting up the flask structure, the different routes in our app as well as different HTTP methods that we would like to support. Tianhe has no experience in databases so he was stuck. Yichen took over and showed him how to set up a database, define the schemas and turn the user input (the csv files) into entries in the database. Yichen also completed the methods for querying data from the database. You will notice that in the commit, Yichen uses mostly placeholders or hardcoded values for user input. That is because he didn’t know how to properly get the HTTP requests from the users and parse them to get the relevant information. Tianhe then helped Yichen implement the code for getting information from the requests. Together the team did some code review as well as developed the proper APIs to put onto Swagger.

As a group we think the experience was very positive. We usually do pair programming without even noticing it. Online video chatting and code sharing apps (codeTogether for example) make this experience easier than ever. Compared to simply dividing the work, pair programming gives the benefit of learning something new in the process and thinking together when stuck. We helped each other along the way and caught plenty of mistakes/typos in the code that otherwise wouldn’t be noticed that quickly. A small negative would be that the two of us must have a common time slot in our busy schedule to sit down and work together. This could be unviable for some, but fortunately it worked out well for us.

## Program Design

### Structure
**The program structure can easily be viewed & tested on Swagger, the introduction below will be brief.**
* Uploads: The upload route lets you upload your files. We think it would be very clear to have the type of the file you are uploading in the route.

  * /time_series/<data_type> (post, put):
This is for uploading time_series data. The data_type specifies what the numbers in the csv form represent (death, confirmed, active or recovered).

  * /daily_report/< date > (post, put):
This is for uploading a daily report. The program will parse the information for you. You need to give a date for the daily report.

* Queries
  * /cases (get):
This is where you can make queries on the data. Again, we think this is very intuitive to have a route for querying data. Parameters of the query will be supplied as parameters of the request.

The main objective is to make this program as clear as possible without super long routes or unclear names. And we made sure that post, put and get methods are implemented in their most intuitive ways, e.g. querying data would be a get and uploading a file to the system would be a post.

* Database: We design the database so that we can store only the relevant information. We have 4 tables in our database representing the death, confirmed, active and recovered table. Within each table, we have country_region, state_province, combined_key, cases, and date. This results in a fast search speed and any relevant information can be found within those four tables.

### API design
For uploading the time series data, we need the type of the data in the url. For daily report we require a date for this report (yyyy-mm-dd). This is to avoid any confusions or misinterpretation of the content where the program parses a date that is not intended.

For querying the data, we support querying multiple locations and with multiple types of cases. In swagger, hold ctrl and click on the types of data you would like to get. **Note that we will query the data exactly as the input**, that means we will look for the exact combination of country, state, and combined key as you supplied (you may leave at most two fields blank). This is to avoid any data being a subset of another query result. We also support queries on a single day or a time period. For a single day query, simply enter the start date and leave the end date blank.

## CICD and testing
The deployment can be viewed at `https://simple-covid.herokuapp.com/`. We used Circle CI for the CICD tool. **Click [HERE](https://app.circleci.com/pipelines/github/csc301-fall-2021/assignment-2-8-cycv5-qe201020335?invite=true)** to join and see our CICD progress. Or **click [HERE](https://app.circleci.com/pipelines/github/csc301-fall-2021/assignment-2-8-cycv5-qe201020335/38/workflows/f1115916-3672-43bd-838c-5c430a7a9c5e/jobs/38)** to view the progress. Note that it might require you to log into Circle CI first since the repo is private. You can also see the cicd progress directly on github. The CICD tool also generate our test coverage report as the artifact. It is in a zip file. The test coverage is **85%**. For you convenience, we have included the zip file in this repo **[here](/coverage_test.zip)**. Once downloaded, open the zip file and you can view the coverage test result in htmlcov/main_py.html

## Notes on Testing the API
* The upload part could take quite some time to complete. This is to make the querying fast.
* We gave a lot of examples on swagger showing you the expected input and output format.

