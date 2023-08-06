#!/usr/bin/env python3
from __future__ import annotations

import sys
import argparse
from collections import defaultdict

from typing import TextIO
from typing import Any, Optional, Union
from typing import (
    List, Sequence,
    Iterator, Iterable,
    Tuple,
    DefaultDict,
    Set,
    Literal,
)

from predectorutils.gff import (
    Strand,
    Phase,
    GFFRecord,
)


def cli(parser: argparse.ArgumentParser) -> None:

    parser.add_argument(
        "genes",
        type=argparse.FileType('r'),
        help="Gene GFF to use."
    )

    parser.add_argument(
        "annotations",
        type=argparse.FileType('r'),
        help="Annotation GFF to use (i.e. the GFF3 output of predector)"
    )

    parser.add_argument(
        "-o", "--outfile",
        type=str,
        default="stdout",
        help=(
            "Where to write the output to. If using the --split parameter "
            "this becomes the prefix. Default: stdout"
        )
    )

    parser.add_argument(
        "--split",
        type=str,
        choices=["source", "type"],
        default=None,
        help="Output distinct GFFs for each analysis or type of feature."
    )

    # parser.add_argument(
    #     "-c", "--concat",
    #     action="store_true",
    #     default=False,
    #     help=(
    #         "Output both the genes and annotations linked "
    #         "using the 'Derives_from' attribute."
    #     )
    # )

    parser.add_argument(
        "--no-filter-kex2",
        dest="filter_kex2",
        action="store_false",
        default=True,
        help=(
            "Output kex2 cutsites even if there is no signal peptide"
        )
    )

    parser.add_argument(
        "--id",
        dest="id_field",
        default="Parent",
        help=(
            "What GFF attribute field corresponds to your protein feature "
            "seqids? Default uses the Parent field. Because some fields "
            "(like Parent) can have multiple values, we'll raise an error "
            "if there is more than 1 unique value. Any CDSs missing the "
            "specified field (e.g. ID) will be skipped."
        )
    )

    return


def make_polypeptide(
    cds: GFFRecord,
    derives_from: bool = False
) -> GFFRecord:
    pep = cds.copy()
    pep.source = "Predector"
    pep.type = "polypeptide"
    pep.phase = Phase.NOT_CDS
    id_ = pep.attributes.id
    assert id_ is not None
    pep.attributes.id = "polypeptide-" + id_

    if derives_from:
        pep.attributes.derives_from = [cds.seqid]

    pep.attributes.alias = []
    pep.attributes.name = None
    pep.attributes.note = []
    pep.attributes.dbxref = []
    pep.attributes.custom = {}
    return pep


def cds_to_polypeptide(
    cdss: Iterable[GFFRecord],
    derives_from: bool = False
) -> List[GFFRecord]:
    peps = []
    for cds in cdss:
        pep = make_polypeptide(cds, derives_from=derives_from)
        peps.append(pep)

    return [pep]


def project_plus(
    cds: Sequence[GFFRecord],
    feature: GFFRecord
) -> Iterator[Tuple[int, int]]:
    """ Projects a feature in protein space to genome coordinates
    on the forward strand.

    Note that at this point the coordinates should already
    be multiplied by 3 and the correct seqid and strand should be set.
    """

    from copy import copy
    feature = copy(feature)

    cds = sorted(cds, key=lambda c: c.start)
    for c in cds:
        if (feature.start + c.start) > c.end:
            feature.start -= len(c)
            feature.end -= len(c)
        elif (feature.end + c.start) <= c.end:
            start = feature.start + c.start
            end = feature.end + c.start
            yield (start, end)
            break
        else:
            start = feature.start + c.start
            end = c.end
            yield (start, end)
            feature.start = 0
            feature.end -= len(c)
    return


def project_minus(
    cds: Sequence[GFFRecord],
    feature: GFFRecord
) -> Iterator[Tuple[int, int]]:
    """ Projects a feature in protein space to genome coordinates
    on the reverse strand.

    Note that at this point the coordinates should already
    be multiplied by 3 and the correct seqid and strand should be set.
    """

    from copy import copy
    feature = copy(feature)

    cds = sorted(cds, reverse=True, key=lambda c: c.start)
    for c in cds:
        if (c.end - feature.start) < c.start:
            feature.start -= len(c)
            feature.end -= len(c)
        elif (c.end - feature.end) >= c.start:
            start = c.end - feature.end
            end = c.end - feature.start
            yield (start, end)
            break
        else:
            start = c.start
            end = c.end - feature.start
            yield (start, end)
            feature.start = 0
            feature.end -= len(c)
    return


