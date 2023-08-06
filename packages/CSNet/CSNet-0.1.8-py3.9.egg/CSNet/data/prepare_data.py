import scanpy as sc
import numpy as np
import os
import gc
import yaml
from sklearn.model_selection import train_test_split


def preprocess(adata: sc.AnnData, min_genes: int = 200, min_cells: int = 50, thresh_count: int = 2500, thresh_mt: int = 5, batch_key: str = None, n_top_genes: int = 2000):
    adata.var_names_make_unique()
    sc.pp.filter_cells(adata, min_genes=min_genes)
    sc.pp.filter_genes(adata, min_cells=min_cells)
    adata.var['mt'] = adata.var_names.str.startswith('mt-')
    if adata.var['mt'].sum() == 0:
        adata.var['mt'] = adata.var_names.str.startswith('MT-')
    sc.pp.calculate_qc_metrics(
        adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    if thresh_count != None:
        adata = adata[adata.obs.n_genes_by_counts < thresh_count, :]
    if thresh_mt != None:
        adata = adata[adata.obs.pct_counts_mt < thresh_mt, :]
    adata.layers["counts"] = adata.X.copy()
    sc.pp.normalize_total(adata, target_sum=1e4)
    sc.pp.log1p(adata)
    # adata.raw = adata
    sc.pp.highly_variable_genes(
        adata,
        n_top_genes=n_top_genes,
        # subset=True,
        layer="counts",
        flavor="seurat_v3",
        batch_key=batch_key
    )
    # adata = adata[:, adata.var.highly_variable]

    return adata


def train_test_generate(adata: sc.AnnData, output_dir: str, train_size: float = 0.8, val_size: float = None):
    if val_size is None:
        val_size = 1 - train_size        
    train_index, test_index = train_test_split(
        range(len(adata)), train_size=train_size)
    train_index, val_index = train_test_split(train_index, test_size=val_size)
    try:
        os.makedirs(output_dir)
    except:
        pass
    adata[train_index].write(os.path.join(output_dir, 'train.h5ad'))
    adata[val_index].write(os.path.join(output_dir, 'val.h5ad'))
    adata[test_index].write(os.path.join(output_dir, 'test.h5ad'))


def generate_yaml(output_dir: str):
    orgin = os.path.join(os.path.dirname(__file__), 'config.yaml')
    destination = os.path.join(output_dir, 'step1.yaml')
    os.system('cp {} {}'.format(orgin, destination))


if __name__ == '__main__':
    # python -m CSNet.data.prepare_data
    adata_path = '/data/xizhu/shen/ST/CSNet/data/smaf/adata.h5ad'
    DIR = '/data/xizhu/shen/ST/CSNet/data/CSNet'
    adata = sc.read_h5ad(adata_path)
    adata = preprocess(adata, min_cells=1, min_genes=10)
    train_test_generate(adata, DIR, 0.8)
    generate_yaml(DIR)
