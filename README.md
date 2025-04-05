# Intel Bug Detection Project

An AI-powered tool for detecting and analyzing bugs in code using machine learning techniques.

## Project Overview
This project uses advanced machine learning models to detect potential bugs in source code, helping developers identify and fix issues early in the development process.

## Repository Contents
- `bug_detector_model/`: Model configuration and inference code
- `data/`: Training and testing datasets
- `src/`: Source code files
- `utils/`: Utility functions and helper scripts

## Required Model File
The large model file (`model.safetensors`) is not included in this repository due to size limitations. 

### How to Get the Model File
1. Download the model file from [Google Drive Link/Hugging Face/etc]
2. Place it in the following directory:
   ```
   bug_detector_model/model.safetensors
   ```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Mainudheen/Mainudheen-intel-mine.git
   cd Mainudheen-intel-mine
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Model File**
   - Download `model.safetensors` from [INSERT_LINK]
   - Place it in the `bug_detector_model/` directory

## Usage

1. **Prepare Your Code**
   - Place the code you want to analyze in the input directory

2. **Run the Bug Detection**
   ```bash
   python main.py --input_file your_code.py
   ```

3. **View Results**
   - Results will be saved in the `results/` directory
   - Check the console output for immediate findings

## Features
- Static code analysis
- Machine learning-based bug detection
- Detailed bug reports and suggestions
- Support for multiple programming languages

## Requirements
- Python 3.8 or higher
- PyTorch
- Transformers library
- CUDA (optional, for GPU support)

## Model Information
- Model Type: Neural Bug Detection
- Size: 475.52 MB
- Framework: PyTorch
- Base Architecture: Transformer

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[Insert your license information here]

## Contact
For any queries or support, please contact:
[Your contact information]

## Acknowledgments
- Intel for project support
- [Any other acknowledgments]

4.# Model Download Instructions

1. Download the model file from: https://huggingface.co/YOUR_USERNAME/intel-bug-detector/blob/main/model.safetensors

2. Place the downloaded file in:
   ```
   bug_detector_model/model.safetensors
   ```
