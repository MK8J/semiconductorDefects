# Semiconductor Defects

This is an attempt at creating a collection of defect parameters of
semiconductors in plain text. The idea is that such a plain text file
should reduce allow for everyone to be able to access the information
for now and into the future.

The information currently stored in the repository is currently limited
to Shockley Read Hall parameterization, which allow calculation of how
electron and holes electronically interact with the defect.

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

The naming convention for the file are now detailed. The first element
written corresponds to the folder that the file is in. Following this
all the elements are written in alphabetical order.

The crystal site abbreviation currently used are:

  - s: substitutional
  - i: interstitial

The abbreviations for the defect charge state are:

  - aa: double acceptor. The defect can change been a net change of -2
    and -1.
  - a: acceptor. The defect can change been a net charge of -1 and 0.
  - d: donor. The defect can change been a net charge of 0 and 1.
  - dd: double donor. The defect can change been a net charge of 1 and
    2.

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
      measurement_technique: Review, DLTS
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

TODO: The problem with this notation is when several samples are used. A
better way is to recorded this information.

#### measurement\_technique

There are a range of techniques that have been used to determine these
defect properties. If several techniques are used, they are just comma
separated. These are recorded in the repository using the following
abbreviation:

1.  LS: Lifetime spectroscopy. This can be performed in different ways.
    These ways are depicted as suffixes, being:
      - D - doping dependent,
      - I - represents Injection dependent,
      - N - samplings with varying number of defects. Unlike other
        techniques the number of defects affects the measured value.
      - T - temperature
    dependent,
2.  [DLTS](https://en.wikipedia.org/wiki/Deep-level_transient_spectroscopy):
    Deep level transient spectroscopy. There are many varients on DLTS,
    again these are separated by providing different suffixes, being:
      - O - optical DLTS.
      - L - Laplace DLTS
      - D - Double correlations
    DLTS
3.  [Hall](https://www.nist.gov/pml/engineering-physics-division/popular-links/hall-effect/hall-effect):
    Temperature dependent ionized dopant concentration via the hall
    effect.
4.  Photocurrent: Measurement of the current from a device. Suffixes
    include:
      - S - spectral
5.  PC: Measurement of the photoconductivity from a device. Suffixes
    include:
      - S - spectral
      - T - measurement of trapping time constants

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
      Ed: Ev+0.3
      dEd: -0.1, 0.53
      sigma_h: "3.9e-16 * exp(-0.045/kT) "
      dsigma_h: 1e-13
      k: 10

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
