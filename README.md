# Urban vs. Natural Pollinator Diversity in the Bay Area

This project analyzes iNaturalist data to compare pollinator diversity (bees, hoverflies) between urban and natural habitats in the Bay Area. I wanted to create some visualizations of INat data 

## Structure
- `data_raw/`: raw downloaded data
- `data_clean/`: cleaned datasets
- `figures/`: plots and maps
- `reports/`: write-ups
- `src/`: scripts for data pipeline

## Getting Started
Clone the repository and install the required Python packages
```bash
pip install -r requirements.txt
```
Run these scripts in order:  
    1. Download raw data   
```bash
python src/01_download.py
```
  
    2. Clean the data  
```bash
python src/02_clean_enhanced.py
```  

    3. Generate Summary statistics and graphs  
```bash
python src/03_eda_report.py
```  

    4. Generate Interactive maps  
```bash
python src/07_super_interactive.py
```  

    5. View outputs: cleaned datasets are saved in the `data_clean` folder. Summary plots and charts are saved in the `reports` folder. Interactive maps are saved in the `figures` folder