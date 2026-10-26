## acs_omega / PMC13628994.pdf
**Sustainable Biodiesel Production over a Novel Magnetic Solid Acid Catalyst Derived from Copper Ferrite: Statistical Optimization and Catalytic Performance Evalu** (pdf, 19.3s, 4.98 MB, authors parsed: 3)

flags: lowercase_starts(9), unterminated_paragraphs(8), table_captions_without_image(5>4)

warnings: none

dropped: {'running header/footer': 87, 'figure text': 9, 'equation': 1, 'page-1 metadata box': 1, 'table body': 384, 'noise': 9, 'page footnote': 2, 'front matter': 4, 'citation markers': 1, 'section': 63}

outline:
```
Abstract
1. INTRODUCTION
2. MATERIALS AND METHODS
  2.1. Materials
  2.2. Magnetic Solid Catalyst Synthesis (MoO3/CuFe2O4)
    2.2.2. Loading of the Active Phase onto the Support. The
  2.3. Techniques for Material Characterization
  2.4. Transesterification Process
  2.5. Statistical Analysis and Response Surface Methodology (RSM)
  2.6. Physicochemical Characterization of Biodiesel
  2.7. Catalyst Reuse Study
3. RESULTS AND DISCUSSION
  3.1. Effect of Molybdenum Content on Catalyst Composition
  3.2. Characterization of the Magnetic Catalyst 30-MoO3/CuFe2O4
  3.3. Optimization of Transesterification Reaction Parameters
    3.3.1. Regression Model Development and Evaluation of the Effects of Process Variables on 
    3.3.2. Optimization and Validation of the Developed
  3.4. Characterization of the Synthesized Biodiesel
  3.5. Reusability Study of the 30-MoO3/CuFe2O4 Catalyst
  3.6. Comparison of Heterogeneous Acid Catalysts Reported for Biodiesel Production
  Productiona
```
first paragraphs:
- In this study, a novel magnetic solid acid catalyst based on molybdenum oxide-impregnated copper ferrite was synthesized and applied to methyl transesterification from waste cooking oil (WCO). The catalytic solid was characterized by surface acidity, XRD, FTIR
- The consumption of fossil fuels has grown exponentially due to population growth and increased consumer demand, leading to the depletion of nonrenewable resources and an unprecedented environmental crisis. Many fossil fuels, including gasoline, coal, and petro
- Consequently, there is a vital need for renewable energy sources (e.g., ethanol, biodiesel, hydrogen, etc.) to supplement the already established fossil fuel sources, making it imperative for numerous researchers to conduct diverse studies in this area.
- The use of renewable raw materials derived from reuse, such as waste cooking oil (WCO), will not only reduce production costs but also prevent potential environmental contamination from improper disposal in sewage systems. Among renewable energy sources, biodi

suspect paragraphs:
- impregnation step of the active phase onto the support was carried out according to the methodology described by Santos et al. with adaptations, as shown in Figure 1 (II). A series of catalysts were s
- msample
- n ~ (1) where Mb is the NaOH molarity; Ma is the HCl molarity; Va and Vb are the volumes of HCl and NaOH used, respectively; and msample is the sample mass.
- k k k X2 +
- ii i i

