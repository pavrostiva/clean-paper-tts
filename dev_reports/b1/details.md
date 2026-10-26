## acs_omega / PMC13628633.pdf
**Molecular Mechanisms of CTAB-Induced Oil Droplet Detachment in** (pdf, 6.4s, 5.48 MB, authors parsed: 5)

flags: none

warnings: none

dropped: {'running header/footer': 87, 'figure text': 10, 'equation': 1, 'page-1 metadata box': 1, 'noise': 6, 'page-1 footnote': 1, 'front matter': 3, 'section': 52}

outline:
```
Abstract
1. INTRODUCTION
2. MODELS AND METHODS
  2.1. Molecular Models
  2.2. Simulation Methods
3. RESULTS AND DISCUSSIONS
  3.1. Effect of Different Surfactants on Oil Droplet Detachment
  3.2. Mechanism of CTAB Promoted Oil Droplet Detachment in Nanopores
  3.3. Effects of Different Factors on CTAB-Induced Oil Droplet Detachment
    3.3.1. Effect of Temperature on the Detachment
    3.3.2. Effect of Crude Oil Composition on the
  3.4. Applicability, Limitations, and Future Perspectives
4. CONCLUSIONS
```
first paragraphs:
- The efficient recovery of shale oil is severely hindered by the strong oil−solid interactions and nanoscale confinement within shale reservoirs, which substantially restrict crude oil mobility. Although surfactant flooding has emerged as an effective enhanced 
- Shale oil is one of the most promising unconventional hydrocarbon resources and has attracted considerable attention because of its significant potential to enhance global energy security. However, the efficient recovery of shale oil is severely hindered by th
- Furthermore, recent advances in nanoscale interfacial science have increasingly highlighted the intricate fluid−solid and fluid− fluid interactions under tight confinement. A systematic understanding of multiphase coupling mechanisms is critical, as salt ions 
- Surfactant flooding has emerged as one of the most promising enhanced oil recovery (EOR) techniques for unconventional reservoirs because of its ability to reduce oil−water interfacial tension, alter rock wettability, and promote emulsification, thereby facili

suspect paragraphs:
- Shale pore structures are generally classified into pore-type and slittype morphologies. Considering that slit-shaped nanopores are the dominant transport pathways in shale formations, a slit-pore mod
- The observed temperature dependence of oil droplet detachment is governed by a synergistic combination of kinetic and thermodynamic factors rather than simple adsorption enhancement. Kinetically, elev

dropped sample:
- [page-1 metadata box] [vector box near page foot]
- [noise: licence] This article is licensed under CC-BY-NC-ND 4.0
- [noise: article tag] Article
- [noise: citation banner] ACCESS
- [noise: citation banner] Metrics & More
- [noise: citation banner] Read Online
- [noise: citation banner] Article Recommendations
- [page-1 footnote] © 2026 The Authors. Published by American Chemical Society
- [front matter] [figure image]
- [front matter] Yangnan Shangguan, Xinwei Liao, Weiliang Xiong, Xiangji Dou,* and Jinmei Bai*
- [front matter] [formula image]

## bioinformatics / PMC13693595.pdf
**METANet: a supervised ensemble learning framework for reconstructing direct and functional tissue-specific transcription factor networks** (pdf, 4.5s, 2.2 MB, authors parsed: 7)

flags: lowercase_starts(5), unterminated_paragraphs(5), noise:doi/url(2), table_captions_without_image(6>5)

warnings: ["Page 10: could not locate the body of 'Table 5 Empirical test of tissue-specifi'; its text is left inline."]

dropped: {'running header/footer': 28, 'table body': 94, 'page-1 footnote': 2, 'noise': 3, 'front matter': 5, 'section': 16}

outline:
```
  Abstract
1 Introduction
2 Methods
  2.1 Motif expression TF association networks
  2.2 Construction of binding labels
  2.3 Construction of expression-based features
  2.4 Marbach networks
  2.5 PANDA networks
  2.6 Network quality evaluation
    2.6.1 Binding metric
    2.6.2 Gene ontology metric
    2.6.3 GO-directness metric
    2.6.4 PPI metric
    2.6.5 Empirical null
  2.7 Tissue-specificity evaluation
    2.7.1 Tissue-specific edge filtering
    2.7.2 Validation of tissue specificity using eQTL data
    2.7.3 Evaluation against cell line-specific binding labels
  2.8 Gene–trait association analysis using FISHNET
3 Results
  3.1 Overview of TF network map reconstruction
  3.2 METANets capture direct and likely functional targets of TFs
    3.2.1 Binding
    3.2.2 GO enrichment
    3.2.3 GO-directness
    3.2.4 Protein–protein interaction
  3.3 Combining motif and expression
  features improves network mapping
  3.4 Linear and nonlinear expression features are synergistic
  3.5 Combining tissue-specific and tissue-aggregate expression features is helpful
  3.6 METANets are tissue specific and comparable to existing networks
  3.7 METANets are as tissue specific as the Marbach networks
  3.8 METANets are comparable to PANDA in tissue specificity but outperform in network quali
    Empirical test for tissue specificity for 26 tissues
    Wilcoxon signed-rank test versus tissue-specific PANDA
  3.9 Tissue aggregation of binding labels does not distort network evaluation
  3.10 Tissue-specific METANets are useful for genetic analyses
4 Discussion
```
first paragraphs:
- Motivation: Reconstructing tissue-specific transcription factor (TF) networks remains challenging. TF-motif-based methods often lack functional validation, while expression-based methods struggle to distinguish direct binding from indirect regulation. Integrat
- Results: We introduce METANet (Motif Expression TF Association Networks), a supervised ensemble learning framework that combines TF motifs, cis-regulatory element activity, and linear and nonlinear expression-derived features to predict TF binding. Applied to 
- Availability and implementation: All code and network maps are freely available at Zenodo https://doi.org/10.5281/zen odo.20614479.
- (White et al. 2013, Cusanovich et al. 2014, Slattery et al. 2014).

suspect paragraphs:
- direct and likely functional TF–TG interactions relative to other networks. We use the term 'likely functional' because METANet
- incorporates gene expression-derived features as predictors:
- the distribution of 10 000 permutation sums. Bold face indicates P < 0.05. See also Fig. S9, available as supplementary data at Bioinformatics online. tissue ranks of METANets and Marbach networks for
- comparable tissue specificity while outperforming the Marbach networks in all network quality metrics.
- eQTL support 0.485 (125.0) eQTL counts 0.881 (168.5)

dropped sample:
- [page-1 footnote] Received: 6 January 2026. Revised: 7 August 2026. Accepted: 28 September 2026 © The Author(s) 2026. 
- [page-1 footnote] This is an Open Access article distributed under the terms of the Creative Commons Attribution Licen
- [noise: web ui] References
- [noise: copyright] © The Author(s) 2026. Published by Oxford University Press.
- [noise: licence] This is an Open Access article distributed under the terms of the Creative Commons Attribution Licen
- [front matter] Bioinformatics, 2026, 42(10), btag738 https://doi.org/10.1093/bioinformatics/btag738 Published: 7 Oc
- [front matter] Original Paper | Gene expression
- [front matter] Wooseok J. Jung* , Sandeep Acharya , Daniel P. Ruskin, Shu Liao, Vaha Akbary Moghaddam, Zolboo Erden
- [front matter] 1Department of Computer Science and Engineering, Washington University, St. Louis, MO 63130, United 
- [front matter] Associate Editor: Bjorn Gr€ uning€

