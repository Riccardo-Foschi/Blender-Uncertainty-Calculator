Blender plugin for uncertainty assessment of hypothetical 3D reconstruction of lost or never-built architecture

[Download the Blender plugin from here!](https://github.com/Riccardo-Foschi/Blender-Uncertainty-Calculator/releases/download/v3.9.0/AU_VR_390.zip)


[Download the Grasshopper algorithm for model proofing from here! (click on VIEW RAW)](https://1drv.ms/u/c/a7d9a4eda8acae29/EUOLBSGiG79Phn4ulexkUUoBE1M8x9B3Z0l2mcUkzhuVRQ?e=UyH49G)

[Download the Grasshopper algorithm for Uncertainty assessment from here! (click on VIEW RAW)](https://github.com/Riccardo-Foschi/Blender-Uncertainty-Calculator/blob/main/AUV_AUVR_100.gh)


How to install: Edit -> Preferences -> Add-ons -> Install from Disk -> Browse to the "AU_VR.py" python script downloaded from the link above -> The plugin will appear on the sidebar in the newly created "Uncertainty" tab.

<img src="https://github.com/user-attachments/assets/6e354786-3ca5-4855-a36d-bbe82779feaf" alt="install plugin" width="400" height="">




The following image shows the plugin tabs and buttons and explains the tools for importing and proofing the 3D model:
<img src="https://github.com/user-attachments/assets/57a7ba16-0aa1-406a-84ea-df013407819f" alt="Tutorial" width="800" height="">

The following image shows the plugin tabs and buttons and explains the tools for uncertainty assessment:
<img src="https://github.com/user-attachments/assets/1818fe78-8388-4ee5-bcb5-0beb17ed2354" alt="Tutorial" width="800" height="">


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





 Additional resources here: 
 

- [Video tutorials Playlist here](https://youtube.com/playlist?list=PLLmlU1B4q43scy1ThLHEWiLueoWRum8pR&si=VojWHCa3DOwLsFzG)

- [Download 3D model of a Palladian villa from here (one OBJ for each layer)](https://1drv.ms/f/c/a7d9a4eda8acae29/EimurKjtpNkggKch8QQAAAABrZ7ZHPGGXgH4T-5APFPMEA?e=WpPRoA)

BIBLIOGRAFIC REFERENCES:

- Foschi, R., Fallavollita, F., & Apollonio, F. I. (2024). Quantifying Uncertainty in Hypothetical 3D Reconstruction—A User-Independent Methodology for the Calculation of Average Uncertainty. Heritage, 7(8), 4440-4454. https://doi.org/10.3390/heritage7080209
- Apollonio, F. I., Fallavollita, F., Foschi, R., & Smurra, R. (2024). Multi-Feature Uncertainty Analysis for Urban-Scale Hypothetical 3D Reconstructions: Piazza delle Erbe Case Study. Heritage, 7(1), 476-498. https://doi.org/10.3390/heritage7010023
- Apollonio, F. I., Fallavollita, F., & Foschi, R. (2019, October). The critical digital model for the study of unbuilt architecture. In Workshop on Research and Education in Urban History in the Age of Digital Libraries (pp. 3-24). Cham: Springer International Publishing. https://doi.org/10.1007/978-3-030-93186-5_1
