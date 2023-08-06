# ----------------------------------------------------------------------------
# Copyright (c) 2022, Franck Lejzerowicz.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

def post_processes(self):
    if self.name.startswith('map__spades') or self.name in [
        'count_reads', 'humann2', 'midas', 'cazy', 'prodigal',
        'count_reads_grep', 'diamond_custom', 'hmmer_custom'
    ]:
        out_merge_samples = merge_samples(soft, output_paths)
        self.outputs['%s_merge' % self.name] = out_merge_samples
    if self.name in ['cazy']:
        out_cazy = cazy_post_processing(soft, soft_prev, output_paths)
        output_paths['%s_data' % self.name] = out_cazy
        cazy_sequence_analysis(soft, soft_prev, output_paths)
    if self.name in ['midas']:
        out_postprocess_samples = postprocess(soft, output_paths)
    if self.name in ['spades']:
        outs = contigs_per_sample(soft, output_paths)
        output_paths['%s_per_sample' % self.name] = outs
        outs = longest_contigs_per_sample(soft, output_paths)
        output_paths['%s_longest' % self.name] = outs
        prep_quast(soft, output_paths)
    if self.name in [
            'metawrap_analysis_reassemble_bins', 'metawrap_ref', 'yamb']:
        rename_bins(soft, output_paths)
    if self.name in ['drep']:
        faindex_contig_to_bin_drep(soft, output_paths)
        outs = longest_contigs_per_drep_bin(soft, output_paths)
        output_paths['%s_longest' % self.name] = outs
        outs = contigs_per_drep_bin(soft, output_paths)
        output_paths['%s_bins_contigs' % self.name] = outs
        outs = genes_per_mag(soft, output_paths)
        output_paths['%s_genes_per_mag' % self.name] = outs
    if self.name in ['yamb']:
        outs = yamb_across(soft, output_paths)
        output_paths['%s_maps' % self.name] = outs
    if self.name in ['read_mapping']:
        collect_reads_per_contig(soft, soft_prev, output_paths)

    return all_sh, output_paths, mem_n_u, procs, cnd, pooling_groups, IOs