## bmc_bioinformatics / PMC13659980.pdf
**Wild-AC: A fast, index-free multi-pattern string matching algorithm with wildcard support for proteomics** (pdf, 2.8s, 2.01 MB, authors parsed: 0)

flags: lowercase_starts(9), unterminated_paragraphs(7), huge_paragraph, noise:doi/url(2), noise:copyright(5)

warnings: none

dropped: {'running header/footer': 33, 'figure text': 1, 'table body': 84, 'equation': 2, 'noise': 5, 'front matter': 3, 'section': 55}

outline:
```
Abstract
Background
Methods
    Notation and definitions
    Wild-AC algorithm
  16: end for
  24: end for
  35: end for
  37: end for 38: end procedure
  43: end while
  46: end procedure
  53: end procedure
  62: end for 63: end procedure
    Benchmarking procedure
    Input protein databases
    Input peptide sequences
    Algorithms
    Wall time benchmark
    Memory consumption benchmark
Results
    Correctness and number of hits
    Runtime
    Memory consumption
Discussion
Conclusion
```
first paragraphs:
- Chris Bielow
- Background Efficient multi-pattern string matching with wildcard support is essential
- chris.bielow@fu-berlin.de 1Institut für Mathematik und
- in proteomics, where peptides must be mapped to protein databases containing

suspect paragraphs:
- chris.bielow@fu-berlin.de 1Institut für Mathematik und
- in proteomics, where peptides must be mapped to protein databases containing
- ambiguous amino acids (e.g., B, Z, X). Existing approaches either require preprocessing
- sequence after every Lysine (K) or Arginine (R), unless followed by Proline (P). We allow up to two missed cleavages, where trypsin fails to cut at an expected cleavage site. Consequently, peptides ma
- occur per pattern), but impractical at the text level (the text is long, so the number of wildcard positions, and thus combinations, can be very large). Similarly, there are also algorithms for multi-

dropped sample:
- [noise: publisher url lin] https://doi.org/10.1186/s12859-026-06686-8
- [noise: correspondence] *Correspondence:
- [noise: history line] Received: 4 May 2026 / Accepted: 28 September 2026
- [noise: web ui] References
- [noise: publisher url lin] https://academic.oup.com/nargab/article/doi/10.1093/nargab/lqaf025/8084725
- [front matter] BMC Bioinformatics
- [front matter] Open Access RESEARCH
- [front matter] Chris Bielow1*

## brief_bioinform / PMC13662220.html
**DecBin: Bayesian-optimized deep clustering for long-read metagenomic binning** (html, 7.3s, 2.36 MB, authors parsed: 7)

flags: noise:doi/url(1)

warnings: none

dropped: {'noise': 1, 'section': 16}

outline:
```
Abstract
Introduction
Materials and methods
  Datasets
    Simulated datasets
    Experimental mock-community dataset
    Strain-level resolution dataset
  Overview of the DecBin workflow
    Feature representation
    Variational autoencoder pre-training
    Bayesian optimization
    Deep embedded clustering
    Joint fine-tuning
  Evaluation metrics
  Implementation details and parameter settings
Results
  Benchmark experiments on simulated datasets
    Table 1.
    Table 2.
  Contribution analysis of key DecBin components
  Performance on experimental mock-community datasets
    Table 3.
  Strain-level resolution in a natural whey starter culture
Discussion and conclusion
  Key Points
Contributor Information
Associated Data
```
first paragraphs:
- Accurate metagenomic binning is essential for reconstructing microbial genomes, thereby facilitating the discovery of novel taxa, the identification of pathogens, and the characterization of antimicrobial resistance genes. Most existing methods are designed fo
- Metagenomic binning groups sequence fragments inferred to originate from the same genome into distinct bins, facilitating the reconstruction of microbial draft genomes. Accurate binning is critical for improving genome completeness and reducing contamination, 
- Conventional metagenomic binning is generally performed on contigs assembled from sequencing reads and relies on the assumption that sufficiently long contigs originating from the same genome exhibit similar sequence composition and abundance profiles. For exa
- Despite these advances in contig-level binning, the growing use of third-generation sequencing has created an increasing demand for methods that can directly bin raw long reads. Third-generation sequencing technologies generate reads reaching lengths of up to 

suspect paragraphs:
- none

dropped sample:
- [noise: keywords line] Keywords: long reads, metagenomic binning, variational autoencoder, Bayesian optimization, deep clus

## cancers / PMC13664292.pdf
**Interpretable CT-Based Radiomics for Prediction of High-Affinity Neoantigens Associated Immunogenic States in Advanced Hepatocellular Carcinoma Treated with TAC** (pdf, 5.8s, 2.92 MB, authors parsed: 5)

flags: lowercase_starts(1), noise:doi/url(2), table_captions_without_image(2>1)

warnings: ["Page 13: could not locate the body of 'Table S3: multivariable_cox; Table S4: U'; its text is left inline."]

dropped: {'running header/footer': 50, 'table body': 252, 'noise': 13, 'page-1 footnote': 5, 'front matter': 4, 'section': 41}

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
- Objectives: To develop and validate a CT radiomics-based machine learning model for the noninvasive prediction of HANS status in advanced HCC and to investigate the prognostic and genomic characteristics associated with HANS status. Materials and Methods: This
- Academic Editor: Samuel Samnick
- radiomic feature extraction. A radiomics model (HANS-Rad), a clinical model (HANS-Clin), and a combined model (HANS-RC) were developed using least absolute shrinkage and selection operator regression. Model performance was evaluated using receiver operating ch
- (median age, 54 years; IQR, 44–62 years; 90% men). The HANS-High group demonstrated longer overall survival compared with the HANS-Low group (median, 23.0 vs. 10.0 months; hazard ratio, 0.60; p = 0.026). The combined HANS-RC model achieved the best performance

suspect paragraphs:
- radiomic feature extraction. A radiomics model (HANS-Rad), a clinical model (HANS-Clin), and a combined model (HANS-RC) were developed using least absolute shrinkage and selection operator regression.
- Objectives: To develop and validate a CT radiomics-based machine learning model for the noninvasive prediction of HANS status in advanced HCC and to investigate the prognostic and genomic characterist
- radiomic feature extraction. A radiomics model (HANS-Rad), a clinical model (HANS-Clin), and a combined model (HANS-RC) were developed using least absolute shrinkage and selection operator regression.
- Patients with HCC who underwent TACE combined with antiangiogenic and ICIs were recruited between January 2015 and December 2023. Inclusion criteria were (1) age 18–75 years; (2) Barcelona Clinic Live

dropped sample:
- [noise: article tag] Article
- [noise: stray symbol] *
- [noise: correspondence] Correspondence: fwzhe@mail.sysu.edu.cn (W.F.); lijiap@mail.sysu.edu.cn (J.L.)
- [noise: stray symbol] †
- [noise: equal contributio] These authors contributed equally to this work.
- [noise: history line] Received: 8 September 2026
- [noise: history line] Revised: 23 September 2026
- [noise: history line] Accepted: 30 September 2026
- [noise: history line] Published: 6 October 2026
- [noise: copyright] Copyright: © 2026 by the authors.
- [page-1 footnote] Licensee MDPI, Basel, Switzerland.
- [page-1 footnote] This article is an open access article

## cell_rep / PMC13663908.pdf
**HHS Public Access** (pdf, 4.9s, 2.4 MB, authors parsed: 3)

flags: lowercase_starts(17), unterminated_paragraphs(19), noise:doi/url(13)

