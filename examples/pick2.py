import pandas as pd
import numpy as np
import plotly.graph_objects as go

def visualize3DData(X, ids, df):
    fig = go.Figure()

    # Add scatter plot
    scatter = fig.add_trace(
        go.Scatter3d(
            x=X[:, 0],
            y=X[:, 1],
            z=X[:, 2],
            mode='markers',
            marker=dict(size=5, color='blue'),
            text=ids,
            hoverinfo='text'
        )
    )

    def handle_click(trace, points, state):
        if points.point_inds:
            # Get the frame id of the clicked point
            clicked_frame_id = ids.iloc[points.point_inds[0]]

            # Call a custom function with the frame id
            handle_click_event(clicked_frame_id)

    def handle_click_event(frame_id):
        # Do something with the frame id
        print('Clicked frame id:', frame_id)

        # Remove the row based on the frame id from the DataFrame
        df.drop(df[df['frame_id'] == frame_id].index, inplace=True)

        # Update the scatter plot with the new DataFrame
        scatter.update(
            x=df['index_x_coor'],
            y=df['index_y_coor'],
            z=df['index_z_coor'],
            text=df['frame_id']
        )

    # Register the on_click function
    scatter.on_click(handle_click)

    fig.update_layout(scene=dict(aspectmode='cube'))
    fig.show()

# Simulate DataFrame from CSV (replace this with your actual DataFrame loading)
csv_file_path = 'Signatures/2.csv'
df = pd.read_csv(csv_file_path)
ids = df['frame_id']
X = df[['index_x_coor', 'index_y_coor', 'index_z_coor']].to_numpy()

# Call the function to visualize the data
visualize3DData(X, ids, df)
