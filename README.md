# Image to PDF Converter

This application allows users to convert multiple images to a single PDF file. The user can select multiple image files, preview them, and save them as a single PDF. The application has a modern dark theme and a user-friendly interface.

## Features

- Select multiple images to convert.
- Preview selected images as thumbnails.
- Enter a custom name for the output PDF file.
- Choose the save location for the output PDF.
- Progress bar to indicate conversion progress.
- Responsive and modern dark-themed UI.

## Requirements

- Python 3.x
- `tkinter` (comes pre-installed with Python)
- `Pillow` (Python Imaging Library)
- `reportlab` (PDF generation library)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/image-to-pdf-converter.git
   ```
2. Navigate to the project directory:
   ```sh
   cd image-to-pdf-converter
   ```
3. Install the required packages:
   ```sh
   pip install Pillow reportlab
   ```

## Usage

1. Run the `main.py` script:
   ```sh
   python main.py
   ```
2. Use the application interface to:
   - Click on "Select Images" to choose images from your file system.
   - Preview the selected images in the preview area.
   - Enter a name for the output PDF file.
   - Click on "Convert to PDF!" to choose the save location and start the conversion process.
   - The progress bar will indicate the conversion progress, and a message box will notify you upon completion.
