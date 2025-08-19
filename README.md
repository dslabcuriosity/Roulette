### Roulette Bias Analysis Application

This Python application is a strategic tool designed to help roulette players by analyzing historical game data and identifying potential biases in a roulette wheel. The main goal is to provide players with data-driven insights to inform their betting strategy.

-----

### Business Understanding

The project was created to provide a systematic, analytical approach to a game of chance. Traditional roulette betting often relies on intuition or superstitions. This application aims to challenge that by using statistical analysis to uncover non-random patterns in the outcomes of a roulette wheel. The primary objective is to offer a tool that can potentially improve a player's odds by highlighting sections of the wheel that are statistically more likely to win. The main challenge was to translate a complex statistical concept into a simple, user-friendly interface.

-----

### Data Understanding

The application works with numerical data representing winning roulette outcomes. Users can input this data in two ways:

1.  **Manual Keyboard Input:** For real-time analysis as a game progresses.
2.  **Excel File Import:** For analyzing a larger history of outcomes. The recommended format is a simple Excel sheet (`.xlsx`) with numbers listed in a single row or column. This data is the foundation of the statistical analysis, and its accuracy is crucial for the program's effectiveness.

-----

### Technologies

  * **Python:** The core programming language used to build the application.
  * **Pandas:** A powerful library for data manipulation and analysis, used to handle the Excel data.
  * **Openpyxl:** A library for reading and writing Excel files, a dependency for Pandas.

-----

### Setup

To set up and run this project, follow these steps:

1.  **Create a Project:** In PyCharm, create a new project.
2.  **Add Your File:** Place your Python script (`analizador_ruleta.py`) and your Excel file (`datos.xlsx`) in the same project folder.
3.  **Install Dependencies:** Open the terminal in PyCharm and run the following command to install the required libraries:
    ```bash
    pip install pandas openpyxl
    ```
4.  **Run the Script:** Execute the Python file. The program will prompt you to choose between manual input and using the Excel file.

***Example of file structure:***

```
Mi_Proyecto/
├── analizador_ruleta.py  
├── datos.xlsx          
└── ...
```

For the Excel file to be recognized, just type its name (`datos.xlsx`) when prompted. The application is designed to be beginner-friendly, defaulting to `datos.xlsx` if no name is entered.

-----

### Approach

The application uses a **statistical bias analysis** approach. After ingesting the data, it calculates the frequency of outcomes for each "square" (dozens and columns) on the roulette table. It then compares these observed frequencies to the expected frequencies of a truly random wheel. The program calculates a **"confidence score"** for each section based on this deviation. A higher confidence score suggests a greater statistical bias toward that section, providing a clear, actionable recommendation to the player.

-----

### Status

This project is **Complete** and ready for use. It is a stable version that provides the core functionality described. There are no immediate plans for major new features, but future enhancements could include a graphical user interface (GUI) or more advanced statistical models.

-----

### Credits

This project was developed by a solo developer as a personal portfolio piece to demonstrate proficiency in Python, data analysis, and problem-solving.
