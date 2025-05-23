# Clinical-laboratory-schedule-creator 🧪🕒
This is a Python CLI tool that generates a fair and organized shift schedule for a clinical laboratory that operates 24/7, every day of the year. It considers staff availability, holidays, night shift rules, absences, and licenses for a given month.

# 🧰 Features
CLI prompts for month, year, and holiday days.

Assigns 3 agents per night shift, considering:

Agent availability (based on a JSON config)

Licenses (time off)

Requested absences

# Outputs:

Daily shift assignments

Summary of hours worked per agent and their ratio of completed to expected hours

# 📂 JSON Agent Configuration Format
json
{
  "agentes": [
    {
      "nombre": "joaquin",
      "apellido": "morillas",
      "rol": "bioquimico",
      "dias_de_trabajo": {
        "0": [7, 14],
        "1": [7, 13],
        "4": [7, 14]
      },
      "dias_de_guardia": [],
      "hace_guardia": true,
      "licencias": [],
      "reduccion_horaria": 0
    }
  ]
}
"0" to "6" are weekdays (Monday=0, Sunday=6).

dias_de_trabajo maps days to working time ranges.

dias_de_guardia gets populated by the script.

hace_guardia indicates whether the agent is eligible for night shifts.

# 🚀 Getting Started
Prerequisites
Python 3.11+

No external libraries required (uses only standard modules)

Run the app
bash
Copiar
Editar
python3 main.py
Follow the interactive prompts to:

Enter the month and year.

List holidays in that month.

Select the night-shift agents (3 required).

Mark requested absences.

Register agent licenses.

The final schedule will be printed to the terminal or exported (if implemented).

# 🖨️ Example Output
plaintext

May 1 - Agent A, Agent B, Agent C
May 2 - Agent D, Agent E, Agent F
...

Hours Summary:
- Joaquin Morillas: 112 / 160 hrs (70%)
- Laura Perez: 154 / 160 hrs (96%)
- 
# 🛠️ Built With
Python 3.11

Standard Libraries:

datetime, date, calendar, random, json

# 📜 License
This project is licensed under the MIT License. You’re free to use, modify, and distribute it.
