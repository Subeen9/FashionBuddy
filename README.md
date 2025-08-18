# FashionBuddy
A simple fashion assistant built with Python, Gradio, Ollama, and Pandas.

## Folder Structure
 - assets to store your clothes data.
 - query.py the main business logic is here.
 - requirement.txt to install the dependencies.

 ## Tools Used
 Python Gradio for UI

 Ollama[phi3:mini model] Local llm for responses.

 Pandas for data handeling.

 ## Prereq
 - Download ollama [Download Here](https://ollama.com/download/windows)

 ```bash
 ollama serve # To start ollama server
 ```
 - Download the model[phi3:mini in this case]
 ```bash
 ollama pull phi3:mini
 ```

 ## Getting Started

- Clone the repository.
 ```bash
 git clone https://github.com/Subeen9/FashionBuddy.git

 ```
 - Install the dependencies
 ```bash
 pip install -r requirement.txt
 ```

 Run the code
 ```bash
 python query.py
```
The python module will convert the excel data into string.
Gradio will run on  http://127.0.0.1:7860
Ask the qns in the browser and it will answer your question.

**The response time depends upon model and your GPU/CPU.**

**Other Lightweight model options in ollama**
- gemma2:2b
- qwen3

## Notes

- Create a virtual environment and add it to .gitignore for clean setup.

- The code assumes your Excel file has specific column names. If your data uses different column names, update query.py accordingly to avoid errors.

## Sample Excel Data Format
| Clothes  | Color | Category   | Outdoor | Size | Tshirt | PANT | Hoodie | Business | Ocassion   |
| -------- | ----- | ---------- | ------- | ---- | ------ | ---- | ------ | -------- | ---------- |
| Polo Tee | Blue  | Casual     | Yes     | M    | Yes    | No   | No     | No       | Party      |
| Jeans    | Black | Bottomwear | Yes     | 32   | No     | Yes  | No     | No       | Daily Wear |
| Hoodie   | Grey  | Winter     | Yes     | L    | No     | No   | Yes    | No       | Travel     |
| Suit     | Navy  | Formal     | No      | 40   | No     | No   | No     | Yes      | Wedding    |

- Click on flag to save the response on the folder gradio/flagged.