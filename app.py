import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from torch import nn
import torch
import gradio as gr

ts_data = pd.read_csv('data_daily.csv')

data = ts_data['Receipt_Count']

def calc_rmse(pred, true):
    total = 0
    for i in range(len(pred)):
        square = (pred[i] - true[i]) ** 2
        total += square
    mean_square = total / len(pred)
    root_mean_square = mean_square ** .5
    return root_mean_square

b0s = [7250000, 7500000, 7625000, 7750000]
alphas = [7000, 7270, 7400, 7500]

best_error = 10000000

for b0 in b0s:
    for alpha in alphas:
        values = [b0 + alpha * i for i in range(365)]
        error = calc_rmse(values, data)
        if error < best_error:
            best_alpha = alpha
            best_b0 = b0
            best_error = error


stationary = []

for i, elem in enumerate(data):
    stationary.append(elem - alpha * i)
    
std = np.var(stationary) ** .5
    
preds = []

for i in range(730):
    preds.append(np.round(b0 + alpha * i + np.random.normal(0, std)))

    
alpha = best_alpha
b0 = best_b0

ts_data['# Date'] = pd.to_datetime(ts_data['# Date'])
pred_dates = ts_data["# Date"].apply(lambda dt: dt.replace(year=2022))
new_frame = pd.DataFrame(pred_dates)
new_frame['Receipt_Count'] = preds[365:]
ts_data = pd.concat([ts_data, new_frame])


ts_data['Year'] = ts_data['# Date'].dt.year
ts_data['Month'] = ts_data['# Date'].dt.month
ts_data['Day'] = [i % 365 for i in range(1,731)]


monthly_data = ts_data.groupby(['Month', 'Year']).sum().reset_index()

def line_plot_fn(plot_type):
    if plot_type == "Monthly":
        
        return gr.LinePlot(monthly_data, x="Month", y="Receipt_Count", color="Year", overlay_point=True, tooltip="Receipt_Count")
    else:
        return gr.LinePlot(ts_data, x="Day", y="Receipt_Count", color="Year", overlay_point=True, tooltip="Receipt_Count")

with gr.Blocks() as line_plot:
    with gr.Row():
        with gr.Column():
            plot = gr.LinePlot()
            
            year_button = gr.Radio(label="Plot Type",
                      choices=['Daily', 'Monthly'], value="Monthly")
            year_button.input(fn=line_plot_fn, inputs=[year_button], outputs=[plot])
            line_plot.load(fn=line_plot_fn, inputs=[year_button], outputs=[plot])

        line_plot.launch()
