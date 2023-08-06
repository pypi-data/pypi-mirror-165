"""
Module to find biomarkers.
"""
from .assay import Assay
from .utils import logger, tqdmbar
from numba import jit
import numpy as np
import pandas as pd
from scipy.stats import linregress
from typing import Optional
from joblib import Parallel, delayed
from scipy.stats import rankdata

__all__ = [
    "find_markers_by_rank",
    "find_markers_by_regression",
    "knn_clustering",
]


def read_prenormed_batches(store, cell_idx: np.ndarray, batch_size: int, desc: str):
    batch = {}
    for i in tqdmbar(store.keys(), desc=desc):
        batch[int(i)] = store[i][:][cell_idx]
        if len(batch) == batch_size:
            yield pd.DataFrame(batch)
            batch = {}
    if len(batch) > 0:
        yield pd.DataFrame(batch)


def find_markers_by_rank(
    assay: Assay,
    group_key: str,
    cell_key: str,
    threshold: float,
    batch_size: int,
    use_prenormed: bool,
    prenormed_store: Optional[str],
    n_threads: int,
    **norm_params,
) -> dict:
    """
    Identify marker genes for given groups

    Args:
        assay:
        group_key:
        cell_key:
        threshold:
        batch_size:
        use_prenormed:
        prenormed_store:
        n_threads:

    Returns:

    """

    @jit(nopython=True)
    def calc_mean_rank(v):
        """
        Calculates the mean rank of the data.
        """
        r = np.ones(n_groups)
        for x in range(n_groups):
            r[x] = v[int_indices == x].mean()
        return r / r.sum()

    def mean_rank_wrapper(v):
        """
        Wraps `calc_mean_rank` function.
        """
        return calc_mean_rank(v.values)

    def prenormed_mean_rank_wrapper(gene_idx):
        mr = calc_mean_rank(
            rankdata(prenormed_store[gene_idx][:][cell_idx], method="dense")
        )
        idx = mr > threshold
        if np.any(idx):
            return np.array([ii[idx], np.repeat(gene_idx, idx.sum()), mr[idx]])
        else:
            return None

    groups = assay.cells.fetch(group_key, cell_key)
    group_set = sorted(set(groups))
    n_groups = len(group_set)
    # Since, numba needs int arrays to work properly but the dtype of 'groups' may not be integer type
    # Hence we need to create a indexed version of 'groups'
    idx_map = dict(zip(group_set, range(n_groups)))
    rev_idx_map = {v: k for k, v in idx_map.items()}
    int_indices = np.array([idx_map[x] for x in groups])
    results = {x: [] for x in group_set}
    if use_prenormed:
        if prenormed_store is None:
            if "prenormed" in assay.z:
                prenormed_store = assay.z["prenormed"]
            else:
                use_prenormed = False

    if use_prenormed:
        ii = np.array(list(rev_idx_map.values()))
        cell_idx = assay.cells.active_index(cell_key)
        batch_iterator = tqdmbar(prenormed_store.keys(), desc="Finding markers")
        res = Parallel(n_jobs=n_threads)(
            delayed(prenormed_mean_rank_wrapper)(i) for i in batch_iterator
        )
        res = pd.DataFrame(np.hstack([x for x in res if x is not None])).T
        res[1] = res[1].astype(int)
        res[2] = res[2].astype(float)
        results = {}
        for i in group_set:
            results[i] = (
                res[res[0] == str(i)]
                .sort_values(by=2, ascending=False)[[1, 2]]
                .set_index(1)[2]
            )
        return results
    else:
        batch_iterator = assay.iter_normed_feature_wise(
            cell_key, "I", batch_size, "Finding markers", **norm_params
        )
        for val in batch_iterator:
            res = val.rank(method="dense").astype(int).apply(mean_rank_wrapper)
            # Removing genes that were below the threshold in all the groups
            res = res.T[(res < threshold).sum() != n_groups]
            for j in res:
                results[rev_idx_map[j]].append(res[j][res[j] > threshold])

        for i in results:
            results[i] = pd.concat(results[i]).sort_values(ascending=False)
        return results


