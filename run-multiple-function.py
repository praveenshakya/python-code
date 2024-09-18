
import pandas as pd
import time  # For simulating some delay (optional)

def function_amrs(name: str, env: str) -> str:
    """Simulates running the 'amrs' environment command with parameters."""
    time.sleep(1)  # Simulating processing time (optional)
    return f"Output from {name} environment in {env}."

def function_apac() -> str:
    """Simulates running the 'apac' environment command without parameters."""
    time.sleep(1)  # Simulating processing time (optional)
    return "Output from APAC environment."

def function_emea() -> str:
    """Simulates running the 'emea' environment command without parameters."""
    time.sleep(1)  # Simulating processing time (optional)
    return "Output from EMEA environment."

def main():
    # Dictionary to hold the function names and their outputs
    output_dict = {"Function": [], "Output": []}

    # List of functions to execute (AMRS with parameters, others without)
    functions = [
        ("AMRS", function_amrs, ("amrs", "uat")),  # Passing parameters to AMRS
        ("APAC", function_apac, None),             # No parameters for APAC
        ("EMEA", function_emea, None)              # No parameters for EMEA
    ]

    for name, func, params in functions:
        print(f"{name}..........", end="", flush=True)  # Progress message

        # Check if parameters exist; if yes, pass them to the function
        if params:
            output = func(*params)  # Unpacking parameters
        else:
            output = func()  # No parameters passed

        print("Done")  # Mark as done after the function completes

        # Store the results
        output_dict["Function"].append(name)
        output_dict["Output"].append(output)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(output_dict)

    # Save the DataFrame to an Excel file
    df.to_excel("function_outputs.xlsx", index=False)

if __name__ == "__main__":
    main()
