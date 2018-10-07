# Website Fingerprinting

This project contains implementations based on multiple research papers on website access classifcation against network data protected by encryption such as SSL, TLS, and Tor network. Data contained in this project are retrieved from different profile from the same domain in comparison to data presented in the papers.

This project is not meant to be a 100% accurate implementation of the technique presented in the papers, but it should approximate the result of an accurate implementation of the technique.

Paper 1: Website Fingerprinting at Internet Scale, Pachenko et al.\
Paper 2: Touching from a Distance: Website Fingerprinting Attacks and Defenses, Cai et al.\
Paper 3: k-fingerprinting: a Robust Scalable Website Fingerprinting Technique, Hayes et al.

Requirement for TOR sniffing:\
TOR browser 7.5.6\
Geckodriver 0.17\
tbselenium

Requirement for Firefox sniffing:\
Geckodriver latest version

Python library requirement:\
pip\
selenium\
scikit-learn\
numpy\
pyxdameraulevenshtein\
matplotlib\
scapy
