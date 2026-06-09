"""Contract display helpers independent from Pyxel drawing."""

from mendels_greenhouse.core.contracts import PhenotypeContract


def contract_progress_width(contract: PhenotypeContract, width: int) -> int:
    """Return filled progress-bar width for a contract."""
    if contract.target_count <= 0:
        return 0
    progress = min(contract.progress_count / contract.target_count, 1)
    return int(width * progress)


def contract_progress_label(contract: PhenotypeContract) -> str:
    """Return compact progress text."""
    return f"{contract.progress_count}/{contract.target_count}"
