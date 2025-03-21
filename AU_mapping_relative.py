import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
class AU_mapping():
    def prob_au(self, df, columns, labels, threshold=0.1):
        # Create a dictionary of dictionaries: {AU: {label: ratio, ...}, ...}
        ratios = {}
        total_samples = df.shape[0]
        # Overall activation rate for each AU
        P_c = {c: df[df[c] >= threshold].shape[0] / total_samples for c in columns}
        
        for c in columns:
            ratios[c] = {}
            for label in labels:
                d = df[df["Label_y"] == label].shape[0]
                if d == 0:
                    ratios[c][label] = np.nan
                    continue
                activated_count = df.loc[(df[c] >= threshold) & (df["Label_y"] == label)].shape[0]
                P_c_li = activated_count / d  # Conditional probability P(c|l)
                if P_c[c] > 0:
                    ratios[c][label] = P_c_li / P_c[c]
                else:
                    ratios[c][label] = np.nan
        return ratios

    def au_heatmap(self, df):
        df_au = df.loc[:, "AU01_r":"AU45_r"]
        columns = df_au.columns
        df_y = df["Label_y"]
        df_au = pd.concat([df_au, df_y], axis=1)
        
        # Define your engagement labels (adjust these if your df uses different values)
        labels = [0, 1, 2]
        
        # Calculate the ratio for each AU and each label
        ratios = self.prob_au(df_au, columns, labels, threshold=0.1)
        # Create a DataFrame from the ratios dictionary
        df_ratio = pd.DataFrame(ratios).T
        df_ratio.columns = ["Disengaged", "Partially engaged", "Engaged"]
        # Optionally, sort the rows by one of the label columns
        # df_ratio = df_ratio.sort_values(by=labels[0], ascending=False)
        
        # Plot the heatmap with multiple columns (one per label)
        fig = plt.figure(figsize=(12, 8))
        ax=sns.heatmap(df_ratio, cmap='magma_r', linewidths=0.7, annot=True,vmin=0.5,vmax=2.7, annot_kws={"size": 16})
        # plt.title("AU Activation Ratio per Label\n(Ratio = P(AU|Label)/P(AU))")
        
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)

        # Increase font size for color bar ticks and label
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(labelsize=18)
        plt.show()
        
        return fig, df_ratio
