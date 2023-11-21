To solve this problem, I used differencing to stationarize the time series and fitted a simple autoregressive model. First, I looked at the autocorrelation function for the time series to determine the degree of differencing required. After determining that the time series data exhibited only first order differencing, I fitted an autoregressive model of the form y = b_0 + alpha * t + e. The optimal values for b_0 and alpha were found by fitting different models and comparing the root mean squared error. To make the simulation more realistic, I also added Gaussian white noise with standard deviation equal to the std of the stationarized data. 

I displayed my results in an interactive lineplot built with Gradio. To run the app, enter the following command into the command line: 

$ docker run -p 7860:7860 -e GRADIO_SERVER_NAME=0.0.0.0 sample

Afterwards, go to http://localhost:7860/, where the Gradio app should be running. 