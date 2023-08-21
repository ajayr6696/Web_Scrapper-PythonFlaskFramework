# Web Scrapper using Python Flask Framework
A simple Web Scraping website. Using a URL from Online Retailer site: https://www.target.com/ products and an HTML tag provided by a user scraps the page and returns the total number of elements fetched and then display the results from the scrap.

## Requirements ,Packages used and Installation
Download and install Python. Make sure you install Python v3.6.+
 
## Installation
          
Navigate to your directory of choice the proceed as follows;<br>
          
### 1 .Clone the git repo and create a virtual environment 
          
Depending on your operating system,make a virtual environment to avoid messing with your machine's primary dependencies
          
> **Windows**
          
```
git clone https://github.com/ajayr6696/Web_Scrapper-PythonFlaskFramework
cd Web_Scrapper-PythonFlaskFramework
python app.py
```
          
> **macOS/Linux**
          
```
git clone https://github.com/ajayr6696/Web_Scrapper-PythonFlaskFramework.git
cd Web_Scrapper-PythonFlaskFramework
python app.py
```

### 3 .Install the requirements

Applies for windows/macOS/Linux

```pip install -r requirements.txt```

### 4. Run the application 

> **For linux and macOS**
Make the run file executable by running the code

```chmod 777 run```

Then start the application by executing the run file

```./run```

> **On windows**
```
set FLASK_APP=main
flask run
```
Then on your browser open `localhost:5000` or `http://127.0.0.1:5000/`

The Results of the data that is scrapped from the Web Page is returned in a Excel Sheet.