warnings: none

dropped: {'margin watermark': 1, 'running header/footer': 80, 'equation': 1, 'noise': 15, 'page-1 footnote': 1, 'front matter': 12, 'section': 122}

outline:
```
SUMMARY
  In brief
INTRODUCTION
RESULTS
      Probing the effects of phasic LC activation on taste-evoked GC activity
    PHASIC LC ACTIVATION BIDIRECTIONALLY MODULATES TASTE-EVOKED GC RESPONSES
      Phasic LC activation enhances GC palatability correlation without altering tastant separab
      Phasic LC activation reshapes GC population coding along a palatability axis
      Phasic LC activation stretches and rotates GC representations of mixture ratios
      Phasic LC activation modestly expands and rotates GC representations of sucrose concentrat
      Parsing tuning modulations underlying population-level effects of phasic LC activation
      LC-mediated gain modulation is structured and attribute specific
      Distinct contributions of scale-shift and flexible modulation to LC-induced transformation
      Tonic LC activation has limited impact on GC taste encoding
DISCUSSION
      Population-level effects of LC modulation
      Mechanisms of LC-induced neuronal effects
      Links to state-dependent modulation
      Open questions
      Limitations of the study
STAR★METHODS
    EXPERIMENTAL MODEL AND STUDY PARTICIPANT DETAILS
    METHOD DETAILS
      Fiber photometry recordings of photostimulation-evoked NE release: Five
    QUANTIFICATION AND STATISTICAL ANALYSIS
      Miniscope movie pre-processing and cell-identification: Miniscope recordings
      Identification of taste-discriminative and LC-modulated neurons: All analyses
      Principal component analysis (PCA) and LC-induced transformations: Because
RESOURCE AVAILABILITY
      Lead contact
      Materials availability
      Highlights
      GC palatability representation
      intensity
      KEY RESOURCES TABLE
      REAGENT or RESOURCE SOURCE
      IDENTIFIER
      REAGENT or RESOURCE SOURCE
      IDENTIFIER
```
first paragraphs:
- Noradrenergic neurons in the locus coeruleus (LC) shape sensory processing, yet how LC activity influences population taste coding remains unclear. Using optogenetic LC activation with miniscope imaging in the gustatory cortex (GC), we examined LC modulation o
- AUTHOR CONTRIBUTIONS Conceptualization, W.F. and N.R.S.; investigation, W.F. and P.T.; formal analysis, W.F.; data visualization, W.F., P.T., and N.R.S.; writing – original draft, W.F. and N.R.S.; writing – review and editing, W.F., P.T., and N.R.S.; project a
- DECLARATION OF INTERESTS The authors declare no competing interests.
- Fan et al. showed that phasic, but not tonic, locus coeruleus activation strengthens the relationship between cortical activity and palatability while reorganizing taste population geometry to increase separation between highly palatable and less palatable tas

suspect paragraphs:
- tastants, but the direction of modulation within each neuron was consistently enhancing or suppressive (Figure 2B). The proportions of LC-enhanced and LC-suppressed neurons were roughly balanced.
- elicited robust NE release that persisted throughout each stimulation block (Figures 5B and 5C).
- consistent with prior work showing that behavioral state differentially influences taste identity and palatability representations in GC. Notably, the palatability shift was driven mainly by aversive 
- stimulation pattern and may transiently prime GC before each influx of gustatory input. LC activity is also suppressed during consumption bouts, potentially stabilizing sensory representations by redu
- above the LC at coordinates AP: −5.45 mm, ML: −1.25 mm, DV: −3.85 mm relative to bregma, and secured to the skull using Metabond (S371, S398, and S396, Parkell), while leaving the GC craniotomy open.

dropped sample:
- [margin watermark] Author Manuscript
- [noise: licence] This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/)
- [page-1 footnote] DECLARATION OF GENERATIVE AI AND AI-ASSISTED TECHNOLOGIES IN THE WRITING PROCESS During the preparat
- [noise: stray symbol] •
- [noise: stray symbol] •
- [noise: stray symbol] •
- [noise: web ui] REFERENCES
- [noise: stray symbol] •
- [noise: stray symbol] •
- [noise: stray symbol] •
- [noise: stray symbol] •
- [noise: publisher url lin] https://imagej.net/software/imagej2/;

## cells / PMC13664011.html
**Dissecting Adult Peripheral Cellular Immunity to Bordetella pertussis: Innate-Associated IFN-γ Responses, Transient T-Cell Recall, and HLA-A*02-Associated CD8+ ** (html, 4.3s, 0.84 MB, authors parsed: 5)

flags: none

warnings: none

dropped: {'noise': 1, 'section': 15}

outline:
```
Abstract
  Highlights
  Abstract
1. Introduction
2. Materials and Methods
  2.1. Donors
    Table 1.
  2.2. HLA-A*02 Genotyping
  2.3. Isolation of Peripheral Blood Mononuclear Cells and CD4+ and CD8+ T Cells
  2.4. Standard and Modified IFN-γ Enzyme-Linked Immunospot (ELISpot) Assay
  2.5. Statistical Analysis
3. Results
  3.1. Rapid B. pertussis-Induced IFN-γ Responses in PBMCs Are Not Clearly Stratified by Pre
  3.2. Bacterial Innate-Biased Stimuli and Antigenic Recall Generate Distinct Total PBMC and
  3.3. Circulating Pattern-Defined T-Cell-Associated IFN-γ Responses Show Temporal Variabili
  3.4. B. pertussis-Reactive CD8+ IFN-γ Responses Are Associated with HLA-A*02
4. Discussion
5. Conclusions
Institutional Review Board Statement
Informed Consent Statement
Footnotes
Associated Data
```
first paragraphs:
- Bordetella pertussis elicits both innate and adaptive cellular responses, yet their relative contributions to peripheral interferon-γ (IFN-γ) measurements and the temporal dynamics of circulating T-cell reactivity in adults remain incompletely defined. B. pert
- Whooping cough (pertussis) is a respiratory infection caused by Bordetella pertussis and remains an important global public-health problem despite widespread vaccination [,,]. Although antibodies contribute to protection against symptomatic disease, cellular i
- Although B. pertussis has traditionally been regarded as a predominantly extracellular respiratory pathogen, this view has been refined by experimental evidence showing that the bacterium can enter and persist within host phagocytic cells, including human macr
- Because antigen recognition by CD8+ T cells depends on peptide presentation by HLA class I molecules, HLA genotype represents a potential source of inter-individual heterogeneity in detectable CD8+ T-cell responses. HLA-dependent differences in peptide present

suspect paragraphs:
- none

dropped sample:
- [noise: keywords line] Keywords: Bordetella pertussis, cellular immunity, IFN-γ, T-cell recall, CD4+ T cells, CD8+ T cells,

## comput_struct_biotec / PMC13594419.pdf
**A New Unsupervised Machine Learning Method for Metabarcoding Analysis Based on Selected Mock Community Data** (pdf, 5.1s, 1.74 MB, authors parsed: 0)

flags: no_abstract_heading, lowercase_starts(3), noise:doi/url(3), table_captions_without_image(2>1)

warnings: ["Page 8: could not locate the body of 'Table S22 .'; its text is left inline."]

dropped: {'running header/footer': 32, 'table body': 47, 'noise': 6, 'section': 116}

