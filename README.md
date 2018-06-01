# Semiconductor Defects

This is an attempt at creating a collection of all the defect parameters of semiconductors in plain text. The information about the defects is contained in both the file structure and the end files. The finial files are written with [yaml](https://en.wikipedia.org/wiki/YAML) syntax.
At the moment the database contains:

1. The Shockey Read Hall defect parameters, stored in .srh files:
  * Ed: The defects energy level
  * &sigma;<sub>e</sub>: The electron capture cross section
  * &sigma;<sub>h</sub>: The hole capture cross section
  * k: The ratio of &sigma;<sub>e</sub>/&sigma;<sub>h</sub>. This is recorded as lifetime spectroscopy measurements only provide a measure of the ratio of the capture cross sections and not the total capture cross sections.

The database is currently formatted in the following manner:


* database folder

    * folder representing the bulk material

         * folder representing the element in the defect

             * file containing the defect, with a .srh extension.


## Naming convention

### Measurement techniques

There are a range of techniques that have been used to determine these defect properties. These are recorded in the repository using the following abbreviation:

1. LS: Lifetime spectroscopy. This can be performed in different ways. These ways are depicted as suffixes, being:  I represents Injection dependent, T temperature dependent, D doping dependent, and N the number of defects.
2. [DLTS](https://en.wikipedia.org/wiki/Deep-level_transient_spectroscopy): Deep level transient spectroscopy. There are many varients on DLTS, again these are seperated by providing different suffixes, being: O for optical DLTS.
3. [Hall](https://www.nist.gov/pml/engineering-physics-division/popular-links/hall-effect/hall-effect): Temperature dependent ionized dopant concentration via the hall effect.
3. Photocurrent: Measurement of the current from a device. Suffixes inxlude S for spectral.
