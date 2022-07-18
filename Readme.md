# Django Websites Named Entity Recognition and Relation Extraction

<img src="static/media/photos/mahasiswa_dimas.jpg" alt="MarineGEO circle logo" style="height: 60px; width:60px;border-radius:50%"/>
<img src="static/media/photos/lipi_slamet.jpg" alt="MarineGEO circle logo" style="height: 60px; width:60px;border-radius:50%"/>
<img src="static/media/photos/lipi_alhafiz.jpg" alt="MarineGEO circle logo" style="height: 60px; width:60px;border-radius:50%"/>
<img src="static/media/photos/pembimbing_fitrianingsih.jpg" alt="MarineGEO circle logo" style="height: 60px; width:60px;border-radius:50%"/>
<img src="static/media/photos/pembimbing_rodiah.jpg" alt="MarineGEO circle logo" style="height: 60px; width:60px;border-radius:50%"/>

## Websites Test
| Prediksi                       | Prediksi Time<br>(Hour:Minutes:Seconds) | Framework | Runtime                  | Ram  | Disk               | Machine          |
| ------------------------------ | --------------------------------------- | --------- | ------------------------ | ---- | ------------------ | ---------------- |
| Named Entity Recognition (NER) | 00.00.06                                | Django    | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| Relation Extraction (RE)       | 00.03.01                                | Django    | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |

## After
<img src="After.png" width="1345">

## Demo
<img src="Demo.gif">

## NER Research (BILSTM-CRF)
| Model           | Micro F1 | Macro F1 | Weighted F1 | Training Time<br>(Hour:Minutes:Seconds) | Runtime                  | Ram  | Disk               | Machine          |
| --------------- | -------- | -------- | ----------- | --------------------------------------- | ------------------------ | ---- | ------------------ | ---------------- |
| CRF             | 77%      | 77%      | 77%         | 0.00.13                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BILSTM          | 75%      | 76%      | 75%         | 0.06.21                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BERT            | 61%      | 60%      | 61%         | 0.22.35                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BILSTM-CRF      | 87%      | 86%      | 86%         | 0.59.04                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BERT-CRF        | 58%      | 57%      | 58%         | 1.01.40                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BERT-BILSTM     | 61%      | 60%      | 61%         | 0.25.28                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BERT-BILSTM-CRF | 60%      | 59%      | 60%         | 1.04.07                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |

## RE Research (BILSTM-CRF)
| Model      | Micro F1 | Macro F1 | Weighted F1 | Training Time<br>(Hour:Minutes:Seconds) | Runtime                  | Ram  | Disk               | Machine          |
| ---------- | -------- | -------- | ----------- | --------------------------------------- | ------------------------ | ---- | ------------------ | ---------------- |
| BERT       | 79%      | 84%      | 79%         | 00.41.07                                | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
| BILSTM-CRF | 75%      | 64%      | 64%         | 1.07.48                                 | GPU Tesla P100-PCIE-16GB | High | Google Drive 100gb | Google Colab Pro |