dropped sample:
- [page-1 metadata box] [vector box near page foot]
- [noise: licence] This article is licensed under CC-BY 4.0
- [noise: article tag] Article
- [noise: citation banner] ACCESS
- [noise: citation banner] Metrics & More
- [noise: citation banner] Read Online
- [noise: supporting info p] sı
- [page footnote] © 2026 The Authors. Published by American Chemical Society
- [noise: stray symbol] (
- [noise: bare number] 2
- [page footnote] rate.19,20,23
- [noise: stray symbol] *

## bmc_bioinformatics / PMC13689177.pdf
**ENflorA: a flexible tool for the bulk submission of next generation sequencing data to the European Nucleotide Archive** (pdf, 1.7s, 0.41 MB, authors parsed: 2)

flags: no_abstract_heading, lowercase_starts(1), noise:download notice(1), noise:doi/url(1)

warnings: none

dropped: {'running header/footer': 19, 'table body': 141, 'noise': 4, 'page footnote': 11, 'front matter': 5, 'citation markers': 1, 'section': 60}

outline:
```
Implementation
  Environment management
  Metadata parsing and validation
  Module breakdown
  ID transfer
  Robust data transfer with lftp
  Testing
Discussion
Conclusions
```
first paragraphs:
- Background With the advancement of sequencing technologies and increasing quality of assembly and annotation tools, the amount of biological sequence data produced by research grows rapidly. To keep this data accessible for potential re-analysis, it is typical
- Results We developed ENflorA, a set of scripts by which sample, sequence read and (annotated) assembly data can be uploaded to ENA in a simple and standardized manner. Our software allows easy metadata entry via spreadsheets, is suitable for batch upload of da
- Conclusions By easing the ENA submission process, ENflorA contributes to making high-throughput sequencing data findable, accessible, interoperable and reusable.
- Keywords ENA, FAIR data, File transfer protocol, INSDC, High-throughput sequencing, Plastome, Submission

suspect paragraphs:
- runs.py, and analysis.py, which mirror ENA's hierarchical object model (Fig. 1). While the typical use case would be the submission of first sample metadata (biosamples.py), then the associated read f
- ENflorA is implemented as a modular suite of Python 3 scripts, designed to be platform-independent and easily deployable in diverse computing environments, from personal laptops running under Windows,
- Analysis (A); 1:1 – the software expects a bijective relationship between the created datatypes (e.g. one Run per Biosample only) or cannot reference already databased objects; First for – taxon for w

dropped sample:
- [noise: publisher url lin] https://doi.org/10.1186/s12859-026-06714-7
- [noise: correspondence] *Correspondence:
- [page footnote] © The Author(s) 2026. Open Access This article is licensed under a Creative Commons Attribution 4.0 
- [noise: history line] Received: 7 May 2026 / Accepted: 12 October 2026
- [noise: web ui] References
- [page footnote] eukaryotic tree of life. Front Sci. 2025;3:1514835. https://doi.org/10.3389/fsci.2025.1514835.
- [page footnote] 2. Lavergne S, Pouchon C, Roquet C, Alberti A, Boleda M, Perrier C, et al. Towards a comprehensive b
- [page footnote] nomic reference for the European arctic–alpine flora. Bot Lett. 2025;172:495–507. https://doi.org/10
- [page footnote] 3. Wetterstrand KDNA, Sequencing Costs. DNA Sequencing Costs: Data from the NHGRI Genome Sequencing 
- [page footnote] (GSP). https://www.genome.gov/about-genomics/fact-sheets/DNA-Sequencing-Costs-Data. Accessed 26 Apr 
- [page footnote] 4. Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR Guiding P
- [page footnote] data management and stewardship. Sci Data. 2016;3:160018. https://doi.org/10.1038/sdata.2016.18.

## brief_bioinform / PMC13575936.pdf
ERROR: timeout after 240s

## cancers / PMC13664407.pdf
**The Molecular Landscape of the Senescence–EMT Interplay: Deciphering Tumour Plasticity Through Molecular Signatures and Multi-Omic Profiling** (pdf, 3.7s, 1.1 MB, authors parsed: 4)

flags: none

warnings: none

dropped: {'running header/footer': 71, 'table body': 133, 'noise': 8, 'page footnote': 8, 'front matter': 7, 'citation markers': 1, 'section': 108}

outline:
```
  Abstract
1. Introduction
2. Senescence as a Driver of EMT and Cellular Plasticity
3. Therapy-Induced Tumour Evolution and Adaptation
4. Characterisation of Senescent Subpopulations and Clinical Stratification Using a Multi-
5. Liquid Biopsy for Monitoring Therapy-Induced Senescence
6. Conclusions and Future Perspectives
    Institutional Review Board Statement: Not applicable.
```
first paragraphs:
- Therapy-induced senescence (TIS) is a common response to anticancer treatments, characterised by stable cell cycle arrest and the acquisition of a complex senescence-associated secretory phenotype (SASP). Initially regarded as a beneficial mechanism that limit
- Cellular senescence is a stress response mechanism characterised by a stable and generally long-lasting arrest of the cell cycle. It can be triggered by a variety of stimuli, including telomere shortening, DNA damage, oxidative stress, oncogene activation, and
- From a physiological perspective, cellular senescence plays essential roles in embryonic development, tissue repair, wound healing, and tumour suppression. By preventing genetically damaged cells from continuing to proliferate, it acts as one of the primary na
- In this context, therapy-induced senescence (TIS) has emerged as a widely recognised response to anticancer treatment. Importantly, physiological senescence and TIS are not interchangeable, as they may differ substantially in their inducing stimuli, cellular c

suspect paragraphs:
- none

dropped sample:
- [noise: article tag] Review
- [noise: history line] Received: 23 August 2026
- [noise: history line] Revised: 20 September 2026
- [page footnote] Accepted: 2 October 2026
- [page footnote] Published: 4 October 2026
- [page footnote] Copyright: © 2026 by the authors.
- [page footnote] Licensee MDPI, Basel, Switzerland.
- [page footnote] This article is an open access article
- [page footnote] distributed under the terms and
- [page footnote] conditions of the Creative Commons
- [page footnote] Attribution (CC BY) license.
- [noise: stray symbol] *

## cell_rep / PMC13650770.pdf
**HHS Public Access** (pdf, 5.1s, 0.59 MB, authors parsed: 18)

flags: lowercase_starts(4), huge_paragraph

warnings: none

dropped: {'margin watermark': 1, 'running header/footer': 74, 'noise': 10, 'page footnote': 70, 'front matter': 18, 'citation markers': 1, 'section': 393}

outline:
```
SUMMARY
  In brief
INTRODUCTION
RESULTS
      Ablating endothelial PERK or blocking PERK activation promotes early HSC and lymphoid rege
      PERK-mediated HSC and lymphoid progenitor recovery is compromised by DLL4 ablation
      PERK-DLL4 regulates regenerative vascular homeostasis and integrity
      PERK and DLL4 differentially regulate pathways supporting B progenitor and HSC regeneratio
      PERK-DLL4 axis orchestrates the stroma network for HSC lymphoid priming
      NOTCH3 is the major NOTCH homolog in CARs, and Notch3−/− mice exhibit impaired post-irradi
DISCUSSION
      Limitations of the study
STAR★METHODS
    EXPERIMENTAL MODEL AND STUDY PARTICIPANT DETAILS
      BM transplantation, irradiation, and 5-FU treatment: BM transplantation was
    METHOD DETAILS
      Analysis of peripheral and bone marrow hematopoiesis: BM reconstitution was
      Multiphoton imaging and analysis for vessel leakiness: Intravital 2-photon
    QUANTIFICATION AND STATISTICAL ANALYSIS
```
first paragraphs:
- 9Department of Pathology, University of South Alabama, Mobile, AL 36688, USA
- 10Department of Urology, Houston Methodist Research Institute, Houston, TX 77030, USA
- 11Translational Biophotonics Laboratory, Department of Systems Medicine and Bioengineering, Houston Methodist Neal Cancer Center, Houston, TX 77030, USA
- 12Department of Pathology and Laboratory Medicine and Microbiology and Immunology, Weill Medical College of Cornell University, New York City, NY 10021, USA

suspect paragraphs:
- performed as described previously. Briefly, 2.0 × 106 total BM cells from WT donor mice (Ly5.1) were transferred retro-orbitally to lethally irradiated (950 cGy Cesium-137 irradiator or 850 cGy X-ray 
- analyzed at d21 and monthly thereafter by manual peripheral blood white blood cell counts (hemocytometer) and FACS immunophenotyping. Three independent groups of transplanted mice were analyzed separa
- imaging preparation was performed as previously described. Mice were anesthetized with isoflurane and placed in a stereotactic holder. The skin above the calvarium was carefully removed and a well was
- scRNA-seq library construction: For scRNA-seq, mice were irradiated with a sublethal 550 cGy sufficient to induce evident damage to the BM vasculature and myelosuppression. Single-cell RNA sequencing 
- 11Translational Biophotonics Laboratory, Department of Systems Medicine and Bioengineering, Houston Methodist Neal Cancer Center, Houston, TX 77030, USA

dropped sample:
- [margin watermark] Author Manuscript
- [noise: licence] This is an open access article under the CC BY-NC-ND license (http://creativecommons.org/licenses/by
- [page footnote] •
- [page footnote] Single-cell RNA-seq data have been deposited to the Gene Expression Omnibus database: https:// www.n
- [page footnote] •
- [page footnote] This paper does not report original code.
- [page footnote] •
- [page footnote] Any additional information required to reanalyze the data reported in this paper is available from t
- [noise: equal contributio] 14These authors contributed equally
- [page footnote] Cell Rep. Author manuscript; available in PMC 2026 October 09.
- [page footnote] Cell Rep. Author manuscript; available in PMC 2026 October 09.
- [page footnote] Cell Rep. Author manuscript; available in PMC 2026 October 09.

## cells / PMC13664028.pdf
**Kaempferol Restores Cilia Length Through Axonemal Microtubule Stabilization** (pdf, 9.4s, 2.8 MB, authors parsed: 4)

flags: lowercase_starts(1), noise:doi/url(2)

warnings: none

dropped: {'running header/footer': 68, 'noise': 7, 'page footnote': 8, 'front matter': 8, 'citation markers': 1, 'section': 85}

outline:
```
  Abstract
1. Introduction
2. Materials and Methods
3. Results
4. Discussion
5. Conclusions
```
first paragraphs:
- Ciliary shortening disrupts cilium-dependent signaling and tissue homeostasis and contributes to diverse ciliopathies and acquired disorders. However, the underlying mechanisms and pharmacological strategies for restoring ciliary length remain poorly understoo
- Cilia are evolutionarily conserved, microtubule-based, antenna-like sensory organelles that protrude from the surface of most mammalian cells, functioning as critical signaling platforms for sensing and integrating extracellular signals. Characterized by micro
- Despite growing interest in ciliary biology, pharmacological agents that directly target ciliogenesis or structural restoration remain scarce. Traditional studies on natural compounds, such as quercetin, platycodin D, and hesperidin, have largely focused on th
- Kaempferol (Kae), a natural flavonol abundant in various medicinal sources, possesses versatile pharmacological activities. Beyond its well-documented cytoprotective properties, emerging evidence suggests that Kae can modulate cytoskeletal dynamics and tubulin

suspect paragraphs:
- frequency (B), ciliary length (C), and length frequency distribution (D). Data are presented as mean ± SEM (Cilia length was measured across 10 fields of view, with approximately 30–40 cilia measured 

dropped sample:
- [noise: article tag] Article
- [noise: history line] Received: 12 August 2026
- [noise: history line] Revised: 1 October 2026
- [page footnote] Accepted: 1 October 2026
- [page footnote] Published: 3 October 2026
- [page footnote] Copyright: © 2026 by the authors.
- [page footnote] Licensee MDPI, Basel, Switzerland.
- [page footnote] This article is an open access article
- [page footnote] distributed under the terms and
- [page footnote] conditions of the Creative Commons
- [page footnote] Attribution (CC BY) license.
- [noise: correspondence] * Correspondence: ruodanxu@gmail.com (R.X.); lin@ibtcm.ac.cn (N.L.)

## comput_struct_biotec / PMC13554421.pdf
**Skill-File-Guided Virtual Screening: A Single-Target Formyl Peptide Receptor 2 Case Study of Large-Language-Model-Coordinated Physics and Diffusion Docking** (pdf, 4.2s, 1.09 MB, authors parsed: 0)

flags: no_abstract_heading, lowercase_starts(5), unterminated_paragraphs(4), huge_paragraph

warnings: none

dropped: {'running header/footer': 22, 'table body': 173, 'figure text': 4, 'noise': 5, 'front matter': 8, 'citation markers': 1, 'section': 52}

outline:
```
Methods
  Agent setup and workflow
  Target system
  Active compound curation
  Decoy generation
  Library preparation
  Ligand protonation, tautomers, and conformers
  Docking engines
  Single-ligand redocking validation
  Evaluation metrics
  Computational resources
Results
  Agent-driven pipeline execution
  Dataset characteristics
  Single-ligand redocking
  VS performance
  Computational cost
  The effect of skill-guided protocol selection
Discussion
  Agentic AI for VS pipeline construction
  The skill-versus-naive contrast is multi-axis, not a controlled skill-file ablation
  Practical implications: ranking power versus early enrichment
  Physics-based versus ML-based docking on this GPCR
  Limitations
Conclusion
```
first paragraphs:
- state-of-the-art blind docking performance, but subsequent Structure-based virtual screening (VS) is widely used in computaindependent benchmarks have raised concerns about training set tional drug discovery to prioritize candidate molecules for experimemoriza
- In this study, I therefore asked whether giving an LLM coding agent (Claude Code) access to such a skill file changes the quality of the VS protocol it produces and whether any such effect depends on the docking engine the agent is directing.
- I used the agent to design, implement, and execute a VS benchmark pipeline under close human scientific supervision, requiring only high-level scientific direction (e.g., "dock these against FPR2, compare Uni-Dock vs DiffDock"); this execution capability is th
- All computational work was performed by Claude Code (Anthropic, model claude-opus-4-8), an LLM-based coding agent operating in a Linux terminal environment with access to file system operations, shell commands, and Python/conda package management. The runs wer

suspect paragraphs:
- state-of-the-art blind docking performance, but subsequent Structure-based virtual screening (VS) is widely used in computaindependent benchmarks have raised concerns about training set tional drug di
- under the precision–recall curve; CI, confidence interval; BCa, bias-corrected and accelerated
- set after PAINS/Brenk filtering (see "Library preparation" section). The paired comparisons reported in the "Results" and "Discussion" sections use the intersection of compounds scored by both protoco
- is computed on a smaller, chemotype-restricted active set, not the same ground truth used for the naive arm; this is a potential source of the observed AUC difference independent of docking-parameter 
- section and the Supplementary execution log, so this run is, in principle, reproducible from the deposited artifacts.

dropped sample:
- [noise: article tag] RESEARCH ARTICLE
- [noise: copyright] Copyright © 2026 Osman Gani.
- [noise: licence] No claim to original U.S. Government Works. Distributed under a Creative Commons Attribution License
- [noise: funding line] Funding: No funding was received for this work.
- [noise: web ui] References
- [front matter] Osman Gani
- [front matter] Section for Pharmaceutical Chemistry, Department of Pharmacy, University of Oslo, 0316 Oslo, Norway.
- [front matter] Address correspondence to: osman.gani@farmasi.uio.no
- [front matter] Background: Virtual screening outcomes depend on protocol choices normally made implicitly by expert
- [front matter] Citation: Gani O. Skill-File-Guided Virtual Screening: A Single-Target Formyl Peptide Receptor 2 Cas
- [front matter] Submitted 16 May 2026 Revised 9 July 2026 Accepted 13 July 2026 Published 9 September 2026
- [front matter] rotations, and torsion angles. DiffDock was reported to achieve

## elife / PMC13690340.pdf
**A hormonal message for a longer life** (pdf, 0.9s, 0.66 MB, authors parsed: 0)

flags: no_abstract_heading, few_words(1122), lowercase_starts(1), noise:doi/url(10)

warnings: none

dropped: {'running header/footer': 14, 'page footnote': 1, 'noise': 2, 'citation markers': 1}

outline:
```
STEROID SIGNALING
  KYLE FEOLA AND PETER M DOUGLAS
```
first paragraphs:
- The steroid hormone dafachronic acid may carry the effects of reduced mTOR activity between tissues to coordinate metabolism and longevity across the body.
- interventions in aging biology. However, mTOR Related research article Schilling K, also supports growth, reproduction, immunity Zaufel A, Morris KM, Löhrke A, Saini R, and tissue repair. The challenge is therefore Knölker HJ, Moustafa T, Antebi A. 2026. not s
- – identify a compelling candidate for this long-Aging is a coordinated process across range signal.
- Most explanations for mTOR-dependent multiple tissues.

suspect paragraphs:
- interventions in aging biology. However, mTOR Related research article Schilling K, also supports growth, reproduction, immunity Zaufel A, Morris KM, Löhrke A, Saini R, and tissue repair. The challeng
- interventions in aging biology. However, mTOR Related research article Schilling K, also supports growth, reproduction, immunity Zaufel A, Morris KM, Löhrke A, Saini R, and tissue repair. The challeng
- Harrison DE, Strong R, Sharp ZD, Nelson JF, Astle CM, Flurkey K, Nadon NL, Wilkinson JE, Frenkel K, Carter CS, Pahor M, Javors MA, Fernandez E, Miller RA. 2009. Rapamycin fed late in life extends life

dropped sample:
- [page footnote] Copyright Feola and Douglas. This article is distributed under the terms of the Creative Commons Att
- [noise: history line] Published 22 October 2026
- [noise: web ui] References
- [citation markers] 3 removed: (Vellai et al., 2003; Harrison et al., 2009) (Schilling et al., 2026) (Motola et al., 200

## front_pharmacol / PMC13683676.pdf
**Third-generation EGFR-TKI plus pemetrexed-platinum chemotherapy versus TKI monotherapy as first-line treatment for EGFR-mutant lung adenocarcinoma with brain pa** (pdf, 8.5s, 2.11 MB, authors parsed: 7)

flags: many_short_paragraphs(44/107), lowercase_starts(1)

warnings: none

dropped: {'running header/footer': 73, 'table body': 509, 'noise': 5, 'page footnote': 6, 'front matter': 13, 'citation markers': 1, 'section': 20}

outline:
```
Abstract
1 Introduction
2 Materials and methods
  2.1 Study design and participants
  2.2 Treatment regimens
  2.3 Efficacy assessment and study endpoints
  2.4 Follow-up
  2.5 Statistical analysis
3 Results
  3.1 Baseline clinicopathological characteristics of patients
  3.2 Intracranial and systemic tumor responses
  3.3 Survival outcome analyses
  3.4 Subgroup analyses of intracranial PFS
  3.5 Patterns of first intracranial progression
  3.6 Safety analysis
  3.7 Prognostic factor analyses
4 Discussion
5 Conclusion
Generative AI statement
Glossary
  ALK
  AUC
  CNS
  CSCO
  CTCAE
  DCR
  ECOG PS
  EGFR
  GPA
  IQR
  MRI
  NCCN
  NSCLC
  ORR
  PET-CT
  PFS
  PSM
  RECIST
  ROS1
  SMD
```
first paragraphs:
- Objective: To evaluate the efficacy and safety of first-line third-generation EGFR-tyrosine kinase inhibitor (EGFR-TKI) combined with pemetrexed-platinum chemotherapy in patients with EGFR-mutant advanced lung adenocarcinoma and brain parenchymal metastases.
- Methods: A bicenter retrospective cohort study was conducted. A total of 150 eligible patients were enrolled and balanced by 1:1 propensity score matching. Tumor response, survival outcomes, and treatment-related adverse events were compared between groups.
- Results: After matching, 60 patients were assigned to each group. The intracranial objective response rate was 78.3% in the combination group versus 61.7% in the monotherapy group (P = 0.046). The median intracranial progression-free survival was 28.3 months i
- Conclusion: First-line third-generation EGFR-TKI plus pemetrexed-platinum chemotherapy is associated with superior intracranial and systemic survival benefits in EGFR-mutant lung adenocarcinoma patients with brain parenchymal metastases, with a favorable safet

suspect paragraphs:
- brain parenchymal metastases, EGFR mutation, intracranial progression-free survival, lung adenocarcinoma, pemetrexed-platinum chemotherapy, third-generation EGFR-TKI
- brain parenchymal metastases, EGFR mutation, intracranial progression-free survival, lung adenocarcinoma, pemetrexed-platinum chemotherapy, third-generation EGFR-TKI
- Baseline characteristics before PSM are summarized in Table 1. The combination group exhibited marginally more favorable baseline prognostic profiles, including a higher proportion of oligometastatic 

dropped sample:
- [noise: correspondence] *CORRESPONDENCE
- [noise: equal contributio] †These authors have contributed equally to this work
- [noise: history line] RECEIVED 06 August 2026 REVISED 13 September 2026 ACCEPTED 15 September 2026 PUBLISHED 07 October 20
- [noise: copyright] COPYRIGHT
- [page footnote] KEYWORDS
- [noise: web ui] References
- [page footnote] da Cunha Santos, G., Shepherd, F. A., and Tsao, M. S. (2011). EGFR mutations and lung cancer. Annu. 
- [page footnote] Gray, J. E., Laktionov, K., Kim, S. W., Kato, T., Wang, J., Han, Z., et al. (2026). Patient-reported
- [page footnote] Jänne, P. A., Planchard, D., Kobayashi, K., Yang, J. C., Liu, Y., Valdiviezo, N., et al. (2026). Sur
- [page footnote] Jia, C., Xu, Q., Zhao, L., Kong, F., and Jia, Y. (2024). Therapeutic role of EGFR - Tyrosine kinase 
- [page footnote] Lee, C. K., Lefresne, S., Soon, Y. Y., Robledo, K., Nichol, A., Sahgal, A., et al. (2026). Osimertin
- [front matter] OPEN ACCESS

## genome_biol / PMC13685163.pdf
**modifications in plasma-derived extracellular vesicles as fingerprints for breast cancer subtypes** (pdf, 4.5s, 2.25 MB, authors parsed: 12)

flags: lowercase_starts(1)

warnings: none

dropped: {'running header/footer': 47, 'figure text': 3, 'code listing': 17, 'noise': 6, 'page footnote': 11, 'front matter': 5, 'citation markers': 1, 'section': 91}

outline:
```
Abstract
Background
Results
    Sequential isolation and profiling of plasma-derived EV proteome and PTMome
    Reactome enrichment analysis differentiates LAB and TNBC
    Relationship between EV PTM markers and established gene-level prognostic indicators
    Integrated EV PTMs to distinguish breast cancer subtypes
Discussion
Conclusions
Methods
    Plasma samples
    Extracellular vesicle isolation
    Enzymatic digestion
    Tyrosine phosphopeptides enrichment
    Lysine acetylation peptide enrichment
    PolyMAC phosphopeptides enrichment
    N-glycopeptides enrichment
  LC–MS/MS
    Data processing
    Quantitative data analysis
    Machine learning approach
```
first paragraphs:
- Background: Addressing tumor heterogeneity in breast cancer research is crucial, given the distinct subtypes like triple-negative, luminal A/B, and HER2, requiring precise differentiation for effective treatment. This study introduces a non-invasive method by 
- Result: The study identified over 28,000 unique non-modified peptides, 5,000 phosphopeptides, 680 acetyl peptides and 1,300 glycopeptides that are successfully characterized. Bioinformatics analyses revealed significant overexpression of 815 non-modified prote
- Conclusions: This research reveals diagnostic markers and enhances understanding of the molecular landscape, contributing to more effective and personalized breast cancer diagnostics and treatments.
- Extracellular vesicles (EVs), including exosomes and microvesicles, contain a wealth of nucleic acids, proteins and signaling molecules vital for intercellular communication. With growing evidence that EVs reflect the molecular signature of the parent cell, th

suspect paragraphs:
- representing 3,311 proteins, 1,865 phosphoproteins, 564 N-glycoproteins, and 316 acetylated proteins, with 1% FDR cut-off (Fig. 2A-E, see Additional file 1: Table S1 for the table format, see Addition
- We have recently proposed a pipeline to sequentially analyze phospho- and N-glyco-proteomics of EVs from the same plasma samples. Here, we expanded the workflow for isolation of EVs from plasma, seque
- The glycopeptide enrichment was performed according to the reported protocol. Desalted peptides were oxidized with 10 mM sodium periodate in 50% ACN and 0.1% TFA at room temperature and shaken in the 

dropped sample:
- [code listing] 55. Courcelles M, Frémin C, Voisin L, Lemieux S, Meloche S, Thibault P. Phosphoproteome dynamics rev
- [code listing] MAP kinase substrates with broad spectrum of functions. Mol Syst Biol. 2013;9. Available from: https
- [code listing] ress.org/doi/10.1038/msb.2013.25.
- [code listing] 56. Issman L, Brenner B, Talmon Y, Aharon A. Cryogenic transmission electron microscopy nanostructur
- [code listing] microparticles. Frischknecht F, editor. PLoS One. 2013;8:e83680. Available from: https://dx.plos.org
- [code listing] pone.0083680.
- [code listing] 57. Masuda T, Tomita M, Ishihama Y. Phase transfer surfactant-aided trypsin digestion for membrane p
- [code listing] J Proteome Res. 2008;7:731–40.
- [code listing] 58. Iliuk AB, Martin VA, Alicie BM, Geahlen RL, Tao WA. In-depth analyses of kinase-dependent tyrosi
- [code listing] teomes based on metal ion-functionalized soluble nanopolymers. Mol Cell Proteomics. 2010;9:2162–72.
- [code listing] 59. Tyanova S, Cox J. Perseus: a bioinformatics platform for integrative analysis of proteomics data
- [code listing] Methods Mol Biol. 2018:133–48. Available from: http://link.springer.com/10.1007/978-1-4939-7493-1_7.

## heliyon / PMC12434933.pdf
**Corrigendum to "A secure data transmission framework for IoT enabled healthcare" [Heliyon Volume 10, Issue 16, August 2024, Article e36269]** (pdf, 0.4s, 0.0 MB, authors parsed: 6)

flags: no_abstract_heading, few_words(43), no_headings, many_short_paragraphs(2/5), noise:doi/url(2)

warnings: none

dropped: {'noise': 3, 'front matter': 10}

outline:
```

```
first paragraphs:
- The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.
- DOI of original article: https://doi.org/10.1016/j.heliyon.2024.e36269.
- * Corresponding author.
- E-mail address: kovtun_v_v@vntu.edu.ua (V. Kovtun).

suspect paragraphs:
- none

dropped sample:
- [noise: publisher url lin] https://doi.org/10.1016/j.heliyon.2025.e43506
- [noise: history line] Available online 20 June 2025 2405-8440/© 2024 The Author(s).
- [noise: licence] This is an open access article under the CC BY-NC-ND license ( http://creativecommons.org/licenses/b
- [front matter] Heliyon 11 (2025) e43506
- [front matter] [figure image]
- [front matter] Contents lists available at ScienceDirect
- [front matter] Heliyon
- [front matter] journal homepage: www.cell.com/heliyon
- [front matter] Corrigendum
- [front matter] Sohail Saif a, Priya Das b, Suparna Biswas c, Shakir Khan d,e, Mohd Anul Haq f, Viacheslav Kovtun g,
- [front matter] a Department of Computer Applications, Maulana Abul Kalam Azad University of Technology, Haringhata,
- [front matter] In this article, reference [55] was incorrectly included: [55] G.T. Chavan, S. Agrawal, N.N. Sakhare

## ijms / PMC13665136.pdf
**Beyond Taxonomy: Fungal Nutraceutical Supplementation Modifies the Functional Potential of the Gut Microbiome in Colorectal Cancer** (pdf, 4.9s, 1.19 MB, authors parsed: 7)

flags: unterminated_paragraphs(6), noise:doi/url(8), noise:journal line(3), reference_like_paragraphs(32)

warnings: ["Page 4: could not locate the body of 'Supplementary Table S1.'; its text is left inline."]

dropped: {'running header/footer': 59, 'table body': 15, 'code listing': 10, 'noise': 9, 'page footnote': 8, 'front matter': 8, 'citation markers': 1}

outline:
```
Abstract
1. Introduction
2. Results
3. Discussion
4. Materials and Methods
5. Conclusions
```
first paragraphs:
- The gut microbiome is increasingly recognized as an important determinant of host immune regulation, intestinal homeostasis, and recovery after colorectal cancer (CRC) surgery. Although our previous randomized, double-blind, placebo-controlled clinical trial d
- Colorectal cancer (CRC) remains one of the leading causes of cancer-related morbidity and mortality worldwide, accounting for more than 1.9 million new cases and nearly a million deaths annually. Despite major advances in screening programs, surgical technique
- Over the last decade, increasing evidence has demonstrated that the intestinal microbiota plays a critical role in colorectal carcinogenesis, host immune regulation, intestinal barrier integrity, and postoperative recovery. Alterations in gut microbial composi
- These observations have led to an increasing interest in microbiota-targeted interventions as potential strategies to improve perioperative outcomes in patients with CRC. Among such interventions, fungal-derived nutraceuticals have attracted attention due to t

suspect paragraphs:
- The differentially abundant orthologues were distributed across several functional categories, including transport systems, metabolic enzymes, transcriptional regulators, and DNA-associated proteins. 
- K10119 6411.87 −0.50 0.70 1.09 × 10−4 IdnD L-idonate 5-dehydrogenase 0.72 3.27 × 10−2 PotI, SpuH Putrescine transport system permease protein Conjugal transfer mating pair stabilization 0.73 3.82 × 10
- 5. Lianos, G.D.; Frountzas, M.; Kyrochristou, I.D.; Sakarellos, P.; Tatsis, V.; Kyrochristou, G.D.; Bali, C.D.; Gazouli, M.; Mitsis, M.;
- 8. Regueiro, C.; Diez Martín, A.I.; Pérez, S.; Daviña-Núñez, C.; Zarraquiños, S.; Remedios, D.; Sánchez Gómez, C.A.; Alonso Lorenzo,
- 24. Foster, K.R.; Schluter, J.; Coyte, K.Z.; Rakoff-Nahoum, S. The evolution of the host microbiome as an ecosystem on a leash. Nature

dropped sample:
- [code listing] 43. Puente-Sánchez, F.; García-García, N.; Tamames, J. SQMtools: Automated processing and visual ana
- [code listing] and anvi'o. BMC Bioinform. 2020, 21, 358. [CrossRef] [PubMed]
- [code listing] 44. McMurdie, P.J.; Holmes, S. phyloseq: An R package for reproducible interactive analysis and grap
- [code listing] PLoS ONE 2013, 8, e61217. [CrossRef] [PubMed]
- [code listing] 45. Sjoberg, D.D.; Whiting, K.; Curry, M.; Lavery, J.A.; Larmarange, J. Reproducible summary tables 
- [code listing] J. 2021, 13, 570–594. [CrossRef]
- [code listing] 46. Love, M.I.; Huber, W.; Anders, S. Moderated estimation of fold change and dispersion for RNA-seq
- [code listing] Biol. 2014, 15, 550. [CrossRef]
- [code listing] 47. Wu, T.; Hu, E.; Xu, S.; Chen, M.; Guo, P.; Dai, Z.; Feng, T.; Zhou, L.; Tang, W.; Zhan, L.I.; et
- [code listing] enrichment tool for interpreting omics data. Innovation 2021, 2, 100141. [CrossRef] [PubMed]
- [noise: article tag] Brief Report
- [noise: history line] Received: 11 September 2026

## j_cheminform / PMC13374194.pdf
**framework for 3D molecular design with optimized properties** (pdf, 8.1s, 2.56 MB, authors parsed: 6)

flags: no_abstract_heading, lowercase_starts(5), unterminated_paragraphs(8), noise:doi/url(1)

warnings: none

dropped: {'running header/footer': 35, 'figure text': 3, 'table body': 94, 'equation': 35, 'noise': 5, 'page footnote': 18, 'front matter': 4, 'citation markers': 1, 'section': 85}

outline:
```
Scientific contribution
Results and discussion
  Framework overview
  Molecular generation
  Comparison with state-of-the-art methods
  Evolutionary trajectory and diversity maintenance
  Multi-property optimization
  ADMET property optimization
  Scaffold-constrained molecular design
  Scaffold-constrained property optimization
Conclusion
Methods
  Datasets and molecular properties
  Evolutionary-diffusion integration
  Diffusion models
  Neural network dynamics
  Performance evaluation
```
first paragraphs:
- Designing molecules with specific target properties remains a fundamental challenge in computational chemistry. While existing approaches show promise, most rely on simplified representations like SMILES strings or 2D graphs that lack essential three-dimension
- This manuscript has been authored by UT-Battelle, LLC, under contract DE-AC05-00OR22725 with the US Department of Energy (DOE). The US Government retains, and the publisher, by accepting the article for publication, acknowledges that the US Government retains 
- Xiaobo Lin linx1@ornl.gov Logan T. Kearney kearneylt@ornl.gov Amit K. Naskar naskarak@ornl.gov Debsindhu Bhowmik bhowmikd@ornl.gov Full list of author information is available at the end of the article
- representation offers advantages in maintaining structural validity during iterative optimization, with potential for geometry-aware applications in materials science and drug discovery.

suspect paragraphs:
- representation offers advantages in maintaining structural validity during iterative optimization, with potential for geometry-aware applications in materials science and drug discovery.
- independent runs): QED = 0.936 ± 0.001 (between-run std), Tanimoto = 0.173 ± 0.002, scaffold diversity = 73.1% ± 1.2% (see Supporting Information Table S6)
- evolutionary contribution: the diffusion model alone achieves QED = 0.79, while evolutionary optimization raises this to 0.94, a +19% improvement. This indicates that the evolutionary optimization is 
- αt
- the predicted noise removal. This parameterization enables stable training by predicting noise rather than the clean signal directly.

dropped sample:
- [noise: publisher url lin] https://doi.org/10.1186/s13321-026-01237-y
- [noise: correspondence] *Correspondence:
- [page footnote] © UT-Battelle, LLC and Zhaoqian Su, Yunchao Liu 2026. Open Access This article is licensed under a C
- [noise: bare number] 1
- [page footnote] Supplementary material 1.
- [page footnote] Research was sponsored by the US Department of Energy, Office of Science, Basic Energy Sciences, Mat
- [noise: history line] Received: 20 December 2025 Accepted: 27 May 2026
- [noise: web ui] References
- [page footnote] 6. Bickerton GR, Paolini GV, Besnard J et al (2012) Quantifying the chemical
- [page footnote] beauty of drugs. Nat Chem 4(2):90–98
- [page footnote] 7. Bilodeau C, Jin W, Jaakkola T et al (2022) Generative models for molecular
- [page footnote] discovery: recent advances and challenges. Wiley Interdiscip Rev Comput Mol Sci 12(5):e1608

## j_med_chem / PMC13492272.pdf
**Fragment-Based Discovery of Potent RNA-Competitive Inhibitors of the DEAH-Box RNA Helicase DHX8** (pdf, 10.7s, 4.07 MB, authors parsed: 37)

flags: lowercase_starts(24), unterminated_paragraphs(5), table_captions_without_image(8>6)

warnings: ["Page 8: could not locate the body of 'Table 2. Investigating the Carboxylic Ac'; its text is left inline.", "Page 14: could not locate the body of 'Table 8. Effect of Inhibitor Binding on '; its text is left inline."]

dropped: {'running header/footer': 135, 'figure text': 9, 'page-1 metadata box': 1, 'table body': 20, 'noise': 10, 'page footnote': 1, 'front matter': 3, 'citation markers': 1, 'section': 67, 'characterization data': 33}

outline:
```
Abstract
INTRODUCTION
RESULTS AND DISCUSSION
    Chemistry
    DHX8 Fragment Screening
    Fragment Hit Confirmation
    Determining the Fragment Binding Mode
    Optimizing the Fragment Binding Mode
    Extending into the RNA-Binding Tunnel
    Substituting the Extended Linker
    Potent DHX8 Inhibitors Showing Cellular Target Engagement
    Mode of Action of RNA-Competitive DHX8 Inhibitors
  Compared to Wild-Type DHX8a
    Comparison with Other DExH-Box Helicase Inhibitors
CONCLUSIONS
EXPERIMENTAL SECTION
    General Synthetic Chemistry
    Preparation of Compounds 2-((4-Isopropylphenyl)thio)nicotinic Acid (13). To a solution
2 2-((4-Isopropylphenyl)thio)benzoic Acid (14). To a solution
      2-((2,4-Dichlorophenyl)thio)benzoic Acid (15). 2-Iodobenzoic
      3-((4-Isopropylphenyl)thio)picolinic Acid (16). To a solution
      3-((4-Isopropylphenyl)thio)pyrazine-2-carboxylic Acid (17).
      2-((1-Chloronaphthalen-2-yl)thio)nicotinic Acid (22). To a
      2-((6-(Methylsulfonamido)naphthalen-2-yl)thio)nicotinic
      2-((4-(Ethylamino)phenethyl)thio)nicotinic Acid Hydro-
      2-((4-((2-Methoxyethyl)amino)phenethyl)thio)nicotinic
      2-((4-((2-Fluoroethyl)amino)phenethyl)thio)nicotinic Acid
      2-((4-(Dimethylamino)phenethyl)thio)nicotinic Acid (32). 2-
      2-((4-(Cyclopentylamino)phenethyl)thio)nicotinic Acid Hy-
      2-[2-(4-Isopropylamino-phenyl)-ethylsulfanyl]-nicotinic
      2-((4-Isopropoxyphenethyl)thio)nicotinic Acid (35). To a
      2-((2-Phenylpropyl)thio)nicotinic Acid (36). 2-Mercaptonico-
      2-((1-Phenylpropan-2-yl)thio)nicotinic Acid (37). To a 250
      2-((1,2-Diphenylethyl)thio)nicotinic Acid (38). A mixture of 2-
      2-((1-Amino-1-oxo-3-phenylpropan-2-yl)thio)nicotinic Acid
      2-((1,3-Diphenylpropan-2-yl)thio)nicotinic Acid (40). In a 50
      2-((1-Benzylcyclopentyl)thio)nicotinic Acid (41). To a 30 mL
      (R)-2-((1-Phenylpropan-2-yl)thio)nicotinic Acid (42). 37 2-
      (S)-2-((1-Phenylpropan-2-yl)thio)nicotinic Acid (43). 37 2-
      (S)-2-((1,2-Diphenylethyl)thio)nicotinic Acid (44). 38 2-((1,2-
```
first paragraphs:
- Human DHX8 is a spliceosomal DEAH-box RNA helicase involved in releasing mRNA from the spliceosome and crucial in ensuring splicing fidelity. DHX8 was identified as a promising therapeutic oncology target due to its role in regulating stress-adaptive gene expr
- DHX8 is a spliceosomal RNA helicase belonging to the DEAH-box helicase family that couples the hydrolysis of nucleoside triphosphates (NTPs) with RNA translocation to facilitate the release of mature mRNA from the spliceosome. In addition, DHX8 is thought to b
- We recently identified and validated DHX8 in a functional genomic screen for regulators of Heat Shock Factor (HSF1) − a ligand-less and difficult-to-drug master regulator transcription factor that plays a central role in the cellular response to stress. HSF1 i
- JohnPhos, Pd2(dba)3, t-BuONa, 1,4-Dioxane, 80 °C, 13 h; d: Fe, NH4Cl, EtOH/H2O, 80 °C, 2 h; and e: Acetone, NaBH(OAc)3, AcOH, DCM, rt, 1 h However, helicases are considered challenging drug targets due to the conserved nature of their active sites and the tran

suspect paragraphs:
- reductive amination reaction with acetone to install the isopropylaniline moiety in (v). Nucleophilic displacement of alcohol (v) with thioacetic acid under Mitsunobu reaction conditions gave thioeste
- aDHX8 fragment binding was confirmed using a fluorescence assay based on a fluorescently labeled poly(A) ssRNA substrate. The effect of fragment binding on DHX8 ATP hydrolysis was characterized using 
- efficiency in the ATPase assay, although not in the RNA FA assay. We therefore concluded that neither linker shortening nor extension was beneficial and retained the ethanethiol linker.
- aDHX8 binding was confirmed using a fluorescence anisotropy assay based on a fluorescently labeled pol(A)ssRNA substrate. The effect of compound binding on DHX8 ATP hydrolysis was characterized using 
- tional rearrangements during RNA translocation, which involves the opening and closing of the RNA-binding tunnel. A study on yeast Prp43, the functional homologue of human DHX15, demonstrated that in 

dropped sample:
- [page-1 metadata box] [vector box near page foot]
- [noise: licence] This article is licensed under CC-BY 4.0
- [noise: article tag] Article
- [noise: citation banner] Cite This: J. Med. Chem. 2026, 69, 18277−18299
- [noise: citation banner] ACCESS
- [noise: citation banner] Metrics & More
- [noise: citation banner] Read Online
- [noise: supporting info p] sı
- [page footnote] © 2026 The Authors. Published by American Chemical Society
- [noise: stray symbol] *
- [noise: correspondence] Email: rob.vanmontfort@icr.ac.uk
- [noise: equal contributio] #B.J.R. and C.E. contributed equally to this work. The manuscript was written through contributions 

## molecules / PMC13687675.pdf
**RETRACTED: Kim et al. Anthocyanins Derived from Vitis coignetiae Pulliat Contributes Anti-Cancer Effects by Suppressing NF-B Pathways in Hep3B Human Hepatocellu** (pdf, 0.2s, 0.0 MB, authors parsed: 9)

flags: no_abstract_heading, few_words(201), no_headings

warnings: none

dropped: {'running header/footer': 5, 'noise': 3, 'page footnote': 8, 'front matter': 11, 'citation markers': 1, 'section': 3}

outline:
```

```
first paragraphs:
- The journal retracts the article titled "Anthocyanins Derived from Vitis coignetiae Pulliat Contributes Anti-Cancer Effects by Suppressing NF-κB Pathways in Hep3B Human Hepatocellular Carcinoma Cells and In Vivo", cited above.
- Following publication, concerns were brought to the attention of the Editorial Office regarding the integrity of a figure presented in this article.
- According to the journal's standard procedures, the Editorial Office and Editorial Board conducted an investigation that identified indications of image duplications and inappropriate editing within Figure 1B, as well as incomplete reporting of the ethical app
- Although the authors cooperated during the investigation, the explanations and supporting materials provided were not deemed sufficient by the Editorial Board to resolve the identified concerns. As a result, the Editorial Board has decided to retract this pape

suspect paragraphs:
- none

dropped sample:
- [noise: history line] Received: 14 October 2026
- [page footnote] Accepted: 16 October 2026
- [page footnote] Published: 21 October 2026
- [page footnote] Copyright: © 2026 by the authors.
- [page footnote] Licensee MDPI, Basel, Switzerland.
- [page footnote] This article is an open access article
- [page footnote] distributed under the terms and
- [page footnote] conditions of the Creative Commons
- [page footnote] Attribution (CC BY) license.
- [noise: stray symbol] *
- [noise: correspondence] Correspondence: lwshmo@hanmail.net or lwshmo@gnu.ac.kr; Tel.: +82-55-750-8733; Fax: +82-55-758-9122
- [front matter] Retraction Min Jeong Kim , Anjugam Paramanantham , Won Sup Lee *, Jeong Won Yun , Seong Hwan Chang ,

## nat_commun / PMC13687067.pdf
**Strain-engineered fabrication of high-density aligned graphene-based nanoscrolls via UV-tunable adhesive tapes** (pdf, 10.5s, 2.61 MB, authors parsed: 4)

flags: no_abstract_heading, lowercase_starts(13), unterminated_paragraphs(8), figure_captions_without_image(8>6)

warnings: none

dropped: {'margin watermark': 6, 'running header/footer': 55, 'figure text': 261, 'equation': 1, 'sideways table text': 8, 'noise': 8, 'front matter': 5, 'citation markers': 1, 'section': 77}

outline:
```
Results
Discussion
Methods
```
first paragraphs:
- Graphene nanoscrolls (GNSs), one-dimensional nanostructures formed by rolling up a single sheet of graphene, exhibit electronic and mechanical properties distinct from the original graphene sheet. Although several methods have been proposed to synthesize GNSs,
- graphene sheet. Confining electrons in one-dimensional (1D) graphene Graphene is a two-dimensional (2D) material that exhibits exotic structures significantly changes the electronic band structure due to physical properties and possesses many potential applica
- 1Faculty of Engineering Sciences, Kyushu University, Kasuga, Fukuoka 816-8580, Japan. Department of Physics, Tokyo University of Science, Kagurazaka, Shinjuku, Tokyo 162-8602, Japan. SANKEN (The Institute of Scientific and Industrial Research), The University 
- There are two main approaches to synthesize nanoscrolls. The first method involves sonication or stirring graphite intercalation compounds (GICs), GO, or graphene flake dispersions in solvents, eventually forming GNSs due to van der Waals interaction between a

suspect paragraphs:
- graphene sheet. Confining electrons in one-dimensional (1D) graphene Graphene is a two-dimensional (2D) material that exhibits exotic structures significantly changes the electronic band structure due
- tensile strain. On the other hand, a weak adhesion force cannot effectively apply tensile strain, as graphene would slip on the tape surface. In our case, the tape was illuminated by UV light after it
- was confirmed by independent experiments for more than 10 times. c Evolution of crack density of graphene with nominal tensile strain, measured at three different positions. d in-situ Raman spectra me
- of this shift is retained even after releasing the strain of the stack. This result indicates that the graphene experiences tensile strain even after relaxing the UV tape. This residual strain is supp
- lifted out from the SiO2 surface with a probe tip. j After the graphene flake gradually detaches from the SiO2 surface, it immediately starts to scroll, owing to the residual tensile strain in the gra

dropped sample:
- [margin watermark] 1234567890():,;
- [margin watermark] Nanoscroll density (mm-1)
- [margin watermark] Crack density (mm-1)
- [margin watermark] Intensity
- [margin watermark] �E (meV C-atom)
- [margin watermark] Normalized intensity
- [noise: article tag] Article
- [noise: publisher url lin] https://doi.org/10.1038/s41467-026-78264-8
- [noise: history line] Received: 29 December 2025 Satoru Fukamachi, Tomoki Maezawa, Tatsuya Ikuta, Takako Matsunaga, Accept
- [noise: check updates] Check for updates
- [noise: bare number] 0
- [noise: web ui] References

## plos_comp_biol / PMC13686291.pdf
**CardamomOT: A mechanistic optimal transport-based framework for gene regulatory network inference, trajectory reconstruction and generative modeling** (pdf, 13.6s, 4.41 MB, authors parsed: 2)

flags: no_abstract_heading, lowercase_starts(36), unterminated_paragraphs(22), noise:doi/url(3), table_captions_without_image(1>0)

warnings: ["Page 33: could not locate the body of 'Table 1. Positioning of CardamomOT withi'; its text is left inline."]

dropped: {'running header/footer': 76, 'equation': 64, 'code listing': 32, 'noise': 14, 'page footnote': 23, 'front matter': 11, 'citation markers': 1, 'section': 99}

outline:
```
      Data availability statement: The algo
Author summary
1 Introduction
2 Methods
  2.1 Mechanistic modeling of cellular dynamics
  2.2 Overview of CardamomOT
    2.2.1 Preprocessing: Inferring the NB mixture and initializing basin labels. We first cali
    Algorithm 1 CardamomOT
3 Results
  3.1 Simulation of temporal snapshots
  3.2 The statistical mixture model captures both mechanistic parameters and biological cell
  3.3 Benchmarking CardamomOT: Performance, robustness and scalability of GRN inference
    CardamomOT achieves scalable GRN inference across network topologies on model-matched simu
  3.4 CardamomOT accurately reconstructs hidden protein vectors, cellular trajectories and v
    CardamomOT reconstructs protein trajectories from transcriptomic snapshots. A key feature 
  3.5 The calibrated model regenerates cellular trajectories consistent with experimental da
  3.6 In silico perturbations predict some observed experimental outcomes and identify poten
4 Discussion
  Appendix
    A Detailed interpolation procedure
    B Link with other model learning approaches
    B.2 Reference fitting and Wasserstein Lagrangian flows. Reference Fitting. RF [25] replace
    C Details on GRN inference for experimental datasets
    S1 Table. Comparison of reference parameters and parameters inferred by CardamomOT for dif
    S1 Fig. Representation of the inferred gene regulatory network for the Semrau dataset. (A)
      Reference process Q Lagrangian modification Ambient space
      Non-linear PDMP (2)
      None basin
    S2 Fig. Representation of the inferred gene regulatory network for the Kameneva dataset. (
    S3 Fig. Representation of the inferred gene regulatory network for the Schiebinger dataset
    S4 Fig. Marginal mRNA distributions for selected genes, showing (leftmost column) all time
    S5 Fig. Pairwise gene expression correlation structure across reference, NB mixture and si
    S6 Fig. UMAPs of reference and CardamomOT inferred protein trajectories for the (A–B) FN4,
    S7 Fig. Evaluation of the cell-to-cell coupling accuracy on true trajectory data for Carda
    S8 Fig. Evolution of the loss function and AUPR score during training for the networks FN4
    S9 Fig. For each of the three experimental datasets (Semrau, Kameneva, Schiebinger), the i
    S10 Fig. CardamomOT simulations broadly preserve the global structure and temporal orderin
    S11 Fig. Sensitivity of GRN inference accuracy to the switching-time grid resolution npas.
```
first paragraphs:
- A key challenge in inferring gene regulatory networks (GRNs) governing cellular processes such as differentiation and reprogramming from experimental data lies in the impossibility of directly measuring protein dynamics at the single-cell level, which prevents
- which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.
- rithm CardamomOT, as well as the codes for generating the figures of this article, are available at https://github.com/eliasventre/ CardamomOT, and the documentation of the package at https://cardamomot.readthedocs. io/en/latest/. Data analyzed in this article
- Competing interests: The authors have declared that no competing interests exist.

suspect paragraphs:
- which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.
- rithm CardamomOT, as well as the codes for generating the figures of this article, are available at https://github.com/eliasventre/ CardamomOT, and the documentation of the package at https://cardamom
- inference, trajectory reconstruction, and simulation of realistic datasets into a unified framework for scRNA-seq time series analysis.
- dt 1,i i – 1,i i
- s0,i

dropped sample:
- [code listing] 2: for k = 0, 1, ... until convergence do
- [code listing] 3: Compute cost matrices {Cj} via interpolation (Appendix A); solve N – 1 OT problems (9); sample L
- [code listing] protein trajectories from the multimarginal coupling π1 ⊗· · · ⊗ πN–1. 
- [code listing] (Step 1)
- [code listing] 4: Update θ(k+1) by solving (10). 
- [code listing] (Step 2)
- [code listing] 5: Update basin labels {z(k+1)} via (11). 
- [code listing] (Step 3)
- [code listing] 6: end for
- [code listing] Algorithm 2 ODE recalibration of protein degradation rates d1 (Step (i))
- [code listing] INPUT: converged GRN θ∗, reconstructed trajectories {Pl(tj)}l,j, prior dprior
- [code listing] 1: Initialize d1 ← dprior, scale correction s ← 1

## rsc_adv / PMC13681189.pdf
**RSC Advances** (pdf, 14.1s, 3.77 MB, authors parsed: 2)

flags: lowercase_starts(9), unterminated_paragraphs(8), huge_paragraph

warnings: none

dropped: {'running header/footer': 62, 'table body': 601, 'noise': 6, 'page footnote': 5, 'front matter': 4, 'citation markers': 1, 'section': 57, 'characterization data': 4}

outline:
```
Abstract
1 Introduction
  2.1 Chemistry
    2.3.1 Molecular docking.
3 Conclusion
  4.1 Synthesis
    4.1.1 General procedure for synthesis of 2-(1H-indol-3-yl)- 1-(4-((1-substituted-1H-1,2,3-
```
first paragraphs:
- Tuberculosis remains one of the major infectious diseases and continues to pose a significant public health challenge globally. In the present study, two sets of novel 1,2,3-triazolyl indole-piperazine derivatives (R1– R17) were designed, synthesized and evalu
- DOI: 10.1039/d6ra05893k
- emphasizing the importance of the 1,2,3-triazolyl indole-piperazine scaffold for the development of next-generation anti-TB therapeutics.
- rsc.li/rsc-advances

suspect paragraphs:
- emphasizing the importance of the 1,2,3-triazolyl indole-piperazine scaffold for the development of next-generation anti-TB therapeutics.
- rsc.li/rsc-advances
- aDepartment of Chemistry, School of Technology & School of Sciences, Woxsen University, Hyderabad-502345, Telangana, India.
- existing therapies. Resistance to rst line antitubercular drugs, resistance to uoroquinolone, bedaquiline, and linezolid has made the treatment outcomes and fatality rates more challenging. Recently
- the corresponding alkyl bromides (R1-Br) in the presence of NaN3, CuSO4 and sodium ascorbate in a tBuOH/H2O system to afford the desired 1,2,3-triazolyl indole-piperazine derivatives (R1–R11) with goo

dropped sample:
- [noise: licence] Published on 20 October 2026 Licensed under CC-BY-NC 4.0
- [noise: citation banner] Cite this: DOI: 10.1039/d6ra05893k
- [noise: history line] Received 2nd July 2026
- [noise: history line] Accepted 13th October 2026
- [noise: correspondence] E-mail: rajkumar. reddyrajula111@gmail.com
- [page footnote] bMedicinal Chemistry Laboratory, Department of Chemistry, Osmania University, Hyderabad-500 076, Tel
- [page footnote] cMedicinal Chemistry Research Laboratory, Department of Pharmacy, Birla Institute of Technology and 
- [page footnote] dDepartment of Chemistry, National Institute of Technology Karnataka, Surathkal- 575025, Mangalore, 
- [page footnote] eDepartment of Chemistry, School of Engineering, Dayananda Sagar University, Harohalli, Bengaluru-56
- [page footnote] fDepartment of Chemistry, Birla Institute of Technology and Science Pilani, Hyderabad Campus, Jawaha
- [noise: web ui] References
- [front matter] PAPER
