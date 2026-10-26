from clean_paper_tts.textutil import (build_vocabulary, clean_heading, heading_key, join_lines,
                                      resolve_soft_breaks, strip_citations)


def resolve(lines):
    text = join_lines(lines)
    return resolve_soft_breaks(text, build_vocabulary([text]))


def test_hyphenated_word_is_rejoined():
    assert resolve(["the simul-", "taneous release of damage"]) == "the simultaneous release of damage"


def test_real_compound_keeps_hyphen_when_document_uses_it():
    out = resolve(["a cohort-", "conserved signature, cohort and conserved genes"])
    assert "cohort-conserved signature" in out


def test_acronym_prefix_keeps_hyphen():
    assert resolve(["TME-", "resident cells"]) == "TME-resident cells"


def test_citations_removed():
    t = "Immune cells [12, 14] and T cells [3-5] respond (Smith et al., 2020; Jones 2019) well [ ]."
    out = strip_citations(t)
    assert "[12" not in out and "Smith" not in out and "[3" not in out
    assert out.startswith("Immune cells and T cells respond")


def test_non_citation_brackets_survive():
    assert "[Pt(NH3)2Cl2]" in strip_citations("complex [Pt(NH3)2Cl2] was used")


def test_heading_helpers():
    assert heading_key("2.8 | Acknowledgements") == "acknowledgements"
    assert clean_heading("■ INTRODUCTION") == "INTRODUCTION"
    assert clean_heading("2.8 | Benchmarking") == "2.8 Benchmarking"