outline:
```
Hyung-Eun An1,2†, Min-Ho Mun3†, Jung-Il Kim, and Chang-Bae Kim1*
Introduction
Materials and Methods
  Dataset construction for developing new UML-based methods
  Preprocessing metabarcoding sequences
  Biological feature extraction for the UML-based methods
  UML model and performance evaluation metrics
  Taxonomic assignment and comparative analysis
  Comparison of the UML, OTU, and ASV methods
Results and Discussion
  Development of the UML-based methods
    Clustering analysis of 12S rRNA metabarcoding data
    Clustering analysis of COI metabarcoding data
    Clustering analysis of 18S rRNA metabarcoding data
    Evaluation of clustering performance based on biological features and algorithms
  Comparison of the UML-based methods, OTU clustering, and ASV analysis
    Comparison of relative abundance
    Comparison of detected species
  Further studies of UML-based metabarcoding analysis
Conclusion
```
first paragraphs:
- Citation: An H-E, Mun M-H, Kim J-I, Kim C-B. A New Unsupervised Machine Learning Method for Metabarcoding Analysis Based on
- Selected Mock Community Data.
- Comput. Struct. Biotechnol. J.
- 1Department of Biotechnology, Sangmyung University, Seoul 03016, Republic of Korea. Institute of

suspect paragraphs:
- org/10.34133/csbj.0221
- of Korea. Ocean Climate Response and Ecosystem Research Department, Korea Institute of Ocean Science and Technology, Busan 49111, Republic of Korea.
- identification and assessment of biodiversity across ecosystems. Conventional analytical methods, including operational taxonomic unit (OTU) clustering and amplicon sequence variant (ASV) analysis, ha
- Citation: An H-E, Mun M-H, Kim J-I, Kim C-B. A New Unsupervised Machine Learning Method for Metabarcoding Analysis Based on

dropped sample:
- [noise: article tag] RESEARCH ARTICLE
- [noise: equal contributio] *Address correspondence to: evodevo@smu.ac.kr †These authors contributed equally to this work.
- [noise: history line] Revised 24 August 2026 Accepted 24 August 2026 Published 22 September 2026
- [noise: copyright] Copyright © 2026 Hyung-Eun An et al. No claim to original U.S. Government Works. Distributed under a
- [noise: funding line] Funding: This work was supported by a grant from the National Institute of Biological Resources (NIB
- [noise: web ui] References

## elife / PMC13652542.pdf
**Role of desolvation on biomolecular liquid–liquid phase separation** (pdf, 10.6s, 4.49 MB, authors parsed: 4)

flags: lowercase_starts(29), unterminated_paragraphs(26), noise:doi/url(1), table_captions_without_image(4>3), reference_like_paragraphs(5)

warnings: ["Page 15: could not locate the body of 'Table 1. Global desolvation coefficients'; its text is left inline.", "Page 21: could not locate the body of 'Table 1.'; its text is left inline."]

dropped: {'margin watermark': 2, 'running header/footer': 134, 'figure text': 98, 'equation': 50, 'sideways table text': 3, 'table body': 109, 'noise': 5, 'page-1 footnote': 4, 'caption placeholder': 2, 'front matter': 5, 'section': 37}

outline:
```
Abstract
      Preprint posted
      Sent for Review
      Reviewed preprint v1
      Reviewed preprint v2
      Version of Record
Introduction
    Burke et al., 2015; Biamonti and Vourc'h, 2010; Riback et al., 2017), cellular signaling (
    Dignon et al., 2018b; Regy et al., 2021; Dannenhoffer-Lafage and Best, 2021), and Mpipi, w
    2009; Chen and Chan, 2014; Zhang and Chan, 2010; Karanicolas and Brooks, 2002; Gasic and
    folding cooperativity (Liu and Chan, 2005; Ferguson et al., 2009; Chen and Chan, 2014; Zha
Results
  Effective representation of desolvation effects in coarse-grained models
  Thermodynamic impact of desolvation on the phase diagram
  Conformational modulation by desolvation in dense and dilute phases
  Dynamic consequences of desolvation in phase separation
      Non-Equilibrium
  Desolvation-modulated kinetic arrest of coarsening dynamics
    and Hilliard, 1958).
    sion (Doi and Edwards, 1988).
  Parameterization of desolvation model for IDPs
      Parameters HPS model CALVADOS2 model
Discussion
    relaxation (Tejedor et al., 2023; Biswas and Potoyan, 2024).
Methods
  All-atom MD simulations
  Coarse-grained simulations
  Hydrophobicity scale model
  Simulation framework
  Critical temperature
  Bead-level second virial coefficient
  Temperature normalization of the generalized diffusion coefficient
  Calculation of normalized density variance
  Desolvation parameters
Additional files
    Supplementary files
```
first paragraphs:
- Biomolecular condensates play essential roles in cellular organization and are impli-
- wfli@nju.edu.cn (WL); wangwei@nju.edu.cn (WW)
- cated in diverse pathological processes. Their formation is driven by liquid–liquid phase separation (LLPS), a process that requires coordinated multistep desolvation of biomolecular chains and
- Competing interest: The authors

suspect paragraphs:
- wfli@nju.edu.cn (WL); wangwei@nju.edu.cn (WW)
- cated in diverse pathological processes. Their formation is driven by liquid–liquid phase separation (LLPS), a process that requires coordinated multistep desolvation of biomolecular chains and
- multivalent inter-chain interactions. Although coarse-grained (CG) models with implicit solvent are
- declare that no competing
- widely used to probe LLPS thermodynamics and kinetics, they typically neglect water-mediated

dropped sample:
- [margin watermark] Energy
- [margin watermark] Simulation Time Evolution
- [noise: funding line] Funding: See page 21
- [noise: copyright] Copyright Zhang et al. This article is distributed under the terms of the Creative Commons
- [page-1 footnote] permits unrestricted use and
- [page-1 footnote] redistribution provided that the
- [page-1 footnote] original author and source are
- [page-1 footnote] credited.
- [noise: stray symbol] )
- [noise: stray symbol] )
- [noise: web ui] References
- [caption placeholder] Figure 3 continued on next page

## front_immunol / PMC13685023.pdf
**A crosstalk between the immune system and obstructive sleep apnea** (pdf, 12.8s, 4.87 MB, authors parsed: 1)

flags: no_abstract_heading, lowercase_starts(27), unterminated_paragraphs(15), huge_paragraph

warnings: ["Page 19: could not locate the body of 'TABLE 1 Major immune and inflammatory ma'; its text is left inline.", "Page 20: could not locate the body of 'TABLE 1 Continued'; its text is left inline.", "Page 21: could not locate the body of 'TABLE 1 Continued'; its text is left inline.", "Page 22: could not locate the body of 'TABLE 1 Continued'; its text is left inline."]

dropped: {'running header/footer': 153, 'figure text': 695, 'sideways table text': 20, 'noise': 8, 'section': 248}

