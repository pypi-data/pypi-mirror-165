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

import argparse
import os
import sys

from sciutil import SciUtil

from scie2g import __version__
from scie2g import Bed, Csv


def print_help():
    lines = ['-h Print help information.']
    print('\n'.join(lines))


def run(args):
    if args.t == 'd':
        if not args.value:
            u = SciUtil()
            u.warn_p(['WARNING: You did not pass a column name for the value! Please use --value for the column '
                      'you would like to use as your value in your output file.\n Returning ...'])
            return
        c = Csv(args.l2g, chr_str=args.chr, start=args.start, end=args.end, value=args.value, header_extra=args.hdr,
                overlap_method=args.m, buffer_after_tss=args.downflank,
                buffer_before_tss=args.upflank, buffer_gene_overlap=args.overlap,
                gene_start=args.gstart, gene_end=args.gend, gene_chr=args.gchr,
                gene_direction=args.gdir, gene_name=args.gname
                )
        c.set_annotation_from_file(args.a)
        c.assign_locations_to_genes()  # Now we can run the assign values
        c.save_loc_to_csv(args.o)
        if args.b:
            c.convert_to_bed(c.loc_df, args.b, args.b)
    elif args.t == 'b':
        bed = Bed(args.l2g, overlap_method=args.m, buffer_after_tss=args.downflank,
                  buffer_before_tss=args.upflank, buffer_gene_overlap=args.overlap,
                  gene_start=args.gstart, gene_end=args.gend, gene_chr=args.gchr,
                  gene_direction=args.gdir, gene_name=args.gname, chr_idx=args.chridx, start_idx=args.startidx,
                  end_idx=args.endidx, peak_value=args.valueidx, header_extra=args.hdridx
                  )
        # Add the gene annot
        bed.set_annotation_from_file(args.a)
        # Now we can run the assign values
        bed.assign_locations_to_genes()
        bed.save_loc_to_csv(args.o)


def gen_parser():
    parser = argparse.ArgumentParser(description='scie2g')
    parser.add_argument('--a', type=str, help='Annotation with the gene locations')
    parser.add_argument('--o', type=str, default='l2g_outputfile.csv', help='Output file (csv)')
    parser.add_argument('--b', type=str, default='l2g_outputfile.bed', help='Output file (bed)')
    parser.add_argument('--l2g', type=str, help='Input file to run scie2g on')
    parser.add_argument('--t', type=str, default='b', help='The input file type: d=CSV, b=Bed')
    parser.add_argument('--upflank', type=int, default=2500, help='Maximum distance upstream from TSS'
                                                                  ' (default = 2500) for overlaps and in_promoter')
    parser.add_argument('--downflank', type=int, default=500, help='Maximum distance downstream from gene end '
                                                                   '(default = 500) only used in overlaps')
    parser.add_argument('--overlap', type=int, default=500, help='Overlap with gene body (default = 500) used in'
                                                                 ' in_promoter')
    parser.add_argument('--m', type=str, default='in_promoter', help='Overlap method'
                                                                     ' (overlaps or in_promoter <- default).')

    parser.add_argument('--chr', type=str, default="chr", help='CSV only: name of your chromosone column')
    parser.add_argument('--start', type=str, default="start", help='CSV only: name of your start column')
    parser.add_argument('--end', type=str, default="end", help='CSV only: name of your end column')
    parser.add_argument('--value', type=str, default=None, help='CSV only: name of your value column')
    parser.add_argument('--hdr', type=str, default="", help='CSV only: comma separated list of other columns you '
                                                            'want to include in the output e.g "stat,pvalue"')

    parser.add_argument('--chridx', type=int, default=0, help='BED only: index of your chromosone column')
    parser.add_argument('--startidx', type=int, default=1, help='BED only: index of your start column')
    parser.add_argument('--endidx', type=int, default=2, help='BED only: index of your end column')
    parser.add_argument('--valueidx', type=int, default=7, help='BED only: index of your value column')
    parser.add_argument('--hdridx', type=str, default="0,1,2,3,6,8", help='BED only: comma separated list of indexs')
    parser.add_argument('--hdrlbl', type=str, default='"chr","start","end","peak_name","signal","qvalue"',
                        help='BED only: comma separated list of header in human readable format as output '
                             'to your csv file.')

    parser.add_argument('--gchr', type=int, default=2, help='Position in annotation file that your chr annotation is.')
    parser.add_argument('--gstart', type=int, default=3, help='Position in annotation file that your start is.')
    parser.add_argument('--gend', type=int, default=4, help='Position in annotation file that your end is.')
    parser.add_argument('--gdir', type=int, default=5, help='Position in annotation file that your gene direction is.')
    parser.add_argument('--gname', type=int, default=0, help='Position in annotation file that gene name is.')

    return parser


def main(args=None):
    parser = gen_parser()
    u = SciUtil()
    if args:
        sys.argv = args
    if len(sys.argv) == 1:
        print_help()
        sys.exit(0)
    elif sys.argv[1] in {'-v', '--v', '-version', '--version'}:
        print(f'scie2g v{__version__}')
        sys.exit(0)
    else:
        print(f'scie2g v{__version__}')
        args = parser.parse_args(args)
        # Validate the input arguments.
        if not os.path.isfile(args.a):
            u.err_p([f'The annotation file could not be located, file passed: {args.a}'])
            sys.exit(1)
        if not os.path.isfile(args.l2g):
            u.err_p([f'The input file could not be located, file passed: {args.l2g}'])
            sys.exit(1)
        if args.t != 'b' and args.t != 'd':
            u.err_p([f'The file type passed is not supported: {args.t}, '
                     f'filetype must be "b" for bed or "d" for dmrseq.'])
            sys.exit(1)
        # Otherwise we have need successful so we can run the program
        u.dp(['Running scie2g on input file: ', args.l2g,
              '\nWith annotation file: ', args.a,
              '\nSaving to output file: ', args.o,
              '\nOverlap method:', args.m,
              '\nUpstream flank: ', args.upflank,
              '\nDownstream flank:', args.downflank,
              '\nGene overlap: ', args.overlap])
        u.warn_p(['Assuming your annotation file and your input file are SORTED!'])
        # RUN!
        run(args)
    # Done - no errors.
    sys.exit(0)