def preprocess_protein_feat(cdss, feature):
    """ Adds the new strand and seqid to the feature
    converts AA length to codon length. """

    from copy import copy
    strand = find_strand(cdss)
    seqid = find_seqid(cdss)

    feature = copy(feature)
    feature.seqid = seqid
    feature.strand = strand

    feature.start *= 3
    feature.end *= 3

    return feature


def find_source(cdss: Iterable[GFFRecord]) -> str:
    """ Checks that there is only one source in records. """
    sources = {c.source for c in cdss}
    if len(sources) > 1:
        raise ValueError(f"Got multiple strands {sources}")

    return sources.pop()


def find_strand(cdss: Iterable[GFFRecord]) -> Strand:
    """ Checks that there is only one strand in records. """
    strands = {c.strand for c in cdss}
    if len(strands) > 1:
        raise ValueError(f"Got multiple strands {strands}")

    return strands.pop()


def find_seqid(cdss: Iterable[GFFRecord]) -> str:
    """ Checks that there is only one seqid in records. """
    seqids = {c.seqid for c in cdss}
    if len(seqids) > 1:
        raise ValueError(f"Got multiple seqids {seqids}")

    return seqids.pop()


def split_feature_by_coords(
    coords: Iterable[Tuple[int, int]],
    feature: GFFRecord
) -> Iterator[GFFRecord]:
    """ Just copies a feature for each set of new coordinates. """

    from copy import copy

    cs = []
    fs = []
    an = False
    for (start, end) in coords:
        if start == end:
            continue
        elif start > end:
            an = True
        new_feature = copy(feature)
        new_feature.start = start
        new_feature.end = end
        fs.append(new_feature)
        cs.append((start, end))
        yield new_feature

    # Neither of the below should happen, but It bit me before.
    if an:
        raise ValueError(
            "Splitting the feature yielded a feature with a higher start than end.\n"
            f"Initial feature: {repr(feature)}\n"
            f"Resulting split features: {fs}"
        )
    elif len(fs) == 0:
        raise ValueError(
            "Splitting the feature resulted in no outputs.\n"
            f"Initial feature: {repr(feature)}\n"
            f"Initial coordinates features: {cs}"
        )

    return


def project_to_cds(
    cdss: Sequence[GFFRecord],
    feature: GFFRecord
) -> List[GFFRecord]:
    """ This takes multiple CDS features from which the protein
    is derived and projects a single predicted protein feature
    back onto those CDSs, matching the intron structure.
    """

    from copy import copy
    cdss = list(copy(cdss))

    assert len(cdss) >= 1, cdss
    assert all(cds.end >= cds.start for cds in cdss)
    feature = preprocess_protein_feat(cdss, feature)

    if feature.strand == Strand.PLUS:
        coords = list(project_plus(cdss, feature))
    elif feature.strand == Strand.MINUS:
        coords = list(project_minus(cdss, feature))
    else:
        raise ValueError(f"Got an unexpected strand {feature.strand}.")

    feature.attributes.gap = None
    feats = split_feature_by_coords(coords, feature)
    return list(feats)


def create_match(
    parts: Sequence[GFFRecord],
    type_: str,
    prot_id: str,
    index: Union[int, str]
):
    """ Creates a parent feature that encapsulates all
    members of 'parts'.

    Intended to create "match" features from many "match_part"s.
    """

    from copy import deepcopy
    start = min(p.start for p in parts)
    end = max(p.end for p in parts)

    seqid = find_seqid(parts)
    strand = find_strand(parts)
    score = parts[0].score

    source_ = {p.source for p in parts}
    assert len(source_) == 1
    source = source_.pop()
    del source_

    attributes = deepcopy(parts[0].attributes)
    attributes.id = prot_id + "-" + type_ + "-" + str(index)

    parent = GFFRecord(
        seqid=seqid,
        source=source,
        type=type_,
        start=start,
        end=end,
        score=score,
        strand=strand,
        phase=Phase.NOT_CDS,
        attributes=attributes
    )

    return parent