outline:
```
  Sarfraz Ahmed, David Gozal, Alip Borthakur 1
  and Abdelnaby Khalyfa 1*
1 Introduction
  1.1 Literature search methodology
2 Sleep, OSA and immune directionality
3 Interplay between OSA and the immune system
4 Innate and adaptive immune responses in OSA
  4.1 Leukocytes and leukocyte subsets
    4.1.1 Neutrophils, eosinophils and basophils
    4.1.2 Monocytes
    4.1.3 Dendritic cells and macrophages
    4.1.4 Natural killer and natural killer T cells
    4.1.5 B cells
    4.1.6 T cells
5 Humoral immunity in OSA
  5.1 Immunoglobulins (IgA, IgG and IgM)
    5.1.1 Evidence from experimental sleep deprivation models
    5.1.2 Patients with OSA
  5.2 Complement system in OSA
    5.2.1 Evidence from sleep deprivation models
    5.2.2 Direct evidence from patients with OSA
  5.3 Cell adhesion molecules and endothelial activation
6 OSA and inflammation
  6.1 Low grade inflammation associated with OSA
7 Cytokines and cytokine production in OSA
  7.1 TNF-a
  7.11 ILs 35 and 37
8 Other cytokines and signaling pathways
  8.1 PD-1/PD-L1 immune checkpoints
  8.2 NF-kB
  8.3 Toll-like receptor signaling
  8.4 NLRP3 inflammasome
9 Gut microbiota and immune dysregulation in OSA
10 Conclusions and future directions
  10.1 Conclusions
  10.2 Future directions
Generative AI statement
```
first paragraphs:
- TYPE Review PUBLISHED 07 October 2026 DOI 10.3389/fimmu.2026.1963127
- OPEN ACCESS
- EDITED BY
- Namdev More, Cedars Sinai Medical Center, United States

suspect paragraphs:
- khalyfa@marshall.edu
- tion during sleep. Its hallmark pathophysiological features, intermittent hypoxia (IH) and sleep fragmentation (SF), trigger cellular and molecular responses that disrupt immune homeostasis. Recurrent
- the NLRP3 inflammasome, contributing to sustained inflammatory signaling, en-
- dothelial dysfunction, and alterations in circulating and tissue-resident immune
- the immune system and obstructive

dropped sample:
- [noise: correspondence] *CORRESPONDENCE
- [noise: history line] RECEIVED 10 August 2026
- [noise: history line] REVISED 09 September 2026 ACCEPTED 11 September 2026
- [noise: history line] PUBLISHED 07 October 2026
- [noise: copyright] COPYRIGHT
- [noise: copyright] © 2026 Ahmed, Gozal, Borthakur and
- [noise: licence] distributed under the terms of the Creative Commons Attribution License
- [noise: web ui] References

## front_pharmacol / PMC13683642.pdf
**A mixture of pomegranate peels and propolis extracts reduces inflammation associated with rheumatoid arthritis in vivo** (pdf, 11.7s, 2.55 MB, authors parsed: 0)

flags: no_abstract_heading, lowercase_starts(32), unterminated_paragraphs(14), noise:history(2), table_captions_without_image(2>0)

warnings: ["Page 4: could not locate the body of 'TABLE 1 Scoring system for subjective ev'; its text is left inline.", "Page 7: could not locate the body of 'TABLE 2 Chromatographic (tR = retention '; its text is left inline.", "Page 8: could not locate the body of 'TABLE 2 Continued'; its text is left inline.", "Page 9: could not locate the body of 'TABLE 2 Continued'; its text is left inline."]

dropped: {'running header/footer': 83, 'figure text': 473, 'noise': 5, 'page-1 footnote': 2, 'section': 65}

outline:
```
  Alessandra Braca, Fabrizio Dal Piaz*, Marinella De Leo* and
  Nunziatina De Tommasi1
1 Introduction
2 Materials and methods
  2.1 Chemicals
  2.2 Materials
  2.3 Extraction and design of preparations based on combined extracts
  2.4 High resolution LC-ESI-MS analyses
  2.5 Cell culture
  2.6 Cellular viability assay
  2.9 In vivo study in collagen-induced arthritis (CIA) mouse model
  2.10 Treatment of CIA-induced mice with Pp1:2
  2.11 Histology
  2.12 Immunofluorescence
  2.13 Metabolite analyses in mouse serum samples
  2.14 Statistical analysis
3 Results
  3.3 Pp1:2 inhibits M1 macrophage polarization in human THP-1 cells
  3.5 Pp1:2 reduces RA related inflammation and symptoms of the pathology in vivo
  3.7 Study limitation
4 Discussion
Generative AI statement
```
first paragraphs:
- TYPE Original Research PUBLISHED 07 October 2026 DOI 10.3389/fphar.2026.1910652
- OPEN ACCESS
- EDITED BY
- Michael Heinrich,

suspect paragraphs:
- fdalpiaz@unisa.it Marinella De Leo, 1Department of Pharmacy, University of Salerno, Fisciano, Italy, Department of Medicine, Surgery and marinella.deleo@unipi.it Dentistry, University of Salerno, Baro
- infiltration of immune and inflammatory cells into the synovial membranes, which
- often leads to severe damage to cartilage and bone. In spite of their efficacy, drug-
- based therapies produce severe side effects. Therefore, there remains an unmet
- need for non-pharmacological treatments with a low toxicity profile and limited

dropped sample:
- [noise: correspondence] *CORRESPONDENCE
- [noise: copyright] COPYRIGHT
- [noise: copyright] © 2026 Bellone, Abate, Di Pietro, Parisi,
- [noise: licence] the terms of the Creative Commons
- [page-1 footnote] KEYWORDS
- [page-1 footnote] cytokines, immunohistochemical analysis, in vivo assays, inflammation, M1 polarization, pomegranate,
- [noise: web ui] References

## genome_biol / PMC13685256.html
**Europe PMC** (html, 0.2s, 0.0 MB, authors parsed: 0)

flags: no_abstract_heading, few_words(37), no_headings

warnings: ['Article body located by text-density heuristic; verify the output.']

dropped: {}

outline:
```

```
first paragraphs:
- Europe PMC requires Javascript to function effectively.
- Either your web browser doesn't support Javascript or it is currently turned off. In the latter case, please turn on Javascript support in your web browser and reload this page.

suspect paragraphs:
- none

dropped sample:
- none

