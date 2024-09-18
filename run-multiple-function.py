import pandas as pd
import time  # For simulating some delay (optional)

def function_amrs() -> str:
    """Simulates running the 'amrs' environment command."""
    time.sleep(1)  # Simulating processing time (optional)
    return "Output from AMRS environment."

def function_apac() -> str:
    """Simulates running the 'apac' environment command."""
    time.sleep(1)  # Simulating processing time (optional)
    return "Output from APAC environment."

def function_emea() -> str:
    """Simulates running the 'emea' environment command."""
    time.sleep(1)  # Simulating processing time (optional)
    return "Output from EMEA environment."

def main():
    # Dictionary to hold the function names and their outputs
    output_dict = {"Function": [], "Output": []}

    # List of functions to execute with progress messages
    functions = [
        ("AMRS", function_amrs),
        ("APAC", function_apac),
        ("EMEA", function_emea)
    ]

    for name, func in functions:
        print(f"{name}..........", end="", flush=True)  # Progress message
        output = func()  # Execute the function
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
