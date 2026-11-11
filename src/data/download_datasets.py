from __future__ import annotations

import argparse
from pathlib import Path

from torch_geometric.datasets import MoleculeNet

AVAILABLE_DATASETS = ("BBBP", "Tox21", "ESOL")


def download_dataset(name: str, data_root: Path) -> None:
    # Download a MoleculeNet dataset and print a compact integrity summary.
    if name not in AVAILABLE_DATASETS:
        raise ValueError(f"Unsupported dataset: {name}. Choose from {AVAILABLE_DATASETS}.")

    dataset = MoleculeNet(root=str(data_root / name), name=name)

    print(f"\\n{name}")
    print(f"  Molecules/graphs: {len(dataset)}")
    print(f"  Node feature size: {dataset.num_node_features}")
    print(f"  Edge feature size: {dataset.num_edge_features}")
    print(f"  Number of tasks: {dataset.num_tasks}")

    if len(dataset) > 0:
        sample = dataset[0]
        print(f"  First graph nodes: {sample.num_nodes}")
        print(f"  First graph edges: {sample.num_edges}")
        print(f"  First target shape: {tuple(sample.y.shape)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and inspect MoleculeNet datasets.")
    parser.add_argument(
        "--datasets", nargs="+", choices=AVAILABLE_DATASETS,
        default=list(AVAILABLE_DATASETS),
    )
    parser.add_argument("--data-dir", type=Path, default=Path("data/raw"))
    args = parser.parse_args()

    args.data_dir.mkdir(parents=True, exist_ok=True)
    for dataset_name in args.datasets:
        download_dataset(dataset_name, args.data_dir)


if __name__ == "__main__":
    main()
