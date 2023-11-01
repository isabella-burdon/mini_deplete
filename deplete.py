import subprocess as sp

# Inform user of dependancies

print(""" 
      NB: This code requires minimap2.
      Please activate your minimap2 environment prior to running.
      Ensure python is installed in this environment""")

# Define the commands
commands = {
    "pl": "python deplete_lambda.py",
    "c": "python deplete_chm13.py",
    "b": "python deplete_both.py",
}

# Check for minimap2 and Python dependencies
try:
    sp.run("minimap2 --version", shell=True, check=True)
    sp.run("python --version", shell=True, check=True)
except sp.CalledProcessError:
    print(""" 
          NB: This code requires minimap2 and Python.
          Please ensure that both are installed and accessible in your environment.
          """)
    exit(1)

# Ask the user for the depletion type
deplete_type = input("""
Please select depletion type:
        
    phage lambda only: [pl]
    chm13(human) only: [c]
                 both: [b]

[pl/c/b] : """)

# Check if the selected depletion type is valid
if deplete_type not in commands:
    print("Invalid input. Please select 'pl', 'c', or 'b'.")
else:
    # Execute the selected command
    command = commands[deplete_type]
    try:
        sp.run(command, shell=True, check=True)
        print("Depletion process completed successfully.")
    except sp.CalledProcessError:
        print("An error occurred during the depletion process. Please check your inputs and dependencies.")