if __name__ == "__main__":
    main()
    # ----------- Example below -----------------------
    """
    root_dir = '../scie2g/'
    main(["--a", f'{root_dir}data/hsapiens_gene_ensembl-GRCh38.p13.csv',
          "--o", f'{root_dir}output_file.csv',
          "--l2g", f'{root_dir}tests/data/test_H3K27ac.bed',
          "--t", "b",
          "--upflank", "3000"])
          
    root_dir = '../'
    main(["--a", f'{root_dir}data/hsapiens_gene_ensembl-GRCh38.p13.csv', # mmusculus_gene_ensembl-GRCm38.p6.csv', #
      "--o", f'{root_dir}output_file_2.csv',
      "--l2g", f'{root_dir}tests/data/test_dmrseq.csv',
      "--t", "d",
      "--upflank", "20", "--chr", "seqnames", "--value", "stat"])
    """



    def plot_values_by_rank(self, vis_df_filename, cols, gene_id, rcm_col="RegulatoryLabels", num_values=10,
                                show_plt=False, cluster_rows=False, cluster_cols=False, title='', num_nodes=3,
                            meth_min=-100, meth_max=100, rna_min=-4, rna_max=4, prot_min=-2, prot_max=2, output_dir=""):
        rcm_grps = ["MDS", "TPDE_TMDS", "TPDE", "TMDE", "TPDS_TMDE", "TPDS", "TMDS", "MDE", "MDE_TMDS",
                    "MDE-ncRNA", "MDS-ncRNA"]
        vae_cols = [f'VAE{i}' for i in range(0, num_nodes)]
        vis_df = pd.read_csv(vis_df_filename)
        print(vis_df.head())
        meth_min = np.min(vis_df[self.meth_diff])
        meth_max = np.max(vis_df[self.meth_diff])
        rna_min = np.min(vis_df[self.rna_logfc])
        rna_max = np.max(vis_df[self.rna_logfc])
        prot_min = np.min(vis_df[self.prot_logfc])
        prot_max = np.max(vis_df[self.prot_logfc])
        # Keep things symmetrical
        if abs(prot_min) > prot_max:
            prot_max = abs(prot_min)
        else:
            prot_min = -1 * prot_max
        if abs(rna_min) > rna_max:
            rna_max = abs(rna_min)
        else:
            rna_min = -1 * rna_max
        if abs(meth_min) > meth_max:
            meth_max = abs(meth_min)
        else:
            meth_min = -1 * meth_max
        for rcm_grp in rcm_grps:
            print(rcm_grp)
            sns.set_style("ticks")
            rcm_df = vis_df[vis_df[rcm_col] == rcm_grp]
            if len(rcm_df) > 0:
                for r_i, r_c in enumerate(cols):
                    # First add the bottom ones
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
                                 cmap=self.meth_cmap, linewidths=0) #, vmin=meth_min, vmax=meth_max)
                    ax1 = hm.plot_hm(ax1)
                    ax1.set_xticklabels([])
                    ax1.title.set_text('M. diff')
                    ax1.tick_params(axis=u'x', which=u'both', length=0)
                    ax1.hlines([len(rcm_df_largest)], *ax1.get_xlim(), color="black", linewidth=3, linestyles="dotted")

                    hm = Heatmap(m_df, ['RNA logFC'], 'Gene',  cluster_cols=False, cluster_rows=False,
                                 cmap=self.rna_cmap, linewidths=0)
                    ax2 = hm.plot_hm(ax2)
                    ax2.title.set_text('RNA logFC')
                    ax2.set_yticklabels([])
                    ax2.set_xticklabels([])
                    ax2.tick_params(axis=u'both', which=u'both', length=0)
                    ax2.hlines([len(rcm_df_largest)], *ax2.get_xlim(), color="black", linewidth=3, linestyles="dotted")

                    hm = Heatmap(m_df, ['Prot logFC'], 'Gene',  cluster_cols=False, cluster_rows=False,
                                 cmap=self.prot_cmap, linewidths=0)
                    ax3 = hm.plot_hm(ax3)
                    ax3.title.set_text('Prot. logFC')
                    ax3.set_yticklabels([])
                    ax3.set_xticklabels([])
                    ax3.tick_params(axis=u'both', which=u'both', length=0)
                    ax3.hlines([len(rcm_df_largest)], *ax3.get_xlim(), color="black", linewidth=3, linestyles="dotted")

                    plt.savefig(f'{output_dir}{title.replace(" ", "_")}_{rcm_grp}_{r_c}.pdf')
                    plt.legend(fontsize='small', title_fontsize='6')

                    if show_plt:
                        plt.show()
                    #fig.colorbar(im1, ax=ax1, shrink=0.3, aspect=3, orientation='horizontal')

            else:
                self.u.dp(["No values in grp: ", rcm_grp])