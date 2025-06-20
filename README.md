Blender plugin for uncertainty assessment of hypothetical 3D reconstruction of lost or never-built architecture

[Download the plugin from here!](https://github.com/rikkarlo/Blender-Uncertainty-Calculator/releases/download/v2.5.1/AU_VR.py)



How to install: Edit -> Preferences -> Add-ons -> Install from Disk -> Browse to the "AU_VR.py" python script downloaded from the link above -> The plugin will appear on the sidebar in the newly created "Uncertainty" tab.

<img src="https://github.com/user-attachments/assets/6e354786-3ca5-4855-a36d-bbe82779feaf" alt="install plugin" width="400" height="">


When exporting from another software, pay particular attention to exporting close watertight manifold solids. If the solid meshes have unwelded vertices, the volume calculation might give unexpected results (if a minor part of the edges is unwelded, the volume might still be calculated correctly, but it is not guaranteed, so to avoid any error, it is better to check import-export options and test various formats).
In the following image you can see the suggested option for a fast export from McNeel Rhinoceros to Blender in glTF and Glb exchange formats.

<img src="https://github.com/user-attachments/assets/a8ade583-57fb-46f3-b462-4c6bb5088957" alt="export from rhino to blender" width="600" height="">

ADVANCED IMPORT EXPORT TIPS: Keep in mind that the Glb and glTF formats in Rhino export the visualization mesh which might not be a solid watertight closed manifold mesh, nevertheless from empirical testing we verified that by using the suggested settings the non-manifold edges are a minor part and the volume calculation in Blender will still be accurate, however for a more robust export-import that always guarantees to preserve manifold solids (given that the original objects in Rhino are closed, watertight, manifold poly-surfaces), we suggest to export and import objects in obj format layer by layer and check each layer after importing. Keep in mind that OBJ from Rhino does not store the units of measurement, and Blender uses meters, so if in Rhino the model was made in any other unit of measurement a rescaling must be performed in order to get consistent units between different software packages, remember to apply the scale after rescaling in Blender in order to achieve correct volume calculation.


The following image explains the plugin tabs and buttons:
<img src="https://github.com/user-attachments/assets/ee99f5c0-d2e1-42e5-8321-436bc8fe5541" alt="Tutorial" width="800" height="">

Use the following image as an aid to assign the correct Uncertainty Level:
<img src="https://github.com/user-attachments/assets/14ff314c-132e-4539-b206-ca6142247d37" alt="YES/NO Flow Chart" width="800" height="">

This is an example of a false colour view for the dissemination of the uncertainty of a hypothetical 3D reconstruction:
<img src="https://github.com/user-attachments/assets/0b6edead-6975-40bd-a83e-61b7f02e4e50" alt="Example of false colour view" width="400" height="">

Refer to the following table for the full description of each Level of Uncertainty (Remember that each level description is also accessible directly from the plugin by hovering the mouse on each button):
<img src="https://github.com/user-attachments/assets/1b5756ad-88ba-42d3-89b5-e38b6db0fbc5" alt="Scale of Uncertainty Levels descriptions" width="700" height="">

The mathematical formulas used to calculate the AU_V and AU_VR are reported below:
<img src="https://github.com/user-attachments/assets/ac0c8f2c-1316-43b7-9ea1-061d6a008e3f" alt="AUV_AUVR Formulas" width="500" height="">

The AU_V formula is as user-independent as possible, while the AU_VR formula is more knowledge-oriented, due to the Relevance factor which is critically assigned by the human operator only to the most relevant elements of the 3D model. When a Relevance factor different from 1.00 is used, the resulting difference between AU_V and AU_VR can indicate at a glance if the model is more uncertain in the most relevant parts or not.

The weighting for the volume is used to guarantee segmentation-independent results (two models that have equal shape but are differently segmented will still return the same AU_V or AU_VR results), furthermore, it will foster better modelling practices because closed solid manifold models are reusable in more contexts (e.g. 3D printing, simulations, etc.).

It is important to note that higher uncertainty in hypothetical reconstructions does not imply lower scientific value; well-documented high-uncertainty models can enhance understanding by critically integrating diverse sources and advancing scientific discourse. Nevertheless, since the two formulas AU_V and AU_VR represent the extreme synthesis of the complex process of Uncertainty assessing, they cannot be considered self-sufficient, but complementary to proper documentation and visualisation of the hypothetically reconstructed case study.
 

BIBLIOGRAFIC REFERENCES:

- Foschi, R., Fallavollita, F., & Apollonio, F. I. (2024). Quantifying Uncertainty in Hypothetical 3D Reconstruction—A User-Independent Methodology for the Calculation of Average Uncertainty. Heritage, 7(8), 4440-4454. https://doi.org/10.3390/heritage7080209
- Apollonio, F. I., Fallavollita, F., Foschi, R., & Smurra, R. (2024). Multi-Feature Uncertainty Analysis for Urban-Scale Hypothetical 3D Reconstructions: Piazza delle Erbe Case Study. Heritage, 7(1), 476-498. https://doi.org/10.3390/heritage7010023
- Apollonio, F. I., Fallavollita, F., & Foschi, R. (2019, October). The critical digital model for the study of unbuilt architecture. In Workshop on Research and Education in Urban History in the Age of Digital Libraries (pp. 3-24). Cham: Springer International Publishing. https://doi.org/10.1007/978-3-030-93186-5_1
