###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams
from sciviso import *
from scircm import SciRCM
from sciutil import SciUtil, SciException
from matplotlib_venn import venn3
from scivae import Vis


class SciRCMException(SciException):
    def __init__(self, message=''):
        Exception.__init__(self, message)


"""

A class for making QC and other generic visualisation for the SIRCLE package.

QC Plots: 
    1) Correlation between input features
    2) Correlation between VAE nodes
    3) Correlation between features and VAE nodes
    4) Histograms to validate distribution
    
Visualisations:
    1) Scatter plots of the latent space
    2) 
"""
class RCMVis:

    def __init__(self, rcm: SciRCM, config: dict, df: pd.DataFrame, gene_id: str,
                 prot_padj: str, prot_logfc: str, prot_padj_cutoff: float, prot_logfc_cutoff: float,
                 meth_padj: str, meth_diff: str, meth_padj_cutoff: float, meth_diff_cutoff: float,
                 rna_padj: str, rna_logfc: str, rna_padj_cutoff: float, rna_logfc_cutoff: float,
                 sciutil=None, output_dir="."):
        self.u = SciUtil() if sciutil is None else sciutil
        self.colours = ['#483873', '#1BD8A6', '#B117B7', '#AAC7E2', '#FFC107', '#016957', '#9785C0',
                        '#D09139', '#338A03', '#FF69A1', '#5930B1', '#FFE884', '#35B567', '#1E88E5',
                        '#ACAD60', '#A2FFB4', '#B618F5', '#854A9C']
        self.colour_map = {'MDE': '#6aaf44', 'MDE_TMDS': '#0e8e6d', 'MDE_ncRNA': '#9edb77', 'MDS': '#d8419b',
                           'MDS_TMDE': '#e585c0', 'MDS_ncRNA': '#d880b4', 'TPDE': '#e68e25', 'TPDE_TMDS': '#844c0f',
                           'TPDS': '#462d76', 'TPDS_TMDE': '#9b29b7', 'TMDE': '#fe2323', 'TMDS': '#2952ff'}
        self.prot_c = '#0101d7'
        self.rna_c = '#e68e25'
        self.meth_c = '#6aaf44'
        self.meth_diff = meth_diff
        self.prot_logfc = prot_logfc
        self.rna_logfc = rna_logfc
        self.rna_padj = rna_padj
        self.meth_padj = meth_padj
        self.prot_padj = prot_padj
        self.gene_id = gene_id
        self.meth_cmap = 'PiYG_r'
        self.rna_cmap = 'PuOr_r'
        self.prot_cmap = 'seismic'
        self.rna_padj_cutoff, self.meth_padj_cutoff, self.prot_padj_cutoff = rna_padj_cutoff, meth_padj_cutoff, prot_padj_cutoff
        self.rna_logfc_cutoff, self.meth_diff_cutoff, self.prot_logfc_cutoff = rna_logfc_cutoff, meth_diff_cutoff, prot_logfc_cutoff
        self.output_dir = output_dir
        self.vis = Vis(rcm.vae, rcm.u, None)
        self.base_config = {
            'label_font_size': 10,
            'axis_font_size': 9,
            'text_font_weight': 700,
            'figsize': (2, 2)
        }

    def plot_venn(self, df, output_dir="", title="RNA Protein & DNA Meth overlap", fig_type='svg', show_plt=False,
                  save_fig=True):
        """ Plotting (perhaps modularise) """
        sns.set_style('white')
        font = {'family': 'normal', 'size': 9}
        matplotlib.rc('font', **font)
        rcParams['figure.figsize'] = (2, 2)
        prot_genes = df[self.gene_id].values[np.where(df[self.prot_padj].values < self.prot_padj_cutoff)[0]]
        meth_genes = df[self.gene_id].values[np.where(df[self.meth_padj].values < self.meth_padj_cutoff)[0]]
        rna_genes = df[self.gene_id].values[np.where(df[self.rna_padj].values < self.rna_padj_cutoff)[0]]

        venn3([set(prot_genes), set(rna_genes), set(meth_genes)], set_labels=['Proteomics', 'RNAseq',
                                                                              'DNA Methylation'],
              set_colors=(self.prot_c, self.rna_c, self.meth_c),)
        plt.title(title)
        if save_fig:
            plt.savefig(os.path.join(output_dir, f'Venn3{title.replace(" ", "")}.{fig_type}'))
        if show_plt:
            plt.show()

    def __merge_config(self, default_config, user_config):
        """ Merge two style configurations together. """
        # Add in default params from our base
        for c in self.base_config:
            if not default_config.get(c):
                default_config[c] = self.base_config[c]
        if user_config:
            for c in default_config:
                # Update any of the config if the user has supplied it
                user_config[c] = user_config.get(c) if user_config.get(c) else default_config.get(c)
            return user_config
        return default_config

    @staticmethod
    def get_min_max_center(df, colname):
        vmin = abs(np.min(df[colname].values))
        vmax = np.max(df[colname].values)
        vmin = -1*vmin if vmin > vmax else -1 * vmax
        vmax = vmax if vmax > abs(vmin) else abs(vmin)
        return vmin, vmax

    def plt_values(self, df: pd.DataFrame, genes: list, gene_labels: list, vae_data, gene_id=None,
                   show_plt=False, save_fig=True, fig_type='svg', user_config=None, angle_plot=90):
        color_map = []
        for c in gene_labels:
            color_map.append(self.colour_map.get(c))
        gene_id = gene_id if gene_id else self.gene_id
        config = self.__merge_config({'figsize': (3.5, 3.5), 's': 80}, user_config)

        self.vis.plot_values_on_scatters(df, gene_id, gene_labels, genes, vae_data=vae_data, color_map=color_map,
                                         show_plt=show_plt, save_fig=save_fig, fig_type=fig_type,
                                         user_config=config, output_dir=self.output_dir, angle_plot=angle_plot)

    def plot_feature_scatters(self, df, vae_data, gene_id=None, show_plt=False, save_fig=True, fig_type='svg',
                              angle_plot=90, user_meth_config=None, user_rna_config=None, user_prot_config=None):
        # Plot each of the feature scatters separately (this allows us to change the colour map)
        # get min and max so that it is centered around 0
        gene_id = gene_id if gene_id else self.gene_id
        vmin, vmax = self.get_min_max_center(df, self.meth_diff)
        config = self.__merge_config({'cmap': self.meth_cmap, 'vmin': vmin, 'vmax': vmax, 's': 80}, user_meth_config)
        self.vis.plot_feature_scatters(df, gene_id, vae_data, columns=[self.meth_diff], show_plt=show_plt,
                                       fig_type=fig_type, save_fig=save_fig, angle_plot=angle_plot,
                                       user_config=config, output_dir=self.output_dir)

        vmin, vmax = self.get_min_max_center(df, self.rna_logfc)
        config = self.__merge_config({'cmap': self.rna_cmap, 'vmin': vmin, 'vmax': vmax, 's': 80}, user_rna_config)
        self.vis.plot_feature_scatters(df, gene_id, vae_data, columns=[self.rna_logfc], show_plt=show_plt,
                                       fig_type=fig_type, save_fig=save_fig, angle_plot=angle_plot,
                                       user_config=config, output_dir=self.output_dir)

        vmin, vmax = self.get_min_max_center(df, self.prot_logfc)
        config = self.__merge_config({'cmap': self.prot_cmap, 'vmin': vmin, 'vmax': vmax, 's': 80}, user_prot_config)
        self.vis.plot_feature_scatters(df, gene_id, vae_data, columns=[self.prot_logfc], show_plt=show_plt,
                                       fig_type=fig_type, save_fig=save_fig,  angle_plot=angle_plot,
                                       user_config=config, output_dir=self.output_dir)

    def plt_hists(self, df: pd.DataFrame, columns=None, show_plt=False, save_fig=True,
                  fig_type='svg', user_config=None):
        config = self.__merge_config({}, user_config)
        self.vis.plot_node_hists(show_plt=show_plt, save_fig=save_fig, fig_type=fig_type, user_config=config,
                                 output_dir=self.output_dir)
        config = self.__merge_config({'figsize': (2, 2)}, user_config)
        self.vis.plot_input_distribution(df, columns=columns, show_plt=show_plt, save_fig=save_fig, user_config=config,
                                         output_dir=self.output_dir)

    def plt_venn(self, df: pd.DataFrame, show_plt=False, save_fig=True):
        self.plot_venn(df, show_plt=show_plt, save_fig=save_fig)

    def plt_node_feature_correlation(self, df: pd.DataFrame, cols: list, vae_data, gene_id=None, show_plt=False,
                                     save_fig=True, fig_type='svg', user_config=None):
        config = self.__merge_config({'figsize': (2.5, 2.5)}, user_config)
        self.vis.plot_node_feature_correlation(df, gene_id, vae_data=vae_data, columns=cols, show_plt=show_plt, save_fig=save_fig,
                                               fig_type=fig_type, output_dir=self.output_dir, print_vals=True,
                                               encoding_type="z",  title="RCM heatmap corr.", user_config=config)

    def plt_node_correlation(self, show_plt=False, save_fig=True,
                              fig_type='svg', user_config=None):
        config = self.__merge_config({'figsize': (2.5, 2.5)}, user_config)
        self.vis.plot_node_correlation(show_plt=show_plt, save_fig=save_fig, user_config=config, fig_type=fig_type,
                                       output_dir=self.output_dir)

    def plt_feature_correlation(self, df: pd.DataFrame, cols: list, gene_id=None, show_plt=False, save_fig=True,
                 fig_type='svg', user_config=None):
        config = self.__merge_config({'figsize': (2.5, 2.5)}, user_config)
        self.vis.plot_feature_correlation(df, gene_id, columns=cols, show_plt=show_plt, save_fig=save_fig, fig_type=fig_type,
                                          user_config=config, output_dir=self.output_dir)

    def plot_values_by_rank(self, vis_df_filename, cols, gene_id, rcm_col, num_values=10,
                            show_plt=False, title='', meth_min=None, meth_max=None, rna_min=None,
                            rna_max=4, prot_min=-2, prot_max=2, output_dir=""):
        rcm_grps = ["MDS", "TPDE_TMDS", "TPDE", "TMDE", "TPDS_TMDE", "TPDS", "TMDS", "MDE", "MDE_TMDS",
                    "MDE-ncRNA", "MDS-ncRNA"]
        vis_df = pd.read_csv(vis_df_filename)

        for rcm_grp in rcm_grps:
            print(rcm_grp)
            sns.set_style("ticks")
            rcm_df = vis_df[vis_df[rcm_col] == rcm_grp]
            if len(rcm_df) > 0:
                for r_i, r_c in enumerate(cols):
                    # First add the bottom ones
                    params = {'legend.fontsize': 6,
                              'legend.handlelength': 2}
                    plt.rcParams.update(params)
                    fig, axes = plt.subplots(ncols=3, figsize=(4, 3))
                    rcm_df_sorted = rcm_df.sort_values(by=[r_c])
                    rcm_df_largest = rcm_df_sorted.nlargest(num_values, r_c)
                    rcm_df_tails = rcm_df_largest.append(rcm_df_sorted.nsmallest(num_values, r_c))  # Add the smallest and the largest
                    ax1, ax2, ax3 = axes
                    m_df = pd.DataFrame()
                    m_df['Gene'] = rcm_df_tails[gene_id].values
                    m_df['M. diff'] = rcm_df_tails[self.meth_diff].values
                    m_df['RNA logFC'] = rcm_df_tails[self.rna_logfc].values
                    m_df['Prot logFC'] = rcm_df_tails[self.prot_logfc].values

                    hm = Heatmap(m_df, ['M. diff'], 'Gene', cluster_cols=False, cluster_rows=False,
                                 cmap=self.meth_cmap, linewidths=0, label_font_size=9, title_font_size=10,
                                 vmin=meth_min, vmax=meth_max)
                    ax1 = hm.plot_hm(ax1)
                    ax1.set_xticklabels([])
                    ax1.title.set_text('M. diff')
                    ax1.tick_params(axis=u'x', which=u'both', length=0)
                    ax1.hlines([len(rcm_df_largest)], *ax1.get_xlim(), color="black", linewidth=3, linestyles="dotted")

                    hm = Heatmap(m_df, ['RNA logFC'], 'Gene',  cluster_cols=False, cluster_rows=False,
                                 cmap=self.rna_cmap, linewidths=0 , label_font_size=9, title_font_size=10,
                                 vmin=rna_min, vmax=rna_max)
                    ax2 = hm.plot_hm(ax2)
                    ax2.title.set_text('RNA logFC')
                    ax2.set_yticklabels([])
                    ax2.set_xticklabels([])
                    ax2.tick_params(axis=u'both', which=u'both', length=0)
                    ax2.hlines([len(rcm_df_largest)], *ax2.get_xlim(), color="black", linewidth=3, linestyles="dotted")

                    hm = Heatmap(m_df, ['Prot logFC'], 'Gene',  cluster_cols=False, cluster_rows=False,
                                 cmap=self.prot_cmap, linewidths=0, vmin=prot_min, vmax=prot_max)
                    ax3 = hm.plot_hm(ax3)
                    ax3.title.set_text('Prot. logFC')
                    ax3.set_yticklabels([])
                    ax3.set_xticklabels([])
                    ax3.tick_params(axis=u'both', which=u'both', length=0)
                    ax3.hlines([len(rcm_df_largest)], *ax3.get_xlim(), color="black", linewidth=3, linestyles="dotted")

                    plt.savefig(f'{output_dir}{title.replace(" ", "_")}_{rcm_grp}_{r_c}.svg')
                    plt.legend(fontsize='small', title_fontsize='6')

                    if show_plt:
                        plt.show()

            else:
                self.u.dp(["No values in grp: ", rcm_grp])

        # Make one based on all
        rcm_df = vis_df
        for r_i, r_c in enumerate(cols):
            # First add the bottom ones
            params = {'legend.fontsize': 6,
                      'legend.handlelength': 2}
            plt.rcParams.update(params)
            fig, axes = plt.subplots(ncols=3, figsize=(4, 3))
            rcm_df_sorted = rcm_df.sort_values(by=[r_c])
            rcm_df_largest = rcm_df_sorted.nlargest(num_values, r_c)
            rcm_df_tails = rcm_df_largest.append(
                rcm_df_sorted.nsmallest(num_values, r_c))  # Add the smallest and the largest
            ax1, ax2, ax3 = axes
            m_df = pd.DataFrame()
            m_df['Gene'] = rcm_df_tails[gene_id].values
            m_df['M. diff'] = rcm_df_tails[self.meth_diff].values
            m_df['RNA logFC'] = rcm_df_tails[self.rna_logfc].values
            m_df['Prot logFC'] = rcm_df_tails[self.prot_logfc].values

            hm = Heatmap(m_df, ['M. diff'], 'Gene', cluster_cols=False, cluster_rows=False,
                         cmap=self.meth_cmap, linewidths=0, label_font_size=9, title_font_size=10,
                         vmin=meth_min, vmax=meth_max)
            ax1 = hm.plot_hm(ax1)
            ax1.set_xticklabels([])
            ax1.title.set_text('M. diff')
            ax1.tick_params(axis=u'x', which=u'both', length=0)
            ax1.hlines([len(rcm_df_largest)], *ax1.get_xlim(), color="black", linewidth=3, linestyles="dotted")

            hm = Heatmap(m_df, ['RNA logFC'], 'Gene', cluster_cols=False, cluster_rows=False,
                         cmap=self.rna_cmap, linewidths=0, label_font_size=9, title_font_size=10,
                         vmin=rna_min, vmax=rna_max)
            ax2 = hm.plot_hm(ax2)
            ax2.title.set_text('RNA logFC')
            ax2.set_yticklabels([])
            ax2.set_xticklabels([])
            ax2.tick_params(axis=u'both', which=u'both', length=0)
            ax2.hlines([len(rcm_df_largest)], *ax2.get_xlim(), color="black", linewidth=3, linestyles="dotted")

            hm = Heatmap(m_df, ['Prot logFC'], 'Gene', cluster_cols=False, cluster_rows=False,
                         cmap=self.prot_cmap, linewidths=0, vmin=prot_min, vmax=prot_max)
            ax3 = hm.plot_hm(ax3)
            ax3.title.set_text('Prot. logFC')
            ax3.set_yticklabels([])
            ax3.set_xticklabels([])
            ax3.tick_params(axis=u'both', which=u'both', length=0)
            ax3.hlines([len(rcm_df_largest)], *ax3.get_xlim(), color="black", linewidth=3, linestyles="dotted")

            plt.savefig(f'{output_dir}{title.replace(" ", "_")}_ALL_{r_c}.svg')
            plt.legend(fontsize='small', title_fontsize='6')

            if show_plt:
                plt.show()