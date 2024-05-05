# FilterPlayground

![Header Image](header_thumbnail.png)

<strong>Filter Playground is an interactive GUI application for studying and experimenting
with filters and convolution techniques in image processing. The application provides
a user-friendly interface for exploring various filters, convolution operations,
and their effects on images. Users can visualize the results in real-time and gain insights into the fundamentals of
image processing.<br>
For run the GUI follow the instructions, please refer to [Run the GUI](#run-the-gui).
You can change and modify the filters in the 'filter_script' folder.
</strong>

## Key Features:

- **Interactive GUI for studying filters and convolution**
- **Supports exploration of various filter types and configurations**
- **Real-time visualization of filter effects on images**
- **Educational tool for learning image processing concepts**
- **Cross-platform compatibility (Windows, macOS)**

## overview

**This section provides a screenshot of the GUI**.

- ### dark mode

![screenshot1.png](screenshot1.png)

- ### light mode

![screenshot2.png](screenshot2.png)

## Run the GUI

### 1. Clone the repository:

```bash
git clone https://github.com/AmirHDevo/FilterPlayground.git
``` 

### 2. Navigate to the project directory:

```bash 
cd FilterPlayground
```

### 3.Install the required dependencies using pip:

```
pip install -r requirements.txt
```

### 4. run app

```bash 
python app.py
```

#### or

```bash
py app.py
```

## Create Executable file
 
Here's how you can create a virtual environment, activate it, and then run the PyInstaller command on both macOS and 
Windows, all within a Markdown code block for your README.md:
### 1.Clone the repository:

```bash
git clone https://github.com/AmirHDevo/FilterPlayground.git
```

### 2.Create a virtual environment
- #### macOS:
```bash 
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```
- #### windows
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\activate
```


### 3. Navigate to the project directory:

```bash 
cd FilterPlayground
```

### 4.Install the required dependencies using pip:

```
pip install -r requirements.txt
```

### 5.Run PyInstaller to generate the executable:
```bash
pyinstaller --onefile --windowed --icon=logo.icn --name=FilterPlayground app.py
```
### 6.Run exe
**Now the exe is created and its in the dist folder copy it to the current folder(FilterPlayground).
double-click the FilterPlayground.exe to open and run it.
```
## License

- **This project is licensed under the [MIT License.](LICENSE)**