## heliyon / PMC12435017.pdf
**Corrigendum to "Adjustable tongue vane for improving the energy performance of a submersible single-channel pump for wastewater treatment" [Heliyon Volume 11, I** (pdf, 0.3s, 0.07 MB, authors parsed: 1)

flags: no_abstract_heading, few_words(192), many_short_paragraphs(2/7), lowercase_starts(2), noise:doi/url(1)

warnings: none

dropped: {'noise': 3, 'section': 6}

outline:
```
Heliyon
    Corrigendum
  Duc-Anh Nguyen a,b, Kexin Wu c, Xiaojun Li c, Gyeong Sung Kim d, JinHyuk Kim a,b,d,*
      Introduction
      Introduction
```
first paragraphs:
- Heliyon 11 (2025) e43589
- Contents lists available at ScienceDirect
- journal homepage: www.cell.com/heliyon
- a Convergence Manufacturing System Engineering (Green Process and Energy System Engineering), University of Science & Technology, Daejeon, 34113, South Korea b Carbon Neutral Technology R&D Department, Korea Institute of Industrial Technology, Cheonan, 31056, 

suspect paragraphs:
- journal homepage: www.cell.com/heliyon
- a Convergence Manufacturing System Engineering (Green Process and Energy System Engineering), University of Science & Technology, Daejeon, 34113, South Korea b Carbon Neutral Technology R&D Department
- a Convergence Manufacturing System Engineering (Green Process and Energy System Engineering), University of Science & Technology, Daejeon, 34113, South Korea b Carbon Neutral Technology R&D Department

dropped sample:
- [noise: publisher url lin] https://doi.org/10.1016/j.heliyon.2025.e43589
- [noise: history line] Available online 4 July 2025 2405-8440/© 2025 The Author(s).
- [noise: licence] This is an open access article under the CC BY-NC license ( http://creativecommons.org/licenses/by-n

## ijms / PMC13688135.pdf
**RETRACTED: Abou-ElNaga et al. Novel Nano-Therapeutic Approach Actively Targets Human Ovarian Cancer Stem Cells After Xenograft into Nude Mice. Int. J. Mol. Sci.** (pdf, 0.2s, 0.0 MB, authors parsed: 6)

flags: no_abstract_heading, few_words(426), no_headings, unterminated_paragraphs(4)

warnings: none

dropped: {'running header/footer': 1, 'noise': 8, 'page-1 footnote': 6}

outline:
```

```
first paragraphs:
- Retraction
- , Ibrahim M. El-Sherbiny 2, Hassan Abd-ElGhaffar, Amoura Abou-ElNaga, Ghada Mutawa 1 Ahmed A. Allam, Jamaan Ajarem and Shaker A. Mousa *
- 1 Zoology Department, Faculty of Sciences, Mansoura University, Mansoura 35516, Egypt; dramabouelnaga@yahoo.com (A.A.-E.); ghada.adel.mutawa@gmail.com (G.M.) 2 Center for Materials Science, Zewail City of Science and Technology, Cairo 12588, Egypt; ielsherbiny
- NY 12144, USA

suspect paragraphs:
- , Ibrahim M. El-Sherbiny 2, Hassan Abd-ElGhaffar, Amoura Abou-ElNaga, Ghada Mutawa 1 Ahmed A. Allam, Jamaan Ajarem and Shaker A. Mousa *
- 1 Zoology Department, Faculty of Sciences, Mansoura University, Mansoura 35516, Egypt; dramabouelnaga@yahoo.com (A.A.-E.); ghada.adel.mutawa@gmail.com (G.M.) 2 Center for Materials Science, Zewail Cit
- 1. Abou-ElNaga, A.; Mutawa, G.; El-Sherbiny, I.M.; Abd-ElGhaffar, H.; Allam, A.A.; Ajarem, J.; Mousa, S.A. RETRACTED: Novel
- 2. Abou-ElNaga, A.; Mutawa, G.; El-Sherbiny, I.M.; Abd-ElGhaffar, H.; Allam, A.A.; Ajarem, J.; Mousa, S.A. Correction: Abou-

dropped sample:
- [noise: stray symbol] *
- [noise: correspondence] Correspondence: shaker.mousa@acphs.edu
- [noise: history line] Received: 28 September 2026
- [noise: history line] Accepted: 9 October 2026
- [noise: history line] Published: 20 October 2026
- [noise: copyright] Copyright: © 2026 by the authors.
- [page-1 footnote] Licensee MDPI, Basel, Switzerland.
- [page-1 footnote] This article is an open access article
- [page-1 footnote] distributed under the terms and
- [page-1 footnote] conditions of the Creative Commons
- [page-1 footnote] Attribution (CC BY) license.
- [page-1 footnote] Int. J. Mol. Sci. 2026, 27, 9309 https://doi.org/10.3390/ijms27209309

## iscience / PMC13691245.html
**Bridging soil resistome and clinical inference: A four-tier evidentiary framework** (html, 2.9s, 1.36 MB, authors parsed: 4)

flags: huge_paragraph, noise:doi/url(2)

warnings: none

dropped: {'noise': 1, 'section': 8}

outline:
```
Summary
Graphical abstract
Glossary
  Antimicrobial resistance
  Antibiotic resistant bacteria (ARB)
  Antibiotic resistance gene (ARG)
  Antibiotic resistance gene-mobile genetic element (ARG-MGE) linkage
  Cross-compartment tracking
  ESKAPEE pathogens
  Functional metagenomics
  Homology-based annotation
  Metagenomics
  Metaproteomics
  Mobile genetic element (MGE)
  One Health
  Quantitative polymerase chain reaction (qPCR)
  Resistome
  Scopus
Review
  Introduction
  To date environmental AMR evidence frameworks
  A four-tier evidentiary framework
  Current evidentiary gap in soil-resistome research
  Bridging environmental ARG detection and clinical inference
  Concluding remarks
Methods
```
first paragraphs:
- Soils support a varied range of microbial communities and are important repositories of antimicrobial resistance genes. Sequence-based techniques, such as quantitative polymerase chain reaction and shotgun metagenomics, have substantially aided soil-resistome 
- Soil science; Microbiology; Soil biology
- The ability of microorganisms to survive antimicrobial exposure. In this review, antimicrobial resistance (AMR) is discussed as an environmental and clinical problem, however environmental detection alone is not treated as evidence of clinical burden.
- A bacterium capable of growing at antibiotic concentrations that inhibit the growth of susceptible members of the same species. Resistance may result from intrinsic properties, resistance-conferring mutations, or acquired antimicrobial resistance genes (ARGs).

suspect paragraphs:
- Soil is one of the most microbially rich and physicochemically varied habitats on Earth and contains numerous antimicrobial resistance genes (ARGs) (see glossary) and antimicrobial resistance (AMR) de
- Tier 2 represents functional/activity-based evidence. At this tier, evidence moves beyond DNA-level detection by showing that a resistance determinant is active under defined conditions, either throug

dropped sample:
- [noise: keywords line] Keywords: antimicrobial resistance, soil resistome, one health, clinical relevance, evidence tiers, 

## j_chem_inf_model / PMC13663857.html
**Europe PMC** (html, 0.2s, 0.0 MB, authors parsed: 0)

flags: no_abstract_heading, few_words(37), no_headings

warnings: ['Article body located by text-density heuristic; verify the output.']

dropped: {}

outline:
```

```
first paragraphs:
- Europe PMC requires Javascript to function effectively.
- Either your web browser doesn't support Javascript or it is currently turned off. In the latter case, please turn on Javascript support in your web browser and reload this page.

suspect paragraphs:
- none

dropped sample:
- none

## j_cheminform / PMC13563705.pdf
**for the calculation of local features for atoms and bonds in molecules** (pdf, 4.8s, 2.33 MB, authors parsed: 4)

flags: lowercase_starts(1), noise:doi/url(1)

warnings: none

dropped: {'running header/footer': 27, 'figure text': 3, 'noise': 5, 'page-1 footnote': 1, 'front matter': 3, 'section': 119}

outline:
```
Abstract
  Scientific contribution
Introduction
Results and discussion
    General overview
    Dependencies and from-scratch feature implementations
    Individual functionalities
    Applications Runtime analysis
    Amine featurization workflow
Conclusion
```
first paragraphs:
- Data-driven chemistry relies on robust, efficient, and reproducible pipelines for generating digital molecular representations. While comprehensive software for global molecular descriptors is widely available, the calculation of local atom and bond features r
- This work introduces a Python software package denoted BONAFIDE, which facilitates the calculation of descriptors for atoms and bonds in molecules. By providing a unified interface that bridges diverse cheminformatics and quantum chemistry tools, this package 
- Keywords Atom and bond descriptors, Local features, Reactivity prediction, Open-source software
- Lukas M. Sigmund lukas.sigmund@astrazeneca.com Full list of author information is available at the end of the article

suspect paragraphs:
- molecule was considered, and electronic structure calculations (B3LYP/6-31G* with Gaussian) were conducted independently to decouple the computational cost of structure optimization and single-point e
- Next, featurization was performed for the respective 3D molecular structures. Both the 2D and 3D descriptors were calculated to cover the entire feature space implemented within BONAFIDE. One conforme

dropped sample:
- [noise: publisher url lin] https://doi.org/10.1186/s13321-026-01283-6
- [noise: equal contributio] †Michele Assante and Matthew Ball have contributed equally to this work.
- [noise: correspondence] *Correspondence:
- [page-1 footnote] © The Author(s) 2026. Open Access This article is licensed under a Creative Commons Attribution-NonC
- [noise: history line] Received: 7 April 2026 Accepted: 2 August 2026
- [noise: web ui] References
- [front matter] Journal of Cheminformatics
- [front matter] [figure image]
- [front matter] Lukas M. Sigmund1* , Michele Assante2,3† , Matthew Ball1,4† and Mikhail Kabeshov

## j_med_chem / PMC13576395.pdf
**Chemical Stabilization and Transformation of Schiff Base Scaffold: A Path toward Superior Platinum-Based Anti-Cancer Stem Cell Drugs** (pdf, 14.2s, 6.24 MB, authors parsed: 6)

flags: lowercase_starts(10), unterminated_paragraphs(13), noise:doi/url(4), table_captions_without_image(7>6)

warnings: ["Page 6: could not locate the body of 'Table 2. Particle Size and ζ-Potential o'; its text is left inline."]

dropped: {'running header/footer': 141, 'figure text': 8, 'equation': 1, 'page-1 metadata box': 1, 'table body': 185, 'noise': 7, 'page-1 footnote': 1, 'front matter': 5, 'section': 120, 'characterization data': 13}

outline:
```
Abstract
INTRODUCTION
RESULTS AND DISCUSSION
    Synthesis, Transformation, and Characterization of Platinum Complexes
    Single-Crystal X-Ray Diffraction Analysis
      and b) [PtCl(L1)]Cl·H2O.
    Stability of the Compounds in Aqueous Solution
    Ligands L1 and L1H
    Complexes [PtCl(L1H)]Cl and [PtCl(L1)]
  [PtCl(L1H)]Cl in Water at Different Times
    Cytotoxicity and Cellular Uptake
  Cells after 3 h of 20 μM Treatment with the Complexesa
    Evaluation of DNA-Binding Potential of the Platinum Compounds
    BSA Interaction Fluorescence Assays
    Cell Cycle, DNA Damage Response, and Apoptosis
    Mitochondrial Dysfunction and ROS Accumulation
  Red. N = 3
    Effect on 3D Models: CSC-Enriched Tumorospheres
    Transcriptomic Profiling and Functional Studies
CONCLUSIONS
EXPERIMENTAL SECTION
    Materials and Methods
    Synthesis and Characterization
      General Method for Ligands L2H to L4H Synthesis. In the first
    Stability Studies
    Cell Culture
    Cell Viability
    Cellular Uptake and Distribution by ICP-MS
    Fluorescence Binding Studies with Bovine Serum Albumin (BSA)
    Electrophoresis Assays
    Viscosity Assays
    Clonogenic Assay
    Tumor Sphere Assay
    Cell Cycle Analysis
    ROS and Mitochondrial Assays
    Western Blotting
    RNA Sequencing and Bioinformatic Analysis
    Cell Migration and Invasion Assay
    Statistics and Reproducibility
```
first paragraphs:
- The clinical application of platinum-based anticancer agents is limited by poor aqueous stability, low solubility, and dose-limiting toxicities. Here, we report two Pt(II) complexes based on a Schiff base ligand and its reduced imine derivative, designed to ov
- Gastric cancer (GC) remains one of the leading causes of cancer-related mortality worldwide, and its incidence is projected to continue to rise in the coming years. The clinical management of GC frequently relies on tumor resection, followed by FOLFOX-based ch
- Platinum-based drugs are used in clinical practice. Cisplatin remains one of the most established and extensively studied agents, continuing to be a cornerstone in the treatment of several solid malignancies. Currently, it is employed in combination regimens f
- Rationally designing the ligand environment is a key strategy for tuning the biological activity of platinum complexes, as ligands critically influence the stability, solubility, reactivity, and activation under physiological conditions. The incorporation of s

suspect paragraphs:
- shift relative to the free ligand, confirming its coordination to the platinum center. A significant change was observed for the CH2−signal, which was a sharp singlet at 4.22 ppm in the spectra of the
- by C−H···π interactions, and a short Pt···Pt contact of 3.353 Å suggests the presence of weak metallophilic interactions, often observed in d8 closed-shell Pt(II) systems.
- nuclear accumulation supports a distinct intracellular distribution pattern and may contribute to the enhanced biological activity observed for [PtCl(L1H)]Cl. Nonetheless, both complexes showed substa
- phase, [PtCl(L1)] and [PtCl(L1H)]Cl exhibited an accumufollowing treatment with the complexes and the ligands in MKN45 cells. While cisplatin produced a strong arrest in the S lation of cells in G2/M,
- perturbations. None of the ligands affected the cell cycle distribution at the concentrations studied (Figure 10, Figure S55 and Table S2).

dropped sample:
- [page-1 metadata box] [vector box near page foot]
- [noise: licence] This article is licensed under CC-BY 4.0
- [noise: article tag] Article
- [noise: citation banner] ACCESS
- [noise: citation banner] Metrics & More
- [noise: citation banner] Read Online
- [noise: supporting info p] sı
- [page-1 footnote] © 2026 The Authors. Published by American Chemical Society
- [noise: stray symbol] *
- [front matter] [figure image]
- [front matter] Cynthia Sinaí Novoa-Ramirez,△ Jorge Melones Herrero,△ Susana Priego Gutierrez, Leticia Cubo Martín, 
- [front matter] [formula image]

## molecules / PMC13666728.html
**Checking your browser - reCAPTCHA** (html, 0.1s, 0.0 MB, authors parsed: 0)

flags: no_abstract_heading, few_words(17), no_headings

warnings: ['Could not locate an article body; using the whole page.']

dropped: {}

outline:
```

```
first paragraphs:
- Checking your browser before accessing pmc.ncbi.nlm.nih.gov...
- Click here if you are not automatically redirected after 5 seconds.

suspect paragraphs:
- none

dropped sample:
- none

## nat_commun / PMC13687067.pdf
**Strain-engineered fabrication of high-density aligned graphene-based nanoscrolls via UV-tunable adhesive tapes** (pdf, 10.9s, 2.61 MB, authors parsed: 1)

flags: no_abstract_heading, lowercase_starts(13), unterminated_paragraphs(8), figure_captions_without_image(8>6)

warnings: none

dropped: {'margin watermark': 6, 'running header/footer': 55, 'figure text': 261, 'equation': 1, 'sideways table text': 8, 'noise': 8, 'section': 77}

outline:
```
Results
Discussion
Methods
```
first paragraphs:
- Maki Nakatani, Akari Sudo, Pablo Solís-Fernández 1, Haiming Sun
- 3,
- 5,
- 3, Takahiro Yamamoto & Hiroki Ago Rika Matsumoto, Kazu Suenaga

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

## nucleic_acids_res / PMC13691376.html
**Emerging roles of RIF1 in mitosis** (html, 7.2s, 1.79 MB, authors parsed: 4)

flags: huge_paragraph

warnings: none

dropped: {'section': 13}

outline:
```
Abstract
Graphical Abstract
Introduction
  Discovery of RIF1
  RIF1 as a PP1 adaptor
Structural elements and conservation of the RIF1 PP1-binding motif
  Conservation and structural organization of RIF1 across evolution
RIF1 functions in mitosis
  Introduction to mitosis
  RIF1 and UFB resolution during anaphase
    The nature of anaphase UFBs
    RIF1-mediated resolution of UFBs in anaphase
  RIF1-mediated regulation of abscission timing
  RIF1–PP1 binding and catalytic activity is restrained in early mitosis by multiple kinase 
  RIF1 and cancer: potential links to mitosis and genomic instability?
Conclusion
Contributor Information
Associated Data
```
first paragraphs:
- Faithful chromosome segregation during cell division requires precise coordination of kinase– and phosphatase–driven signaling pathways. Defects in this balance can cause chromosome missegregation and cytokinesis failure, resulting in genomic instability. Rap1
- RAP1-interacting factor 1 (RIF1) was first identified in 1992 in budding yeast for its role in restricting telomere lengthening through interaction with repressor/activator protein 1 (Rap1). Rap1 binds telomeric repeats to negatively regulate telomere lengthen
- The mechanistic link connecting the functions of RIF1 in both replication timing and DSB repair pathway choice lies in its function as an adaptor for PP1 [,,]. PP1 is a ubiquitous serine/threonine phosphatase whose substrate specificity and subcellular localiz
- While RIF1 orthologs vary widely in size and sequence across eukaryotes, several key structural features are conserved. RIF1 consists of three distinct domains: an N-terminal domain (NTD), a C-terminal domain (CTD), and between, a long intrinsically disordered

suspect paragraphs:
- none

dropped sample:
- none

## plos_comp_biol / PMC13649120.html
**Checking your browser - reCAPTCHA** (html, 0.1s, 0.0 MB, authors parsed: 0)

flags: no_abstract_heading, few_words(17), no_headings

warnings: ['Could not locate an article body; using the whole page.']

dropped: {}

outline:
```

```
first paragraphs:
- Checking your browser before accessing pmc.ncbi.nlm.nih.gov...
- Click here if you are not automatically redirected after 5 seconds.

suspect paragraphs:
- none

dropped sample:
- none

## plos_one / PMC13693877.pdf
**The applications of artificial intelligence in liver transplantation: A comprehensive scoping review** (pdf, 4.7s, 2.63 MB, authors parsed: 11)

flags: lowercase_starts(33), unterminated_paragraphs(6), noise:doi/url(5)

warnings: none

dropped: {'running header/footer': 52, 'table body': 25, 'noise': 11, 'page-1 footnote': 1, 'front matter': 6, 'section': 124}

outline:
```
Abstract
  Introduction
    Background to artificial intelligence and its evolution
    Historically, classical statistical models and rule-based expert systems
  Methods
    Eligibility criteria
    Search strategy
    Data items and charting process
    Synthesis of results
    Bibliometric analysis
  Results
    Search results
    Bibliometric analysis
    Study design
    Overall themes
  Pre-transplant
    Transplant assessment
    Allocation policy
    Image segmentation
  Organ retrieval
  Intra-operative period
    Blood transfusion requirements
    Intra-operative identification of anatomical structures
  Post-operative period: Short-term outcomes
    Acute Kidney Injury
    Sepsis and infection
    Early graft dysfunction and rejection
    Early mortality
    Miscellaneous
  Post-operative period: Long-term outcomes
    Long-term survival
    Graft failure and fibrosis
    Tacrolimus dosing
    Hepatocellular carcinoma (HCC) recurrence and mortality
    Other long-term outcomes
  Natural language processing
  Discussion
    Evidence gaps
    Ethical, governance, and workflow integration challenges
    Recommendations for future research
```
first paragraphs:
- OPEN ACCESS
- Citation: Borakati A, Agilinko J, Wu J, Hunter S,
- Liver transplantation (LT) is a complex surgical intervention, with intricate decision-
- Alhaq A, Froghi F, et al. (2026) The applications

suspect paragraphs:
- making and risks at all stages before, during and after the procedure itself. Artificial
- of artificial intelligence in liver transplantation:
- intelligence (AI) may assist the process but has seen limited use. This scoping review
- assessed primary articles reporting on clinical AI in LT in MEDLINE and Embase from
- journal.pone.0361120

dropped sample:
- [noise: article tag] RESEARCH ARTICLE
- [noise: history line] Received: March 26, 2026
- [noise: history line] Accepted: October 6, 2026
- [noise: history line] Published: October 23, 2026
- [noise: copyright] Copyright: © 2026 Borakati et al. This is an open access article distributed under the terms
- [noise: licence] of the Creative Commons Attribution License,
- [page-1 footnote] which permits unrestricted use, distribution,
- [noise: funding line] Funding: Aditya Borakati is supported by the UK Engineering and Physical Sciences
- [noise: supporting info p] Supporting information
- [noise: web ui] References
- [noise: publisher url lin] https://doi.org/10.1016/j.jclinepi.2024.111572
- [noise: publisher url lin] https://doi.org/10.17605/OSF.IO/TUVRZ

## rsc_adv / PMC13684429.pdf
**RSC Advances** (pdf, 6.8s, 3.37 MB, authors parsed: 1)

flags: no_abstract_heading, lowercase_starts(5), unterminated_paragraphs(7)

warnings: none

dropped: {'running header/footer': 39, 'equation': 1, 'noise': 5, 'page-1 footnote': 2, 'section': 12}

outline:
```
PAPER
  Facile synthesis of a cube-shaped MnO@C composite as a long-life anode material for
  lithium-ion batteries
1. Introduction
2. Experimental section
  2.1. Preparation of the MnCO3@C precursor
  2.2. Preparation of the MnO@C composite
  2.3. Material characterization
  2.4. Electrochemical performance measurements
3. Results and discussion
4. Conclusions
```
first paragraphs:
- Zhenyuan Zhang,a Jiayu Liu,a Yuanhao Ma, a Beibei Pan,a Jiawei Zhao,a Hong Jiang,b Qiuju Zheng,a Yuebo Hu *a and Yang Shen*a
- Manganese oxides are promising anode materials for lithium-ion batteries due to their high specific capacities and excellent chemical stability. However, the considerable volume expansion/contraction that occurs during their charge/discharge process limits the
- 1000 cycles, with negligible capacity fading. Carbon compositing improved the electrical conductivity and structural stability. The numerous channels within the MnO secondary particles facilitated Li+
- DOI: 10.1039/d6ra05506k

suspect paragraphs:
- diffusion. This strategy can provide guidance for preparing other high-performance anode materials for lithium-ion batteries.
- rsc.li/rsc-advances
- uniform carbon on the MnO surface, which enhances the electrical conductivity of MnO and signicantly improves its capacity. Furthermore, the carbon-containing components on the sample surface effecti
- at a scan rate of 1.0 mV s−1 (c), and contribution ratio of capacitive- and diffusion-controlled capacities at different scan rates (d).
- diffusive contribution (k1v1/2) and capacitive contribution (k2v) to the total reaction current (i) could be quantied according to the following equations:31 i = k1v1/2 + k2v (3)

dropped sample:
- [noise: licence] Published on 21 October 2026 Licensed under CC-BY-NC 4.0
- [noise: citation banner] Cite this: DOI: 10.1039/d6ra05506k
- [noise: history line] Received 22nd June 2026
- [noise: history line] Accepted 21st September 2026
- [page-1 footnote] aShandong Key Laboratory of Advanced Glass Manufacturing and Technology, School of Materials Science
- [page-1 footnote] bState Key Laboratory of Tropic Ocean Engineering Materials and Materials Evaluation, Hainan Univers
- [noise: web ui] References
