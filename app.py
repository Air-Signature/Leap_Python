import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import tensorflow as tf
from sklearn.metrics import confusion_matrix


def create_dataset(X, y, time_steps, step=1):
    Xs, ys = [], []
    for i in range(0, len(X) - time_steps, step):
        x = X.iloc[i:(i + time_steps)].values

        labels = y.iloc[i: i + time_steps]

        Xs.append(x)
        ys.append(stats.mode(labels)[0])
    return np.array(Xs), np.array(ys).reshape(-1, 1)

# Load the saved model


loaded_model = keras.models.load_model("intermittent1.h5")

test_df2 = pd.read_csv('./Sign/1.csv')
test_df2 = test_df2.dropna(how='any',axis=0)

X_test2 = test_df2.drop(['frame_id', 'target'], axis=1)  # Features
# X_test2 = X_test2[[ 'index_x_coor', 'index_y_coor', 'index_z_coor', 'palm_x_coor', 'palm_y_coor', 'index_x_velocity', 'index_z_velocity', 'palm_velocity_x', 'confidence', 'armPosition_x', 'armPosition_y', 'tip_rotation_w', 'menger_curvature', 'index_x_acc', 'index_y_acc', 'index_y_jrk', 'index_z_jrk', 'slope_phi_x', 'slope_phi_z', 'Tx', 'Tz', 'dTz', 'mag_dT', 'Nx', 'Nz']]
y_test2 = test_df2['target']  # Target variable

X_test2,y_test2 = create_dataset(X_test2, y_test2, 20, step=1)


y_pred_binary2 = (loaded_model.predict(X_test2) > 0.5).astype("int32")

zeros_array = np.ones((20, 1), dtype=np.int32)

# Concatenate the arrays
y_pred_binary2 = np.concatenate((zeros_array, y_pred_binary2), axis=0)
test_df2['pred'] = y_pred_binary2

# conf_matrix = confusion_matrix(y_test2, y_pred_binary2)
#
# print("Confusion Matrix:")
# print(conf_matrix)


# Assuming df_1 is your DataFrame
x_coords = test_df2['index_x_coor']
y_coords = test_df2['index_y_coor']
targets = test_df2['pred']

# Initialize variables to track segment start indices
segment_start = 0

# Plot each segment separately
for i in range(1, len(targets)):
    if targets.iloc[i] == 0:
        # If target is 0, plot the current segment and move to the next one
        plt.plot(x_coords[segment_start:i], y_coords[segment_start:i], '-', color='black')
        segment_start = i + 1

# Plot the last segment (if any)
if segment_start < len(targets):
    plt.plot(x_coords[segment_start:], y_coords[segment_start:], '-', color='black')

# Turn off axes and ticks
plt.axis('off')
plt.xticks([])
plt.yticks([])

# Show the plot
plt.show()

