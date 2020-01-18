# Trained Models

## MIT-BIH Arrhythmia Database

The "MIT" models refer to models trained on the [1] MIT-BIH Arrhythmia Database which was obtained from PhysioNet.com

Models trained on the MIT database are non-binary models that classify heartbeats into 1 of 5 predetermined classes

### Database Description

- The MIT-BIH Arrhythmia Database contains 48 half-hour excerpts of two-channel ambulatory ECG recordings, obtained from 47 subjects studied by the BIH Arrhythmia Laboratory between 1975 and 1979.
- The recordings were digitized at 360 samples per second per channel with 11-bit resolution over a 10 mV range. 
- Two or more cardiologists independently annotated each record.

Below is an outline of how the 5 classes in which heartbeats were categorized based on [2] AAMI EC57 categories

| Category | Diagnostic Annotations |
| --- | --- |
| **N** | <ul><li>Normal</li><li>Left/Right Bundle Branch Block</li><li>Atrial Escape</li><li>Nodal Escape</li></ul> |
| **S** | <ul><li>Atrial Premature</li><li>Aberrant Atrial Premature</li><li>Nodal Premature</li><li>Supra-Ventricular Premature</li></ul> |
| **V** | <ul><li>Premature Ventricular Contraction</li><li>Ventricular Escape</li></ul> |
| **F** | <ul><li>Fusion Of Ventricular and Normal</li></ul> |
| **Q** | <ul><li>Paced</li><li>Fusion of Paced and Normal</li><li>Unclassifiable</li></ul> |

### Citations

[1] Moody GB, Mark RG. The impact of the MIT-BIH Arrhythmia Database. IEEE Eng in Med and Biol 20(3):45-50 (May-June 2001). (PMID: 11446209)

[2] A. for the Advancement of Medical Instrumentation et al., “Testing and reporting performance results of cardiac rhythm and st segment measurement algorithms,” ANSI/AAMI EC38, vol. 1998, 1998.

https://physionet.org/content/mitdb/1.0.0/

## PTB Diagnostic ECG Database

The "PTB" models refer to models trained on the [3] PTB Diagnostic ECG Database which was obtained from PhysioNet.com. 

Models trained on the PTB database are binary classification models that differentiate between normal and abnormal heartbeats

### Database Description

- The ECGs in this collection were obtained using a non-commercial PTB prototype recorder.
- The database contains 549 records from 290 subjects. (aged 17 to 87, mean 57.2; 209 men, mean age 55.5, and 81 women, mean age 61.6)
- 16 Input channels were digitized at 1000 samples per second per channel with 16-bit resolution.

Below is an outline of subject class within the database

| Diagnostic Class | Number of Subjects |
| --- | --- |
| Myocardial infarction | 148 |
| Cardiomyopathy/Heart failure | 18 |
| Bundle branch block | 15 |
| Dysrhythmia | 14 |
| Myocardial hypertrophy | 7 |
| Valvular heart disease | 6 |
| Myocarditis | 4 |
| Miscellaneous | 4 |
| Healthy controls | 52 |

### Citations

[3] Bousseljot R, Kreiseler D, Schnabel, A. Nutzung der EKG-Signaldatenbank CARDIODAT der PTB über das Internet. Biomedizinische Technik, Band 40, Ergänzungsband 1 (1995) S 317
