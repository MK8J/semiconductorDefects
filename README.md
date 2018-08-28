# Semiconductor Defects

This is an attempt at creating a collection of defect parameters of
semiconductors in plain text. The idea is that such a plain text file
should reduce allow for everyone to be able to access the information
for now and into the future.

The information currently stored in the repository is currently limited
to Shockley Read Hall parameterization, which allow calculation of how
electron and holes electronically interact with the defect.

## Referencing

If you use this, please reference our work:

M. Juhl et al., “AN OPEN SOURCE BASED REPOSITORY FOR DEFECTS IN
SILICON,” presented at the 7th World Conference on Photovoltaic Energy
Conversion, Hawaii, 2018.

## Contributing

There are two ways to contribute.

1.  Fork this repository, make your changes and push it back
2.  Fill in this [csv file](example.csv) and email it to
    mattias.juhl@gmail.com. For details of what each category means
    please see this readme.
3.  Email the papers to mattias.juhl@gmail.com

## Shockley Read Hall parameterization

The Shockley Read Hall parameterisation assumes that there is a level
within the forbidden region in a semiconductor’s through which electrons
and holes can pass. A schematic of such a defect is shown in Figure
[1](#fig:SRH).

![Figure 1: Shockley Read Hall description of a single defect level.
Here E<sub>c</sub> is the condition band edge, E<sub>v</sub> is the
valance bade edge, E<sub>i</sub> is the intrinsic level of the
semiconductor, E<sub>d</sub> is the energy level of the defect, G is the
generation of free carriers, k is Boltzmann constant, and T is the
temperature. The remaining terms are specific for electrons and holes as
depicted by their subscripts being e and h, respectively. These
remaining terms are: c is a capture rate of particles, e is an emission
rate of particles, σ is the capture cross section, n is the number of
free particles (electrons in the conduction band or holes in the valance
band), N<sub>d</sub> is the number of defects filled with a spectific
particle](./images/Defect.png)

*Shockley Read Hall description of a single defect level. Here
E<sub>c</sub> is the condition band edge, E<sub>v</sub> is the valance
bade edge, E<sub>i</sub> is the intrinsic level of the semiconductor,
E<sub>d</sub> is the energy level of the defect, G is the generation of
free carriers, k is Boltzmann constant, and T is the temperature. The
remaining terms are specific for electrons and holes as depicted by
their subscripts being e and h, respectively. These remaining terms are:
c is a capture rate of particles, e is an emission rate of particles, σ
is the capture cross section, n is the number of free particles
(electrons in the conduction band or holes in the valance band),
N<sub>d</sub> is the number of defects filled with a specific particle*

The Shockley Read Hall parameterization of a defect has three values,
all of which should be assumed to be temperature dependent:

  - E<sub>d</sub>: The energy level of the defect. We capture this value
    as reported in literature. This is usually reported as a distance to
    another energy level, i.e. E<sub>c</sub>, E<sub>v</sub>, or
    E<sub>i</sub>.
  - σ<sub>e</sub>: The capture cross section for electrons
  - σ<sub>h</sub>: The capture cross section for holes

A 4th value that is recorded as a SRH parameter is k. k is
σ<sub>e</sub>/σ<sub>h</sub>. This is recorded as lifetime spectroscopy
usually provides a measure of k rather than absolute capture cross
sections.

TODO: ‘k’ is obviously poor notation, but it is currently the standard
notation. This should be improved both here and in literature.

## How information is stored

The information is stored in both the file structure and the finial text
files within the repository. The file structure of the repository is
illustrated in Figure [2](#fig:structure). The repository has two nested
folders, with the text file in the finial folder.

![Figure 2: Folder and file structure of the repository. Square boxes
represent a folder, while hexagonal boxes represent text
files.](./images/FolderStructure.png)

*Folder and file structure of the repository. Square boxes represent a
folder, while hexagonal boxes represent text files.*

The naming convention for the file are now detailed. The first element
written corresponds to the folder that the file is in. Following this
all the elements are written in alphabetical order.

The crystal site abbreviation currently used are:

  - s: substitutional
  - i: interstitial
  - v: vacancy
  - p: precipitate

The abbreviations for the defect charge state are:

  - aa: double acceptor. The defect can change been a net change of -2
    and -1.
  - a: acceptor. The defect can change been a net charge of -1 and 0.
  - d: donor. The defect can change been a net charge of 0 and 1.
  - dd: double donor. The defect can change been a net charge of 1 and
    2.
  - ddd: triple donor. The defect can change been a net charge of 2 and
    3.

The “.srh” file is an ASCII file written in plain text. The structure of
its contents is described in the following subsection.

### “.srh” file continence

The contents of the finial file, and naming convention is now described.
There are all optional inputs. To have an entry the minimum is the
params section.

The text file is written with a
[yaml](https://en.wikipedia.org/wiki/YAML) syntax. This makes it both
easy for a human and computer to read\! An example is found in
W\_s\_s.srh:

    Graff1995_1:
      title: Metal impurities in silicon-device fabrication
      DOI: 10.1007/978-3-642-97593-6
      measurement_technique: Review of DLTS
      sample:
        growth: CZ
        dopant: boron
        resistivity: 1
        incorporation: ion implantation
      comments: Taken from table 1 in the appendix. The table only provides
          the majority carrier capture cross section. The majority carrier has
          been estimated from the position of the defect level. e.g. if higher
          than the intrinsic level, it is assume the majority carrier was electrons.
      params:
        Ed: Ev+0.41

The initial value Graff1995\_1, is the author year notation commonly
used for publications. The \_1 indicates that in the same publication
two values were published for this impurity. If there author year
notation is not unique the second name is appended with a letter rather
than a number, e.g. Graff1995\_a.

#### title

The title of the paper publication.

#### DOI

The Digital Object Identifier (DOI) for the file.

#### ISBN

The international standard book number.

#### sample

Sample provides a nested heading to provide sample details. This include
the growth of the material, the dopant, and the resistivity (Ω.cm). An
example is:

    sample:
      growth: CZ
      dopant: boron
      resistivity: 1
      incorporation: ion implantation

The inputs for incorporation are:

  - ion implantation: as the name suggests
  - ingot: This means it is incorporated during ingot growth
  - thermal: This means it is incorporated into the wafter with a
    thermal step
  - quenched: Refers to a fast cooling after thermal incorporation.

TODO: The problem with this notation is when several samples are used. A
better way is to recorded this information.

options:

  - growth: CZ, FZ, cast
  - dopant: elemental names all lower case and comma separated,
    e.g. boron, phorphous, aluminum
  - resistivity: resistivity in Ω.cm. If several samples are used comma
    separate them. If a range of resistivities are provided simply write
    that range, e.g. 3, 50, 1-10
  - incorporation: options are: melt, thermal, ion implantation

#### measurement\_technique

There are a range of techniques that have been used to determine these
defect properties. If several techniques are used, they are just comma
separated. These are recorded in the repository using the following
abbreviation:

1.  [DLTS](https://en.wikipedia.org/wiki/Deep-level_transient_spectroscopy):
    Deep level transient spectroscopy. There are many variants on DLTS,
    again these are separated by providing different suffixes, being:
      - Mo - minority carrier based DLTS where the excess minority
        carriers are excited with photons of energy larger than the
        bandgap of the semiconductor.
      - Me - minority carrier based DLTS where the excess minority
        carriers are excited by a bias.
      - L - Laplace DLTS
      - D - Double correlations DLTS
      - Cc - constant capacitance DLTS.
2.  CV: Capacitance voltage as a function of frequency. The major
    difference with DLTS is that this is not a transient measurement.
      - O - An optical biased technique where sub band-gap light was
        used to investigate a defect.
      - T - The temperature was varied
3.  TS: Thermal stimulated spectroscopy. This is when the sample
    temperature is increased and a value is monitored. The sample is not
    subjected to a varied biased.
      - I - current
      - C -
    capacitance
4.  [Hall](https://www.nist.gov/pml/engineering-physics-division/popular-links/hall-effect/hall-effect):
    Temperature dependent ionized dopant concentration via the hall
    effect.
5.  DC: diode current: Measurement of the current from a device.
    Suffixes include:
      - S - spectral
      - I - impurity effect. The defect level occupation is changed
        through sub band-gap illumination. It can not separate between
        electron and hole emission.
      - T - transient dark current measurement. This includes
        measurement of the reversed biased and the time constant and
        magnitude of the change in dark current is determined.
6.  PC: Measurement of the photoconductivity from a device. Suffixes
    include:
      - S - spectral
      - Tr - measurement of trapping time constants
      - N - samples with varying number of defects
7.  SCP: Solar cell performance. This involves making solar cells from
    contaminated material and evaluating the impact of the impurity on
    the finial device performance.
8.  Res: Resistivity measurements: Suffixes
      - T - temperature
9.  LS: Lifetime spectroscopy. This can be performed in different ways.
    These ways are depicted as suffixes, being:
      - D - doping dependent,
      - I - represents Injection dependent,
      - N - samplings with varying number of defects. Unlike other
        techniques the number of defects affects the measured value.
      - T - temperature dependent
      - M - accounting for a single defect having multiple levels

#### comments

Any comments about the file that maybe helpful.

#### params

This contains the published SRH parameterisation. As stated before the
Shockley Read-Hall parameters captured are: “Ed” the energy level of the
defect, “simga\_e” the electron capture cross section, “sigma\_h” the
hole capture cross section, and “k” the ratio of the capture cross
sections. k is captured as this is the value directly measured in
lifetime spectroscopy, and thus allows easy entry into the database
without the assumption of capture cross-sections from other
publications. An example of an entry is:

    params:
      Ed: Ev+0.3 # units of eV
      dEd: -0.1, 0.53 # units of eV
      sigma_h: 3.9e-16 * exp(-0.045/kT) # uunits of cm
      dsigma_h: 1e-13 # units of cm^2
      k: 10 # unitless

The energy level of the defect is usually measured relative to the
conduction band edge, or valence band edge. These values are recorded
here in electron volts as “Ev+0.38”. The capture cross section are
generally temperature dependent values, and reported in cm<sup>2</sup>.
The temperature dependence is using standard scientific notation,
e.g. the temperature dependence of σ<sub>h</sub> for interstitial iron
acting as a donor is recorded under “sigma\_h” as “3.9e-16 \*
exp(-0.045/kT)”. Published errors on these values are also able to be
captured with the entry key being the parameter the the prefix “d”,
e.g. the error in E<sub>d</sub> is recorded under dE<sub>d</sub>.
Symmetric error values are recorded through listing a single number,
while asymmetric errors are comma separated starting with the negativity
error value. For example, to enter the error reports for Cobalt’s
acceptor capture cross-sectional ratio (k) being -0.1 and +0.53, it is
entered under the dk as “-0.1, 0.53”.

## Optical absorption and emission

Similar to the electrical or thermal transitions, defects are able to
absorb or emit light. This section will describe how we will store this
information. We also limit this section to process which move an
electron or hole between a band (conduction or valance) and a defect.
There are other process which involve absorption of light by the defect
such as absorption by vibrational modes.

These details are saved in an “.opt” file, in yaml format. The details
saved are currently under discussion. They could include:

1.  Raw optical capture cross section data
2.  Fitted models to this data

### “.opt” file continence

The contents of the finial file, and naming convention is now described.
There are all optional inputs. To have an entry the minimum is the
params section.

The text file is written with a
[yaml](https://en.wikipedia.org/wiki/YAML) syntax. This makes it both
easy for a human and computer to read\! An example is found in
W\_s\_s.srh:

    okuyama1979:
      title: Photoionization cross-sections and energy levels of gold, iron,
       platinum, silver, and titanium in silicon
      DOI: 10.1007/BF02652402
      comments: A_e was extracted from figure 2 and manually fit. The change in
       refractive index was not determined. Between 0.77 and 0.8eV in Fig. 2
       there is scatter from the Lucovsky line but this may be caused by a
       change from a germanium to a silicon filter in this range. Defect
       concentration determined with CV(T).
      measurement_technique: Bo-EQE
      temperature: 77.15
      Fit:
        form: one
        A_e: 7.27e-16 # units of cm
        power1: 3/2 # unitless
        Ed: 0.77 # units of eV
        power2: 3

The initial value Graff1995\_1, is the author year notation commonly
used for publications. The \_1 indicates that in the same publication
two values were published for this impurity. If there author year
notation is not unique the second name is appended with a letter rather
than a number, e.g. Graff1995\_a.

the current fitted forms are:

1.  Lucovsky: \(A \times \frac{(E-E_d)^{power}}{E^power}\)