def split_protein_features(  # noqa: W0611
    prots: Sequence[GFFRecord],
    cdss: Sequence[GFFRecord],
    derives_from: bool = False,
    filter_kex2: bool = True,
    separate_peps: bool = False,
    regions: bool = False
):
    from copy import deepcopy
    prots = deepcopy(prots)

    if len(cdss) == 0:
        return None

    if len(prots) == 0:
        return None

    prot_id = prots[0].seqid

    # Kex2 functions during the conventional secretion pathway.
    # Things missing a signal peptide are unlikely to have real kex cutsites.
    if filter_kex2:
        has_sp = any(p.type == "signal_peptide" for p in prots)
        if not has_sp:
            prots = [p for p in prots if p.type != "propeptide_cleavage_site"]

    prots_tmp = []
    for prot in prots:
        if prot.type in (
            "n_terminal_region",
            "c_terminal_region",
            "central_hydrophobic_region_of_signal_peptide"
        ):
            continue
        prots_tmp.append(prot)
    prots = prots_tmp
    del prots_tmp

    out_parents = []
    out_features = []

    new_prots: DefaultDict[Any, List[GFFRecord]] = defaultdict(list)

    for prot in prots:
        excl_target = (prot.type, prot.source, prot.start, prot.end)
        big_boy = (prot.type, prot.source, prot.attributes.target,
                   prot.start, prot.end)
        if prot.type == "transmembrane_polypeptide_region":
            new_prots[excl_target].append(prot)
        elif prot.type == "polypeptide_motif":
            new_prots[excl_target].append(prot)
        elif prot.type == "propeptide_cleavage_site":
            new_prots[excl_target].append(prot)
        elif prot.type in (
            "signal_peptide",
            "n_terminal_region",
            "c_terminal_region",
            "central_hydrophobic_region_of_signal_peptide"
        ):
            new_prots[(prot.type, prot.source)].append(prot)
        elif prot.type in ("protein_hmm_match", "protein_match"):
            new_prots[big_boy].append(prot)
        else:
            new_prots[(prot.type, prot.source)].append(prot)

    index = 1
    peps = cds_to_polypeptide(cdss, derives_from=derives_from)
    if regions:
        region = peps[0]
        start = min(c.start for c in peps)
        end = max(c.end for c in peps)
        region.start = start
        region.end = end
        region.type = "region"
        peps = [region]

    for key, prots in new_prots.items():
        split_prot = []

        for prot in prots:
            split_prot.extend(project_to_cds(cdss, prot))

        type_ = key[0]
        source = find_source(prots)

        if type_ in ("protein_hmm_match", "protein_match"):
            if len(cdss) > 1:
                for s in split_prot:
                    s.type = "match_part"

                parents = [create_match(split_prot, type_, prot_id, index)]
                index += 1
            else:
                # parent_type = type_
                parents = []

        else:
            # parent_type = "polypeptide"
            if separate_peps:
                parents = deepcopy(peps)
                for p in parents:
                    p.attributes.id = f"{p.attributes.id}-{index}"
                    p.source = source
                index += 1

            else:
                parents = peps

            for parent in parents:
                parent.attributes.custom["kind"] = type_

        for parent in parents:
            parent.add_children(split_prot)

        for feat in split_prot:
            feat.update_parents()

        if regions and (len(parents) > 0):
            assert len(parents) == 1
            parents[0].expand_to_children()
            parents[0].shrink_to_children()

        out_parents.extend([p for p in parents if p not in out_parents])
        out_features.extend(split_prot)

    return out_parents + out_features


def get_id(
    record: GFFRecord,
    id_field: str
) -> Optional[str]:

    id_ = record.attributes.get(id_field, None)
    if id_ is None:
        return None

    if isinstance(id_, list):
        id_ = list(set(id_))  # Remove duplicates
        if len(id_) > 1:
            raise ValueError(
                f"Feature had multiple ids for specified ID field "
                f"{id_field}. Got: {','.join(id_)}."
            )
        elif len(id_) == 0:
            return None
        else:
            id_ = id_.pop()

    assert isinstance(id_, str)
    return id_


def write_gff(
    gff: Iterable[GFFRecord],
    handle: TextIO
):
    seen: Set[GFFRecord] = set()
    for feature in sorted(
        gff,
        key=lambda g: (g.seqid, g.start, g.end, g.type)
    ):
        if len(feature.parents) > 0:
            continue

        for child in feature.traverse_children(sort=True):
            if child in seen:
                continue
            elif child.type in (
                'n_terminal_region',
                'central_hydrophobic_region_of_signal_peptide',
                'c_terminal_region'
            ):
                seen.add(child)
                continue

            seen.add(child)
            child.update_parents()
            print(child, file=handle)
        print("###", file=handle)