def find_markers_by_regression(
    assay: Assay,
    cell_key: str,
    regressor: np.ndarray,
    min_cells: int,
    batch_size: int = 50,
    **norm_params,
) -> pd.DataFrame:
    """

    Args:
        assay:
        cell_key:
        regressor:
        min_cells:
        batch_size:

    Returns:

    """

    res = {}
    for df in assay.iter_normed_feature_wise(
        cell_key,
        "I",
        batch_size,
        "Finding correlated features",
        **norm_params,
    ):
        for i in df:
            v = df[i].values
            if (v > 0).sum() > min_cells:
                lin_obj = linregress(regressor, v)
                res[i] = (lin_obj.rvalue, lin_obj.pvalue)
            else:
                res[i] = (0, 1)
    res = pd.DataFrame(res, index=["r_value", "p_value"]).T
    return res


def knn_clustering(
    d_array, n_neighbours: int, n_clusters: int, n_threads: int, ann_params: dict = None
) -> np.ndarray:
    """

    Args:
        d_array:
        n_neighbours:
        n_clusters:
        n_threads:
        ann_params:

    Returns:

    """

    from .ann import instantiate_knn_index, fix_knn_query
    from .utils import controlled_compute, tqdmbar, show_dask_progress
    from scipy.sparse import csr_matrix

    def make_knn_mat(data, k, t):
        """

        Args:
            data:
            k:
            t:

        Returns:

        """

        for i in tqdmbar(data.blocks, desc="Fitting KNNs", total=data.numblocks[0]):
            i = controlled_compute(i, t)
            ann_idx.add_items(i)
        s, e = 0, 0
        indices = []
        for i in tqdmbar(
            data.blocks, desc="Identifying feature KNNs", total=data.numblocks[0]
        ):
            e += i.shape[0]
            i = controlled_compute(i, t)
            inds, d = ann_idx.knn_query(i, k=k + 1)
            inds, _, _ = fix_knn_query(inds, d, np.arange(s, e))
            indices.append(inds)
            s = e
        indices = np.vstack(indices)
        assert indices.shape[0] == data.shape[0]

        return csr_matrix(
            (
                np.ones(indices.shape[0] * indices.shape[1]),
                (
                    np.repeat(range(indices.shape[0]), indices.shape[1]),
                    indices.flatten(),
                ),
            ),
            shape=(indices.shape[0], indices.shape[0]),
        )

    def make_clusters(mat, nc):
        """

        Args:
            mat:
            nc:

        Returns:

        """
        import sknetwork as skn

        paris = skn.hierarchy.Paris(reorder=False)
        logger.info("Performing clustering, this might take a while...")
        dendrogram = paris.fit_transform(mat)
        return skn.hierarchy.cut_straight(dendrogram, n_clusters=nc)

    def fix_cluster_order(data, clusters, t):
        """

        Args:
            data:
            clusters:
            t:

        Returns:

        """

        idxmax = show_dask_progress(data.argmax(axis=1), "Sorting clusters", t)
        cmm = pd.DataFrame([idxmax, clusters]).T.groupby(1).median()[0].sort_values()
        return (
            pd.Series(clusters)
            .replace(dict(zip(cmm.index, range(1, 1 + len(cmm)))))
            .values
        )

    default_ann_params = {
        "space": "l2",
        "dim": d_array.shape[1],
        "max_elements": d_array.shape[0],
        "ef_construction": 80,
        "M": 50,
        "random_seed": 444,
        "ef": 80,
        "num_threads": 1,
    }
    if ann_params is None:
        ann_params = {}
    default_ann_params.update(ann_params)
    ann_idx = instantiate_knn_index(**default_ann_params)
    return fix_cluster_order(
        d_array,
        make_clusters(make_knn_mat(d_array, n_neighbours, n_threads), n_clusters),
        n_threads,
    )