def split_on_type(
    records: Iterable[GFFRecord]
) -> DefaultDict[str, List[GFFRecord]]:
    seen: Set[GFFRecord] = set()
    out: DefaultDict[str, List[GFFRecord]] = defaultdict(list)

    type_map = {
        "signal_peptide": "signal_peptide",
        "n_terminal_region": "signal_peptide",
        "c_terminal_region": "signal_peptide",
        "central_hydrophobic_region_of_signal_peptide": "signal_peptide",
        "mitochondrial_targeting_signal": "peptide_localization_signal",
        "peptide_localization_signal": "peptide_localization_signal",
        "transmembrane_polypeptide_region": "transmembrane_polypeptide_region",
        "propeptide_cleavage_site": "propeptide_cleavage_site",
        "polypeptide_motif": "polypeptide_motif",
        "protein_match": "protein_match",
        "protein_hmm_match": "protein_match",
        "match_part": "protein_match",
    }

    for record in records:
        if record in seen:
            continue

        if record.type in type_map:
            type_ = type_map[record.type]
            out[type_].append(record)
            seen.add(record)

            for parent in record.traverse_parents():
                if parent in seen:
                    continue
                out[type_].append(parent)
                seen.add(parent)

            for child in record.traverse_children():
                if child in seen:
                    continue
                out[type_].append(child)
                seen.add(child)

    return out


def split_on_source(
    records: Iterable[GFFRecord]
) -> DefaultDict[str, List[GFFRecord]]:
    out: DefaultDict[str, List[GFFRecord]] = defaultdict(list)
    for record in records:
        out[record.source].append(record)

    return out


def inner(  # noqa: C901
    genes: TextIO,
    annotations: TextIO,
    outfile: str,
    id_field: str,
    filter_kex2: bool,
    split: Literal['source', 'type', None],
):
    genes_gff = list(GFFRecord.from_file(genes))

    cdss: DefaultDict[str, List[GFFRecord]] = defaultdict(list)
    for g in genes_gff:
        if g.type != "CDS":
            continue

        id_ = get_id(g, id_field)
        if id_ is None:
            continue
        cdss[id_].append(g)

    prots: DefaultDict[str, List[GFFRecord]] = defaultdict(list)
    for prot in GFFRecord.from_file(annotations):
        if prot.seqid not in cdss:
            continue

        if prot.type in (
            "n_terminal_region",
            "c_terminal_region",
            "central_hydrophobic_region_of_signal_peptide"
        ):
            continue
        elif (
            (prot.attributes.id is not None) and
            (prot.type == "signal_peptide")
        ):
            prot.attributes.id = None
            prot.children = []

        if (
            (prot.source == "SignalP:3.0b") and
            ("d_decision" in prot.attributes.custom)
        ):
            prot.source = "SignalPNN:3.0b"
        elif (prot.source == "SignalP:3.0b"):
            prot.source = "SignalPHMM:3.0b"

        prots[prot.seqid].append(prot)

    mapped: List[GFFRecord] = []
    for id_, these_prots in prots.items():
        these_cdss = cdss[id_]
        feats = split_protein_features(
            these_prots,
            these_cdss,
            separate_peps=True,
            filter_kex2=filter_kex2,
            regions=True
        )
        mapped.extend(feats)

    if (split is None) and (outfile in ("stdout", "-")):
        write_gff(mapped, sys.stdout)
    elif (split is None):
        with open(outfile, "w") as handle:
            write_gff(mapped, handle)
    elif split == "type":
        for type_, split_mapped in split_on_type(mapped).items():
            with open(f"{outfile}{type_}.gff3", "w") as handle:
                write_gff(split_mapped, handle)
    elif split == "source":
        for source, split_mapped in split_on_source(mapped).items():
            with open(f"{outfile}{source}.gff3", "w") as handle:
                write_gff(split_mapped, handle)
    else:
        print(split, outfile)
    return


def runner(args: argparse.Namespace) -> None:
    try:
        inner(
            genes=args.genes,
            annotations=args.annotations,
            outfile=args.outfile,
            id_field=args.id_field,
            filter_kex2=args.filter_kex2,
            split=args.split,
        )
    except Exception as e:
        raise e
    return
